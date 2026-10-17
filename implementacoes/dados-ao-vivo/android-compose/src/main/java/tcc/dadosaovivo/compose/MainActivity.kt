package tcc.dadosaovivo.compose

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.semantics
import tcc.dadosaovivo.JOGOS
import tcc.dadosaovivo.Lote
import tcc.dadosaovivo.MENSAGENS
import tcc.dadosaovivo.agora
import tcc.dadosaovivo.formatarAtualizacao
import tcc.dadosaovivo.formatarPlacar
import tcc.dadosaovivo.formatarTempo
import tcc.dadosaovivo.golsNovos
import tcc.dadosaovivo.iniciarRelogio
import tcc.dadosaovivo.inscreverNosPlacares
import tcc.dadosaovivo.noPalpite

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Como o createRoot(...).render(...) do React; o Tema faz o papel
        // do import do estilo.css.
        setContent { Tema { DadosAoVivo() } }
    }
}

// Função que descreve o painel a partir do estado, como o componente React.
// A aparência fica em Estilo.kt.
@Composable
fun PainelDePlacares() {
    // Como os useState: alterar um valor faz a função rodar de novo.
    var pausado by remember { mutableStateOf(false) }
    // Os dois últimos lotes: o atual dá o placar, o anterior, os gols novos.
    var anterior by remember { mutableStateOf<Lote?>(null) }
    var atual by remember { mutableStateOf<Lote?>(null) }
    // A hora em que chegou o último lote e a do último tique do relógio.
    var chegada by remember { mutableStateOf<Long?>(null) }
    var ultimoTique by remember { mutableStateOf(agora()) }

    // Como o useEffect com [pausado]: roda de novo quando pausado se altera,
    // e o onDispose cancela a inscrição antes disso e quando o painel sai da
    // tela.
    DisposableEffect(pausado) {
        if (pausado) return@DisposableEffect onDispose {}
        val inscricao = inscreverNosPlacares { lote ->
            anterior = atual
            atual = lote
            chegada = agora()
        }
        onDispose { inscricao.close() }
    }

    // O relógio vive com o painel, e não com a inscrição: como o useEffect
    // com [], o onDispose o para só quando o painel sai da tela.
    DisposableEffect(Unit) {
        val relogio = iniciarRelogio { ultimoTique = agora() }
        onDispose { relogio.close() }
    }

    val situacao =
        if (pausado) MENSAGENS.pausado
        else if (atual != null) "" else MENSAGENS.aguardando

    Painel {
        // Como o role="status": o leitor de tela anuncia a atualização.
        Situacao(
            situacao,
            Modifier.semantics { liveRegion = LiveRegionMode.Polite },
        )
        Atualizacao(formatarAtualizacao(chegada, ultimoTique))
        Tabela {
            Cabecalho {
                Celula("Jogo")
                Celula("Placar")
                Celula("Tempo")
                Celula("Gols novos")
                Celula("Palpite")
            }
            for (jogo in JOGOS) {
                val placar = atual?.get(jogo.codigo)
                Linha(alerta = noPalpite(jogo, placar)) {
                    Celula(jogo.codigo)
                    Celula(formatarPlacar(placar))
                    Celula(formatarTempo(placar))
                    Celula(golsNovos(anterior?.get(jogo.codigo), placar))
                    Celula(formatarPlacar(jogo.palpite))
                }
            }
        }
        Botao(onClick = { pausado = !pausado }) {
            Text(if (pausado) "Retomar" else "Pausar")
        }
    }
}

// A página: o botão que tira o painel da página e o põe de volta.
@Composable
fun DadosAoVivo() {
    var visivel by remember { mutableStateOf(true) }
    Placares {
        Botao(onClick = { visivel = !visivel }) {
            Text(if (visivel) "Esconder painel" else "Mostrar painel")
        }
        if (visivel) PainelDePlacares()
    }
}
