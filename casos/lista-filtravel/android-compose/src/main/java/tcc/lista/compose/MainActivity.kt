package tcc.lista.compose

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.lazy.items
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.semantics
import tcc.lista.Ordem
import tcc.lista.categorias
import tcc.lista.comparador
import tcc.lista.correspondeABusca
import tcc.lista.daCategoria
import tcc.lista.formatarPreco
import tcc.lista.produtos
import tcc.lista.textoDaContagem

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Como o createRoot(...).render(...) do React; o Tema faz o papel
        // do import do estilo.css.
        setContent { Tema { CatalogoDeProdutos() } }
    }
}

// Função que descreve a tela a partir do estado, como o componente React.
// A aparência fica em Estilo.kt.
@Composable
fun CatalogoDeProdutos() {
    // Como os useState: mudar um valor faz a função rodar de novo.
    var busca by remember { mutableStateOf("") }
    var categoria by remember { mutableStateOf("") }
    var ordem by remember { mutableStateOf(Ordem.NOME) }

    // A lista visível é derivada do estado a cada recomposição.
    val visiveis = produtos
        .filter { correspondeABusca(it, busca) && daCategoria(it, categoria) }
        .sortedWith(comparador(ordem))

    Catalogo {
        Filtros {
            Rotulo("Buscar") {
                Entrada(busca, { busca = it }, dica = "Nome do produto")
            }
            Rotulo("Categoria") {
                Selecao(
                    opcoes = listOf("" to "Todas") + categorias.map { it to it },
                    escolhida = categoria,
                    aoEscolher = { categoria = it },
                )
            }
            Rotulo("Ordenar por") {
                Selecao(
                    opcoes = Ordem.entries.map { it to it.rotulo },
                    escolhida = ordem,
                    aoEscolher = { ordem = it },
                )
            }
        }
        // Como o role="status": o leitor de tela anuncia a mudança.
        Contagem(textoDaContagem(visiveis.size), Modifier.semantics { liveRegion = LiveRegionMode.Polite })
        // Como o map com key do React: a LazyColumn só compõe os itens que
        // aparecem na tela.
        Produtos {
            items(visiveis, key = { it.id }) { produto ->
                Produto(produto.nome, produto.categoria, formatarPreco(produto.preco))
            }
        }
        if (visiveis.isEmpty()) Contagem("Nenhum produto encontrado.")
    }
}
