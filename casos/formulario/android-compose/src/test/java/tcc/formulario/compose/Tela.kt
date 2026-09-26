package tcc.formulario.compose

import androidx.compose.ui.semantics.SemanticsActions
import androidx.compose.ui.semantics.SemanticsConfiguration
import androidx.compose.ui.semantics.SemanticsProperties
import androidx.compose.ui.semantics.getOrNull
import androidx.compose.ui.test.SemanticsMatcher
import androidx.compose.ui.test.hasAnyAncestor
import androidx.compose.ui.test.hasText
import androidx.compose.ui.test.isPopup
import androidx.compose.ui.test.junit4.AndroidComposeTestRule
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performSemanticsAction
import androidx.compose.ui.test.requestFocus
import androidx.compose.ui.text.AnnotatedString
import tcc.formulario.TipoDeVoo

private val ROTULOS = mapOf(TipoDeVoo.IDA to "Só ida", TipoDeVoo.IDA_E_VOLTA to "Ida e volta")

private val MENSAGENS_DE_ERRO = setOf(
    "Informe o nome do passageiro.",
    "Informe um e-mail válido.",
    "Use uma data válida no formato DD/MM/AAAA.",
    "A volta não pode ser antes da ida.",
)

// Ações e leituras usadas pelas cenas e pelo roteiro, como as funções do
// roteiro-de-teste.js. A Tela do Views tem os mesmos nomes. Os campos são
// achados pela ordem (nome, e-mail, ida, volta), sem marcas só para teste.
class Tela(private val regra: AndroidComposeTestRule<*, *>) {
    private var tipo = TipoDeVoo.IDA

    // Todo campo tem texto editável, mesmo desabilitado (quando perde a ação
    // de editar).
    private fun no(campo: Campo) =
        regra.onAllNodes(SemanticsMatcher.keyIsDefined(SemanticsProperties.EditableText))[campo.ordinal]

    private fun config(campo: Campo) = no(campo).fetchSemanticsNode().config

    fun focar(campo: Campo) {
        no(campo).requestFocus()
        regra.waitForIdle()
    }

    // Como o setter + evento "input" do roteiro: muda o texto sem mudar o foco.
    // (O performTextReplacement foca o campo antes de escrever.)
    fun digitar(campo: Campo, texto: String) {
        no(campo).performSemanticsAction(SemanticsActions.SetText) { it(AnnotatedString(texto)) }
        regra.waitForIdle()
    }

    // Como o fill() do Playwright: foca o campo e escreve.
    fun preencher(campo: Campo, texto: String) {
        focar(campo)
        digitar(campo, texto)
    }

    // Como o blur do roteiro: o foco passa para outro campo.
    fun sair(campo: Campo) {
        focar(campo)
        focar(if (campo == Campo.NOME) Campo.EMAIL else Campo.NOME)
    }

    // Abre a seleção pelo rótulo atual e escolhe a opção no menu.
    fun escolherTipo(novo: TipoDeVoo) {
        if (novo == tipo) return
        regra.onNodeWithText(ROTULOS.getValue(tipo)).performClick()
        regra.onNode(hasText(ROTULOS.getValue(novo)) and hasAnyAncestor(isPopup())).performClick()
        regra.waitForIdle()
        tipo = novo
    }

    fun reservar() {
        regra.onNodeWithText("Reservar").performClick()
        regra.waitForIdle()
    }

    fun botaoHabilitado() =
        SemanticsProperties.Disabled !in regra.onNodeWithText("Reservar").fetchSemanticsNode().config

    fun habilitado(campo: Campo) = SemanticsProperties.Disabled !in config(campo)

    fun valor(campo: Campo) = config(campo)[SemanticsProperties.EditableText].text

    fun invalido(campo: Campo) = SemanticsProperties.Error in config(campo)

    // Mensagens de erro visíveis, de cima para baixo.
    fun erros(): List<String> =
        regra.onAllNodes(SemanticsMatcher("mensagem de erro") { textoDe(it.config) in MENSAGENS_DE_ERRO })
            .fetchSemanticsNodes()
            .map { textoDe(it.config) }

    fun confirmacao(): String =
        regra.onAllNodes(SemanticsMatcher("confirmação") { textoDe(it.config).startsWith("Voo ") })
            .fetchSemanticsNodes()
            .map { textoDe(it.config) }
            .singleOrNull() ?: ""

    private fun textoDe(config: SemanticsConfiguration) =
        config.getOrNull(SemanticsProperties.Text)?.joinToString("") { it.text } ?: ""
}
