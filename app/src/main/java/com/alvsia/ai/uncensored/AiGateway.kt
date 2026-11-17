package com.alvsia.ai.uncensored

import com.alvsia.ai.uncensored.security.HttpBodyGuard
import okhttp3.CertificatePinner
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.nio.charset.StandardCharsets
import java.util.concurrent.TimeUnit

class AiGateway(private val baseUrl: String) {
    private val client = OkHttpClient.Builder()
        .certificatePinner(CertificatePinner.Builder()
            .add("alvsiapanel.unaux.com", "sha256/84+S6cn1vo+IjlQMR5mvqIe5XKMPh28WV9xYVtFKTkk=")
            .build())
        .connectTimeout(20, TimeUnit.SECONDS)
        .readTimeout(120, TimeUnit.SECONDS)
        .callTimeout(150, TimeUnit.SECONDS)
        .retryOnConnectionFailure(false)
        .build()

    fun chat(model: AiModel, message: String, token: String?, hwid: String): Result<String> = runCatching {
        require(baseUrl.startsWith("https://")) { "AI gateway must use HTTPS" }
        require(message.toByteArray(StandardCharsets.UTF_8).size <= MAX_REQUEST_BYTES) {
            "Pesan terlalu besar. Batas permintaan adalah 1 MiB."
        }

        val body = JSONObject().apply {
            put("model", model.id)
            put("message", message)
            put("provider", "openai-compatible")
            put("hwid", hwid)
            put("app", "ALVSIA_AI_UNCENSORED")
        }.toString().toRequestBody("application/json".toMediaType())

        val request = Request.Builder()
            .url(baseUrl.trimEnd('/') + "/api/ai/chat.php")
            .post(body)
            .header("Accept", "application/json")
            .header("User-Agent", "ALVSIA-AI-UNCENSORED")
            .header("X-ALVSIA-App", "ALVSIA_AI_UNCENSORED")
            .header("X-ALVSIA-HWID", hwid)
            .apply { if (!token.isNullOrBlank()) header("Authorization", "Bearer $token") }
            .build()

        client.newCall(request).execute().use { response ->
            val responseText = HttpBodyGuard.readUtf8(response.body, MAX_RESPONSE_BYTES)
            if (!response.isSuccessful) {
                val detail = if (responseText.trimStart().startsWith("<")) {
                    "server mengembalikan halaman web"
                } else {
                    responseText.take(240)
                }
                error("AI service HTTP ${response.code}: $detail")
            }
            if (responseText.trimStart().startsWith("<") || responseText.contains("<html", true)) {
                error("AI service belum tersedia: endpoint /api/ai/chat mengembalikan HTML, bukan JSON. Backend AI perlu dipasang pada gateway Unaux.")
            }
            val json = runCatching { JSONObject(responseText) }.getOrElse {
                error("Format respons AI tidak valid (bukan JSON).")
            }
            val direct = listOf("answer", "message", "content", "response", "output")
                .firstNotNullOfOrNull { key ->
                    json.optString(key).takeIf { it.isNotBlank() && it != "null" }
                }
            if (direct != null) return@use direct

            val choices = json.optJSONArray("choices")
            val first = choices?.optJSONObject(0)
            val openAiContent = first?.optJSONObject("message")?.optString("content")
                ?: first?.optString("text")
            if (!openAiContent.isNullOrBlank()) return@use openAiContent
            error("Respons AI diterima tetapi tidak berisi teks jawaban yang dikenali.")
        }
    }

    private companion object {
        const val MAX_REQUEST_BYTES = 1 * 1024 * 1024
        const val MAX_RESPONSE_BYTES = 4 * 1024 * 1024
    }
}
