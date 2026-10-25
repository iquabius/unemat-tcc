package tcc.logincomquarentena

import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test

// Casos-limite do porte do dominio.ts: o que a web calcula, o Kotlin calcula.
// As corrotinas rodam no despachante Unconfined, que as retoma na hora, na
// thread do teste, e só o relógio falso as faz andar.
class DominioTest {
    @get:Rule val relogio = RelogioFalso()

    private val escopo = CoroutineScope(Dispatchers.Unconfined)

    @Test
    fun entrar() {
        assertFalse(podeEntrar("a", "bb"))
        assertFalse(podeEntrar("ana", "s"))
        assertTrue(podeEntrar("an", "ss"))
        // Como o length do JavaScript, o do Kotlin conta unidades de UTF-16:
        // um emoji vale dois caracteres nas duas plataformas.
        assertTrue(podeEntrar("😀", "ss"))
        assertEquals("Tempo de sessão: 3 s", tempoDeSessao(3))
    }

    @Test
    fun autenticacao() {
        val respostas = mutableListOf<Boolean>()
        escopo.launch { respostas += autenticar("ana", "segredo") }
        escopo.launch { respostas += autenticar("ana", "errada") }
        escopo.launch { respostas += autenticar("Ana", "segredo") }
        assertEquals(3, contarAbertos())
        relogio.avancar(999)
        assertEquals(emptyList<Boolean>(), respostas)
        relogio.avancar(1)
        assertEquals(listOf(true, false, false), respostas)
        assertEquals(0, contarAbertos())
    }

    @Test
    fun cancelamento() {
        val respostas = mutableListOf<Boolean>()
        val tentativa = escopo.launch {
            respostas += autenticar("ana", "segredo")
        }
        relogio.avancar(500)
        tentativa.cancel()
        assertEquals(0, contarAbertos())
        relogio.avancar(1000)
        assertEquals(emptyList<Boolean>(), respostas)
    }

    @Test
    fun relogioDaSessao() {
        var tiques = 0
        val sessao = escopo.iniciarRelogio { tiques++ }
        assertEquals(1, contarAbertos())
        relogio.avancar(999)
        assertEquals(0, tiques)
        relogio.avancar(2001)
        assertEquals(3, tiques)

        sessao.cancel()
        sessao.cancel()
        assertEquals(0, contarAbertos())
        relogio.avancar(5000)
        assertEquals(3, tiques)
    }

    // A expiração: o tique que para o próprio relógio, como o
    // encerrarSessao() dentro do aoTique.
    @Test
    fun relogioParadoNoTique() {
        var tiques = 0
        lateinit var sessao: Job
        sessao = escopo.iniciarRelogio {
            tiques++
            if (tiques == 2) sessao.cancel()
        }
        relogio.avancar(5000)
        assertEquals(2, tiques)
        assertEquals(0, contarAbertos())
    }
}
