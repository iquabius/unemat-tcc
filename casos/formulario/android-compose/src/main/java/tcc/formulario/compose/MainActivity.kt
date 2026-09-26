package tcc.formulario.compose

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.autofill.ContentType
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.contentType
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.input.KeyboardType
import tcc.formulario.Reserva
import tcc.formulario.TipoDeVoo
import tcc.formulario.erroDaData
import tcc.formulario.erroDaOrdem
import tcc.formulario.erroDoEmail
import tcc.formulario.erroDoNome
import tcc.formulario.hoje
import tcc.formulario.mensagemDeConfirmacao

// Os campos que podem ser tocados, como o type Campo do React.
enum class Campo { NOME, EMAIL, IDA, VOLTA }

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Como o createRoot(...).render(...) do React; o Tema faz o papel
        // do import do estilo.css.
        setContent { Tema { FormularioDeReserva() } }
    }
}

// Função que descreve a tela a partir do estado, como o componente React.
// A aparência fica em Estilo.kt.
@Composable
fun FormularioDeReserva() {
    // Como os useState: mudar um valor faz a função rodar de novo.
    var nome by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var tipo by remember { mutableStateOf(TipoDeVoo.IDA) }
    var ida by remember { mutableStateOf(hoje()) }
    var volta by remember { mutableStateOf(hoje()) }
    var tocados by remember { mutableStateOf(setOf<Campo>()) }
    var confirmacao by remember { mutableStateOf("") }

    // Os erros são derivados do estado a cada recomposição.
    val idaEVolta = tipo == TipoDeVoo.IDA_E_VOLTA
    val erroNome = erroDoNome(nome)
    val erroEmail = erroDoEmail(email)
    val erroIda = erroDaData(ida)
    val erroVolta = if (idaEVolta) erroDaData(volta) else null
    val erroOrdem = if (idaEVolta) erroDaOrdem(ida, volta) else null
    val temErro = listOf(erroNome, erroEmail, erroIda, erroVolta, erroOrdem).any { it != null }

    fun tocado(campo: Campo) = campo in tocados
    fun tocar(campo: Campo) {
        tocados = tocados + campo
    }

    val erroVisivel = mapOf(
        Campo.NOME to if (tocado(Campo.NOME)) erroNome else null,
        Campo.EMAIL to if (tocado(Campo.EMAIL)) erroEmail else null,
        Campo.IDA to if (tocado(Campo.IDA)) erroIda else null,
        Campo.VOLTA to ((if (tocado(Campo.VOLTA)) erroVolta else null)
            ?: (if (tocado(Campo.IDA) || tocado(Campo.VOLTA)) erroOrdem else null)),
    )

    // O Compose não tem onBlur. O onFocusChanged avisa toda mudança de foco,
    // inclusive o estado inicial, sem foco; por isso só conta como saída
    // quando o campo já teve foco.
    val focados = remember { mutableSetOf<Campo>() }
    fun Modifier.aoSair(campo: Campo) = onFocusChanged {
        if (it.isFocused) focados += campo else if (campo in focados) tocar(campo)
    }

    Formulario {
        Rotulo("Nome do passageiro") {
            Entrada(
                nome,
                { nome = it },
                Modifier.aoSair(Campo.NOME).semantics { contentType = ContentType.PersonFullName },
                invalida = erroVisivel[Campo.NOME] != null,
            )
        }
        erroVisivel[Campo.NOME]?.let { Erro(it) }

        Rotulo("E-mail") {
            Entrada(
                email,
                { email = it },
                Modifier.aoSair(Campo.EMAIL).semantics { contentType = ContentType.EmailAddress },
                invalida = erroVisivel[Campo.EMAIL] != null,
                teclado = KeyboardType.Email,
            )
        }
        erroVisivel[Campo.EMAIL]?.let { Erro(it) }

        Rotulo("Tipo de voo") {
            Selecao(
                opcoes = listOf(TipoDeVoo.IDA to "Só ida", TipoDeVoo.IDA_E_VOLTA to "Ida e volta"),
                escolhida = tipo,
                aoEscolher = { tipo = it },
            )
        }

        Rotulo("Data de ida") {
            Entrada(
                ida,
                { ida = it },
                Modifier.aoSair(Campo.IDA),
                invalida = erroVisivel[Campo.IDA] != null,
                dica = "DD/MM/AAAA",
            )
        }
        erroVisivel[Campo.IDA]?.let { Erro(it) }

        Rotulo("Data de volta") {
            Entrada(
                volta,
                { volta = it },
                Modifier.aoSair(Campo.VOLTA),
                invalida = erroVisivel[Campo.VOLTA] != null,
                habilitada = idaEVolta,
                dica = "DD/MM/AAAA",
            )
        }
        erroVisivel[Campo.VOLTA]?.let { Erro(it) }

        Botao(
            onClick = { confirmacao = mensagemDeConfirmacao(Reserva(nome, email, tipo, ida, volta)) },
            habilitado = !temErro,
        ) {
            Text("Reservar")
        }
    }
    // Como o role="status": o leitor de tela anuncia a mudança.
    Confirmacao(confirmacao, Modifier.semantics { liveRegion = LiveRegionMode.Polite })
}
