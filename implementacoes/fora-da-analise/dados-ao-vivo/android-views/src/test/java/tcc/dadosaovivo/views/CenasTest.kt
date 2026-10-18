package tcc.dadosaovivo.views

import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.annotation.Config
import tcc.captura.SemAnimacoes
import tcc.captura.capturar
import tcc.dadosaovivo.RelogioFalso

// Mesmas cenas de implementacoes/dados-ao-vivo/cenas.mts, com a largura da
// captura da web. O placar depende do relógio falso, que começa às 10:00:00
// UTC; cada cena esconde e mostra o painel, para a inscrição começar com ela.
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w480dp-h320dp-xhdpi")
class CenasTest {
    @get:Rule(order = 0) val relogio = RelogioFalso()

    @get:Rule(order = 1) val semAnimacoes = SemAnimacoes()

    @get:Rule(order = 2)
    val regra = ActivityScenarioRule(MainActivity::class.java)

    private val tela by lazy { Tela(regra.scenario, relogio) }

    private fun mostrarDeNovo() {
        tela.alternar()
        tela.alternar()
    }

    // Os dois primeiros lotes da especificação, às 10:00:01 e às 10:00:02
    // UTC: os gols novos, o destaque do FLA × PAL e o GRE × INT que perdeu o
    // destaque.
    private fun doisLotes() {
        mostrarDeNovo()
        tela.avancar(2000)
    }

    @Test
    fun aguardando() {
        mostrarDeNovo()
        capturar("aguardando")
    }

    @Test
    fun aoVivo() {
        doisLotes()
        capturar("ao-vivo")
    }

    @Test
    fun pausado() {
        doisLotes()
        tela.pausa()
        capturar("pausado")
    }

    @Test
    fun escondido() {
        tela.alternar()
        capturar("escondido")
    }
}
