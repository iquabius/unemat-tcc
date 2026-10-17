package tcc.captura

import android.animation.ValueAnimator
import android.graphics.Bitmap
import android.graphics.Canvas
import androidx.test.espresso.Espresso
import androidx.test.runner.lifecycle.ActivityLifecycleMonitorRegistry
import androidx.test.runner.lifecycle.Stage
import com.github.takahirom.roborazzi.captureRoboImage
import org.junit.rules.ExternalResource

// Grava a janela da Activity em primeiro plano (sem diálogos nem popups, que
// são outras janelas) em <destino>/<tecnologia>-<cena>.png, com o mesmo
// esquema de nomes das capturas web. Destino e tecnologia vêm do Gradle
// (build.gradle.kts da raiz); quem compara com as versionadas é o
// implementacoes/capturar.mts.
//
// A imagem sai do desenho da janela num Bitmap, como o View.draw, e não da
// cópia da superfície (PixelCopy) que o captureScreenRoboImage faz: na API 37,
// o Robolectric 4.17 desenha de verdade, e a cópia às vezes devolvia a tela de
// antes da última alteração (no Login, o "Conectando…" na cena da falha). O
// desenho mostra o que as views dizem agora.
fun capturar(cena: String) {
    val destino = System.getProperty("capturas.destino")
    val tecnologia = System.getProperty("capturas.tecnologia")
    Espresso.onIdle()
    val raiz =
        ActivityLifecycleMonitorRegistry.getInstance()
            .getActivitiesInStage(Stage.RESUMED)
            .single()
            .window
            .decorView
    val imagem =
        Bitmap.createBitmap(raiz.width, raiz.height, Bitmap.Config.ARGB_8888)
    raiz.draw(Canvas(imagem))
    imagem.captureRoboImage("$destino/$tecnologia-$cena.png")
}

// Regra JUnit que zera a duração das animações durante o teste, como a opção
// de desenvolvedor "Escala de duração do Animator: desligada". Sem ela, o
// efeito de toque (ripple) fica pela metade na captura, com um brilho que
// muda a cada execução, no Views e no Compose. O setDurationScale é público
// no Android, mas escondido do SDK; por isso a reflexão.
class SemAnimacoes : ExternalResource() {
    override fun before() = escala(0f)

    override fun after() = escala(1f)

    private fun escala(valor: Float) {
        ValueAnimator::class
            .java
            .getMethod("setDurationScale", Float::class.javaPrimitiveType)
            .invoke(null, valor)
    }
}
