package tcc.logincomquarentena

import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.CoroutineStart
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

// Regras, mensagens, o servidor simulado e o relógio da sessão do Login com
// quarentena, iguais nas tecnologias do Android: o porte do dominio.ts da
// web, com os mesmos nomes, regras e mensagens. Nada aqui depende de
// interface nem do Android, para o desktop compilar o mesmo arquivo pela
// JVM. A espera é a das corrotinas (ADR 0005): o cancelamento da corrotina
// faz o papel do AbortSignal e do clearInterval.

/** Nome e senha mais curtos que isso deixam o "Entrar" desabilitado. */
const val MINIMO_DE_CARACTERES = 2

/** Latência fixa do servidor simulado. */
const val LATENCIA_MS = 1000L

/** Intervalo entre dois tiques do relógio da sessão. */
const val TIQUE_MS = 1000L

/** Duração da sessão, em tiques (segundos). */
const val DURACAO_DA_SESSAO = 10

// Como o objeto MENSAGENS.
object MENSAGENS {
    const val desconectado = "Desconectado."
    const val conectando = "Conectando…"
    const val conectado = "Conectado."
    const val falha = "Nome ou senha incorretos."
}

fun tempoDeSessao(segundos: Int) = "Tempo de sessão: $segundos s"

fun podeEntrar(nome: String, senha: String): Boolean =
    nome.length >= MINIMO_DE_CARACTERES && senha.length >= MINIMO_DE_CARACTERES

// A espera do servidor e do relógio, como o setTimeout e o setInterval da
// web. O teste a troca pela do relógio falso (RelogioFalso), como o teste da
// web troca os temporizadores da página.
var esperar: suspend (ms: Long) -> Unit = { delay(it) }

// Requisições e relógios abertos agora, para a limpeza ao sair da tela.
private var abertos = 0

/**
 * Servidor simulado, com a forma de uma chamada de rede suspensa (como o await
 * de um fetch): devolve true só para ana/segredo, depois de LATENCIA_MS.
 * Cancelar a corrotina que espera, como o abort() do AbortController, cancela a
 * requisição, e a resposta nunca chega.
 */
suspend fun autenticar(nome: String, senha: String): Boolean {
    abertos++
    try {
        esperar(LATENCIA_MS)
    } finally {
        abertos--
    }
    return nome == "ana" && senha == "segredo"
}

/**
 * Relógio da sessão: chama aoTique a cada TIQUE_MS, como um setInterval, numa
 * corrotina do escopo. Devolve o Job que o para (cancel), no papel da função
 * que o iniciarRelogio da web devolve; cancelá-lo de novo não faz nada. A
 * corrotina roda já, até a primeira espera (UNDISPATCHED), e o relógio conta
 * como aberto na volta da chamada, como na web.
 */
fun CoroutineScope.iniciarRelogio(aoTique: () -> Unit): Job =
    launch(start = CoroutineStart.UNDISPATCHED) {
        abertos++
        try {
            while (true) {
                esperar(TIQUE_MS)
                aoTique()
            }
        } finally {
            abertos--
        }
    }

/** Requisições e relógios abertos agora, para o teste de conformidade. */
fun contarAbertos(): Int = abertos
