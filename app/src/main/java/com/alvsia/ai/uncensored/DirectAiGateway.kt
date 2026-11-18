package com.alvsia.ai.uncensored

import com.alvsia.ai.uncensored.security.HttpBodyGuard
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.nio.charset.StandardCharsets
import java.util.concurrent.TimeUnit

class DirectAiGateway {
    private val client = OkHttpClient.Builder()
        .connectTimeout(20, TimeUnit.SECONDS)
        .readTimeout(120, TimeUnit.SECONDS)
        .callTimeout(150, TimeUnit.SECONDS)
        .retryOnConnectionFailure(true)
        .build()

    fun chat(model: AiModel, message: String, apiKey: String, endpoint: String): Result<String> = runCatching {
        require(endpoint.startsWith("https://")) { "AI endpoint harus memakai HTTPS." }
        require(message.toByteArray(StandardCharsets.UTF_8).size <= MAX_REQUEST_BYTES) {
            "Pesan terlalu besar. Batas permintaan adalah 1 MiB."
        }

        val payload = JSONObject().apply {
            put("model", model.id)
            put("messages", JSONArray().put(JSONObject().apply {
                put("role", "user")
                put("content", message)
            }))
        }.toString()

        val request = Request.Builder()
            .url(endpoint.trimEnd('/'))
            .post(payload.toRequestBody("application/json".toMediaType()))
            .header("Accept", "application/json")
            .header("Content-Type", "application/json")
            .header("User-Agent", "ALVSIA-AI/0.5.0")
            .apply {
                if (apiKey.isNotBlank()) header("Authorization", "Bearer ${apiKey.trim()}")
            }
            .build()

        client.newCall(request).execute().use { response ->
            val body = HttpBodyGuard.readUtf8(response.body, MAX_RESPONSE_BYTES)
            if (!response.isSuccessful) {
                error("AI service HTTP ${response.code}: ${body.take(300)}")
            }
            val json = runCatching { JSONObject(body) }.getOrElse {
                error("Format respons AI tidak valid.")
            }
            val choices = json.optJSONArray("choices")
            val content = choices?.optJSONObject(0)
                ?.optJSONObject("message")
                ?.optString("content")
                ?.takeIf { it.isNotBlank() }
                ?: json.optString("answer").takeIf { it.isNotBlank() }
                ?: json.optString("response").takeIf { it.isNotBlank() }
                ?: json.optString("output").takeIf { it.isNotBlank() }
            content ?: error("Respons AI tidak berisi teks jawaban.")
        }
    }

    companion object {
        const val DEFAULT_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
        private const val MAX_REQUEST_BYTES = 1 * 1024 * 1024
        private const val MAX_RESPONSE_BYTES = 4 * 1024 * 1024
    }
}
