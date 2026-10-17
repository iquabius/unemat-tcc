package tcc.logincomquarentena.views

import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.annotation.Config
import tcc.logincomquarentena.RelogioFalso
import tcc.logincomquarentena.contarAbertos

// As 23 verificações de
// implementacoes/login-com-quarentena/teste-de-conformidade.js, na mesma ordem
// e com os mesmos nomes, com latência de 1 s e sessão de 10 s. O relógio falso
// só anda com avancar(ms). Falha listando todas as que não passaram.
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w480dp-h360dp-xhdpi")
class TesteDeConformidade {
    @get:Rule(order = 0) val relogio = RelogioFalso()

    @get:Rule(order = 1)
    val regra = ActivityScenarioRule(MainActivity::class.java)

    private val tela by lazy { Tela(regra.scenario, relogio) }
    private val falhas = mutableListOf<String>()

    private fun conferir(nome: String, obtido: Any?, esperado: Any?) {
        if (obtido != esperado)
            falhas += "$nome: obtido $obtido, esperado $esperado"
    }

    @Test
    fun verificacoes() {
        val regiao = tela.regiao()
        conferir(
            "1 começa desconectado",
            listOf(
                tela.situacao(),
                tela.tempo(),
                tela.temSair(),
                tela.entrarHabilitado(),
            ),
            listOf("Desconectado.", null, false, false),
        )

        tela.digitar(Campo.NOME, "a")
        tela.digitar(Campo.SENHA, "bb")
        conferir(
            "2 nome com 1 caractere desabilita o Entrar",
            tela.entrarHabilitado(),
            false,
        )
        tela.digitar(Campo.NOME, "ana")
        tela.digitar(Campo.SENHA, "s")
        conferir(
            "2 senha com 1 caractere desabilita o Entrar",
            tela.entrarHabilitado(),
            false,
        )
        tela.digitar(Campo.SENHA, "errada")
        conferir(
            "2 nome e senha com 2 caracteres ou mais habilitam o Entrar",
            tela.entrarHabilitado(),
            true,
        )

        tela.entrar()
        conferir("3 conectando", tela.situacao(), "Conectando…")
        tela.avancar(1000)
        conferir(
            "4 falha",
            listOf(
                tela.situacao(),
                tela.tempo(),
                tela.temSair(),
                tela.entrarHabilitado(),
            ),
            listOf("Nome ou senha incorretos.", null, false, true),
        )

        tela.entrar()
        tela.avancar(500)
        tela.digitar(Campo.SENHA, "segredo")
        tela.entrar()
        conferir("5 tentativa nova cancela a anterior", contarAbertos(), 1)
        tela.avancar(600)
        conferir(
            "5 resposta da tentativa substituída não aparece",
            tela.situacao(),
            "Conectando…",
        )
        tela.avancar(400)
        conferir(
            "6 sucesso",
            listOf(tela.situacao(), tela.tempo(), tela.temSair()),
            listOf("Conectado.", "Tempo de sessão: 0 s", true),
        )
        tela.avancar(3000)
        conferir(
            "6 tempo de sessão soma 1 por segundo",
            tela.tempo(),
            "Tempo de sessão: 3 s",
        )

        tela.digitar(Campo.SENHA, "x")
        conferir(
            "7 edição na sessão só muda o Entrar",
            listOf(
                tela.situacao(),
                tela.tempo(),
                tela.temSair(),
                tela.entrarHabilitado(),
            ),
            listOf("Conectado.", "Tempo de sessão: 3 s", true, false),
        )

        tela.digitar(Campo.SENHA, "segredo")
        tela.entrar()
        conferir(
            "8 Entrar na sessão a encerra",
            listOf(tela.situacao(), tela.tempo(), tela.temSair()),
            listOf("Conectando…", null, false),
        )
        tela.avancar(900)
        conferir(
            "8 relógio da sessão encerrada não volta",
            listOf(tela.situacao(), tela.tempo(), contarAbertos()),
            listOf("Conectando…", null, 1),
        )
        tela.avancar(100)
        conferir(
            "8 sessão nova começa em 0 s",
            listOf(tela.situacao(), tela.tempo()),
            listOf("Conectado.", "Tempo de sessão: 0 s"),
        )

        tela.digitar(Campo.SENHA, "errada")
        tela.entrar()
        tela.digitar(Campo.SENHA, "segredo")
        tela.entrar()
        tela.digitar(Campo.SENHA, "outra")
        tela.avancar(1000)
        conferir(
            "9 edição na tentativa não a muda",
            listOf(tela.situacao(), tela.tempo()),
            listOf("Conectado.", "Tempo de sessão: 0 s"),
        )

        tela.sair()
        conferir(
            "10 Sair",
            listOf(
                tela.situacao(),
                tela.tempo(),
                tela.temSair(),
                contarAbertos(),
            ),
            listOf("Desconectado.", null, false, 0),
        )
        tela.avancar(5000)
        conferir(
            "10 relógio parado depois de Sair",
            listOf(tela.situacao(), tela.tempo()),
            listOf("Desconectado.", null),
        )

        tela.digitar(Campo.SENHA, "segredo")
        tela.entrar()
        tela.avancar(1000)
        tela.avancar(9000)
        conferir(
            "11 aos 9 s ainda conectado",
            listOf(tela.situacao(), tela.tempo()),
            listOf("Conectado.", "Tempo de sessão: 9 s"),
        )
        tela.avancar(1000)
        conferir(
            "11 expira aos 10 s",
            listOf(
                tela.situacao(),
                tela.tempo(),
                tela.temSair(),
                contarAbertos(),
            ),
            listOf("Desconectado.", null, false, 0),
        )

        conferir(
            "12 a situação é a mesma região de status",
            listOf(tela.regiao() == regiao, tela.papelDaRegiao()),
            listOf(true, "status"),
        )

        tela.entrar()
        tela.avancar(1000)
        val relogiosNaSessao = contarAbertos()
        tela.alternar()
        conferir(
            "13 esconder na sessão fecha o relógio",
            listOf(
                relogiosNaSessao,
                tela.painelNaPagina(),
                tela.textoDoAlternar(),
                contarAbertos(),
            ),
            listOf(1, false, "Mostrar login", 0),
        )
        tela.avancar(2000)
        tela.alternar()
        conferir(
            "13 mostrar começa do zero",
            listOf(
                tela.situacao(),
                tela.valor(Campo.NOME),
                tela.valor(Campo.SENHA),
                tela.entrarHabilitado(),
                tela.tempo(),
                tela.temSair(),
                tela.textoDoAlternar(),
            ),
            listOf(
                "Desconectado.",
                "",
                "",
                false,
                null,
                false,
                "Esconder login",
            ),
        )

        tela.digitar(Campo.NOME, "ana")
        tela.digitar(Campo.SENHA, "segredo")
        tela.entrar()
        val requisicoesNaTentativa = contarAbertos()
        // Confere antes de o relógio andar: com 1 s, a requisição esquecida
        // terminaria sozinha.
        tela.alternar()
        conferir(
            "14 esconder na tentativa cancela a requisição",
            listOf(requisicoesNaTentativa, contarAbertos()),
            listOf(1, 0),
        )

        assertTrue(falhas.joinToString("\n"), falhas.isEmpty())
    }
}
