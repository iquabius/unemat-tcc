package tcc.formulario.views

import android.os.Looper
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import android.widget.TextView
import androidx.core.view.isVisible
import androidx.test.core.app.ActivityScenario
import org.robolectric.Shadows.shadowOf
import tcc.formulario.TipoDeVoo
import java.time.Duration

enum class Campo(val id: Int) {
    NOME(R.id.nome),
    EMAIL(R.id.email),
    IDA(R.id.ida),
    VOLTA(R.id.volta),
}

// Ações e leituras usadas pelas cenas e pelo roteiro, como as funções do
// roteiro-de-teste.js. A Tela do Compose tem os mesmos nomes.
class Tela(private val cenario: ActivityScenario<MainActivity>) {
    private fun <T> naTela(bloco: (MainActivity) -> T): T {
        var resultado: Any? = null
        cenario.onActivity { resultado = bloco(it) }
        shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(100))
        @Suppress("UNCHECKED_CAST")
        return resultado as T
    }

    private fun campo(atividade: MainActivity, campo: Campo): EditText = atividade.findViewById(campo.id)

    fun focar(campo: Campo) = naTela { campo(it, campo).requestFocus() }

    // Como o setter + evento "input" do roteiro: muda o texto sem mudar o foco.
    // O cursor vai para o fim, como depois de digitar (o setText o põe no início).
    fun digitar(campo: Campo, texto: String) = naTela {
        campo(it, campo).setText(texto)
        campo(it, campo).setSelection(texto.length)
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

    fun escolherTipo(tipo: TipoDeVoo) = naTela { it.findViewById<Spinner>(R.id.tipo).setSelection(tipo.ordinal) }

    fun reservar() = naTela { it.findViewById<Button>(R.id.reservar).performClick() }

    fun botaoHabilitado() = naTela { it.findViewById<Button>(R.id.reservar).isEnabled }

    fun habilitado(campo: Campo) = naTela { campo(it, campo).isEnabled }

    fun valor(campo: Campo) = naTela { campo(it, campo).text.toString() }

    fun invalido(campo: Campo) = naTela { campo(it, campo).isActivated }

    // Mensagens de erro visíveis, de cima para baixo.
    fun erros(): List<String> = naTela { atividade ->
        listOf(R.id.erro_nome, R.id.erro_email, R.id.erro_ida, R.id.erro_volta)
            .map { atividade.findViewById<TextView>(it) }
            .filter(View::isVisible)
            .map { it.text.toString() }
    }

    fun confirmacao() = naTela { it.findViewById<TextView>(R.id.confirmacao).text.toString() }
}
