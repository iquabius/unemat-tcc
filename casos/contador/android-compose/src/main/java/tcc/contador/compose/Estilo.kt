package tcc.contador.compose

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.RowScope
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ProvideTextStyle
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// Aparência do Contador, no papel do estilo.css da web: a tela só usa os
// nomes daqui (Tema, Estilo.contador, Valor, Botao), como o className.

// body: o tema da tela inteira.
@Composable
fun Tema(conteudo: @Composable () -> Unit) {
    MaterialTheme {
        Surface(Modifier.fillMaxSize(), color = Color(0xFF2B2B2B), content = conteudo)
    }
}

object Estilo {
    // .contador: duas colunas iguais. O espaço entre elas (1rem) e a
    // margem (0.5rem) vêm das margens de 8dp de cada célula.
    val contador = Modifier.safeDrawingPadding()

    // Célula: 3rem de altura e 8dp de margem; a largura (metade da linha)
    // vem do weight(1f), que só existe dentro de uma Row.
    val celula = Modifier.padding(8.dp).height(48.dp)
}

// .contador output
@Composable
fun RowScope.Valor(texto: String) {
    Box(
        Modifier.weight(1f).then(Estilo.celula).background(Color(0xFF2E4D24)),
        contentAlignment = Alignment.Center,
    ) {
        Text(texto, color = Color(0xFFEEEEEE), fontSize = 24.sp)
    }
}

// .contador button (sem os cantos arredondados e as margens internas do
// botão do Material).
@Composable
fun RowScope.Botao(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    conteudo: @Composable () -> Unit,
) {
    Button(
        onClick = onClick,
        modifier = Modifier.weight(1f).then(Estilo.celula).then(modifier),
        shape = RectangleShape,
        border = BorderStroke(1.dp, Color(0xFF555555)),
        colors = ButtonDefaults.buttonColors(
            containerColor = Color(0xFF3A3A3A),
            contentColor = Color(0xFFF5D33B),
        ),
        contentPadding = PaddingValues(0.dp),
    ) {
        ProvideTextStyle(TextStyle(fontSize = 40.sp), conteudo)
    }
}
