package tcc.contador.compose

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.style.TextAlign

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Como o createRoot(...).render(...) do React.
        setContent { MaterialTheme { Contador(valorInicial = 0) } }
    }
}

// Função que descreve a tela a partir do estado, como o componente React.
@Composable
fun Contador(valorInicial: Int) {
    // Como o useState: mudar o valor faz a função rodar de novo.
    var contador by remember { mutableIntStateOf(valorInicial) }

    Row(Modifier.safeDrawingPadding(), verticalAlignment = Alignment.CenterVertically) {
        Text("$contador", Modifier.weight(1f), textAlign = TextAlign.Center)
        Button(
            onClick = { contador = contador + 1 },
            // Como o aria-label do botão na web.
            modifier = Modifier.weight(1f).semantics { contentDescription = "Incrementar" },
        ) {
            Text("+")
        }
    }
}
