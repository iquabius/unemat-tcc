package tcc.dadosaovivo.compose

import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.SemanticsActions
import androidx.compose.ui.semantics.SemanticsNode
import androidx.compose.ui.semantics.SemanticsProperties
import androidx.compose.ui.semantics.getOrNull
import androidx.compose.ui.test.SemanticsMatcher
import androidx.compose.ui.test.hasAnyAncestor
import androidx.compose.ui.test.junit4.AndroidComposeTestRule
import androidx.compose.ui.test.performClick
import androidx.compose.ui.text.TextLayoutResult
import androidx.compose.ui.text.font.FontWeight
import tcc.dadosaovivo.JOGOS
import tcc.dadosaovivo.RelogioFalso

private val botao =
    SemanticsMatcher.expectValue(SemanticsProperties.Role, Role.Button)
private val regiaoDeStatus =
    SemanticsMatcher.keyIsDefined(SemanticsProperties.LiveRegion)
private val texto = SemanticsMatcher.keyIsDefined(SemanticsProperties.Text)

// Ações e leituras usadas pelas cenas e pelo teste, como as funções do
// teste-de-conformidade.js. A Tela do Views tem os mesmos nomes. Os elementos
// são achados pela semântica, sem marcas só para teste: os botões pelo papel
// e pela ordem (o que esconde e mostra o painel, e o de pausa), a situação
// pela região anunciada e as células da tabela pelo texto e pela posição.
class Tela(
    private val regra: AndroidComposeTestRule<*, *>,
    private val relogio: RelogioFalso,
) {
    private fun botoes() = regra.onAllNodes(botao)

    private fun textoDe(no: SemanticsNode) =
        no.config.getOrNull(SemanticsProperties.Text)?.joinToString("") {
            it.text
        }

    private fun situacaoNo() =
        regra.onAllNodes(regiaoDeStatus).fetchSemanticsNodes().singleOrNull()

    // O botão que esconde e mostra o painel (.alternar na web).
    fun alternar() {
        botoes()[0].performClick()
        regra.waitForIdle()
    }

    // O botão de pausa (.pausa na web).
    fun pausa() {
        botoes()[1].performClick()
        regra.waitForIdle()
    }

    fun avancar(ms: Long) {
        relogio.avancar(ms)
        regra.waitForIdle()
    }

    fun textoDoAlternar() = textoDe(botoes()[0].fetchSemanticsNode())

    // null sem o painel na página.
    fun textoDaPausa(): String? =
        botoes().fetchSemanticsNodes().getOrNull(1)?.let { textoDe(it) }

    fun painelNaPagina() = situacaoNo() != null

    fun situacao(): String? = situacaoNo()?.let { textoDe(it) }

    // As linhas dos jogos, com os textos das células separados por " | ",
    // como o linhas() da web.
    fun linhas(): List<String> =
        linhasDosJogos().map { linha ->
            linha.joinToString(" | ") { textoDe(it)!! }
        }

    // O código dos jogos das linhas destacadas (tr.alerta na web): as que o
    // estilo põe em negrito.
    fun destacadas(): List<String> =
        linhasDosJogos().filter { negrito(it[0]) }.map { textoDe(it[0])!! }

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

    // As células da tabela, agrupadas pela altura em que estão, da esquerda
    // para a direita; ficam as linhas que começam pelo código de um jogo.
    private fun linhasDosJogos(): List<List<SemanticsNode>> {
        val codigos = JOGOS.map { it.codigo }
        return regra
            .onAllNodes(
                texto and !hasAnyAncestor(botao) and !regiaoDeStatus,
                useUnmergedTree = true,
            )
            .fetchSemanticsNodes()
            .groupBy { it.boundsInRoot.top }
            .toSortedMap()
            .values
            .map { linha -> linha.sortedBy { it.boundsInRoot.left } }
            .filter { textoDe(it[0]) in codigos }
    }

    private fun negrito(no: SemanticsNode): Boolean {
        val layouts = mutableListOf<TextLayoutResult>()
        no.config[SemanticsActions.GetTextLayoutResult].action?.invoke(layouts)
        return layouts.single().layoutInput.style.fontWeight == FontWeight.Bold
    }
}
