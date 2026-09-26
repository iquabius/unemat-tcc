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

// [0-9] em vez de \d, que em alguns motores de regex aceita outros algarismos.
private val FORMATO_DE_DATA = Regex("""^([0-9]{2})/([0-9]{2})/([0-9]{4})$""")
private val FORMATO_DE_EMAIL = Regex("""^[^\s@]+@[^\s@]+\.[^\s@]+$""")

// De onde vem "hoje". Os testes o fixam em 26/09/2026, a data que o script
// de capturas fixa na web.
var relogio: Clock = Clock.systemDefaultZone()

/** Converte "DD/MM/AAAA" numa data, ou `null` se o texto não for uma data real. */
fun parsearData(texto: String): LocalDate? {
    val partes = FORMATO_DE_DATA.matchEntire(texto.trim()) ?: return null
    val (dia, mes, ano) = partes.destructured
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
    if (nome.trim().isEmpty()) "Informe o nome do passageiro." else null

fun erroDoEmail(email: String): String? =
    if (FORMATO_DE_EMAIL.matches(email.trim())) null else "Informe um e-mail válido."

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
            "Voo só de ida reservado para ${nome.trim()} em $ida."
        } else {
            "Voo de ida e volta reservado para ${nome.trim()}: ida em $ida e volta em $volta."
        }
    return "$trecho A confirmação vai para ${email.trim()}."
}
