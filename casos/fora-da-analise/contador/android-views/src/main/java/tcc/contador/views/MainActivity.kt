package tcc.contador.views

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    // O estado fica na Activity, como a variável do jQuery.
    private var contador = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Como $("#valor"): busca a view pelo id do layout.
        val valor = findViewById<TextView>(R.id.valor)
        valor.text = contador.toString()

        // Como $("#incrementar").on("click", ...): muda o estado e a tela.
        findViewById<Button>(R.id.incrementar).setOnClickListener {
            contador = contador + 1
            valor.text = contador.toString()
        }
    }
}
