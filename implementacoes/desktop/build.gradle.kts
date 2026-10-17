// Configuração comum a todos os módulos de desktop, para que o
// build.gradle.kts de cada um traga só o que é dele: plugins, mainClass e,
// no JavaFX, os módulos.
import org.jetbrains.kotlin.gradle.dsl.KotlinJvmProjectExtension

plugins {
    alias(libs.plugins.kotlin.jvm) apply false
    alias(libs.plugins.javafx) apply false
}

// Formatação dos .kts do desktop pelo ktfmt, com as opções da tarefa de mesmo
// nome de implementacoes/android/, que não alcança esta pasta (tcc-6wha). O
// npm run formatar e o npm run conferir-formatacao, em implementacoes/,
// chamam as duas depois do Prettier, que formata o Java.
val ktfmt by configurations.creating {
    // O ktfmt publica também um jar com as dependências dentro; sem dizer
    // qual, o Gradle não escolhe entre os dois.
    attributes {
        attribute(Usage.USAGE_ATTRIBUTE, objects.named(Usage.JAVA_RUNTIME))
        attribute(Bundling.BUNDLING_ATTRIBUTE, objects.named(Bundling.SHADOWED))
    }
}

dependencies { ktfmt(libs.ktfmt) }

val arquivosKotlin =
    fileTree(rootDir.parentFile) {
        include("desktop/*.kts", "*/swing/*.kts", "*/javafx/*.kts")
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
        args(arquivosKotlin.files.map { it.path }.sorted())
    }

ktfmtTask("formatarKotlin", "Formata os .kts do desktop com o ktfmt.")

ktfmtTask(
    "conferirFormatacaoKotlin",
    "Falha se algum .kts do desktop não estiver formatado.",
    "--dry-run",
    "--set-exit-if-changed",
)

// Destino das capturas: o capturar.mts passa -Pcapturas.destino=<pasta>.
val destinoDasCapturas = providers.gradleProperty("capturas.destino")

subprojects {
    apply(plugin = "application")
    // O Kotlin só compila o domínio da interface; a tela é Java.
    apply(plugin = "org.jetbrains.kotlin.jvm")

    // Domínio da interface (implementacoes/<interface>/dominio-kotlin/), o
    // mesmo do Android, no papel do dominio.ts da web. Dos testes de lá só
    // entra a regra DataFixa: o DominioTest já roda no projeto Android.
    val dominio = projectDir.resolveSibling("dominio-kotlin")
    if (dominio.isDirectory) {
        extensions.configure<KotlinJvmProjectExtension> {
            sourceSets.getByName("main").kotlin.srcDir(dominio.resolve("main"))
            sourceSets.getByName("test").kotlin.srcDir(dominio.resolve("test"))
            sourceSets.getByName("test").kotlin.include("**/DataFixa.kt")
        }
    }

    // Aparência do JavaFX (implementacoes/<interface>/javafx-estilo/
    // estilo.css), fora da tela, como o estilo.css da web.
    val estilo = projectDir.resolveSibling("javafx-estilo")
    if (estilo.isDirectory && !name.endsWith("-swing")) {
        extensions.configure<SourceSetContainer> {
            getByName("main").resources.srcDir(estilo)
        }
    }

    // Apoio das Telas de teste e das cenas (implementacoes/desktop/teste/),
    // um por tecnologia e um comum às duas, como o
    // implementacoes/android/captura/.
    val tecnologia = if (name.endsWith("-swing")) "swing" else "javafx"
    extensions.configure<SourceSetContainer> {
        getByName("test").java.srcDir(rootDir.resolve("teste/$tecnologia"))
        getByName("test").java.srcDir(rootDir.resolve("teste/comum"))
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
        // Texto suavizado, como no desktop Linux: sem janela, o Swing não lê
        // a configuração do sistema.
        systemProperty("awt.useSystemAAFontSettings", "on")
        // O JavaFX carrega bibliotecas nativas pelo classpath.
        jvmArgs("--enable-native-access=ALL-UNNAMED")
        // Onde as cenas gravam as capturas (Captura.java).
        systemProperty("capturas.tecnologia", projectDir.name)
        systemProperty(
            "capturas.destino",
            destinoDasCapturas.getOrElse(
                layout.buildDirectory.dir("capturas").get().asFile.path
            ),
        )
        testLogging {
            exceptionFormat =
                org.gradle.api.tasks.testing.logging.TestExceptionFormat.FULL
        }
    }
}
