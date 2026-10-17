package tcc.dadosaovivo.views

import android.graphics.Typeface
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TableLayout
import android.widget.TableRow
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.children
import java.io.Closeable
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

class MainActivity : AppCompatActivity() {
    // O painel na página (null quando escondido) e a linha de cada jogo, pelo
    // código, como o this.painel do Web Component e o Map dele, que guarda as
    // células; aqui, as células se acham na linha pelo id.
    private var painel: View? = null
    private val linhas = mutableMapOf<String, TableRow>()

    // Estado da coordenação, na Activity: a inscrição aberta (nenhuma em
    // pausa, com o painel escondido ou com a tela fora de vista), a pausa, o
    // último lote mostrado, que dá os gols novos, a hora em que ele chegou e
    // o relógio, que vive com o painel, e não com a inscrição (aberto também
    // em pausa).
    private var inscricao: Closeable? = null
    private var pausado = false
    private var ultimo: Lote? = null
    private var chegada: Long? = null
    private var relogio: Closeable? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        findViewById<Button>(R.id.alternar).setOnClickListener {
            if (painel != null) {
                esconder()
            } else {
                mostrar()
                inscrever()
                abrirRelogio()
            }
        }
        mostrar()
    }

    // A tela ficou à vista: abre o relógio, se o painel está na página, e a
    // inscrição, se ele não está em pausa. Como o connectedCallback do Web
    // Component.
    override fun onStart() {
        super.onStart()
        if (painel == null) return
        if (!pausado) inscrever()
        abrirRelogio()
    }

    // Sem isto, a fonte continua mandando lotes, e o relógio continua
    // batendo, para uma tela fora de vista. Como o disconnectedCallback.
    override fun onStop() {
        super.onStop()
        cancelar()
        fecharRelogio()
    }

    private fun inscrever() {
        inscricao = inscreverNosPlacares { receber(it) }
    }

    private fun cancelar() {
        inscricao?.close()
        inscricao = null
    }

    // Como o iniciarRelogio do connectedCallback do Web Component. O texto se
    // recalcula já ao abrir: de volta do segundo plano, ele ainda diria a idade
    // de quando a tela saiu de vista.
    private fun abrirRelogio() {
        relogio = iniciarRelogio { mostrarAtualizacao() }
        mostrarAtualizacao()
    }

    // Como o pararRelogio do disconnectedCallback.
    private fun fecharRelogio() {
        relogio?.close()
        relogio = null
    }

    // Põe o painel na página como se a interface abrisse, sem pausa nem
    // valores. Como o createElement e o append do Web Component.
    private fun mostrar() {
        pausado = false
        ultimo = null
        chegada = null
        val placares = findViewById<LinearLayout>(R.id.placares)
        val novo = layoutInflater.inflate(R.layout.painel, placares, false)
        val tabela = novo.findViewById<TableLayout>(R.id.tabela)
        linhas.clear()
        for (jogo in JOGOS) {
            val linha =
                layoutInflater.inflate(R.layout.linha, tabela, false)
                    as TableRow
            linha.findViewById<TextView>(R.id.codigo).text = jogo.codigo
            linha.findViewById<TextView>(R.id.placar).text =
                formatarPlacar(null)
            linha.findViewById<TextView>(R.id.tempo).text = formatarTempo(null)
            linha.findViewById<TextView>(R.id.gols_novos).text =
                golsNovos(null, null)
            linha.findViewById<TextView>(R.id.palpite).text =
                formatarPlacar(jogo.palpite)
            tabela.addView(linha)
            linhas[jogo.codigo] = linha
        }
        novo.findViewById<Button>(R.id.pausa).setOnClickListener {
            alternarPausa()
        }
        novo.findViewById<TextView>(R.id.situacao).text = MENSAGENS.aguardando
        placares.addView(novo)
        painel = novo
        findViewById<Button>(R.id.alternar).text = "Esconder painel"
    }

    private fun esconder() {
        cancelar()
        fecharRelogio()
        findViewById<LinearLayout>(R.id.placares).removeView(painel)
        painel = null
        findViewById<Button>(R.id.alternar).text = "Mostrar painel"
    }

    private fun alternarPausa() {
        pausado = !pausado
        val pausa = findViewById<Button>(R.id.pausa)
        val situacao = findViewById<TextView>(R.id.situacao)
        if (pausado) {
            cancelar()
            pausa.text = "Retomar"
            situacao.text = MENSAGENS.pausado
        } else {
            inscrever()
            pausa.text = "Pausar"
            situacao.text = if (ultimo != null) "" else MENSAGENS.aguardando
        }
    }

    private fun receber(lote: Lote) {
        for (jogo in JOGOS) {
            val linha = linhas.getValue(jogo.codigo)
            val placar = lote[jogo.codigo]
            linha.findViewById<TextView>(R.id.placar).text =
                formatarPlacar(placar)
            linha.findViewById<TextView>(R.id.tempo).text =
                formatarTempo(placar)
            linha.findViewById<TextView>(R.id.gols_novos).text =
                golsNovos(ultimo?.get(jogo.codigo), placar)
            // Como o classList.toggle("alerta"): o estilo pinta o fundo da
            // linha ativada. O negrito o estilo não troca pelo estado, e se
            // põe em cada célula.
            val alerta = noPalpite(jogo, placar)
            linha.isActivated = alerta
            val peso = if (alerta) Typeface.BOLD else Typeface.NORMAL
            for (celula in linha.children) {
                (celula as TextView).setTypeface(null, peso)
            }
        }
        ultimo = lote
        chegada = agora()
        findViewById<TextView>(R.id.situacao).text = ""
        mostrarAtualizacao()
    }

    // Chamada a cada lote e a cada tique: o mesmo texto muda pelos dois. Como
    // a mostrarAtualizacao() do Web Component.
    private fun mostrarAtualizacao() {
        findViewById<TextView>(R.id.atualizacao).text =
            formatarAtualizacao(chegada, agora())
    }
}
