package tcc.dadosaovivo

import java.io.Closeable
import java.time.Instant
import org.junit.rules.ExternalResource

// Regra JUnit que troca o relógio da fonte por um relógio falso, como o
// instalarRelogioFalso do teste da web: a hora começa às 10:00:00 UTC de
// 2026-10-12 e só anda com avancar(ms), que roda na hora certa as repetições
// que vencerem até lá. A hora do Robolectric não serve: as esperas do teste
// do Compose a fazem andar até 250 ms a cada clique.
class RelogioFalso : ExternalResource(), Relogio {
    private class Repeticao(
        var quando: Long,
        val ms: Long,
        val acao: () -> Unit,
    )

    private var hora = Instant.parse("2026-10-12T10:00:00Z").toEpochMilli()
    private val pendentes = mutableListOf<Repeticao>()

    override fun before() {
        relogioDaFonte = this
    }

    override fun after() {
        relogioDaFonte = RelogioDoSistema
    }

    override fun agora() = hora

    override fun aCada(ms: Long, acao: () -> Unit): Closeable {
        val repeticao = Repeticao(hora + ms, ms, acao)
        pendentes += repeticao
        return Closeable { pendentes -= repeticao }
    }

    fun avancar(ms: Long) {
        val fim = hora + ms
        while (true) {
            val proxima =
                pendentes.filter { it.quando <= fim }.minByOrNull { it.quando }
                    ?: break
            hora = proxima.quando
            proxima.quando += proxima.ms
            proxima.acao()
        }
        hora = fim
    }
}
