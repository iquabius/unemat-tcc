package tcc.logincomquarentena.compose

import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.SemanticsActions
import androidx.compose.ui.semantics.SemanticsNode
import androidx.compose.ui.semantics.SemanticsProperties
import androidx.compose.ui.semantics.getOrNull
import androidx.compose.ui.test.SemanticsMatcher
import androidx.compose.ui.test.hasText
import androidx.compose.ui.test.junit4.AndroidComposeTestRule
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performSemanticsAction
import androidx.compose.ui.text.AnnotatedString
import tcc.logincomquarentena.RelogioFalso
import tcc.logincomquarentena.tempoDeSessao

// Os campos, pela ordem na tela.
enum class Campo {
    NOME,
    SENHA,
}

private val botao =
    SemanticsMatcher.expectValue(SemanticsProperties.Role, Role.Button)
private val regiaoDeStatus =
    SemanticsMatcher.keyIsDefined(SemanticsProperties.LiveRegion)
private val inicioDoTempo = tempoDeSessao(0).substringBefore("0")
private val editavel =
    SemanticsMatcher.keyIsDefined(SemanticsProperties.EditableText)

// Ações e leituras usadas pelas cenas e pelo teste, como as funções do
// teste-de-conformidade.js. A Tela do Views tem os mesmos nomes. Os elementos
// são achados pela semântica, sem marcas só para teste: os campos pela ordem,
// os botões pelo papel e pelo texto, a situação pela região anunciada e o
// tempo de sessão pelo texto.
class Tela(
    private val regra: AndroidComposeTestRule<*, *>,
    private val relogio: RelogioFalso,
) {
    private fun textoDe(no: SemanticsNode) =
        no.config.getOrNull(SemanticsProperties.Text)?.joinToString("") {
            it.text
        }

    private fun botao(texto: String): SemanticsNode? =
        regra.onAllNodes(botao).fetchSemanticsNodes().singleOrNull {
            textoDe(it) == texto
        }

    private fun clicar(texto: String) {
        regra.onNode(botao and hasText(texto)).performClick()
        regra.waitForIdle()
    }

    private fun situacaoNo() =
        regra.onAllNodes(regiaoDeStatus).fetchSemanticsNodes().singleOrNull()

    // Como o setter + evento "input" da web: altera o texto sem mover o foco.
    // (O performTextReplacement foca o campo antes de escrever.)
    fun digitar(campo: Campo, texto: String) {
        regra.onAllNodes(editavel)[campo.ordinal].performSemanticsAction(
            SemanticsActions.SetText
        ) {
            it(AnnotatedString(texto))
        }
        regra.waitForIdle()
    }

    // Os botões: .entrar, .sair e .alternar na web. O alternar é o primeiro,
    // com o texto que muda.
    fun entrar() = clicar("Entrar")

    fun sair() = clicar("Sair")

    fun alternar() {
        regra.onAllNodes(botao)[0].performClick()
        regra.waitForIdle()
    }

    fun avancar(ms: Long) = relogio.avancar(ms) { regra.waitForIdle() }

    fun situacao(): String? = situacaoNo()?.let { textoDe(it) }

    // null sem o tempo de sessão na tela, como o texto() da web. Achado pelo
    // começo do texto do domínio, o que vem antes dos segundos.
    fun tempo(): String? =
        regra
            .onAllNodes(
                SemanticsMatcher("tempo de sessão") {
                    textoDe(it)?.startsWith(inicioDoTempo) == true
                }
            )
            .fetchSemanticsNodes()
            .singleOrNull()
            ?.let { textoDe(it) }

    fun temSair(): Boolean = botao("Sair") != null

    fun entrarHabilitado(): Boolean =
        SemanticsProperties.Disabled !in botao("Entrar")!!.config

    fun valor(campo: Campo): String =
        regra
            .onAllNodes(editavel)[campo.ordinal]
            .fetchSemanticsNode()
            .config[SemanticsProperties.EditableText]
            .text

    fun textoDoAlternar(): String =
        textoDe(regra.onAllNodes(botao)[0].fetchSemanticsNode())!!

    fun painelNaPagina(): Boolean = situacaoNo() != null

    // A região de status (o id do nó semântico) e o papel dela, "status"
    // quando o leitor de tela a anuncia.
    fun regiao(): Any? = situacaoNo()?.id

    fun papelDaRegiao(): String? =
        situacaoNo()?.let {
            if (
                it.config.getOrNull(SemanticsProperties.LiveRegion) ==
                    LiveRegionMode.Polite
            )
                "status"
            else null
        }
}
