package tcc.contador.compose

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.performClick
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.annotation.Config
import tcc.captura.SemAnimacoes
import tcc.captura.capturar

// Mesmas cenas de casos/contador/cenas.mts.
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w480dp-h200dp-xhdpi")
class CenasTest {
    @get:Rule
    val semAnimacoes = SemAnimacoes()

    @get:Rule
    val regra = createAndroidComposeRule<MainActivity>()

    @Test
    fun inicial() = capturar("inicial")

    @Test
    fun tresCliques() {
        repeat(3) { regra.onNodeWithContentDescription("Incrementar").performClick() }
        // Espera a recomposição do último clique (o Espresso do Views já espera).
        regra.waitForIdle()
        capturar("tres-cliques")
    }
}
