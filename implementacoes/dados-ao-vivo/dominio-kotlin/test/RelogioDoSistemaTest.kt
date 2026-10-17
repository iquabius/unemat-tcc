package tcc.dadosaovivo

import android.os.Looper
import androidx.test.ext.junit.runners.AndroidJUnit4
import java.time.Duration
import org.junit.Assert.assertEquals
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Shadows.shadowOf

// O relógio de verdade da fonte, que os outros testes trocam pelo falso: roda
// no Robolectric, que guarda a thread principal parada até o teste mandar.
@RunWith(AndroidJUnit4::class)
class RelogioDoSistemaTest {
    private fun esperar(ms: Long) =
        shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(ms))

    @Test
    fun repeteAteFechar() {
        var vezes = 0
        val repeticao = RelogioDoSistema.aCada(1000) { vezes++ }
        esperar(999)
        assertEquals(0, vezes)
        esperar(2001)
        assertEquals(3, vezes)
        repeticao.close()
        esperar(5000)
        assertEquals(3, vezes)
    }
}
