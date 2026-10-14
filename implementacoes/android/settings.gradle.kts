// Projeto Gradle único das implementações Android. Cada interface e
// tecnologia é um módulo em implementacoes/<interface>/<tecnologia>/, ao lado
// das implementações web, e se chama :<interface>-<tecnologia> (por exemplo,
// :formulario-android-compose). O código em implementacoes/fora-da-analise/
// fica de fora: a busca desce um nível só.
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "implementacoes-android"

val implementacoes = rootDir.parentFile

implementacoes.listFiles().orEmpty().sorted().forEach { gui ->
    listOf("android-views", "android-compose").forEach { tecnologia ->
        val pasta = gui.resolve(tecnologia)
        if (pasta.resolve("build.gradle.kts").exists()) {
            include(":${gui.name}-$tecnologia")
            project(":${gui.name}-$tecnologia").projectDir = pasta
        }
    }
}
