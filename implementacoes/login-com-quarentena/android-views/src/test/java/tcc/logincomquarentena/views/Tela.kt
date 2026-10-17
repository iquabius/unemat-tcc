package tcc.logincomquarentena.views

import android.os.Looper
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.core.view.isVisible
import androidx.test.core.app.ActivityScenario
import org.robolectric.Shadows.shadowOf
import tcc.logincomquarentena.RelogioFalso

enum class Campo(val id: Int) {
    NOME(R.id.nome),
    SENHA(R.id.senha),
}

// Ações e leituras usadas pelas cenas e pelo teste, como as funções do
// teste-de-conformidade.js. A Tela do Compose tem os mesmos nomes.
class Tela(
    private val cenario: ActivityScenario<MainActivity>,
    private val relogio: RelogioFalso,
) {
    private fun <T> naTela(bloco: (MainActivity) -> T): T {
        var resultado: Any? = null
        cenario.onActivity { resultado = bloco(it) }
        escoar()
        @Suppress("UNCHECKED_CAST")
        return resultado as T
    }

    // Roda o que a thread principal tem para agora, sem andar o tempo.
    private fun escoar() = shadowOf(Looper.getMainLooper()).idle()

    // Como o setter + evento "input" da web: altera o texto sem mover o foco.
    fun digitar(campo: Campo, texto: String) = naTela {
        it.findViewById<EditText>(campo.id).setText(texto)
    }

    // Os botões: .entrar, .sair e .alternar na web.
    fun entrar() = naTela {
        it.findViewById<Button>(R.id.entrar).performClick()
    }

    fun sair() = naTela { it.findViewById<Button>(R.id.sair).performClick() }

    fun alternar() = naTela {
        it.findViewById<Button>(R.id.alternar).performClick()
    }

    fun avancar(ms: Long) = relogio.avancar(ms) { escoar() }

    // Texto visível, ou null sem o elemento na tela, como o texto() da web.
    private fun visivel(atividade: MainActivity, id: Int): String? =
        atividade
            .findViewById<TextView?>(id)
            ?.takeIf { it.isVisible }
            ?.text
            ?.toString()

    fun situacao(): String? = naTela { visivel(it, R.id.situacao) }

    fun tempo(): String? = naTela { visivel(it, R.id.relogio) }

    fun temSair(): Boolean = naTela { visivel(it, R.id.sair) != null }

    fun entrarHabilitado(): Boolean = naTela {
        it.findViewById<Button>(R.id.entrar).isEnabled
    }

    fun valor(campo: Campo): String = naTela {
        it.findViewById<EditText>(campo.id).text.toString()
    }

    fun textoDoAlternar(): String = naTela {
        it.findViewById<Button>(R.id.alternar).text.toString()
    }

    fun painelNaPagina(): Boolean = naTela {
        it.findViewById<View?>(R.id.painel) != null
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
}
