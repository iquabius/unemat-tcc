plugins {
    alias(libs.plugins.javafx)
}

javafx {
    version = libs.versions.javafx.get()
    modules("javafx.controls", "javafx.fxml")
}

application {
    mainClass = "tcc.formulario.fxml.Main"
}
