package tcc.formulario.compose

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.LocalTextStyle
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.semantics.error
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// Aparência do Formulário, no papel do estilo.css da web: a tela só usa os
// nomes daqui (Tema, Formulario, Rotulo, Entrada, Erro, Botao, Confirmacao),
// como o className. Os estados (:disabled, [aria-invalid]) viram parâmetros.

private val texto = Color(0xFFEEEEEE)

// body: o tema da tela inteira, que rola quando não cabe.
@Composable
fun Tema(conteudo: @Composable ColumnScope.() -> Unit) {
    MaterialTheme(colorScheme = darkColorScheme()) {
        Surface(Modifier.fillMaxSize(), color = Color(0xFF2B2B2B), contentColor = texto) {
            // Substitui o texto do Material (com espaçamento entre letras e
            // entrelinha próprios) pelo texto comum, como o do body.
            CompositionLocalProvider(LocalTextStyle provides TextStyle(fontSize = 16.sp)) {
                Column(
                    Modifier.safeDrawingPadding().verticalScroll(rememberScrollState()),
                    content = conteudo,
                )
            }
        }
    }
}

// .formulario: uma coluna com 0.75rem entre os itens e 1rem de margem. Sem o
// max-width de 24rem, como no Views; a captura usa uma tela de 416dp.
@Composable
fun Formulario(conteudo: @Composable ColumnScope.() -> Unit) {
    Column(Modifier.padding(16.dp), Arrangement.spacedBy(12.dp), content = conteudo)
}

// .formulario label: o texto e o campo, com 0.25rem entre eles.
@Composable
fun Rotulo(texto: String, campo: @Composable () -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(texto)
        campo()
    }
}

// Fundo e borda de .formulario input e select; vermelhos quando inválido.
internal fun Modifier.caixa(invalida: Boolean = false) = this
    .border(1.dp, if (invalida) Color(0xFFE05555) else Color(0xFF555555))
    .background(if (invalida) Color(0xFF4A2A2A) else Color(0xFF3A3A3A))
    .padding(6.4.dp)

// .formulario input, com :disabled (opacity: 0.5) e [aria-invalid="true"].
@Composable
fun Entrada(
    valor: String,
    aoMudar: (String) -> Unit,
    modifier: Modifier = Modifier,
    invalida: Boolean = false,
    habilitada: Boolean = true,
    dica: String = "",
    teclado: KeyboardType = KeyboardType.Text,
) {
    BasicTextField(
        value = valor,
        onValueChange = aoMudar,
        modifier = modifier
            .fillMaxWidth()
            .alpha(if (habilitada) 1f else 0.5f)
            // Como o aria-invalid, para o leitor de tela.
            .semantics { if (invalida) error("inválido") }
            .caixa(invalida),
        enabled = habilitada,
        singleLine = true,
        textStyle = TextStyle(color = texto, fontSize = 16.sp),
        keyboardOptions = KeyboardOptions(keyboardType = teclado),
        cursorBrush = SolidColor(texto),
        decorationBox = { campo ->
            Box {
                if (valor.isEmpty()) Text(dica, color = Color(0xFF999999))
                campo()
            }
        },
    )
}

// .formulario .erro
@Composable
fun Erro(mensagem: String) {
    Text(mensagem, color = Color(0xFFFF8A8A), fontSize = 14.sp)
}

// .formulario button, com :disabled nas cores.
@Composable
fun Botao(onClick: () -> Unit, habilitado: Boolean, conteudo: @Composable () -> Unit) {
    Button(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth(),
        enabled = habilitado,
        shape = RectangleShape,
        border = BorderStroke(1.dp, Color(0xFF555555)),
        colors = ButtonDefaults.buttonColors(
            containerColor = Color(0xFF2E4D24),
            contentColor = texto,
            disabledContainerColor = Color(0xFF3A3A3A),
            disabledContentColor = Color(0xFF888888),
        ),
        contentPadding = PaddingValues(8.dp),
    ) {
        CompositionLocalProvider(LocalTextStyle provides TextStyle(fontSize = 16.sp), content = conteudo)
    }
}

// .confirmacao
@Composable
fun Confirmacao(mensagem: String, modifier: Modifier = Modifier) {
    Text(mensagem, modifier.padding(horizontal = 16.dp), color = Color(0xFF9FD88A))
}
