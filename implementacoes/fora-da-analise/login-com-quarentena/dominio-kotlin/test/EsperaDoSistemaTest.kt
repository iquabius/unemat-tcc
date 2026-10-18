package tcc.logincomquarentena

import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertTrue
import org.junit.Test

// A espera de verdade do domínio, o delay, que os outros testes trocam pela
// do relógio falso: a resposta leva LATENCIA_MS de relógio.
class EsperaDoSistemaTest {
    @Test
    fun autenticarEsperaALatencia() {
        val inicio = System.nanoTime()
        val valida = runBlocking { autenticar("ana", "segredo") }
        val decorridos = (System.nanoTime() - inicio) / 1_000_000
        assertTrue(valida)
        assertTrue("$decorridos ms", decorridos >= LATENCIA_MS)
    }
}
