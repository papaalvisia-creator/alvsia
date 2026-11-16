# ALVSIA AI release hardening: allow R8 to obfuscate application code.
# Keep only externally required Android/Compose entry points; no blanket app keep rule.
-dontwarn okhttp3.**
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
}
-repackageclasses 'alvsia.obf'
-allowaccessmodification
-optimizationpasses 5
-optimizations !code/simplification/arithmetic,!field/*,!class/merging/*
