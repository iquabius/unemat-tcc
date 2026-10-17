package tcc.dadosaovivo.views

import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.annotation.Config
import tcc.dadosaovivo.RelogioFalso
import tcc.dadosaovivo.contarInscricoes

// A tela em segundo plano, que a especificação não cobre e em que as duas
// tecnologias diferem (ADR 0005; docs/achados-das-implementacoes.md): no
// Views, o onStop fecha a inscrição, e de volta os gols novos contam desde o
// último lote que o usuário viu. No Compose, a inscrição continua.
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w480dp-h280dp-xhdpi")
class SegundoPlanoTest {
    @get:Rule(order = 0) val relogio = RelogioFalso()

    @get:Rule(order = 1)
    val regra = ActivityScenarioRule(MainActivity::class.java)

    private val tela by lazy { Tela(regra.scenario, relogio) }

    @Test
    fun segundoPlanoFechaAInscricao() {
        tela.avancar(1000)
        tela.irParaSegundoPlano()
        val emSegundoPlano = contarInscricoes()
        relogio.avancar(3000)
        tela.voltarDoSegundoPlano()
        tela.avancar(1000)
        assertEquals(
            listOf(0, 1, "FLA × PAL | 1 × 0 | 5' | +1 × 0 | 1 × 0"),
            listOf(emSegundoPlano, contarInscricoes(), tela.linhas()[0]),
        )
    }
}
