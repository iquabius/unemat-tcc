// Projeto Gradle único dos casos Android. Cada tecnologia de cada caso é um
// módulo em casos/<caso>/android-<tecnologia>/, ao lado das implementações
// web, e se chama :<caso>-android-<tecnologia> (por exemplo,
// :contador-android-compose).
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
    listOf("android-views", "android-compose").forEach { subpasta ->
        val pasta = caso.resolve(subpasta)
        if (pasta.resolve("build.gradle.kts").exists()) {
            include(":${caso.name}-$subpasta")
            project(":${caso.name}-$subpasta").projectDir = pasta
        }
    }
}
