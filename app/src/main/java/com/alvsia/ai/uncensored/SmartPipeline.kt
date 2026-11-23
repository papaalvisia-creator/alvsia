package com.alvsia.ai.uncensored

import android.content.Context
import android.net.Uri
import org.json.JSONObject

enum class SmartOperation { ANALYZE, LUA_DECOMPILE, PAK_EXTRACT, PAK_REPACK, BATCH_AUDIT }

data class SmartCapability(val operation: SmartOperation, val available: Boolean, val reason: String)

data class SmartPipelineReport(
    val fileName: String,
    val size: Long,
    val sha256: String,
    val type: String,
    val capabilities: List<SmartCapability>,
    val diagnostics: List<String>
)

object SmartPipeline {
    fun run(context: Context, uri: Uri): SmartPipelineReport {
        val r: JSONObject = SmartPythonEngine.run(context, SmartToolEngine.materialize(context, uri), "analyze")
        val type = r.optString("type", "BINARY")
        val caps = when (type) {
            "LUA", "LUAJIT" -> listOf(
                SmartCapability(SmartOperation.LUA_DECOMPILE, true, "Python Lua pipeline"),
                SmartCapability(SmartOperation.BATCH_AUDIT, true, "Streaming analysis")
            )
            "UE4_PAK" -> listOf(
                SmartCapability(SmartOperation.PAK_EXTRACT, true, "Tencent/UE4 PAK core"),
                SmartCapability(SmartOperation.PAK_REPACK, true, "Template-preserving writer")
            )
            else -> listOf(SmartCapability(SmartOperation.ANALYZE, true, "Generic analysis"))
        }
        return SmartPipelineReport(
            r.optString("name", "input"),
            r.optLong("size", -1L),
            r.optString("sha256", ""),
            type,
            caps,
            listOf(r.optString("detail", "Analysis complete"))
        )
    }
}
