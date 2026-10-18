package tcc.logincomquarentena

import kotlin.coroutines.Continuation
import kotlin.coroutines.resume
import kotlinx.coroutines.suspendCancellableCoroutine
import org.junit.rules.ExternalResource

// Regra JUnit que troca a espera do domínio pela de um relógio falso, como o
// instalarRelogioFalso do teste da web: o tempo começa em 0 e só anda com
// avancar(ms), que retoma na hora certa as esperas que vencerem até lá. A
// hora do Robolectric e a do relógio do teste do Compose não servem: as
// esperas do teste as fazem andar a cada clique.
class RelogioFalso : ExternalResource() {
    private class Espera(val quando: Long, val continuacao: Continuation<Unit>)

    private var agora = 0L
    private val pendentes = mutableListOf<Espera>()
    private val original = esperar

    override fun before() {
        esperar = { ms ->
            suspendCancellableCoroutine { continuacao ->
                val espera = Espera(agora + ms, continuacao)
                pendentes += espera
                // Como o clearTimeout: a corrotina cancelada sai da fila.
                continuacao.invokeOnCancellation { pendentes -= espera }
            }
        }
    }

    override fun after() {
        esperar = original
        pendentes.clear()
    }

    /**
     * Anda ms, retomando as esperas vencidas uma a uma, pela ordem da hora. A
     * corrotina retomada roda no despachante dela; escoar a deixa rodar até a
     * próxima espera, como o escoar da web, antes de procurar a seguinte.
     */
    fun avancar(ms: Long, escoar: () -> Unit = {}) {
        val fim = agora + ms
        while (true) {
            escoar()
            val proxima =
                pendentes.filter { it.quando <= fim }.minByOrNull { it.quando }
                    ?: break
            pendentes -= proxima
            agora = proxima.quando
            proxima.continuacao.resume(Unit)
        }
        agora = fim
    }
}
