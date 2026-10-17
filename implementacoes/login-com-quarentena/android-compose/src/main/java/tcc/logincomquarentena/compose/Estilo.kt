package tcc.logincomquarentena.compose

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.foundation.layout.sizeIn
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
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
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// Aparência do Login com quarentena, no papel do estilo.css da web: a tela só
// usa os nomes daqui (Tema, Login, Painel, Rotulo, Entrada, Paragrafo,
// Botao), como o className. O :disabled do botão vira parâmetro.

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

// .login: uma coluna com 0.75rem entre os itens, 1rem de margem e no máximo
// 20rem de largura.
@Composable
fun Login(conteudo: @Composable ColumnScope.() -> Unit) {
    Column(
        Modifier.padding(16.dp).widthIn(max = 320.dp),
        Arrangement.spacedBy(12.dp),
        content = conteudo,
    )
}

// .painel: uma coluna com 0.75rem entre os itens.
@Composable
fun Painel(conteudo: @Composable ColumnScope.() -> Unit) {
    Column(
        verticalArrangement = Arrangement.spacedBy(12.dp),
        content = conteudo,
    )
}

// .painel label: o texto e o campo, com 0.25rem entre eles.
@Composable
fun Rotulo(texto: String, campo: @Composable () -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(texto)
        campo()
    }
}

// .painel input; com senha = true, o input type="password", que mostra um
// ponto no lugar de cada caractere.
@Composable
fun Entrada(
    valor: String,
    aoMudar: (String) -> Unit,
    modifier: Modifier = Modifier,
    senha: Boolean = false,
) {
    BasicTextField(
        value = valor,
        onValueChange = aoMudar,
        modifier =
            modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFF555555))
                .background(Color(0xFF3A3A3A))
                .padding(6.4.dp),
        singleLine = true,
        textStyle = TextStyle(color = texto, fontSize = 16.sp),
        keyboardOptions =
            KeyboardOptions(
                keyboardType =
                    if (senha) KeyboardType.Password else KeyboardType.Text
            ),
        visualTransformation =
            if (senha) PasswordVisualTransformation()
            else VisualTransformation.None,
        cursorBrush = SolidColor(texto),
    )
}

// .login p
@Composable
fun Paragrafo(conteudo: String, modifier: Modifier = Modifier) {
    Text(conteudo, modifier)
}

// .login button: o botão padrão do navegador, cinza-claro, com borda e cantos
// de 3px, e 0.4rem de margem interna, esticado na coluna; desabilitado, nas
// cores que o navegador pinta sobre o fundo da página.
@Composable
fun Botao(
    onClick: () -> Unit,
    habilitado: Boolean = true,
    conteudo: @Composable () -> Unit,
) {
    // Sem a área mínima de toque do Material, que aumenta o botão.
    CompositionLocalProvider(
        LocalMinimumInteractiveComponentSize provides Dp.Unspecified
    ) {
        Button(
            onClick = onClick,
            // Um mínimo qualquer desliga o tamanho mínimo do botão do
            // Material, de 58 × 40dp.
            modifier =
                Modifier.fillMaxWidth()
                    .sizeIn(minWidth = 1.dp, minHeight = 1.dp),
            enabled = habilitado,
            shape = RoundedCornerShape(3.dp),
            border =
                BorderStroke(
                    1.dp,
                    if (habilitado) Color(0xFF767676) else Color(0xFF424242),
                ),
            colors =
                ButtonDefaults.buttonColors(
                    containerColor = Color(0xFFEFEFEF),
                    contentColor = Color.Black,
                    disabledContainerColor = Color(0xFF777777),
                    disabledContentColor = Color(0xFF5A5A5A),
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
