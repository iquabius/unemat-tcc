package tcc.lista.compose

import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.SemanticsActions
import androidx.compose.ui.semantics.SemanticsConfiguration
import androidx.compose.ui.semantics.SemanticsProperties
import androidx.compose.ui.semantics.getOrNull
import androidx.compose.ui.test.SemanticsMatcher
import androidx.compose.ui.test.hasAnyAncestor
import androidx.compose.ui.test.hasClickAction
import androidx.compose.ui.test.hasSetTextAction
import androidx.compose.ui.test.hasText
import androidx.compose.ui.test.isPopup
import androidx.compose.ui.test.junit4.AndroidComposeTestRule
import androidx.compose.ui.test.onChildren
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performSemanticsAction
import androidx.compose.ui.test.requestFocus
import androidx.compose.ui.text.AnnotatedString
import tcc.lista.Ordem

private val SELECAO = SemanticsMatcher.expectValue(SemanticsProperties.Role, Role.DropdownList)
private val LISTA = SemanticsMatcher.keyIsDefined(SemanticsProperties.CollectionInfo)
private val CONTAGEM = Regex("""\d+ de \d+ produtos""")

// Ações e leituras usadas pelas cenas e pelo roteiro, como as funções do
// roteiro-de-teste.js. A Tela do Views tem os mesmos nomes. Os controles são
// achados pela semântica (papel, texto), sem marcas só para teste.
class Tela(private val regra: AndroidComposeTestRule<*, *>) {
    private var categoria = "Todas"
    private var ordem = Ordem.NOME.rotulo

    private fun textos(config: SemanticsConfiguration) =
        config.getOrNull(SemanticsProperties.Text)?.map { it.text } ?: emptyList()

    // Como o setter + evento "input" do roteiro: muda o texto sem mudar o foco.
    fun buscar(texto: String) {
        regra.onNode(hasSetTextAction()).performSemanticsAction(SemanticsActions.SetText) { it(AnnotatedString(texto)) }
        regra.waitForIdle()
    }

    // Abre a seleção pelo rótulo atual e escolhe a opção no menu.
    private fun escolher(atual: String, novo: String) {
        if (novo == atual) return
        regra.onNode(SELECAO and hasText(atual)).performClick()
        regra.onNode(hasText(novo) and hasAnyAncestor(isPopup())).performClick()
        regra.waitForIdle()
    }

    fun escolherCategoria(novo: String) {
        val rotulo = novo.ifEmpty { "Todas" }
        escolher(categoria, rotulo)
        categoria = rotulo
    }

    fun escolherOrdem(novo: Ordem) {
        escolher(ordem, novo.rotulo)
        ordem = novo.rotulo
    }

    // Abre o menu de categorias, lê as opções e o fecha escolhendo a atual.
    fun opcoesDeCategoria(): List<String> {
        regra.onNode(SELECAO and hasText(categoria)).performClick()
        val menu = hasAnyAncestor(isPopup()) and hasClickAction()
        val opcoes = regra.onAllNodes(menu).fetchSemanticsNodes().flatMap { textos(it.config) }
        regra.onNode(menu and hasText(categoria)).performClick()
        regra.waitForIdle()
        return opcoes
    }

    // Os textos de cada item da lista, na ordem da tela: nome, categoria, preço.
    private fun itens() = regra.onNode(LISTA).onChildren().fetchSemanticsNodes().map { textos(it.config) }

    fun nomes() = itens().map { it[0] }

    // Como o texto() do roteiro, que troca o espaço não separável do preço.
    fun primeiroPreco() = itens().first()[2].replace(' ', ' ')

    fun contagem() = regra.onAllNodes(SemanticsMatcher("contagem") { textos(it.config).any(CONTAGEM::matches) })
        .fetchSemanticsNodes().single().let { textos(it.config).single() }

    fun vazio() = regra.onAllNodes(hasText("Nenhum produto encontrado.")).fetchSemanticsNodes().isNotEmpty()
}
