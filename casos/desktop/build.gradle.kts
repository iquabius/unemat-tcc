// Configuração comum a todos os módulos de desktop, para que o
// build.gradle.kts de cada um traga só o que é dele: plugins, mainClass e,
// no JavaFX, os módulos.
import org.jetbrains.kotlin.gradle.dsl.KotlinJvmProjectExtension

plugins {
    alias(libs.plugins.kotlin.jvm) apply false
    alias(libs.plugins.javafx) apply false
}

subprojects {
    apply(plugin = "application")
    // O Kotlin só compila o domínio do caso; a tela é Java.
    apply(plugin = "org.jetbrains.kotlin.jvm")

    // Domínio do caso (casos/<caso>/dominio-kotlin/), o mesmo do Android, no
    // papel do dominio.ts da web. Dos testes de lá só entra a regra DataFixa:
    // o DominioTest já roda no projeto Android.
    val dominio = projectDir.resolveSibling("dominio-kotlin")
    if (dominio.isDirectory) {
        extensions.configure<KotlinJvmProjectExtension> {
            sourceSets.getByName("main").kotlin.srcDir(dominio.resolve("main"))
            sourceSets.getByName("test").kotlin.srcDir(dominio.resolve("test"))
            sourceSets.getByName("test").kotlin.include("**/DataFixa.kt")
        }
    }

    dependencies {
        "testImplementation"(rootProject.libs.junit)
    }

    tasks.withType<Test>().configureEach {
        // Sem janela: o Swing monta os componentes sem tela, e o JavaFX usa a
        // plataforma Headless, experimental desde o JavaFX 25.
        systemProperty("java.awt.headless", "true")
        systemProperty("glass.platform", "Headless")
        systemProperty("prism.order", "sw")
        // O JavaFX carrega bibliotecas nativas pelo classpath.
        jvmArgs("--enable-native-access=ALL-UNNAMED")
        testLogging { exceptionFormat = org.gradle.api.tasks.testing.logging.TestExceptionFormat.FULL }
    }
}
