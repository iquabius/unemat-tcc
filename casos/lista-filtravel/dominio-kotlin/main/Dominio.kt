package tcc.lista

import java.text.Collator
import java.text.Normalizer
import java.text.NumberFormat
import java.util.Locale

// Catálogo e regras da Lista filtrável, iguais nas duas tecnologias do
// Android: o porte do dominio.ts da web, com os mesmos dados, nomes e regras.
// Nada aqui depende de interface: cada implementação decide quando chamar.

// Como o type Ordem da web, com o rótulo de cada uma (o ordens da web).
enum class Ordem(val rotulo: String) {
    NOME("Nome (A–Z)"),
    MENOR_PRECO("Menor preço"),
    MAIOR_PRECO("Maior preço"),
}

// Como a interface Produto.
data class Produto(val id: Int, val nome: String, val categoria: String, val preco: Double)

val produtos = listOf(
    Produto(1, "Café em grãos 500 g", "Mercearia", 39.9),
    Produto(2, "Açúcar mascavo 1 kg", "Mercearia", 12.5),
    Produto(3, "Chá de camomila", "Mercearia", 8.99),
    Produto(4, "Azeite extravirgem 500 ml", "Mercearia", 45.0),
    Produto(5, "Pão de fermentação natural", "Mercearia", 22.0),
    Produto(6, "Mel silvestre 300 g", "Mercearia", 27.9),
    Produto(7, "Caneca de cerâmica", "Cozinha", 34.9),
    Produto(8, "Cafeteira italiana", "Cozinha", 129.9),
    Produto(9, "Chaleira elétrica", "Cozinha", 159.0),
    Produto(10, "Frigideira antiaderente", "Cozinha", 119.9),
    Produto(11, "Faca do chef", "Cozinha", 89.9),
    Produto(12, "Tábua de corte", "Cozinha", 49.9),
    Produto(13, "Fone de ouvido sem fio", "Eletrônicos", 249.9),
    Produto(14, "Mouse sem fio", "Eletrônicos", 79.9),
    Produto(15, "Teclado mecânico", "Eletrônicos", 399.0),
    Produto(16, "Cabo USB-C 2 m", "Eletrônicos", 29.9),
    Produto(17, "Carregador portátil", "Eletrônicos", 149.9),
    Produto(18, "Caixa de som Bluetooth", "Eletrônicos", 199.9),
    Produto(19, "Caderno pautado", "Papelaria", 24.9),
    Produto(20, "Canetas esferográficas (10 un.)", "Papelaria", 15.9),
    Produto(21, "Agenda 2027", "Papelaria", 54.9),
    Produto(22, "Marca-texto (4 cores)", "Papelaria", 19.9),
    Produto(23, "Bloco de notas adesivas", "Papelaria", 9.9),
    Produto(24, "Estojo escolar", "Papelaria", 32.9),
    Produto(25, "Garrafa térmica 1 L", "Casa", 99.9),
    Produto(26, "Luminária de mesa", "Casa", 139.9),
    Produto(27, "Vela aromática", "Casa", 44.9),
    Produto(28, "Toalha de banho", "Casa", 59.9),
    Produto(29, "Travesseiro de espuma", "Casa", 119.0),
    Produto(30, "Vaso de cerâmica", "Casa", 69.9),
)

// Como o Intl.Collator e o Intl.NumberFormat da web.
private val compararTextos = Collator.getInstance(Locale.forLanguageTag("pt-BR"))
private val formatoDePreco = NumberFormat.getCurrencyInstance(Locale.forLanguageTag("pt-BR"))

/** Categorias do catálogo, sem repetição e em ordem alfabética. */
val categorias: List<String> = produtos.map { it.categoria }.distinct().sortedWith(compararTextos)

private val MARCAS_DE_ACENTO = Regex("\\p{Mn}")

/** Minúsculas e sem acentos, para comparar textos como o usuário espera. */
private fun normalizar(texto: String): String =
    Normalizer.normalize(texto, Normalizer.Form.NFD).replace(MARCAS_DE_ACENTO, "").lowercase().trim()

fun correspondeABusca(produto: Produto, busca: String): Boolean =
    normalizar(produto.nome).contains(normalizar(busca))

/** Categoria vazia significa "Todas". */
fun daCategoria(produto: Produto, categoria: String): Boolean =
    categoria == "" || produto.categoria == categoria

fun comparador(ordem: Ordem): Comparator<Produto> {
    val porNome = compareBy(compararTextos) { produto: Produto -> produto.nome }
    return when (ordem) {
        Ordem.NOME -> porNome
        Ordem.MENOR_PRECO -> compareBy<Produto> { it.preco }.then(porNome)
        Ordem.MAIOR_PRECO -> compareByDescending<Produto> { it.preco }.then(porNome)
    }
}

fun formatarPreco(preco: Double): String = formatoDePreco.format(preco)

fun textoDaContagem(visiveis: Int): String = "$visiveis de ${produtos.size} produtos"
