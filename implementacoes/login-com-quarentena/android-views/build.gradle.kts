plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "tcc.logincomquarentena.views"
    defaultConfig.applicationId = "tcc.logincomquarentena.views"
}

dependencies {
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
}
