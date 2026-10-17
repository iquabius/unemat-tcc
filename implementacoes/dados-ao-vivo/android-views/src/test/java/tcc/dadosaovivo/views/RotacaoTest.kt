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

// A rotação, que a especificação não cobre: o Android recria a Activity, a
// inscrição da tela antiga fecha, e o painel recomeça como se a interface
// abrisse, sem a pausa nem os valores, também depois de escondido.
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w480dp-h280dp-xhdpi")
class RotacaoTest {
    @get:Rule(order = 0) val relogio = RelogioFalso()

    @get:Rule(order = 1)
    val regra = ActivityScenarioRule(MainActivity::class.java)

    private val tela by lazy { Tela(regra.scenario, relogio) }

    @Test
    fun rotacaoRecomecaOPainel() {
        tela.avancar(2000)
        tela.pausa()
        tela.recriar()
        assertEquals(
            listOf("Aguardando placares…", "Pausar", 1),
            listOf(tela.situacao(), tela.textoDaPausa(), contarInscricoes()),
        )

        tela.alternar()
        tela.recriar()
        assertEquals(
            listOf(true, "Esconder painel", 1),
            listOf(
                tela.painelNaPagina(),
                tela.textoDoAlternar(),
                contarInscricoes(),
            ),
        )
    }
}
