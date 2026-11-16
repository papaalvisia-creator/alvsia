package com.alvsia.ai.uncensored

import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONArray
import java.util.concurrent.TimeUnit

class ModelCatalogRepository(private val baseUrl: String) {
    private val client = OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(20, TimeUnit.SECONDS)
        .build()

    fun load(): List<AiModel> {
        return runCatching {
            val request = Request.Builder()
                .url(baseUrl.trimEnd('/') + "/api/ai/models")
                .header("Accept", "application/json")
                .get()
                .build()
            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) error("model catalog HTTP ${response.code}")
                val root = JSONArray(response.body?.string().orEmpty())
                buildList {
                    for (i in 0 until root.length()) {
                        val item = root.getJSONObject(i)
                        add(
                            AiModel(
                                id = item.getString("id"),
                                name = item.optString("name", item.getString("id")),
                                provider = item.optString("provider", "ALVSIA"),
                                family = item.optString("family", "unknown"),
                                tags = buildList {
                                    val tags = item.optJSONArray("tags")
                                    if (tags != null) for (j in 0 until tags.length()) add(tags.getString(j))
                                },
                                sourceUrl = item.optString("sourceUrl", ""),
                                licenseUrl = item.optString("licenseUrl", ""),
                                remote = true
                            )
                        )
                    }
                }
            }
        }.getOrElse { ModelCatalog.starter }
    }
}
