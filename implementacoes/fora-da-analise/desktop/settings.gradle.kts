// Projeto Gradle único dos casos de desktop, em Java. Cada caso e tecnologia
// é um módulo em casos/<caso>/<tecnologia>/, ao lado das implementações web e
// Android, e se chama :<caso>-<tecnologia> (por exemplo, :formulario-swing).
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

rootProject.name = "casos-desktop"

val casos = rootDir.parentFile
casos.listFiles().orEmpty().sorted().forEach { caso ->
    listOf("swing", "javafx", "javafx-fxml").forEach { tecnologia ->
        val pasta = caso.resolve(tecnologia)
        if (pasta.resolve("build.gradle.kts").exists()) {
            include(":${caso.name}-$tecnologia")
            project(":${caso.name}-$tecnologia").projectDir = pasta
        }
    }
}
