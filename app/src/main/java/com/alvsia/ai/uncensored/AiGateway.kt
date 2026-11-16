package com.alvsia.ai.uncensored

import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.concurrent.TimeUnit

class AiGateway(private val baseUrl: String) {
    private val client = OkHttpClient.Builder()
        .connectTimeout(20, TimeUnit.SECONDS)
        .readTimeout(120, TimeUnit.SECONDS)
        .build()

    fun chat(model: AiModel, message: String, token: String?): Result<String> = runCatching {
        val body = JSONObject().apply {
            put("model", model.id)
            put("message", message)
            put("provider", model.provider)
            put("app", "ALVSIA_AI_UNCENSORED")
        }.toString().toRequestBody("application/json".toMediaType())

        val request = Request.Builder()
            .url(baseUrl.trimEnd('/') + "/api/ai/chat")
            .post(body)
            .header("Accept", "application/json")
            .apply { if (!token.isNullOrBlank()) header("Authorization", "Bearer $token") }
            .build()

        client.newCall(request).execute().use { response ->
            val text = response.body?.string().orEmpty()
            if (!response.isSuccessful) error("AI gateway HTTP ${response.code}: ${text.take(500)}")
            val json = JSONObject(text)
            json.optString("message", json.optString("content", text))
        }
    }
}
