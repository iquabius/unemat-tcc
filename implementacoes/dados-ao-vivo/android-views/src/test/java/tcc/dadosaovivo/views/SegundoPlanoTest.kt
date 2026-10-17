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
import tcc.dadosaovivo.contarRelogios

// A tela em segundo plano, que a especificação não cobre e em que as duas
// tecnologias diferem (ADR 0005; docs/achados-das-implementacoes.md): no
// Views, o onStop fecha a inscrição e o relógio; de volta, o "Atualizado há"
// diz já a idade do último lote, e os gols novos contam desde o último lote
// que o usuário viu. No Compose, a inscrição e o relógio continuam.
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w480dp-h320dp-xhdpi")
class SegundoPlanoTest {
    @get:Rule(order = 0) val relogio = RelogioFalso()

    @get:Rule(order = 1)
    val regra = ActivityScenarioRule(MainActivity::class.java)

    private val tela by lazy { Tela(regra.scenario, relogio) }

    @Test
    fun segundoPlanoFechaAInscricao() {
        tela.avancar(1000)
        tela.irParaSegundoPlano()
        val emSegundoPlano = listOf(contarInscricoes(), contarRelogios())
        relogio.avancar(3000)
        tela.voltarDoSegundoPlano()
        val aoVoltar = tela.atualizacao()
        tela.avancar(1000)
        assertEquals(
            listOf(
                listOf(0, 0),
                "Atualizado há 3 s",
                listOf(1, 1),
                "FLA × PAL | 1 × 0 | 5' | +1 × 0 | 1 × 0",
            ),
            listOf(
                emSegundoPlano,
                aoVoltar,
                listOf(contarInscricoes(), contarRelogios()),
                tela.linhas()[0],
            ),
        )
    }
}
