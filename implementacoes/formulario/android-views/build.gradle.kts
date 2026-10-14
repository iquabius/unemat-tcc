plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "tcc.formulario.views"
    defaultConfig.applicationId = "tcc.formulario.views"
}

dependencies {
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
}
