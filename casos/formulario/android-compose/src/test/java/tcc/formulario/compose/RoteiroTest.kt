package tcc.formulario.compose

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.annotation.Config
import tcc.formulario.DataFixa
import tcc.formulario.TipoDeVoo

// As 19 verificações de casos/formulario/roteiro-de-teste.js, na mesma ordem
// e com os mesmos nomes. Falha listando todas as que não passaram.
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w416dp-h560dp-xhdpi")
class RoteiroTest {
    @get:Rule(order = 0)
    val dataFixa = DataFixa()

    @get:Rule(order = 1)
    val regra = createAndroidComposeRule<MainActivity>()

    private val tela by lazy { Tela(regra) }
    private val falhas = mutableListOf<String>()

    private fun conferir(nome: String, obtido: Any?, esperado: Any?) {
        if (obtido != esperado) falhas += "$nome: obtido $obtido, esperado $esperado"
    }

    @Test
    fun roteiro() {
        val nome = "Informe o nome do passageiro."
        val email = "Informe um e-mail válido."
        val data = "Use uma data válida no formato DD/MM/AAAA."
        val ordem = "A volta não pode ser antes da ida."

        conferir("1 botão começa desabilitado", tela.botaoHabilitado(), false)
        conferir("1 nenhum erro visível", tela.erros(), emptyList<String>())
        conferir("1 datas começam hoje", listOf(tela.valor(Campo.IDA), tela.valor(Campo.VOLTA)), listOf("26/09/2026", "26/09/2026"))
        conferir("1 volta começa desabilitada", tela.habilitado(Campo.VOLTA), false)

        tela.sair(Campo.NOME)
        conferir("2 nome tocado e vazio", listOf(tela.erros(), tela.invalido(Campo.NOME)), listOf(listOf(nome), true))
        tela.digitar(Campo.NOME, "Maria")
        conferir("3 nome preenchido", tela.erros(), emptyList<String>())

        tela.digitar(Campo.EMAIL, "maria@")
        conferir("4 e-mail inválido antes de tocar", tela.erros(), emptyList<String>())
        tela.sair(Campo.EMAIL)
        conferir("4 e-mail inválido depois de tocar", tela.erros(), listOf(email))
        tela.digitar(Campo.EMAIL, "maria@exemplo.com")
        conferir("4 e-mail corrigido", tela.erros(), emptyList<String>())
        conferir("5 botão habilitado (só ida)", tela.botaoHabilitado(), true)

        tela.digitar(Campo.IDA, "31/02/2026")
        tela.sair(Campo.IDA)
        conferir("6 data inexistente", listOf(tela.erros(), tela.botaoHabilitado()), listOf(listOf(data), false))
        tela.digitar(Campo.IDA, "10/10/2099")
        conferir("6 data corrigida", listOf(tela.erros(), tela.botaoHabilitado()), listOf(emptyList<String>(), true))

        tela.escolherTipo(TipoDeVoo.IDA_E_VOLTA)
        conferir("7 volta habilitada", tela.habilitado(Campo.VOLTA), true)
        conferir("7 volta antes da ida", listOf(tela.erros(), tela.botaoHabilitado()), listOf(listOf(ordem), false))
        tela.digitar(Campo.VOLTA, "1/1/2100")
        tela.sair(Campo.VOLTA)
        conferir("8 volta mal formatada", listOf(tela.erros(), tela.botaoHabilitado()), listOf(listOf(data), false))
        tela.digitar(Campo.VOLTA, "15/10/2099")
        conferir("8 volta corrigida", listOf(tela.erros(), tela.botaoHabilitado()), listOf(emptyList<String>(), true))

        tela.reservar()
        conferir(
            "9 confirmação de ida e volta",
            tela.confirmacao(),
            "Voo de ida e volta reservado para Maria: ida em 10/10/2099 e volta em 15/10/2099. " +
                "A confirmação vai para maria@exemplo.com.",
        )

        tela.digitar(Campo.VOLTA, "xx")
        tela.escolherTipo(TipoDeVoo.IDA)
        conferir(
            "10 volta desabilitada não conta",
            listOf(tela.habilitado(Campo.VOLTA), tela.erros(), tela.botaoHabilitado()),
            listOf(false, emptyList<String>(), true),
        )
        tela.reservar()
        conferir(
            "10 confirmação só de ida",
            tela.confirmacao(),
            "Voo só de ida reservado para Maria em 10/10/2099. A confirmação vai para maria@exemplo.com.",
        )

        assertTrue(falhas.joinToString("\n"), falhas.isEmpty())
    }
}
