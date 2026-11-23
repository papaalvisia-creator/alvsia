plugins {
    id("com.android.application")
    id("com.chaquo.python")
    id("org.jetbrains.kotlin.plugin.compose")
    id("app.talsec.plugin") version "1.1.0"
}

android {
    namespace = "com.alvsia.ai.uncensored"
    compileSdk = 37
    ndkVersion = "27.0.12077973"

    defaultConfig {
        applicationId = "com.alvsia.ai.uncensored"
        minSdk = 26
        targetSdk = 37
        versionCode = 7
        versionName = "0.7.0"
        buildConfigField("String", "CERT_SHA256", "\"99b33815c88a17abbcfe22be15250363f6dfc79c11ffc980e71b62b74b1f295c\"")
        val telegramToken = (System.getenv("ALVSIA_TELEGRAM_BOT_TOKEN") ?: "").replace("\\", "\\\\").replace("\"", "\\\"")
        val telegramChatId = (System.getenv("ALVSIA_TELEGRAM_CHAT_ID") ?: "").replace("\\", "\\\\").replace("\"", "\\\"")
        buildConfigField("String", "TELEGRAM_BOT_TOKEN", "\"$telegramToken\"")
        buildConfigField("String", "TELEGRAM_CHAT_ID", "\"$telegramChatId\"")
        ndk { abiFilters += listOf("arm64-v8a") }
    }

    chaquopy {
        defaultConfig {
            version = "3.13"
            pip {
                install("gmalg==1.1.2")
                install("pycryptodome")
                install("zstandard")
            }
            pyc { src = true }
        }
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
        debug { }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
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
