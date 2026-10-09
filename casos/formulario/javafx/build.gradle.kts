plugins {
    alias(libs.plugins.javafx)
}

javafx {
    version = libs.versions.javafx.get()
    modules("javafx.controls")
}

application {
    mainClass = "tcc.formulario.javafx.Main"
}
