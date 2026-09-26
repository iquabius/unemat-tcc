package tcc.lista.compose

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyListScope
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.LocalTextStyle
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// Aparência da Lista filtrável, no papel do estilo.css da web: a tela só usa
// os nomes daqui (Tema, Catalogo, Filtros, Rotulo, Entrada, Contagem,
// Produtos, Produto), como o className.

private val texto = Color(0xFFEEEEEE)

// body: o tema da tela inteira.
@Composable
fun Tema(conteudo: @Composable () -> Unit) {
    MaterialTheme(colorScheme = darkColorScheme()) {
        Surface(Modifier.fillMaxSize().safeDrawingPadding(), color = Color(0xFF2B2B2B), contentColor = texto) {
            // Substitui o texto do Material (com espaçamento entre letras e
            // entrelinha próprios) pelo texto comum, como o do body.
            CompositionLocalProvider(LocalTextStyle provides TextStyle(fontSize = 16.sp), content = conteudo)
        }
    }
}

// .catalogo: uma coluna com 0.75rem entre os itens e 1rem de margem. Os
// filtros ficam parados e só a lista rola (na web, rola a página).
@Composable
fun Catalogo(conteudo: @Composable ColumnScope.() -> Unit) {
    Column(Modifier.padding(16.dp), Arrangement.spacedBy(12.dp), content = conteudo)
}

// .filtros: 0.5rem entre os controles.
@Composable
fun Filtros(conteudo: @Composable ColumnScope.() -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp), content = conteudo)
}

// .filtros label: o texto e o controle, com 0.25rem entre eles.
@Composable
fun Rotulo(texto: String, controle: @Composable () -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(texto)
        controle()
    }
}

// Fundo e borda de .filtros input e select.
internal fun Modifier.caixa() = this
    .border(1.dp, Color(0xFF555555))
    .background(Color(0xFF3A3A3A))
    .padding(6.4.dp)

// .filtros input
@Composable
fun Entrada(valor: String, aoMudar: (String) -> Unit, dica: String = "") {
    BasicTextField(
        value = valor,
        onValueChange = aoMudar,
        modifier = Modifier.fillMaxWidth().caixa(),
        singleLine = true,
        textStyle = TextStyle(color = texto, fontSize = 16.sp),
        cursorBrush = SolidColor(texto),
        decorationBox = { campo ->
            Box {
                if (valor.isEmpty()) Text(dica, color = Color(0xFF999999))
                campo()
            }
        },
    )
}

// .contagem e .vazio
@Composable
fun Contagem(mensagem: String, modifier: Modifier = Modifier) {
    Text(mensagem, modifier, color = Color(0xFFAAAAAA))
}

// .produtos: uma lista com 1px entre os itens, sobre fundo #444.
@Composable
fun Produtos(itens: LazyListScope.() -> Unit) {
    LazyColumn(
        Modifier.background(Color(0xFF444444)),
        verticalArrangement = Arrangement.spacedBy(1.dp),
        content = itens,
    )
}

// .produtos li: o nome e a categoria à esquerda, o preço à direita, centrado.
// O leitor de tela lê o item inteiro de uma vez, como um <li>.
@Composable
fun Produto(nome: String, categoria: String, preco: String) {
    Row(
        Modifier.fillMaxWidth().background(Color(0xFF333333)).padding(8.dp).semantics(mergeDescendants = true) {},
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Column(Modifier.weight(1f)) {
            Text(nome)
            // .produtos .categoria
            Text(categoria, color = Color(0xFF999999), fontSize = 14.sp)
        }
        // .produtos .preco
        Text(preco, Modifier.padding(start = 16.dp), color = Color(0xFF9FD88A))
    }
}
