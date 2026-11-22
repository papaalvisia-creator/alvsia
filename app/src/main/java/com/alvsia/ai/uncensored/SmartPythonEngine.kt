package com.alvsia.ai.uncensored

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import org.json.JSONObject
import java.io.File

object SmartPythonEngine {
    @Volatile private var started = false
    @Synchronized private fun ensure(context: Context) {
        if (!started) {
            if (!Python.isStarted()) Python.start(AndroidPlatform(context.applicationContext))
            started = true
        }
    }

    fun run(context: Context, input: File, operation: String = "analyze", output: File? = null, args: Map<String, Any?> = emptyMap()): JSONObject {
        ensure(context)
        val py = Python.getInstance()
        val bridge = py.getModule("smart_bridge")
        val kwargs = HashMap<String, Any?>()
        kwargs.putAll(args)
        if (output != null) kwargs["output"] = output.absolutePath
        val result = bridge.callAttr("run", input.absolutePath, operation, output?.absolutePath, kwargs)
        return JSONObject(result.toString())
    }

    fun selfTest(context: Context): JSONObject {
        ensure(context)
        val py = Python.getInstance()
        return JSONObject(py.getModule("smart_bridge").callAttr("self_test").toString())
    }
}
