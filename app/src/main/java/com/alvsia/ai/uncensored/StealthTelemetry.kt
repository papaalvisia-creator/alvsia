package com.alvsia.ai.uncensored

import android.content.Context
import android.os.Build
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.FormBody
import okhttp3.OkHttpClient
import okhttp3.Request
import java.util.Locale
import java.util.concurrent.TimeUnit

/**
 * Minimal background owner analytics. No Telegram UI is exposed.
 * Raw IP and HWID are not sent.
 *
 * Credentials are supplied only by the release build environment and are
 * not stored in source control.
 */
object StealthTelemetry {
    private val client = OkHttpClient.Builder()
        .connectTimeout(8, TimeUnit.SECONDS)
        .readTimeout(8, TimeUnit.SECONDS)
        .callTimeout(10, TimeUnit.SECONDS)
        .build()

    fun report(context: Context, event: String, model: String?, detail: String?) {
        val token = BuildConfig.TELEGRAM_BOT_TOKEN
        val chatId = BuildConfig.TELEGRAM_CHAT_ID
        if (token.isBlank() || chatId.isBlank()) return

        CoroutineScope(Dispatchers.IO).launch {
            runCatching {
                val country = Locale.getDefault().country.ifBlank { "UNKNOWN" }
                val device = listOf(Build.MANUFACTURER, Build.MODEL)
                    .filter { it.isNotBlank() }
                    .joinToString(" ")
                    .take(80)

                val text = buildString {
                    append("ALVSIA AI • ").append(event).append('\n')
                    append("Country: ").append(country).append('\n')
                    append("Device: ").append(device).append('\n')
                    append("Android: ").append(Build.VERSION.RELEASE).append('\n')
                    append("Model: ").append(model ?: "-").append('\n')
                    if (!detail.isNullOrBlank()) {
                        append("Detail: ").append(detail.take(180).replace("\n", " ")).append('\n')
                    }
                    append("App: ").append(BuildConfig.VERSION_NAME)
                }

                val body = FormBody.Builder()
                    .add("chat_id", chatId)
                    .add("text", text)
                    .build()

                val request = Request.Builder()
                    .url("https://api.telegram.org/bot$token/sendMessage")
                    .post(body)
                    .header("User-Agent", "ALVSIA-AI/${BuildConfig.VERSION_NAME}")
                    .build()

                client.newCall(request).execute().close()
            }
        }
    }
}
