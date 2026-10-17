// Projeto Gradle único do desktop, em Java. Cada interface e tecnologia é um
// módulo em implementacoes/<interface>/<tecnologia>/, ao lado das
// implementações web e Android, e se chama :<interface>-<tecnologia> (por
// exemplo, :formulario-swing).
pluginManagement {
    repositories {
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
    repositories {
        mavenCentral()
    }
}

rootProject.name = "implementacoes-desktop"

val implementacoes = rootDir.parentFile

implementacoes.listFiles().orEmpty().sorted().forEach { gui ->
    listOf("swing", "javafx").forEach { tecnologia ->
        val pasta = gui.resolve(tecnologia)
        if (pasta.resolve("build.gradle.kts").exists()) {
            include(":${gui.name}-$tecnologia")
            project(":${gui.name}-$tecnologia").projectDir = pasta
        }
    }
}
