package tcc.lista

import org.junit.Assert.assertEquals
import org.junit.Test

// Respostas do próprio dominio.ts, rodado no Node: o porte tem de dar o mesmo
// resultado nas ordens, nos preços, nas categorias e nas buscas.
class DominioTest {
    private fun ids(ordem: Ordem) = produtos.sortedWith(comparador(ordem)).map { it.id }

    private fun busca(texto: String) = produtos.filter { correspondeABusca(it, texto) }.map { it.id }

    @Test
    fun ordens() {
        assertEquals(
            listOf(2, 21, 4, 23, 16, 19, 1, 8, 18, 7, 20, 17, 3, 9, 24, 11, 13, 10, 25, 26, 22, 6, 14, 5, 12, 15, 28, 29, 30, 27),
            ids(Ordem.NOME),
        )
        assertEquals(
            listOf(3, 23, 2, 20, 22, 5, 19, 6, 16, 24, 7, 1, 27, 4, 12, 21, 28, 30, 14, 11, 25, 29, 10, 8, 26, 17, 9, 18, 13, 15),
            ids(Ordem.MENOR_PRECO),
        )
        assertEquals(
            listOf(15, 13, 18, 9, 17, 26, 8, 10, 29, 25, 11, 14, 30, 28, 21, 12, 4, 27, 1, 7, 24, 16, 6, 19, 5, 22, 20, 2, 23, 3),
            ids(Ordem.MAIOR_PRECO),
        )
    }

    @Test
    fun precosECategorias() {
        // Com espaço não separável ( ) depois do R$, como na web.
        assertEquals(
            listOf(
                "39,90", "12,50", "8,99", "45,00", "22,00", "27,90", "34,90", "129,90", "159,00", "119,90",
                "89,90", "49,90", "249,90", "79,90", "399,00", "29,90", "149,90", "199,90", "24,90", "15,90",
                "54,90", "19,90", "9,90", "32,90", "99,90", "139,90", "44,90", "59,90", "119,00", "69,90",
            ).map { "R$ $it" },
            produtos.map { formatarPreco(it.preco) },
        )
        assertEquals(listOf("Casa", "Cozinha", "Eletrônicos", "Mercearia", "Papelaria"), categorias)
        assertEquals("30 de 30 produtos", textoDaContagem(30))
    }

    @Test
    fun buscas() {
        assertEquals(listOf(1, 8), busca("CAFE"))
        assertEquals(listOf(7, 30), busca("  cerâmica "))
        assertEquals(listOf(2), busca("acucar"))
        assertEquals(emptyList<Int>(), busca("ELETRO"))
        assertEquals(listOf(16), busca("usb-c"))
        assertEquals(emptyList<Int>(), busca("xyz"))
        assertEquals((1..30).toList(), busca(""))
        assertEquals(listOf(3, 9), busca("chá"))
        assertEquals(listOf(3, 9), busca("CHA"))
        assertEquals(emptyList<Int>(), busca("ﬁ"))
        assertEquals(emptyList<Int>(), busca("ß"))
    }
}
