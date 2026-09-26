package tcc.captura

import android.animation.ValueAnimator
import com.github.takahirom.roborazzi.ExperimentalRoborazziApi
import com.github.takahirom.roborazzi.captureScreenRoboImage
import org.junit.rules.ExternalResource

// Grava a tela inteira em <destino>/<tecnologia>-<cena>.png, com o mesmo
// esquema de nomes das capturas web. Destino e tecnologia vêm do Gradle
// (build.gradle.kts da raiz); quem compara com as versionadas é o
// casos/capturar.mts.
@OptIn(ExperimentalRoborazziApi::class)
fun capturar(cena: String) {
    val destino = System.getProperty("capturas.destino")
    val tecnologia = System.getProperty("capturas.tecnologia")
    captureScreenRoboImage("$destino/$tecnologia-$cena.png")
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
        ValueAnimator::class.java
            .getMethod("setDurationScale", Float::class.javaPrimitiveType)
            .invoke(null, valor)
    }
}
