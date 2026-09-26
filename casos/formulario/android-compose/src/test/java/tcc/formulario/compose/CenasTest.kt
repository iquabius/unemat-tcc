package tcc.formulario.compose

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.annotation.Config
import tcc.captura.SemAnimacoes
import tcc.captura.capturar
import tcc.formulario.DataFixa
import tcc.formulario.TipoDeVoo

// Mesmas cenas de casos/formulario/cenas.mts. A tela tem 416dp de largura
// para a coluna ficar com os 384dp do max-width da web.
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = "w416dp-h560dp-xhdpi")
class CenasTest {
    @get:Rule(order = 0)
    val dataFixa = DataFixa()

    @get:Rule(order = 1)
    val semAnimacoes = SemAnimacoes()

    @get:Rule(order = 2)
    val regra = createAndroidComposeRule<MainActivity>()

    private val tela by lazy { Tela(regra) }

    @Test
    fun inicial() = capturar("inicial")

    // Erros visíveis: nome tocado e vazio, e-mail mal formatado, volta antes da ida.
    @Test
    fun erros() {
        tela.focar(Campo.NOME)
        tela.preencher(Campo.EMAIL, "maria@")
        tela.escolherTipo(TipoDeVoo.IDA_E_VOLTA)
        tela.preencher(Campo.VOLTA, "01/09/2026")
        tela.focar(Campo.NOME)
        capturar("erros")
    }

    @Test
    fun reservado() {
        tela.preencher(Campo.NOME, "Maria")
        tela.preencher(Campo.EMAIL, "maria@exemplo.com")
        tela.escolherTipo(TipoDeVoo.IDA_E_VOLTA)
        tela.preencher(Campo.IDA, "10/10/2026")
        tela.preencher(Campo.VOLTA, "15/10/2026")
        tela.reservar()
        capturar("reservado")
    }
}
