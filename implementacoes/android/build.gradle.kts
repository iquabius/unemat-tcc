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
            sourceSets.getByName("test").kotlin.directories +=
                rootDir.resolve("captura").path
            // Domínio do caso (casos/<caso>/dominio-kotlin/), o equivalente do
            // dominio.ts da web, compartilhado pelas duas tecnologias.
            val dominio = projectDir.resolveSibling("dominio-kotlin")
            if (dominio.isDirectory) {
                sourceSets.getByName("main").kotlin.directories +=
                    dominio.resolve("main").path
                sourceSets.getByName("test").kotlin.directories +=
                    dominio.resolve("test").path
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
                        destinoDasCapturas.getOrElse(
                            layout.buildDirectory
                                .dir("capturas")
                                .get()
                                .asFile
                                .path
                        ),
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

// Formatação do Kotlin de casos/ pelo ktfmt, no estilo das convenções do
// Kotlin (4 espaços) e com a largura do casos/.editorconfig (tcc-6wha). O
// npm run formatar e o npm run conferir-formatacao, em casos/, chamam estas
// tarefas depois do Prettier. Fica de fora casos/fora-da-analise/,
// congelado.
val ktfmt by configurations.creating {
    // O ktfmt publica também um jar com as dependências dentro, que evita
    // escolher a variante do Guava num projeto Android.
    attributes {
        attribute(Usage.USAGE_ATTRIBUTE, objects.named(Usage.JAVA_RUNTIME))
        attribute(Bundling.BUNDLING_ATTRIBUTE, objects.named(Bundling.SHADOWED))
    }
}

dependencies { ktfmt(libs.ktfmt) }

val arquivosKotlin =
    fileTree(rootDir.parentFile) {
        include("android/*.kts", "android/captura/**/*.kt")
        include("*/android-*/**/*.kt", "*/android-*/**/*.kts")
        include("*/dominio-kotlin/**/*.kt")
        exclude("**/build/**", "fora-da-analise/**")
    }

fun ktfmtTask(nome: String, descricao: String, vararg opcoes: String) =
    tasks.register<JavaExec>(nome) {
        description = descricao
        classpath = ktfmt
        mainClass = "com.facebook.ktfmt.cli.Main"
        // O compilador do Kotlin dentro do ktfmt usa o sun.misc.Unsafe, que o
        // JDK 25 avisa a cada execução.
        jvmArgs("--sun-misc-unsafe-memory-access=allow")
        args("--kotlinlang-style", "--enable-editorconfig", "--quiet", *opcoes)
        // A lista sai quando a tarefa é configurada, só se ela for pedida.
        args(arquivosKotlin.files.map { it.path }.sorted())
    }

ktfmtTask("formatarKotlin", "Formata o Kotlin de casos/ com o ktfmt.")

ktfmtTask(
    "conferirFormatacaoKotlin",
    "Falha se algum arquivo Kotlin de casos/ não estiver formatado.",
    "--dry-run",
    "--set-exit-if-changed",
)
