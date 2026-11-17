package com.alvsia.ai.uncensored

import com.alvsia.ai.uncensored.security.HttpBodyGuard
import okhttp3.CertificatePinner
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONArray
import java.util.concurrent.TimeUnit

class ModelCatalogRepository(private val baseUrl: String) {
    private val client = OkHttpClient.Builder()
        .certificatePinner(CertificatePinner.Builder()
            .add("alvsiapanel.unaux.com", "sha256/84+S6cn1vo+IjlQMR5mvqIe5XKMPh28WV9xYVtFKTkk=")
            .build())
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(20, TimeUnit.SECONDS)
        .callTimeout(25, TimeUnit.SECONDS)
        .build()

    fun load(): List<AiModel> {
        return runCatching {
            require(baseUrl.startsWith("https://")) { "Model catalog must use HTTPS" }
            val request = Request.Builder()
                .url(baseUrl.trimEnd('/') + "/api/ai/models")
                .header("Accept", "application/json")
                .get()
                .build()

            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) error("model catalog HTTP ${response.code}")
                val root = JSONArray(
                    HttpBodyGuard.readUtf8(response.body, MAX_RESPONSE_BYTES)
                )
                require(root.length() <= MAX_MODELS) {
                    "Model catalog contains too many entries"
                }

                buildList {
                    for (i in 0 until root.length()) {
                        val item = root.getJSONObject(i)
                        val id = item.getString("id")
                        require(id.length in 1..MAX_ID_LENGTH)
                        require(id.matches(Regex("^[A-Za-z0-9._:/-]+$")))

                        val name = item.optString("name", id).take(MAX_NAME_LENGTH)
                        val provider = item.optString("provider", "ALVSIA").take(MAX_PROVIDER_LENGTH)
                        val family = item.optString("family", "unknown").take(MAX_FAMILY_LENGTH)
                        val tagsJson = item.optJSONArray("tags")
                        require(tagsJson == null || tagsJson.length() <= MAX_TAGS)

                        add(
                            AiModel(
                                id = id,
                                name = name,
                                provider = provider,
                                family = family,
                                tags = buildList {
                                    if (tagsJson != null) {
                                        for (j in 0 until tagsJson.length()) {
                                            add(tagsJson.getString(j).take(MAX_TAG_LENGTH))
                                        }
                                    }
                                },
                                sourceUrl = item.optString("sourceUrl", "").take(MAX_URL_LENGTH),
                                licenseUrl = item.optString("licenseUrl", "").take(MAX_URL_LENGTH),
                                remote = true
                            )
                        )
                    }
                }
            }
        }.getOrElse { ModelCatalog.starter }
    }

    private companion object {
        const val MAX_RESPONSE_BYTES = 1 * 1024 * 1024
        const val MAX_MODELS = 200
        const val MAX_ID_LENGTH = 160
        const val MAX_NAME_LENGTH = 160
        const val MAX_PROVIDER_LENGTH = 80
        const val MAX_FAMILY_LENGTH = 80
        const val MAX_TAGS = 24
        const val MAX_TAG_LENGTH = 48
        const val MAX_URL_LENGTH = 512
    }
}
