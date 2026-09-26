package tcc.contador.views

import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.click
import androidx.test.espresso.matcher.ViewMatchers.withContentDescription
import androidx.test.ext.junit.rules.ActivityScenarioRule
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
    val regra = ActivityScenarioRule(MainActivity::class.java)

    @Test
    fun inicial() = capturar("inicial")

    @Test
    fun tresCliques() {
        repeat(3) { onView(withContentDescription("Incrementar")).perform(click()) }
        capturar("tres-cliques")
    }
}
