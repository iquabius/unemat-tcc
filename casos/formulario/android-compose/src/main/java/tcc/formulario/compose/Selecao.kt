package tcc.formulario.compose

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.Role

// O <select>, que o Compose não traz pronto: um campo que abre um menu
// (DropdownMenu) com as opções. Na web e no Views (Spinner), a plataforma
// traz o componente inteiro; aqui ele é montado, com o próprio estado.
@Composable
fun <T> Selecao(opcoes: List<Pair<T, String>>, escolhida: T, aoEscolher: (T) -> Unit) {
    var aberta by remember { mutableStateOf(false) }

    Box {
        Text(
            opcoes.first { it.first == escolhida }.second,
            Modifier.fillMaxWidth().clickable(role = Role.DropdownList) { aberta = true }.caixa(),
        )
        DropdownMenu(expanded = aberta, onDismissRequest = { aberta = false }) {
            for ((valor, rotulo) in opcoes) {
                DropdownMenuItem(
                    text = { Text(rotulo) },
                    onClick = {
                        aoEscolher(valor)
                        aberta = false
                    },
                )
            }
        }
    }
}
