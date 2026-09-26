package tcc.formulario

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Rule
import org.junit.Test

// Casos-limite do porte do dominio.ts: o que a web aceita, o Kotlin aceita.
class DominioTest {
    @get:Rule
    val dataFixa = DataFixa()

    @Test
    fun datas() {
        assertNotNull(parsearData("29/02/2028"))
        assertNotNull(parsearData(" 10/10/2026 "))
        assertNull(parsearData("31/02/2026"))
        assertNull(parsearData("29/02/2027"))
        assertNull(parsearData("1/1/2100"))
        assertNull(parsearData("10-10-2026"))
        assertEquals("26/09/2026", hoje())
    }

    @Test
    fun emails() {
        assertNull(erroDoEmail("maria@exemplo.com"))
        assertNull(erroDoEmail(" maria@exemplo.com "))
        assertEquals("Informe um e-mail válido.", erroDoEmail("maria@"))
        assertEquals("Informe um e-mail válido.", erroDoEmail("maria@exemplo"))
        assertEquals("Informe um e-mail válido.", erroDoEmail("ma ria@exemplo.com"))
    }

    @Test
    fun nomeEOrdem() {
        assertEquals("Informe o nome do passageiro.", erroDoNome("   "))
        assertNull(erroDoNome("Maria"))
        assertEquals("A volta não pode ser antes da ida.", erroDaOrdem("10/10/2026", "09/10/2026"))
        assertNull(erroDaOrdem("10/10/2026", "10/10/2026"))
        assertNull(erroDaOrdem("xx", "09/10/2026"))
    }

    @Test
    fun confirmacoes() {
        assertEquals(
            "Voo só de ida reservado para Maria em 10/10/2026. A confirmação vai para maria@exemplo.com.",
            mensagemDeConfirmacao(Reserva(" Maria ", "maria@exemplo.com", TipoDeVoo.IDA, "10/10/2026", "")),
        )
        assertEquals(
            "Voo de ida e volta reservado para Maria: ida em 10/10/2026 e volta em 15/10/2026. " +
                "A confirmação vai para maria@exemplo.com.",
            mensagemDeConfirmacao(
                Reserva("Maria", "maria@exemplo.com", TipoDeVoo.IDA_E_VOLTA, "10/10/2026", "15/10/2026"),
            ),
        )
    }
}
