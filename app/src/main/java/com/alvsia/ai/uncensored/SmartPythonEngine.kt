package com.alvsia.ai.uncensored

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import org.json.JSONObject
import java.io.File

object SmartPythonEngine {
    @Volatile private var started = false

    private fun start(context: Context) {
        if (!started) synchronized(this) {
            if (!started) {
                if (!Python.isStarted()) Python.start(AndroidPlatform(context.applicationContext))
                started = true
            }
        }
    }

    fun analyze(context: Context, input: File, operation: String = "analyze"): JSONObject {
        start(context)
        val py = Python.getInstance().getModule("smart_bridge")
        val value = py.callAttr("run", input.absolutePath, operation)
        return JSONObject(value.toString())
    }
}
