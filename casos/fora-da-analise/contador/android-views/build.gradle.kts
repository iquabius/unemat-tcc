plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "tcc.contador.views"
    defaultConfig.applicationId = "tcc.contador.views"
}

dependencies {
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
}
