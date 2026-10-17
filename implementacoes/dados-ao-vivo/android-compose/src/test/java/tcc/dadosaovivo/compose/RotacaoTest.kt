package tcc.dadosaovivo.compose

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.annotation.Config
import tcc.dadosaovivo.RelogioFalso
import tcc.dadosaovivo.contarInscricoes
import tcc.dadosaovivo.contarRelogios

// A rotação, que a especificação não cobre: o Android recria a Activity, a
// inscrição e o relógio da tela antiga fecham, e o painel recomeça como se a
// interface abrisse, sem a pausa nem os valores, também depois de escondido.
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w480dp-h320dp-xhdpi")
class RotacaoTest {
    @get:Rule(order = 0) val relogio = RelogioFalso()

    @get:Rule(order = 1) val regra = createAndroidComposeRule<MainActivity>()

    private val tela by lazy { Tela(regra, relogio) }

    @Test
    fun rotacaoRecomecaOPainel() {
        tela.avancar(2000)
        tela.pausa()
        tela.recriar()
        assertEquals(
            listOf("Aguardando placares…", "Pausar", 1, 1),
            listOf(
                tela.situacao(),
                tela.textoDaPausa(),
                contarInscricoes(),
                contarRelogios(),
            ),
        )

        tela.alternar()
        tela.recriar()
        assertEquals(
            listOf(true, "Esconder painel", 1, 1),
            listOf(
                tela.painelNaPagina(),
                tela.textoDoAlternar(),
                contarInscricoes(),
                contarRelogios(),
            ),
        )
    }
}
