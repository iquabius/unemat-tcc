package tcc.dadosaovivo.views

import android.os.Looper
import android.view.View
import android.widget.Button
import android.widget.TableLayout
import android.widget.TableRow
import android.widget.TextView
import androidx.core.view.children
import androidx.lifecycle.Lifecycle
import androidx.test.core.app.ActivityScenario
import org.robolectric.Shadows.shadowOf
import tcc.dadosaovivo.RelogioFalso

// Ações e leituras usadas pelas cenas e pelo teste, como as funções do
// teste-de-conformidade.js. A Tela do Compose tem os mesmos nomes.
class Tela(
    private val cenario: ActivityScenario<MainActivity>,
    private val relogio: RelogioFalso,
) {
    private fun <T> naTela(bloco: (MainActivity) -> T): T {
        var resultado: Any? = null
        cenario.onActivity { resultado = bloco(it) }
        shadowOf(Looper.getMainLooper()).idle()
        @Suppress("UNCHECKED_CAST")
        return resultado as T
    }

    // O botão que esconde e mostra o painel (.alternar na web).
    fun alternar() = naTela {
        it.findViewById<Button>(R.id.alternar).performClick()
    }

    // O botão de pausa (.pausa na web).
    fun pausa() = naTela { it.findViewById<Button>(R.id.pausa).performClick() }

    fun avancar(ms: Long) = relogio.avancar(ms)

    // A rotação: o Android recria a Activity.
    fun recriar() {
        cenario.recreate()
        shadowOf(Looper.getMainLooper()).idle()
    }

    // A tela fora de vista e de volta, como quando o usuário troca de
    // aplicativo: a Activity para (onStop) e recomeça (onStart).
    fun irParaSegundoPlano() {
        cenario.moveToState(Lifecycle.State.CREATED)
    }

    fun voltarDoSegundoPlano() {
        cenario.moveToState(Lifecycle.State.RESUMED)
    }

    fun textoDoAlternar() = naTela {
        it.findViewById<Button>(R.id.alternar).text.toString()
    }

    // null sem o painel na página.
    fun textoDaPausa(): String? = naTela {
        it.findViewById<Button?>(R.id.pausa)?.text?.toString()
    }

    fun painelNaPagina() = naTela {
        it.findViewById<View?>(R.id.painel) != null
    }

    fun situacao(): String? = naTela {
        it.findViewById<TextView?>(R.id.situacao)?.text?.toString()
    }

    // As linhas dos jogos, com os textos das células separados por " | ",
    // como o linhas() da web.
    fun linhas(): List<String> = naTela { atividade ->
        linhasDosJogos(atividade).map { linha ->
            linha.children.joinToString(" | ") { (it as TextView).text }
        }
    }

    // O código dos jogos das linhas destacadas (tr.alerta na web).
    fun destacadas(): List<String> = naTela { atividade ->
        linhasDosJogos(atividade)
            .filter { it.isActivated }
            .map { (it.getChildAt(0) as TextView).text.toString() }
    }

    // A região de status (a view) e o papel dela, "status" quando o leitor
    // de tela a anuncia.
    fun regiao(): Any? = naTela { it.findViewById<TextView?>(R.id.situacao) }

    fun papelDaRegiao(): String? = naTela {
        val situacao = it.findViewById<TextView>(R.id.situacao)
        if (
            situacao.accessibilityLiveRegion ==
                View.ACCESSIBILITY_LIVE_REGION_POLITE
        )
            "status"
        else null
    }

    // As linhas da tabela, menos a dos títulos.
    private fun linhasDosJogos(atividade: MainActivity): List<TableRow> =
        atividade
            .findViewById<TableLayout?>(R.id.tabela)
            ?.children
            ?.drop(1)
            ?.map { it as TableRow }
            ?.toList() ?: emptyList()
}
