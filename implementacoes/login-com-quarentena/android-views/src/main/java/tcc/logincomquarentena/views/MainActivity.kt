package tcc.logincomquarentena.views

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.isVisible
import androidx.core.widget.doAfterTextChanged
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import tcc.logincomquarentena.DURACAO_DA_SESSAO
import tcc.logincomquarentena.MENSAGENS
import tcc.logincomquarentena.autenticar
import tcc.logincomquarentena.iniciarRelogio
import tcc.logincomquarentena.podeEntrar
import tcc.logincomquarentena.tempoDeSessao

class MainActivity : AppCompatActivity() {
    // O painel na página (null quando escondido), como o this.painel do Web
    // Component.
    private var painel: View? = null

    // Estado da coordenação, na Activity: a tentativa em andamento e o
    // relógio da sessão, como o AbortController e a função que para o
    // relógio no Web Component; cada um é a corrotina que o cancel() para.
    private var tentativa: Job? = null
    private var relogioDaSessao: Job? = null
    private var segundos = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        findViewById<Button>(R.id.alternar).setOnClickListener {
            if (painel != null) esconder() else mostrar()
        }
        mostrar()
    }

    // Põe o painel na página como se a interface abrisse. Como o
    // createElement e o append do Web Component, e o connectedCallback do
    // painel.
    private fun mostrar() {
        val login = findViewById<LinearLayout>(R.id.login)
        val novo = layoutInflater.inflate(R.layout.painel, login, false)
        login.addView(novo)
        painel = novo

        // Como os addEventListener("input") e ("click"). O doAfterTextChanged
        // é um TextWatcher que só usa o "depois".
        campo(R.id.nome).doAfterTextChanged { habilitarEntrar() }
        campo(R.id.senha).doAfterTextChanged { habilitarEntrar() }
        findViewById<Button>(R.id.entrar).setOnClickListener { tentar() }
        findViewById<Button>(R.id.sair).setOnClickListener { encerrarSessao() }
        findViewById<TextView>(R.id.situacao).text = MENSAGENS.desconectado
        findViewById<Button>(R.id.alternar).text = "Esconder login"
    }

    // Sem os cancel(), a tentativa e o relógio continuam fora da página.
    // Como o remove() e o disconnectedCallback do painel.
    private fun esconder() {
        tentativa?.cancel()
        relogioDaSessao?.cancel()
        findViewById<LinearLayout>(R.id.login).removeView(painel)
        painel = null
        findViewById<Button>(R.id.alternar).text = "Mostrar login"
    }

    // Como o querySelector do Web Component: busca a view pelo id do layout.
    private fun campo(id: Int): EditText = findViewById(id)

    // Como o .value do campo no Web Component.
    private fun texto(id: Int) = campo(id).text.toString()

    private fun habilitarEntrar() {
        findViewById<Button>(R.id.entrar).isEnabled =
            podeEntrar(texto(R.id.nome), texto(R.id.senha))
    }

    private fun tentar() {
        tentativa?.cancel()
        pararSessao()
        findViewById<TextView>(R.id.situacao).text = MENSAGENS.conectando
        // Como o then de autenticar(...): a corrotina espera a resposta sem
        // parar a tela, e a parte depois do autenticar roda quando ela chega.
        tentativa = lifecycleScope.launch {
            if (autenticar(texto(R.id.nome), texto(R.id.senha))) {
                iniciarSessao()
            } else {
                findViewById<TextView>(R.id.situacao).text = MENSAGENS.falha
            }
        }
    }

    private fun iniciarSessao() {
        segundos = 0
        findViewById<TextView>(R.id.situacao).text = MENSAGENS.conectado
        val tempo = findViewById<TextView>(R.id.relogio)
        tempo.text = tempoDeSessao(0)
        tempo.isVisible = true
        findViewById<Button>(R.id.sair).isVisible = true
        relogioDaSessao = lifecycleScope.iniciarRelogio {
            segundos += 1
            if (segundos >= DURACAO_DA_SESSAO) encerrarSessao()
            else tempo.text = tempoDeSessao(segundos)
        }
    }

    // Sem mexer na situação: a tentativa nova escreve a dela, e a região
    // anunciada não recebe "Desconectado." antes de "Conectando…".
    private fun pararSessao() {
        relogioDaSessao?.cancel()
        findViewById<TextView>(R.id.relogio).isVisible = false
        findViewById<Button>(R.id.sair).isVisible = false
    }

    private fun encerrarSessao() {
        pararSessao()
        findViewById<TextView>(R.id.situacao).text = MENSAGENS.desconectado
    }
}
