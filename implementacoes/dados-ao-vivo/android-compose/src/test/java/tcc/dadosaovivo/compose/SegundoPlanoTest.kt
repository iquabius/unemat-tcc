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

// A tela em segundo plano, que a especificação não cobre e em que as duas
// tecnologias diferem (ADR 0005; docs/achados-das-implementacoes.md): no
// Compose, o DisposableEffect vive com a composição, que continua com a
// Activity parada; a inscrição e o relógio seguem abertos, os lotes seguem
// chegando, e de volta os gols novos contam desde o último lote recebido em
// segundo plano. No Views, o onStop fecha os dois.
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w480dp-h320dp-xhdpi")
class SegundoPlanoTest {
    @get:Rule(order = 0) val relogio = RelogioFalso()

    @get:Rule(order = 1) val regra = createAndroidComposeRule<MainActivity>()

    private val tela by lazy { Tela(regra, relogio) }

    @Test
    fun segundoPlanoMantemAInscricao() {
        tela.avancar(1000)
        tela.irParaSegundoPlano()
        val emSegundoPlano = listOf(contarInscricoes(), contarRelogios())
        relogio.avancar(3000)
        tela.voltarDoSegundoPlano()
        val aoVoltar = tela.atualizacao()
        tela.avancar(1000)
        assertEquals(
            listOf(
                listOf(1, 1),
                "Atualizado há 0 s",
                listOf(1, 1),
                "FLA × PAL | 1 × 0 | 5' | = | 1 × 0",
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
