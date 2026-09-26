package tcc.lista.views

import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.annotation.Config
import tcc.captura.SemAnimacoes
import tcc.captura.capturar
import tcc.lista.Ordem

// Mesmas cenas de casos/lista-filtravel/cenas.mts. Cada cena tem a altura de
// tela que a lista pede, como a captura da página inteira na web. A busca é
// escrita sem focar o campo: com foco, o teste seguinte do Compose chegou a
// capturar a tela anterior à busca (e a web também não mostra o cursor).
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w480dp-h1950dp-xhdpi")
class CenasTest {
    @get:Rule(order = 0)
    val semAnimacoes = SemAnimacoes()

    @get:Rule(order = 1)
    val regra = ActivityScenarioRule(MainActivity::class.java)

    private val tela by lazy { Tela(regra.scenario) }

    @Test
    fun inicial() = capturar("inicial")

    // Busca sem acento e em maiúsculas acha nomes com acento.
    @Test
    @Config(qualifiers = "+h420dp")
    fun buscaCafe() {
        tela.buscar("CAFE")
        capturar("busca-cafe")
    }

    @Test
    @Config(qualifiers = "+h640dp")
    fun cozinhaMaiorPreco() {
        tela.escolherCategoria("Cozinha")
        tela.escolherOrdem(Ordem.MAIOR_PRECO)
        capturar("cozinha-maior-preco")
    }

    @Test
    @Config(qualifiers = "+h340dp")
    fun vazio() {
        tela.buscar("xyz")
        capturar("vazio")
    }
}
