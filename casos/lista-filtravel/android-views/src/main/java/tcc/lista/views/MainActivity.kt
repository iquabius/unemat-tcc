package tcc.lista.views

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.EditText
import android.widget.Spinner
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.isVisible
import androidx.core.widget.doAfterTextChanged
import androidx.recyclerview.widget.RecyclerView
import tcc.lista.Ordem
import tcc.lista.Produto
import tcc.lista.categorias
import tcc.lista.comparador
import tcc.lista.correspondeABusca
import tcc.lista.daCategoria
import tcc.lista.formatarPreco
import tcc.lista.produtos
import tcc.lista.textoDaContagem

class MainActivity : AppCompatActivity() {
    private val adaptador = AdaptadorDeProdutos()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Como os $("<option>") do jQuery: as opções dos dois <select>.
        findViewById<Spinner>(R.id.categoria).adapter =
            ArrayAdapter(this, android.R.layout.simple_spinner_item, listOf("Todas") + categorias)
        findViewById<Spinner>(R.id.ordem).adapter =
            ArrayAdapter(this, android.R.layout.simple_spinner_item, Ordem.entries.map { it.rotulo })
        findViewById<RecyclerView>(R.id.produtos).adapter = adaptador

        // Como .on("input") e .on("change"). O Spinner também avisa a seleção
        // inicial, quando aparece na tela.
        findViewById<EditText>(R.id.busca).doAfterTextChanged { atualizarLista() }
        val aoEscolher = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(pai: AdapterView<*>?, item: View?, posicao: Int, id: Long) {
                atualizarLista()
            }

            override fun onNothingSelected(pai: AdapterView<*>?) {}
        }
        findViewById<Spinner>(R.id.categoria).onItemSelectedListener = aoEscolher
        findViewById<Spinner>(R.id.ordem).onItemSelectedListener = aoEscolher

        atualizarLista()
    }

    // Refaz a lista inteira a cada mudança num dos controles.
    @SuppressLint("NotifyDataSetChanged")
    private fun atualizarLista() {
        val busca = findViewById<EditText>(R.id.busca).text.toString()
        val posicao = findViewById<Spinner>(R.id.categoria).selectedItemPosition
        val categoria = if (posicao == 0) "" else categorias[posicao - 1]
        val ordem = Ordem.entries[findViewById<Spinner>(R.id.ordem).selectedItemPosition]

        val visiveis = produtos
            .filter { correspondeABusca(it, busca) && daCategoria(it, categoria) }
            .sortedWith(comparador(ordem))

        // Como o .empty().append(...): troca todos os itens de uma vez.
        adaptador.produtos = visiveis
        adaptador.notifyDataSetChanged()
        findViewById<TextView>(R.id.contagem).text = textoDaContagem(visiveis.size)
        findViewById<TextView>(R.id.vazio).isVisible = visiveis.isEmpty()
    }
}

// O RecyclerView não monta os itens sozinho: o Adapter diz quantos são, cria
// a view de um item (o ViewHolder, aqui Item) e a preenche com um produto,
// no papel do map que monta os <li>. As views são reaproveitadas na rolagem.
class AdaptadorDeProdutos : RecyclerView.Adapter<AdaptadorDeProdutos.Item>() {
    var produtos: List<Produto> = emptyList()

    class Item(view: View) : RecyclerView.ViewHolder(view) {
        val nome: TextView = view.findViewById(R.id.nome)
        val categoria: TextView = view.findViewById(R.id.categoria)
        val preco: TextView = view.findViewById(R.id.preco)
    }

    override fun getItemCount() = produtos.size

    override fun onCreateViewHolder(pai: ViewGroup, tipo: Int) =
        Item(LayoutInflater.from(pai.context).inflate(R.layout.item_produto, pai, false))

    override fun onBindViewHolder(item: Item, posicao: Int) {
        val produto = produtos[posicao]
        item.nome.text = produto.nome
        item.categoria.text = produto.categoria
        item.preco.text = formatarPreco(produto.preco)
    }
}
