package tcc.dadosaovivo.views

import android.content.Context
import android.graphics.Typeface
import android.util.AttributeSet
import androidx.appcompat.widget.AppCompatTextView

// Parte da aparência, fora da análise como o estilo.xml: o negrito de .painel
// tr.alerta. Os seletores de res/color/ e res/drawable/ trocam a cor e o fundo
// pelo estado da view, mas não o peso da fonte; esta TextView o troca quando
// fica ativada, como fica a linha do palpite certo (o TableRow passa o estado
// às células).
class Celula(contexto: Context, atributos: AttributeSet?) :
    AppCompatTextView(contexto, atributos) {
    override fun drawableStateChanged() {
        super.drawableStateChanged()
        val estilo = if (isActivated) Typeface.BOLD else Typeface.NORMAL
        if (typeface?.style != estilo) setTypeface(null, estilo)
    }
}
