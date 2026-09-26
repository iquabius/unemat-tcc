package tcc.contador.compose

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Row
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Como o createRoot(...).render(...) do React; o Tema faz o papel
        // do import do estilo.css.
        setContent { Tema { Contador(valorInicial = 0) } }
    }
}

// Função que descreve a tela a partir do estado, como o componente React.
// A aparência fica em Estilo.kt.
@Composable
fun Contador(valorInicial: Int) {
    // Como o useState: mudar o valor faz a função rodar de novo.
    var contador by remember { mutableIntStateOf(valorInicial) }

    Row(Estilo.contador) {
        Valor("$contador")
        Botao(
            onClick = { contador = contador + 1 },
            // Como o aria-label do botão na web.
            modifier = Modifier.semantics { contentDescription = "Incrementar" },
        ) {
            Text("+")
        }
    }
}
