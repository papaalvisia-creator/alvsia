package com.alvsia.ai.uncensored

import com.alvsia.ai.uncensored.security.HttpBodyGuard
import okhttp3.CertificatePinner
import okhttp3.Cookie
import okhttp3.CookieJar
import okhttp3.HttpUrl
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.ResponseBody.Companion.toResponseBody
import org.json.JSONObject
import java.nio.charset.StandardCharsets
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.TimeUnit
import javax.crypto.Cipher
import javax.crypto.spec.IvParameterSpec
import javax.crypto.spec.SecretKeySpec
import android.util.Base64

class AiGateway(private val baseUrl: String) {
    private val cookieStore = ConcurrentHashMap<String, MutableList<Cookie>>()
    private val jar = object : CookieJar {
        override fun saveFromResponse(url: HttpUrl, cookies: List<Cookie>) {
            val list = cookieStore.getOrPut(url.host) { mutableListOf() }
            synchronized(list) {
                cookies.forEach { cookie ->
                    list.removeAll { it.name == cookie.name }
                    list.add(cookie)
                }
            }
        }
        override fun loadForRequest(url: HttpUrl): List<Cookie> {
            val list = cookieStore[url.host] ?: return emptyList()
            synchronized(list) { return list.filter { it.matches(url) } }
        }
    }

    private val client = OkHttpClient.Builder()
        .cookieJar(jar)
        .certificatePinner(CertificatePinner.Builder()
            .add("alvsiapanel.unaux.com", "sha256/84+S6cn1vo+IjlQMR5mvqIe5XKMPh28WV9xYVtFKTkk=")
            .build())
        .connectTimeout(20, TimeUnit.SECONDS)
        .readTimeout(120, TimeUnit.SECONDS)
        .callTimeout(150, TimeUnit.SECONDS)
        .followRedirects(false)
        .followSslRedirects(false)
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
            .header("User-Agent", "ALVSIA-PRO/5.5.2 (Android)")
            .header("Accept-Language", "en-US,en;q=0.9")
            .header("X-ALVSIA-App", "ALVSIA_AI_UNCENSORED")
            .header("X-ALVSIA-HWID", hwid)
            .apply {
                if (!token.isNullOrBlank()) {
                    header("Authorization", "Bearer $token")
                    // Some shared-host PHP/FastCGI stacks strip Authorization; send a scoped fallback header too.
                    header("X-ALVSIA-Session", token)
                }
            }
            .build()

        executeWithHostingGate(request).use { response ->
            val responseText = HttpBodyGuard.readUtf8(response.body, MAX_RESPONSE_BYTES)
            if (!response.isSuccessful) {
                val detail = if (responseText.trimStart().startsWith("<")) {
                    "server mengembalikan halaman web (HTTP " + response.code + "); periksa rute chat.php dan proteksi hosting"
                } else {
                    responseText.take(240)
                }
                error("AI service HTTP " + response.code + ": " + detail)
            }
            if (responseText.trimStart().startsWith("<") || responseText.contains("<html", true)) {
                error("Gateway Unaux masih mengirim halaman HTML setelah handshake hosting. Periksa apakah chat.php terpasang di /htdocs/api/ai/.")
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

    private fun executeWithHostingGate(request: Request): Response {
        val first = client.newCall(request).execute()
        val firstContentType = first.body?.contentType()
        val firstText = first.body?.string().orEmpty()
        if (firstText.contains("slowAES", ignoreCase = true) ||
            firstText.contains("__test", ignoreCase = true)) {
            if (solveTestCookie(firstText, request.url)) {
                first.close()
                return client.newCall(request).execute()
            }
        }
        return first.newBuilder()
            .body(firstText.toResponseBody(firstContentType))
            .build()
    }

    private fun solveTestCookie(html: String, requestUrl: HttpUrl): Boolean {
        return try {
            val regex = Regex("""a=toNumbers\("([0-9a-f]+)"\),b=toNumbers\("([0-9a-f]+)"\),c=toNumbers\("([0-9a-f]+)"\)""")
            val match = regex.find(html) ?: return false
            val key = hexToBytes(match.groupValues[1])
            val iv = hexToBytes(match.groupValues[2])
            val ciphertext = hexToBytes(match.groupValues[3])
            val cipher = Cipher.getInstance("AES/CBC/NoPadding")
            cipher.init(Cipher.DECRYPT_MODE, SecretKeySpec(key, "AES"), IvParameterSpec(iv))
            val cookieValue = cipher.doFinal(ciphertext).joinToString("") { "%02x".format(it) }
            val cookie = Cookie.Builder()
                .name("__test")
                .value(cookieValue)
                .domain(requestUrl.host)
                .path("/")
                .expiresAt(System.currentTimeMillis() + 6L * 60L * 60L * 1000L)
                .build()
            jar.saveFromResponse(requestUrl, listOf(cookie))
            true
        } catch (_: Exception) {
            false
        }
    }

    private fun hexToBytes(value: String): ByteArray {
        val normalized = if (value.length % 2 == 0) value else "0$value"
        return ByteArray(normalized.length / 2) { i ->
            normalized.substring(i * 2, i * 2 + 2).toInt(16).toByte()
        }
    }

    private companion object {
        const val MAX_REQUEST_BYTES = 1 * 1024 * 1024
        const val MAX_RESPONSE_BYTES = 4 * 1024 * 1024
    }
}
