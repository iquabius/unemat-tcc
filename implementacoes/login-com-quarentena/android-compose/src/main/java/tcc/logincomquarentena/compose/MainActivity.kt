package tcc.logincomquarentena.compose

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.autofill.ContentType
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.contentType
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.semantics
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import tcc.logincomquarentena.DURACAO_DA_SESSAO
import tcc.logincomquarentena.MENSAGENS
import tcc.logincomquarentena.autenticar
import tcc.logincomquarentena.iniciarRelogio
import tcc.logincomquarentena.podeEntrar
import tcc.logincomquarentena.tempoDeSessao

// As situações do painel e a mensagem de cada uma, como o type Situacao =
// keyof typeof MENSAGENS do React.
enum class Situacao(val mensagem: String) {
    DESCONECTADO(MENSAGENS.desconectado),
    CONECTANDO(MENSAGENS.conectando),
    CONECTADO(MENSAGENS.conectado),
    FALHA(MENSAGENS.falha),
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Como o createRoot(...).render(...) do React; o Tema faz o papel
        // do import do estilo.css.
        setContent { Tema { LoginComQuarentena() } }
    }
}

// Função que descreve o painel a partir do estado, como o componente React.
// A aparência fica em Estilo.kt.
@Composable
fun PainelDeLogin() {
    // Como os useState: alterar um valor faz a função rodar de novo.
    var nome by remember { mutableStateOf("") }
    var senha by remember { mutableStateOf("") }
    var situacao by remember { mutableStateOf(Situacao.DESCONECTADO) }
    var segundos by remember { mutableIntStateOf(0) }
    // Como o useRef do AbortController: a tentativa em andamento, que só o
    // tratador lê; cancelar o Job faz o papel do abort().
    var tentativa by remember { mutableStateOf<Job?>(null) }
    // O escopo das corrotinas do painel: quando o painel sai da tela, o
    // Compose o cancela, e a tentativa em andamento com ele. Faz o papel do
    // useEffect que aborta a tentativa na limpeza.
    val escopo = rememberCoroutineScope()

    // Como o useEffect com [situacao]: o relógio vive enquanto a situação for
    // CONECTADO; qualquer outra situação, inclusive uma tentativa nova, e a
    // saída da tela cancelam o efeito, e com ele o relógio.
    LaunchedEffect(situacao) {
        if (situacao != Situacao.CONECTADO) return@LaunchedEffect
        var decorridos = 0
        iniciarRelogio {
            decorridos += 1
            if (decorridos >= DURACAO_DA_SESSAO) {
                situacao = Situacao.DESCONECTADO
            } else {
                segundos = decorridos
            }
        }
    }

    fun tentar() {
        tentativa?.cancel()
        // Zera aqui, e não no efeito, que roda depois da recomposição: a
        // sessão nova mostraria por um quadro o tempo da anterior.
        segundos = 0
        situacao = Situacao.CONECTANDO
        tentativa = escopo.launch {
            situacao =
                if (autenticar(nome, senha)) Situacao.CONECTADO
                else Situacao.FALHA
        }
    }

    Painel {
        Rotulo("Nome") {
            Entrada(
                nome,
                { nome = it },
                Modifier.semantics { contentType = ContentType.Username },
            )
        }
        Rotulo("Senha") {
            Entrada(
                senha,
                { senha = it },
                Modifier.semantics { contentType = ContentType.Password },
                senha = true,
            )
        }
        Botao(onClick = { tentar() }, habilitado = podeEntrar(nome, senha)) {
            Text("Entrar")
        }
        // Como o role="status": o leitor de tela anuncia a atualização.
        Paragrafo(
            situacao.mensagem,
            Modifier.semantics { liveRegion = LiveRegionMode.Polite },
        )
        if (situacao == Situacao.CONECTADO) {
            Paragrafo(tempoDeSessao(segundos))
            Botao(onClick = { situacao = Situacao.DESCONECTADO }) {
                Text("Sair")
            }
        }
    }
}

// A página: o botão que tira o painel da página e o põe de volta.
@Composable
fun LoginComQuarentena() {
    var visivel by remember { mutableStateOf(true) }
    Login {
        Botao(onClick = { visivel = !visivel }) {
            Text(if (visivel) "Esconder login" else "Mostrar login")
        }
        if (visivel) PainelDeLogin()
    }
}
