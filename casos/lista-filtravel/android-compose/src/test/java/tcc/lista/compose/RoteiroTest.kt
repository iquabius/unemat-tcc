package tcc.lista.compose

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.annotation.Config
import tcc.lista.Ordem

// As 11 verificações de casos/lista-filtravel/roteiro-de-teste.js, na mesma
// ordem e com os mesmos nomes. A tela é alta para caber a lista inteira.
// Falha listando todas as que não passaram.
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w480dp-h1950dp-xhdpi")
class RoteiroTest {
    @get:Rule
    val regra = createAndroidComposeRule<MainActivity>()

    private val tela by lazy { Tela(regra) }
    private val falhas = mutableListOf<String>()

    private fun conferir(nome: String, obtido: Any?, esperado: Any?) {
        if (obtido != esperado) falhas += "$nome: obtido $obtido, esperado $esperado"
    }

    @Test
    fun roteiro() {
        conferir("1 contagem inicial", tela.contagem(), "30 de 30 produtos")
        conferir("1 ordem por nome", tela.nomes().take(3), listOf("Açúcar mascavo 1 kg", "Agenda 2027", "Azeite extravirgem 500 ml"))
        conferir("1 categorias", tela.opcoesDeCategoria(), listOf("Todas", "Casa", "Cozinha", "Eletrônicos", "Mercearia", "Papelaria"))
        conferir("1 sem aviso de vazio", tela.vazio(), false)
        conferir("1 preço formatado", tela.primeiroPreco(), "R$ 12,50")

        tela.buscar("CAFE")
        conferir("2 busca sem acento e em maiúsculas", listOf(tela.contagem(), tela.nomes()), listOf("2 de 30 produtos", listOf("Café em grãos 500 g", "Cafeteira italiana")))
        tela.buscar("  cerâmica ")
        conferir("3 busca com acento e espaços", tela.nomes(), listOf("Caneca de cerâmica", "Vaso de cerâmica"))

        tela.buscar("")
        tela.escolherCategoria("Cozinha")
        tela.escolherOrdem(Ordem.MAIOR_PRECO)
        conferir("4 cozinha por maior preço", tela.nomes(), listOf("Chaleira elétrica", "Cafeteira italiana", "Frigideira antiaderente", "Faca do chef", "Tábua de corte", "Caneca de cerâmica"))

        tela.escolherCategoria("")
        tela.escolherOrdem(Ordem.MENOR_PRECO)
        conferir("5 todas por menor preço", listOf(tela.contagem(), tela.nomes().take(2)), listOf("30 de 30 produtos", listOf("Chá de camomila", "Bloco de notas adesivas")))

        tela.buscar("xyz")
        conferir("6 nenhum resultado", listOf(tela.contagem(), tela.nomes().size, tela.vazio()), listOf("0 de 30 produtos", 0, true))
        tela.buscar("")
        conferir("7 volta ao catálogo inteiro", listOf(tela.contagem(), tela.vazio()), listOf("30 de 30 produtos", false))

        assertTrue(falhas.joinToString("\n"), falhas.isEmpty())
    }
}
