package com.alvsia.ai.uncensored

import android.content.Context

class SecurePrefs(context: Context) {
    private val prefs = context.getSharedPreferences("alvsia_ai_session", Context.MODE_PRIVATE)

    fun token(): String? = prefs.getString("session_token", null)
    fun setToken(value: String?) = prefs.edit().putString("session_token", value).apply()

    fun modelId(): String = prefs.getString("model_id", ModelCatalog.starter.first().id)
        ?: ModelCatalog.starter.first().id

    fun setModelId(value: String) = prefs.edit().putString("model_id", value).apply()
}
