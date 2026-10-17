package tcc.dadosaovivo

import android.os.Handler
import android.os.Looper
import java.io.Closeable

// Jogos, mensagens e a fonte simulada de placares dos Dados ao vivo, iguais
// nas duas tecnologias do Android: o porte do dominio.ts da web, com os
// mesmos nomes, regras e mensagens. Nada aqui depende de interface.

// Como a interface Gols: os gols de cada lado, do placar de um jogo ou do
// palpite do usuário.
interface Gols {
    val mandante: Int
    val visitante: Int
}

// O palpite do usuário: só os gols.
data class Palpite(override val mandante: Int, override val visitante: Int) :
    Gols

/**
 * O que a fonte manda de cada jogo: a partida (o ciclo do relógio em que ela se
 * joga), o minuto e os gols.
 */
data class Placar(
    val partida: Int,
    val minuto: Int,
    override val mandante: Int,
    override val visitante: Int,
) : Gols

/** Minutos em que cada lado marca, do roteiro simulado da partida. */
data class Roteiro(val mandante: List<Int>, val visitante: List<Int>)

data class Jogo(val codigo: String, val roteiro: Roteiro, val palpite: Palpite)

/** Placar de cada jogo num lote, pelo código. */
typealias Lote = Map<String, Placar>

/** Intervalo entre dois lotes da fonte. */
const val INTERVALO_MS = 1000L

val JOGOS =
    listOf(
        Jogo("FLA × PAL", Roteiro(listOf(2, 55), listOf(9, 80)), Palpite(1, 0)),
        Jogo("COR × SAO", Roteiro(listOf(15), listOf(32)), Palpite(2, 0)),
        Jogo("GRE × INT", Roteiro(listOf(30), listOf(42)), Palpite(1, 0)),
        Jogo("CAM × CRU", Roteiro(listOf(20, 47), listOf(66)), Palpite(2, 1)),
    )

// Como o objeto MENSAGENS.
object MENSAGENS {
    const val aguardando = "Aguardando placares…"
    const val pausado = "Pausado."
}

// O relógio da partida anda 1 minuto por segundo, num ciclo de 100 s: do
// minuto 0 ao 90, e 9 s de "Fim" antes de a partida recomeçar. O placar
// depende só do segundo em que o lote sai, como num servidor real. Cada jogo
// começou 20 minutos depois do anterior.
private const val CICLO_S = 100
private const val DURACAO_MIN = 90
private const val DEFASAGEM_MIN = 20

fun placaresEm(instante: Long): Lote {
    val segundo = Math.floorDiv(instante, 1000L)
    return JOGOS.withIndex().associate { (i, jogo) ->
        val relogio = segundo + DEFASAGEM_MIN * i
        val minuto = Math.floorMod(relogio, CICLO_S)
        fun ate(gols: List<Int>) = gols.count { it <= minuto }
        jogo.codigo to
            Placar(
                partida = Math.floorDiv(relogio, CICLO_S).toInt(),
                minuto = minuto,
                mandante = ate(jogo.roteiro.mandante),
                visitante = ate(jogo.roteiro.visitante),
            )
    }
}

/** A hora e o intervalo da fonte, como o Date.now e o setInterval da web. */
interface Relogio {
    fun agora(): Long

    /** Roda acao a cada ms, na thread principal, até fechar o Closeable. */
    fun aCada(ms: Long, acao: () -> Unit): Closeable
}

object RelogioDoSistema : Relogio {
    override fun agora() = System.currentTimeMillis()

    override fun aCada(ms: Long, acao: () -> Unit): Closeable {
        val principal = Handler(Looper.getMainLooper())
        val repeticao =
            object : Runnable {
                override fun run() {
                    principal.postDelayed(this, ms)
                    acao()
                }
            }
        principal.postDelayed(repeticao, ms)
        return Closeable { principal.removeCallbacks(repeticao) }
    }
}

// O relógio da fonte. O teste o troca pelo relógio falso (RelogioFalso), como
// o teste da web troca o Date.now e o setInterval da página.
var relogioDaFonte: Relogio = RelogioDoSistema

// Inscrições abertas agora, para a limpeza ao sair da tela.
private var inscricoes = 0

/**
 * Inscreve aoReceber na fonte, como quem abre um WebSocket ou um EventSource: a
 * cada INTERVALO_MS a fonte manda um lote para aoReceber, na thread principal.
 * Devolve o Closeable que cancela a inscrição; fechá-lo de novo não faz nada.
 */
fun inscreverNosPlacares(aoReceber: (Lote) -> Unit): Closeable {
    inscricoes++
    val envio =
        relogioDaFonte.aCada(INTERVALO_MS) {
            aoReceber(placaresEm(relogioDaFonte.agora()))
        }
    var ativa = true
    return Closeable {
        if (ativa) {
            ativa = false
            inscricoes--
            envio.close()
        }
    }
}

/** Inscrições abertas agora, para o teste de conformidade. */
fun contarInscricoes(): Int = inscricoes

/** "2 × 1", ou "—" antes do primeiro lote. */
fun formatarPlacar(gols: Gols?): String =
    if (gols == null) "—" else "${gols.mandante} × ${gols.visitante}"

/** "41'", "Fim" depois dos 90 minutos, ou "—" antes do primeiro lote. */
fun formatarTempo(placar: Placar?): String =
    when {
        placar == null -> "—"
        placar.minuto > DURACAO_MIN -> "Fim"
        else -> "${placar.minuto}'"
    }

/**
 * Gols desde o lote anterior: "+1 × 0", "0 × +1" ou "="; "—" sem os dois lotes
 * ou quando eles são de partidas diferentes.
 */
fun golsNovos(anterior: Placar?, atual: Placar?): String {
    if (anterior == null || atual == null) return "—"
    if (atual.partida != anterior.partida) return "—"
    val m = atual.mandante - anterior.mandante
    val v = atual.visitante - anterior.visitante
    if (m == 0 && v == 0) return "="
    fun lado(n: Int) = if (n > 0) "+$n" else "0"
    return "${lado(m)} × ${lado(v)}"
}

/** O placar bate com o palpite do jogo. */
fun noPalpite(jogo: Jogo, placar: Placar?): Boolean =
    placar != null &&
        placar.mandante == jogo.palpite.mandante &&
        placar.visitante == jogo.palpite.visitante
