package tcc.dadosaovivo.compose

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.foundation.layout.sizeIn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.LocalMinimumInteractiveComponentSize
import androidx.compose.material3.LocalTextStyle
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.Layout
import androidx.compose.ui.layout.Measurable
import androidx.compose.ui.layout.layoutId
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Constraints
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// Aparência dos Dados ao vivo, no papel do estilo.css da web: a tela só usa
// os nomes daqui (Tema, Placares, Painel, Situacao, Tabela, Cabecalho, Linha,
// Celula, Botao), como o className. O tr.alerta vira parâmetro da Linha.

private val texto = Color(0xFFEEEEEE)

// body: o tema da tela inteira.
@Composable
fun Tema(conteudo: @Composable ColumnScope.() -> Unit) {
    MaterialTheme(colorScheme = darkColorScheme()) {
        Surface(
            Modifier.fillMaxSize(),
            color = Color(0xFF2B2B2B),
            contentColor = texto,
        ) {
            // Substitui o texto do Material (com espaçamento entre letras e
            // entrelinha próprios) pelo texto comum, como o do body.
            CompositionLocalProvider(
                LocalTextStyle provides TextStyle(fontSize = 16.sp)
            ) {
                Column(Modifier.safeDrawingPadding(), content = conteudo)
            }
        }
    }
}

// .placares: uma coluna com 0.5rem entre os itens e 1rem de margem,
// alinhados ao início.
@Composable
fun Placares(conteudo: @Composable ColumnScope.() -> Unit) {
    Column(
        Modifier.padding(16.dp),
        Arrangement.spacedBy(8.dp),
        content = conteudo,
    )
}

// .painel: uma coluna com 0.5rem entre os itens.
@Composable
fun Painel(conteudo: @Composable ColumnScope.() -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp), content = conteudo)
}

// .situacao
@Composable
fun Situacao(mensagem: String, modifier: Modifier = Modifier) {
    Text(mensagem, modifier, color = Color(0xFFAAAAAA))
}

// O fundo que cada linha põe antes das células, para a Tabela achar onde a
// linha começa.
private const val FUNDO = "fundo"

// .painel table: as colunas têm a largura do maior conteúdo, como na tabela
// do HTML e no TableLayout do Views. O Compose não traz tabela: a Tabela
// recebe as células de todas as linhas, cada linha começando pelo fundo dela,
// e as arruma em colunas.
@Composable
fun Tabela(linhas: @Composable () -> Unit) {
    Layout(linhas) { filhos, _ ->
        val fundos = mutableListOf<Measurable>()
        val celulasPorLinha = mutableListOf<MutableList<Measurable>>()
        for (filho in filhos) {
            if (filho.layoutId == FUNDO) {
                fundos += filho
                celulasPorLinha += mutableListOf<Measurable>()
            } else {
                celulasPorLinha.last() += filho
            }
        }
        val celulas = celulasPorLinha.map { linha ->
            linha.map { it.measure(Constraints()) }
        }
        val colunas = celulas.maxOf { it.size }
        val larguras =
            (0 until colunas).map { c ->
                celulas.maxOf { linha -> linha.getOrNull(c)?.width ?: 0 }
            }
        val alturas = celulas.map { linha -> linha.maxOf { it.height } }
        val largura = larguras.sum()
        val planos = fundos.mapIndexed { i, fundo ->
            fundo.measure(Constraints.fixed(largura, alturas[i]))
        }
        layout(largura, alturas.sum()) {
            var y = 0
            celulas.forEachIndexed { i, linha ->
                planos[i].place(0, y)
                var x = 0
                linha.forEachIndexed { c, celula ->
                    // td:first-child à esquerda; as outras, à direita.
                    val folga = if (c == 0) 0 else larguras[c] - celula.width
                    celula.place(x + folga, y)
                    x += larguras[c]
                }
                y += alturas[i]
            }
        }
    }
}

@Composable
private fun LinhaDaTabela(
    fundo: Color,
    peso: FontWeight,
    celulas: @Composable () -> Unit,
) {
    Box(Modifier.layoutId(FUNDO).background(fundo))
    CompositionLocalProvider(
        LocalTextStyle provides LocalTextStyle.current.copy(fontWeight = peso),
        content = celulas,
    )
}

// .painel th: a linha dos títulos, em negrito.
@Composable
fun Cabecalho(celulas: @Composable () -> Unit) =
    LinhaDaTabela(Color.Transparent, FontWeight.Bold, celulas)

// .painel tr, com tr.alerta: o fundo e o negrito da linha do palpite certo.
@Composable
fun Linha(alerta: Boolean, celulas: @Composable () -> Unit) =
    LinhaDaTabela(
        if (alerta) Color(0xFF6B4B00) else Color.Transparent,
        if (alerta) FontWeight.Bold else FontWeight.Normal,
        celulas,
    )

// .painel td e th: 0.2rem e 0.6rem de margem interna, sem quebra de linha.
@Composable
fun Celula(conteudo: String) {
    Text(
        conteudo,
        Modifier.padding(horizontal = 9.6.dp, vertical = 3.2.dp),
        softWrap = false,
        maxLines = 1,
    )
}

// .placares button: o botão padrão do navegador, cinza-claro, com borda e
// cantos de 3px, e 0.4rem de margem interna.
@Composable
fun Botao(onClick: () -> Unit, conteudo: @Composable () -> Unit) {
    // Sem a área mínima de toque do Material, que aumenta o botão.
    CompositionLocalProvider(
        LocalMinimumInteractiveComponentSize provides Dp.Unspecified
    ) {
        Button(
            onClick = onClick,
            // Um mínimo qualquer desliga o tamanho mínimo do botão do
            // Material, de 58 × 40dp.
            modifier = Modifier.sizeIn(minWidth = 1.dp, minHeight = 1.dp),
            shape = RoundedCornerShape(3.dp),
            border = BorderStroke(1.dp, Color(0xFF767676)),
            colors =
                ButtonDefaults.buttonColors(
                    containerColor = Color(0xFFEFEFEF),
                    contentColor = Color.Black,
                ),
            contentPadding = PaddingValues(6.4.dp),
        ) {
            CompositionLocalProvider(
                LocalTextStyle provides TextStyle(fontSize = 16.sp),
                content = conteudo,
            )
        }
    }
}
