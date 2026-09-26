// Projeto Gradle único dos casos Android. Cada caso e variante é um módulo
// em casos/<caso>/android-<variante>/, ao lado das implementações web, e se
// chama :<caso>-android-<variante> (por exemplo, :contador-android-compose).
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

rootProject.name = "casos-android"

val casos = rootDir.parentFile
casos.listFiles().orEmpty().sorted().forEach { caso ->
    listOf("android-views", "android-compose").forEach { variante ->
        val pasta = caso.resolve(variante)
        if (pasta.resolve("build.gradle.kts").exists()) {
            include(":${caso.name}-$variante")
            project(":${caso.name}-$variante").projectDir = pasta
        }
    }
}
