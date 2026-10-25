package tcc.dadosaovivo

import java.time.Instant
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Ignore
import org.junit.Rule
import org.junit.Test

// Casos-limite do porte do dominio.ts: o que a web calcula, o Kotlin calcula.
class DominioTest {
    @get:Rule val relogio = RelogioFalso()

    private fun instante(hora: String) = Instant.parse(hora).toEpochMilli()

    private fun linha(lote: Lote, jogo: Jogo) =
        lote.getValue(jogo.codigo).let {
            "${formatarPlacar(it)} ${formatarTempo(it)}"
        }

    @Test
    fun placares() {
        val lote = placaresEm(instante("2026-10-12T10:00:01.999Z"))
        assertEquals(
            listOf("0 × 0 1'", "1 × 0 21'", "1 × 0 41'", "2 × 0 61'"),
            JOGOS.map { linha(lote, it) },
        )
        // O FLA × PAL no minuto 95, em "Fim", e o recomeço da partida.
        val fim = placaresEm(instante("2026-10-12T10:01:35Z"))
        assertEquals("2 × 2 Fim", linha(fim, JOGOS[0]))
        val recomeco = placaresEm(instante("2026-10-12T10:01:40Z"))
        assertEquals("0 × 0 0'", linha(recomeco, JOGOS[0]))
        assertEquals(
            fim.getValue("FLA × PAL").partida + 1,
            recomeco.getValue("FLA × PAL").partida,
        )
    }

    // Documenta a diferença conhecida em relação à web, sem executar: o %
    // do JavaScript dá resto negativo, e o placar de antes de 1970 ninguém
    // pede. A resposta esperada é a do próprio dominio.ts, rodado no Node
    // (docs/adr/0010-dominio-compartilhado-sem-imitar-o-javascript.md).
    @Ignore("diferença conhecida em relação à web; só documenta")
    @Test
    fun igualAoDaWeb() {
        val antes = placaresEm(-1000).getValue("FLA × PAL")
        assertEquals(listOf(-1, -1), listOf(antes.partida, antes.minuto))
    }

    @Test
    fun gols() {
        val antes = Placar(partida = 7, minuto = 1, mandante = 0, visitante = 0)
        assertEquals("—", golsNovos(null, antes))
        assertEquals("—", golsNovos(antes, null))
        assertEquals("=", golsNovos(antes, antes.copy(minuto = 2)))
        assertEquals("+1 × 0", golsNovos(antes, antes.copy(mandante = 1)))
        assertEquals("0 × +1", golsNovos(antes, antes.copy(visitante = 1)))
        assertEquals(
            "+2 × +1",
            golsNovos(antes, antes.copy(mandante = 2, visitante = 1)),
        )
        assertEquals("—", golsNovos(antes, antes.copy(partida = 8)))
    }

    @Test
    fun palpite() {
        val gre = JOGOS[2]
        assertTrue(noPalpite(gre, Placar(0, 41, 1, 0)))
        assertFalse(noPalpite(gre, Placar(0, 42, 1, 1)))
        assertFalse(noPalpite(gre, null))
        assertEquals("1 × 0", formatarPlacar(gre.palpite))
        assertEquals("—", formatarTempo(null))
    }

    @Test
    fun inscricao() {
        val recebidos = mutableListOf<String>()
        val inscricao = inscreverNosPlacares {
            recebidos += linha(it, JOGOS[0])
        }
        assertEquals(1, contarInscricoes())
        relogio.avancar(999)
        assertEquals(emptyList<String>(), recebidos)
        relogio.avancar(1001)
        assertEquals(listOf("0 × 0 1'", "1 × 0 2'"), recebidos)

        inscricao.close()
        inscricao.close()
        assertEquals(0, contarInscricoes())
        relogio.avancar(5000)
        assertEquals(2, recebidos.size)
    }

    @Test
    fun relogioDoPainel() {
        val horas = mutableListOf<Long>()
        val inicio = agora()
        val tiques = iniciarRelogio { horas += agora() - inicio }
        assertEquals(1, contarRelogios())
        relogio.avancar(2500)
        assertEquals(listOf(1000L, 2000L), horas)

        tiques.close()
        tiques.close()
        assertEquals(0, contarRelogios())
        relogio.avancar(5000)
        assertEquals(2, horas.size)
    }

    @Test
    fun atualizacao() {
        val chegada = instante("2026-10-12T10:00:02Z")
        assertEquals("", formatarAtualizacao(null, chegada))
        assertEquals("Atualizado há 0 s", formatarAtualizacao(chegada, chegada))
        assertEquals(
            "Atualizado há 0 s",
            formatarAtualizacao(chegada, chegada + 999),
        )
        assertEquals(
            "Atualizado há 7 s",
            formatarAtualizacao(chegada, chegada + 7000),
        )
        // O agora do último tique, lido antes da chegada do lote.
        assertEquals(
            "Atualizado há 0 s",
            formatarAtualizacao(chegada, chegada - 1000),
        )
    }
}
