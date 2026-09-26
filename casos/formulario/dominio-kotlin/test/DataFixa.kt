package tcc.formulario

import org.junit.rules.ExternalResource
import java.time.Clock
import java.time.Instant
import java.time.ZoneOffset

// Regra JUnit que fixa "hoje" em 26/09/2026 durante o teste, a mesma data
// que o script de capturas fixa na web.
class DataFixa : ExternalResource() {
    override fun before() {
        relogio = Clock.fixed(Instant.parse("2026-09-26T12:00:00Z"), ZoneOffset.UTC)
    }

    override fun after() {
        relogio = Clock.systemDefaultZone()
    }
}
