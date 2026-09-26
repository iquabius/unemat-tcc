package tcc.formulario

import java.time.Clock
import java.time.DateTimeException
import java.time.LocalDate

// Regras de domínio do Formulário, iguais nas duas variantes Android: o
// porte do dominio.ts da web, com os mesmos nomes, regras e mensagens.
// Nada aqui depende de interface: cada implementação decide quando chamar.

// Como o type TipoDeVoo = "ida" | "ida-e-volta".
enum class TipoDeVoo { IDA, IDA_E_VOLTA }

// Como a interface Reserva.
data class Reserva(
    val nome: String,
    val email: String,
    val tipo: TipoDeVoo,
    val ida: String,
    val volta: String,
)

// Os espaços do JavaScript (os do \s e do trim()), que não são os mesmos do
// Kotlin: o \s da JVM só conhece os do ASCII, e o trim() do Kotlin apara
// também \u001C a \u001F e não apara o \uFEFF.
private const val ESPACOS =
    "\t\n\u000B\u000C\r \u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006" +
        "\u2007\u2008\u2009\u200A\u2028\u2029\u202F\u205F\u3000\uFEFF"

// Como o trim() do JavaScript.
private fun String.aparar() = trim { it in ESPACOS }

// [0-9] em vez de \d, que em alguns motores de regex aceita outros algarismos.
private val FORMATO_DE_DATA = Regex("""^([0-9]{2})/([0-9]{2})/([0-9]{4})$""")
private val FORMATO_DE_EMAIL = Regex("^[^$ESPACOS@]+@[^$ESPACOS@]+\\.[^$ESPACOS@]+$")

// De onde vem "hoje". Os testes o fixam em 26/09/2026, a data que o script
// de capturas fixa na web.
var relogio: Clock = Clock.systemDefaultZone()

/** Converte "DD/MM/AAAA" numa data, ou `null` se o texto não for uma data real. */
fun parsearData(texto: String): LocalDate? {
    val partes = FORMATO_DE_DATA.matchEntire(texto.aparar()) ?: return null
    val (dia, mes, ano) = partes.destructured
    // Como na web: o Date do JavaScript lê os anos de 0 a 99 como 1900 a
    // 1999, e a conferência da web recusa essas datas.
    if (ano.toInt() < 100) return null
    // O LocalDate recusa datas inexistentes, como 31/02; o Date do
    // JavaScript as "corrige" (31/02 vira 03/03), e a web confere à mão.
    return try {
        LocalDate.of(ano.toInt(), mes.toInt(), dia.toInt())
    } catch (e: DateTimeException) {
        null
    }
}

fun formatarData(data: LocalDate): String =
    "%02d/%02d/%d".format(data.dayOfMonth, data.monthValue, data.year)

fun hoje(): String = formatarData(LocalDate.now(relogio))

fun erroDoNome(nome: String): String? =
    if (nome.aparar().isEmpty()) "Informe o nome do passageiro." else null

fun erroDoEmail(email: String): String? =
    if (FORMATO_DE_EMAIL.matches(email.aparar())) null else "Informe um e-mail válido."

fun erroDaData(texto: String): String? =
    if (parsearData(texto) != null) null else "Use uma data válida no formato DD/MM/AAAA."

/** Erro de ordem entre as datas; `null` se alguma delas for inválida. */
fun erroDaOrdem(ida: String, volta: String): String? {
    val dataDeIda = parsearData(ida) ?: return null
    val dataDeVolta = parsearData(volta) ?: return null
    return if (dataDeVolta < dataDeIda) "A volta não pode ser antes da ida." else null
}

fun mensagemDeConfirmacao(reserva: Reserva): String {
    val (nome, email, tipo, ida, volta) = reserva
    val trecho =
        if (tipo == TipoDeVoo.IDA) {
            "Voo só de ida reservado para ${nome.aparar()} em $ida."
        } else {
            "Voo de ida e volta reservado para ${nome.aparar()}: ida em $ida e volta em $volta."
        }
    return "$trecho A confirmação vai para ${email.aparar()}."
}
