pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
        maven { url = uri("https://europe-west3-maven.pkg.dev/talsec-artifact-repository/plugin") }
    }
}
dependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories {
        google()
        mavenCentral()
        maven { url = uri("https://europe-west3-maven.pkg.dev/talsec-artifact-repository/common") }
        maven { url = uri("https://europe-west3-maven.pkg.dev/talsec-artifact-repository/freerasp") }
    } }
rootProject.name = "ALVSIA-AI-UNCENSORED"
include(":app")
