package tcc.lista.views

import android.os.Looper
import android.widget.EditText
import android.widget.Spinner
import android.widget.TextView
import androidx.core.view.isVisible
import androidx.recyclerview.widget.RecyclerView
import androidx.test.core.app.ActivityScenario
import org.robolectric.Shadows.shadowOf
import tcc.lista.Ordem
import tcc.lista.categorias
import java.time.Duration

// Ações e leituras usadas pelas cenas e pelo roteiro, como as funções do
// roteiro-de-teste.js. A Tela do Compose tem os mesmos nomes.
class Tela(private val cenario: ActivityScenario<MainActivity>) {
    private fun <T> naTela(bloco: (MainActivity) -> T): T {
        var resultado: Any? = null
        cenario.onActivity { resultado = bloco(it) }
        shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(100))
        @Suppress("UNCHECKED_CAST")
        return resultado as T
    }

    // Como o setter + evento "input" do roteiro; o cursor vai para o fim.
    fun buscar(texto: String) = naTela {
        val busca = it.findViewById<EditText>(R.id.busca)
        busca.setText(texto)
        busca.setSelection(texto.length)
    }

    fun escolherCategoria(categoria: String) = naTela {
        it.findViewById<Spinner>(R.id.categoria).setSelection(categorias.indexOf(categoria) + 1)
    }

    fun escolherOrdem(ordem: Ordem) = naTela { it.findViewById<Spinner>(R.id.ordem).setSelection(ordem.ordinal) }

    fun opcoesDeCategoria() = naTela { atividade ->
        val adaptador = atividade.findViewById<Spinner>(R.id.categoria).adapter
        (0 until adaptador.count).map { adaptador.getItem(it).toString() }
    }

    // Os textos de cada item da lista, na ordem da tela: nome, categoria, preço.
    private fun itens() = naTela { atividade ->
        val lista = atividade.findViewById<RecyclerView>(R.id.produtos)
        (0 until lista.adapter!!.itemCount).map { posicao ->
            val item = lista.findViewHolderForAdapterPosition(posicao)!!.itemView
            listOf(R.id.nome, R.id.categoria, R.id.preco).map { item.findViewById<TextView>(it).text.toString() }
        }
    }

    fun nomes() = itens().map { it[0] }

    // Como o texto() do roteiro, que troca o espaço não separável do preço.
    fun primeiroPreco() = itens().first()[2].replace(' ', ' ')

    fun contagem() = naTela { it.findViewById<TextView>(R.id.contagem).text.toString() }

    fun vazio() = naTela { it.findViewById<TextView>(R.id.vazio).isVisible }
}
