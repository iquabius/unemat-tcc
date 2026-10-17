package tcc.logincomquarentena.views

import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.annotation.Config
import tcc.captura.SemAnimacoes
import tcc.captura.capturar
import tcc.logincomquarentena.RelogioFalso

// Mesmas cenas de implementacoes/login-com-quarentena/cenas.mts, com a largura
// da captura da web e a altura da cena mais alta, a da sessão. As esperas,
// no relógio falso, são as da web: folga sobre a latência de 1 s, e a sessão
// no primeiro segundo.
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w480dp-h360dp-xhdpi")
class CenasTest {
    @get:Rule(order = 0) val relogio = RelogioFalso()

    @get:Rule(order = 1) val semAnimacoes = SemAnimacoes()

    @get:Rule(order = 2)
    val regra = ActivityScenarioRule(MainActivity::class.java)

    private val tela by lazy { Tela(regra.scenario, relogio) }

    private fun entrar(senha: String) {
        tela.digitar(Campo.NOME, "ana")
        tela.digitar(Campo.SENHA, senha)
        tela.entrar()
    }

    @Test fun inicial() = capturar("inicial")

    @Test
    fun conectando() {
        entrar("segredo")
        tela.avancar(300)
        capturar("conectando")
    }

    @Test
    fun falha() {
        entrar("errada")
        tela.avancar(1300)
        capturar("falha")
    }

    @Test
    fun conectado() {
        entrar("segredo")
        tela.avancar(1300)
        capturar("conectado")
    }

    @Test
    fun escondido() {
        tela.alternar()
        capturar("escondido")
    }
}
