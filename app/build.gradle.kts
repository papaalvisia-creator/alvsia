plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.plugin.compose")
    id("app.talsec.plugin")
}

android {
    namespace = "com.alvsia.ai.uncensored"
    compileSdk = 37
    ndkVersion = "27.0.12077973"

    defaultConfig {
        applicationId = "com.alvsia.ai.uncensored"
        minSdk = 26
        targetSdk = 37
        versionCode = 3
        versionName = "0.3.0"
        buildConfigField("String", "CERT_SHA256", "\"99b33815c88a17abbcfe22be15250363f6dfc79c11ffc980e71b62b74b1f295c\"")
        ndk { abiFilters += listOf("arm64-v8a") }
    }

    externalNativeBuild { cmake { path = file("src/main/cpp/CMakeLists.txt"); version = "3.22.1" } }

    talsec {
        sdkVersion = "20.0.1"
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    buildTypes {
        debug {
            buildConfigField("String", "PANEL_BASE_URL", "\"https://alvsiapanel.unaux.com\"")
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            buildConfigField("String", "PANEL_BASE_URL", "\"https://alvsiapanel.unaux.com\"")
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2026.09.00")
    implementation(composeBom)
    implementation("androidx.activity:activity-compose:1.13.0")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.11.0")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    debugImplementation("androidx.compose.ui:ui-tooling")
    implementation("androidx.core:core-ktx:1.17.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.11.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.10.2")
    implementation("com.squareup.okhttp3:okhttp:5.1.0")
}
