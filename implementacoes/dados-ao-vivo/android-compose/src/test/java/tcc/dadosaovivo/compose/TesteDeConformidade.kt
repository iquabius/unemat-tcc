package tcc.dadosaovivo.compose

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.annotation.Config
import tcc.dadosaovivo.RelogioFalso
import tcc.dadosaovivo.contarInscricoes

// As 15 verificações de implementacoes/dados-ao-vivo/teste-de-conformidade.js,
// na mesma ordem e com os mesmos nomes. O relógio falso começa às 10:00:00 UTC
// de 2026-10-12 e só anda com avancar(ms). Falha listando todas as que não
// passaram.
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w480dp-h280dp-xhdpi")
class TesteDeConformidade {
    @get:Rule(order = 0) val relogio = RelogioFalso()

    @get:Rule(order = 1) val regra = createAndroidComposeRule<MainActivity>()

    private val tela by lazy { Tela(regra, relogio) }
    private val falhas = mutableListOf<String>()

    private fun conferir(nome: String, obtido: Any?, esperado: Any?) {
        if (obtido != esperado)
            falhas += "$nome: obtido $obtido, esperado $esperado"
    }

    @Test
    fun verificacoes() {
        val semLote =
            listOf(
                "FLA × PAL | — | — | — | 1 × 0",
                "COR × SAO | — | — | — | 2 × 0",
                "GRE × INT | — | — | — | 1 × 0",
                "CAM × CRU | — | — | — | 2 × 1",
            )
        val primeiroLote =
            listOf(
                "FLA × PAL | 0 × 0 | 1' | — | 1 × 0",
                "COR × SAO | 1 × 0 | 21' | — | 2 × 0",
                "GRE × INT | 1 × 0 | 41' | — | 1 × 0",
                "CAM × CRU | 2 × 0 | 61' | — | 2 × 1",
            )
        val segundoLote =
            listOf(
                "FLA × PAL | 1 × 0 | 2' | +1 × 0 | 1 × 0",
                "COR × SAO | 1 × 0 | 22' | = | 2 × 0",
                "GRE × INT | 1 × 1 | 42' | 0 × +1 | 1 × 0",
                "CAM × CRU | 2 × 0 | 62' | = | 2 × 1",
            )
        // O lote que sai 8 s depois do segundo, com os gols marcados na pausa.
        val loteDepoisDaPausa =
            listOf(
                "FLA × PAL | 1 × 1 | 10' | 0 × +1 | 1 × 0",
                "COR × SAO | 1 × 0 | 30' | = | 2 × 0",
                "GRE × INT | 1 × 1 | 50' | = | 1 × 0",
                "CAM × CRU | 2 × 1 | 70' | 0 × +1 | 2 × 1",
            )

        conferir(
            "1 abre com o painel e uma inscrição",
            listOf(
                tela.textoDoAlternar(),
                tela.painelNaPagina(),
                tela.textoDaPausa(),
                contarInscricoes(),
            ),
            listOf("Esconder painel", true, "Pausar", 1),
        )

        tela.alternar()
        conferir(
            "2 esconder cancela a inscrição",
            listOf(
                tela.painelNaPagina(),
                tela.textoDoAlternar(),
                contarInscricoes(),
            ),
            listOf(false, "Mostrar painel", 0),
        )

        tela.alternar()
        conferir(
            "3 mostrar começa aguardando",
            listOf(
                tela.situacao(),
                tela.linhas(),
                tela.textoDaPausa(),
                tela.textoDoAlternar(),
                contarInscricoes(),
            ),
            listOf(
                "Aguardando placares…",
                semLote,
                "Pausar",
                "Esconder painel",
                1,
            ),
        )
        val regiao = tela.regiao()

        tela.avancar(1000)
        conferir(
            "4 primeiro lote mostra os placares, sem gols novos",
            listOf(tela.situacao(), tela.linhas()),
            listOf("", primeiroLote),
        )
        conferir(
            "4 jogo no palpite fica destacado",
            tela.destacadas(),
            listOf("GRE × INT"),
        )

        tela.avancar(1000)
        conferir(
            "5 lote seguinte mostra os gols desde o anterior",
            tela.linhas(),
            segundoLote,
        )
        conferir(
            "5 jogo que sai do palpite perde o destaque",
            tela.destacadas(),
            listOf("FLA × PAL"),
        )

        tela.pausa()
        conferir(
            "6 pausar cancela a inscrição",
            listOf(tela.situacao(), tela.textoDaPausa(), contarInscricoes()),
            listOf("Pausado.", "Retomar", 0),
        )
        tela.avancar(7000)
        conferir("6 em pausa a tabela não muda", tela.linhas(), segundoLote)

        tela.pausa()
        conferir(
            "7 retomar inscreve o painel de novo",
            listOf(tela.situacao(), tela.textoDaPausa(), contarInscricoes()),
            listOf("", "Pausar", 1),
        )
        // O lote sai 8 s depois do segundo; os gols da pausa contam desde ele.
        tela.avancar(1000)
        conferir(
            "7 gols novos contam desde o último lote mostrado",
            listOf(tela.linhas(), tela.destacadas()),
            listOf(loteDepoisDaPausa, listOf("CAM × CRU")),
        )

        conferir(
            "8 a situação é a mesma região de status",
            listOf(tela.regiao() == regiao, tela.papelDaRegiao()),
            listOf(true, "status"),
        )

        tela.pausa()
        tela.alternar()
        tela.alternar()
        conferir(
            "9 mostrar depois de esconder em pausa começa sem pausa",
            listOf(
                tela.situacao(),
                tela.textoDaPausa(),
                tela.linhas(),
                contarInscricoes(),
            ),
            listOf("Aguardando placares…", "Pausar", semLote, 1),
        )

        tela.pausa()
        tela.pausa()
        conferir(
            "10 retomar antes do primeiro lote volta a aguardar",
            listOf(tela.situacao(), contarInscricoes()),
            listOf("Aguardando placares…", 1),
        )

        repeat(3) {
            tela.alternar()
            tela.alternar()
        }
        conferir(
            "11 esconder e mostrar três vezes deixa uma inscrição",
            contarInscricoes(),
            1,
        )

        assertTrue(falhas.joinToString("\n"), falhas.isEmpty())
    }
}
