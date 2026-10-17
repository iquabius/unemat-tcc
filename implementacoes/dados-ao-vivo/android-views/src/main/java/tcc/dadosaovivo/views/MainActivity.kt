package tcc.dadosaovivo.views

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TableLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import java.io.Closeable
import tcc.dadosaovivo.JOGOS
import tcc.dadosaovivo.Lote
import tcc.dadosaovivo.MENSAGENS
import tcc.dadosaovivo.formatarPlacar
import tcc.dadosaovivo.formatarTempo
import tcc.dadosaovivo.golsNovos
import tcc.dadosaovivo.inscreverNosPlacares
import tcc.dadosaovivo.noPalpite

class MainActivity : AppCompatActivity() {
    // O painel na página (null quando escondido) e a linha de cada jogo, pelo
    // código, como o this.painel e o Map de células do Web Component.
    private var painel: View? = null
    private val linhas = mutableMapOf<String, View>()

    // Estado da coordenação, na Activity: a inscrição aberta (nenhuma em
    // pausa, com o painel escondido ou com a tela fora de vista), a pausa e o
    // último lote mostrado, que dá os gols novos.
    private var inscricao: Closeable? = null
    private var pausado = false
    private var ultimo: Lote? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        findViewById<Button>(R.id.alternar).setOnClickListener {
            if (painel != null) {
                esconder()
            } else {
                mostrar()
                inscrever()
            }
        }
        mostrar()
    }

    // A tela ficou à vista: abre a inscrição, se o painel está na página e
    // não está em pausa. Como o connectedCallback do Web Component.
    override fun onStart() {
        super.onStart()
        if (painel != null && !pausado) inscrever()
    }

    // Sem isto, a fonte continua mandando lotes para uma tela fora de vista.
    // Como o disconnectedCallback.
    override fun onStop() {
        super.onStop()
        cancelar()
    }

    private fun inscrever() {
        inscricao = inscreverNosPlacares { receber(it) }
    }

    private fun cancelar() {
        inscricao?.close()
        inscricao = null
    }

    // Põe o painel na página como se a interface abrisse, sem pausa nem
    // valores. Como o createElement e o append do Web Component.
    private fun mostrar() {
        pausado = false
        ultimo = null
        val placares = findViewById<LinearLayout>(R.id.placares)
        val novo = layoutInflater.inflate(R.layout.painel, placares, false)
        val tabela = novo.findViewById<TableLayout>(R.id.tabela)
        linhas.clear()
        for (jogo in JOGOS) {
            val linha = layoutInflater.inflate(R.layout.linha, tabela, false)
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
            // Como o classList.toggle("alerta"): o estilo pinta a linha
            // ativada.
            linha.isActivated = noPalpite(jogo, placar)
        }
        ultimo = lote
        findViewById<TextView>(R.id.situacao).text = ""
    }
}
