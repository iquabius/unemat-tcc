package tcc.formulario.views

import android.os.Bundle
import android.view.View
import android.widget.AdapterView
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.isVisible
import androidx.core.widget.doAfterTextChanged
import tcc.formulario.Reserva
import tcc.formulario.TipoDeVoo
import tcc.formulario.erroDaData
import tcc.formulario.erroDaOrdem
import tcc.formulario.erroDoEmail
import tcc.formulario.erroDoNome
import tcc.formulario.hoje
import tcc.formulario.mensagemDeConfirmacao

class MainActivity : AppCompatActivity() {
    // Ids dos campos já tocados (que perderam o foco uma vez), como o Set do
    // jQuery. O estado fica na Activity.
    private val tocados = mutableSetOf<Int>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        campo(R.id.ida).setText(hoje())
        campo(R.id.volta).setText(hoje())

        // Como .on("input", validar).on("blur", ...) do jQuery. O
        // doAfterTextChanged é um TextWatcher que só usa o "depois".
        for (id in listOf(R.id.nome, R.id.email, R.id.ida, R.id.volta)) {
            campo(id).doAfterTextChanged { validar() }
            campo(id).setOnFocusChangeListener { _, temFoco ->
                if (!temFoco) {
                    tocados += id
                    validar()
                }
            }
        }

        // Como .on("change") do <select>. O Spinner também avisa a seleção
        // inicial, quando aparece na tela.
        findViewById<Spinner>(R.id.tipo).onItemSelectedListener =
            object : AdapterView.OnItemSelectedListener {
                override fun onItemSelected(pai: AdapterView<*>?, item: View?, posicao: Int, id: Long) {
                    campo(R.id.volta).isEnabled = tipo() == TipoDeVoo.IDA_E_VOLTA
                    validar()
                }

                override fun onNothingSelected(pai: AdapterView<*>?) {}
            }

        // Como .on("submit"): o botão só fica habilitado sem erros.
        findViewById<Button>(R.id.reservar).setOnClickListener {
            findViewById<TextView>(R.id.confirmacao).text = mensagemDeConfirmacao(
                Reserva(texto(R.id.nome), texto(R.id.email), tipo(), texto(R.id.ida), texto(R.id.volta)),
            )
        }

        validar()
    }

    // Como $("#id"): busca a view pelo id do layout.
    private fun campo(id: Int): EditText = findViewById(id)

    // Como $("#id").val().
    private fun texto(id: Int) = campo(id).text.toString()

    private fun tipo() = TipoDeVoo.entries[findViewById<Spinner>(R.id.tipo).selectedItemPosition]

    private fun mostrarErro(id: Int, idDoErro: Int, erro: String?) {
        // Como o aria-invalid: o estilo pinta de vermelho o campo ativado.
        campo(id).isActivated = erro != null
        val paragrafo = findViewById<TextView>(idDoErro)
        paragrafo.text = erro
        paragrafo.isVisible = erro != null
    }

    // Revalida o formulário inteiro a cada evento: mostra os erros dos campos
    // já tocados e habilita o botão só se não houver erro nenhum.
    private fun validar() {
        val idaEVolta = tipo() == TipoDeVoo.IDA_E_VOLTA
        val erroNome = erroDoNome(texto(R.id.nome))
        val erroEmail = erroDoEmail(texto(R.id.email))
        val erroIda = erroDaData(texto(R.id.ida))
        val erroVolta = if (idaEVolta) erroDaData(texto(R.id.volta)) else null
        val erroOrdem = if (idaEVolta) erroDaOrdem(texto(R.id.ida), texto(R.id.volta)) else null

        mostrarErro(R.id.nome, R.id.erro_nome, if (R.id.nome in tocados) erroNome else null)
        mostrarErro(R.id.email, R.id.erro_email, if (R.id.email in tocados) erroEmail else null)
        mostrarErro(R.id.ida, R.id.erro_ida, if (R.id.ida in tocados) erroIda else null)
        mostrarErro(
            R.id.volta,
            R.id.erro_volta,
            (if (R.id.volta in tocados) erroVolta else null)
                ?: (if (R.id.ida in tocados || R.id.volta in tocados) erroOrdem else null),
        )

        val temErro = listOf(erroNome, erroEmail, erroIda, erroVolta, erroOrdem).any { it != null }
        findViewById<Button>(R.id.reservar).isEnabled = !temErro
    }
}
