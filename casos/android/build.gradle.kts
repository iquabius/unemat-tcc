// Configuração comum a todos os módulos (casos e tecnologias), para que o
// build.gradle.kts de cada um traga só o que é dele: plugins e dependências.
import com.android.build.api.dsl.ApplicationExtension

plugins {
    alias(libs.plugins.android.application) apply false
    // O AGP 9 já compila Kotlin; declarar o plugin fixa o Kotlin em 2.4.20.
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.compose) apply false
}

// Destino das capturas: o capturar.mts passa -Pcapturas.destino=<pasta>.
val destinoDasCapturas = providers.gradleProperty("capturas.destino")

subprojects {
    pluginManager.withPlugin("com.android.application") {
        extensions.configure<ApplicationExtension> {
            compileSdk = 37
            defaultConfig {
                minSdk = 26
                targetSdk = 37
                versionCode = 1
                versionName = "1.0"
            }
            // Auxiliar de captura (casos/android/captura/) nos testes de todos.
            sourceSets.getByName("test").kotlin.directories += rootDir.resolve("captura").path
            // Domínio do caso (casos/<caso>/dominio-kotlin/), o equivalente do
            // dominio.ts da web, compartilhado pelas duas tecnologias.
            val dominio = projectDir.resolveSibling("dominio-kotlin")
            if (dominio.isDirectory) {
                sourceSets.getByName("main").kotlin.directories += dominio.resolve("main").path
                sourceSets.getByName("test").kotlin.directories += dominio.resolve("test").path
            }
            testOptions.unitTests {
                isIncludeAndroidResources = true
                all { teste ->
                    // Exigidas pelo Robolectric no Java 17 ou mais novo
                    // (robolectric.org/getting-started).
                    teste.jvmArgs(
                        "--add-opens=java.base/java.io=ALL-UNNAMED",
                        "--add-opens=java.base/java.lang=ALL-UNNAMED",
                        "--add-opens=java.base/java.net=ALL-UNNAMED",
                        "--add-opens=java.base/java.security=ALL-UNNAMED",
                        "--add-opens=java.base/java.text=ALL-UNNAMED",
                        "--add-opens=java.base/java.util=ALL-UNNAMED",
                        "--add-opens=java.base/jdk.internal.access=ALL-UNNAMED",
                        "--add-opens=java.desktop/java.awt.font=ALL-UNNAMED",
                        "--add-opens=jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED",
                    )
                    teste.systemProperty("robolectric.graphicsMode", "NATIVE")
                    teste.systemProperty("roborazzi.test.record", "true")
                    teste.systemProperty("capturas.tecnologia", projectDir.name)
                    teste.systemProperty(
                        "capturas.destino",
                        destinoDasCapturas.getOrElse(layout.buildDirectory.dir("capturas").get().asFile.path),
                    )
                }
            }
        }
        dependencies {
            "testImplementation"(libs.junit)
            "testImplementation"(libs.androidx.test.ext.junit)
            "testImplementation"(libs.robolectric)
            "testImplementation"(libs.roborazzi)
            // Os testes do Compose também usam o Espresso; a versão que vem com
            // eles não conhece a API 37.
            "testImplementation"(libs.espresso.core)
        }
    }
}
