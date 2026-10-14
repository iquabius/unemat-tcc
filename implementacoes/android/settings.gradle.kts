// Projeto Gradle único dos casos Android. Cada caso e tecnologia é um módulo
// em implementacoes/<caso>/<tecnologia>/, ao lado das implementações web, e
// se chama :<caso>-<tecnologia> (por exemplo, :formulario-android-compose). O
// código em implementacoes/fora-da-analise/ fica de fora: a busca desce um
// nível só.
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

implementacoes.listFiles().orEmpty().sorted().forEach { caso ->
    listOf("android-views", "android-compose").forEach { tecnologia ->
        val pasta = caso.resolve(tecnologia)
        if (pasta.resolve("build.gradle.kts").exists()) {
            include(":${caso.name}-$tecnologia")
            project(":${caso.name}-$tecnologia").projectDir = pasta
        }
    }
}
