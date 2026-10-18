plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "tcc.dadosaovivo.views"
    defaultConfig.applicationId = "tcc.dadosaovivo.views"
}

dependencies {
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
}
