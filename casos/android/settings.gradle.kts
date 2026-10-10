// Projeto Gradle único dos casos Android. Cada caso e tecnologia é um módulo
// em casos/<caso>/<tecnologia>/, ao lado das implementações web, e se chama
// :<caso>-<tecnologia> (por exemplo, :contador-android-compose).
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
    listOf("android-views", "android-compose").forEach { tecnologia ->
        val pasta = caso.resolve(tecnologia)
        if (pasta.resolve("build.gradle.kts").exists()) {
            include(":${caso.name}-$tecnologia")
            project(":${caso.name}-$tecnologia").projectDir = pasta
        }
    }
}
