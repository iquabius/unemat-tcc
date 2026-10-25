plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "tcc.lista.views"
    defaultConfig.applicationId = "tcc.lista.views"
}

dependencies {
    implementation(libs.androidx.appcompat)
    implementation(libs.androidx.recyclerview)
    implementation(libs.material)
}
