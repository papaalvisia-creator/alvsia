-keep class com.alvsia.ai.uncensored.** { *; }
-dontwarn okhttp3.**
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
}
