package com.alvsia.ai.uncensored.security

import com.alvsia.ai.uncensored.BuildConfig

import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import java.io.File

data class SecurityReport(val clean: Boolean, val hardSignals: List<String>, val softSignals: List<String>)

object RuntimeGuard {
    private val hardMarkers = listOf("frida-agent","frida-gadget","frida_agent","frida_gadget","libfrida","libgadget","linjector")
    private val softMarkers = listOf("xposed","lsposed","edxposed","substrate","sandhook","libepic","dobby","shadowhook","bytehook","libwhale","riru","zygisk")

    fun inspect(context: Context): SecurityReport {
        val hard = linkedSetOf<String>()
        val soft = linkedSetOf<String>()
        runCatching {
            val tracer = File("/proc/self/status").readLines().firstOrNull { it.startsWith("TracerPid:") }
                ?.substringAfter(":")?.trim()?.toIntOrNull() ?: 0
            if (tracer > 0) hard += "tracer_pid"
        }
        runCatching {
            File("/proc/self/maps").forEachLine { line ->
                val f = line.trim().split(Regex("\\s+"), limit = 6)
                if (f.size >= 2 && 'x' in f[1]) {
                    val path = f.getOrNull(5)?.lowercase().orEmpty()
                    hardMarkers.filter { it in path }.forEach { hard += "active_map:$it" }
                    softMarkers.filter { it in path }.forEach { soft += "hook_library:$it" }
                }
            }
        }
        val nativeFlags = NativeGuard.scanFlags()
        hard += NativeGuard.reasons(nativeFlags)
        if (!NativeGuard.isLoaded() && !BuildConfig.DEBUG) soft += "native_rasp_unavailable"
        if (Build.TAGS?.contains("test-keys") == true) soft += "test_keys"
        return SecurityReport(hard.isEmpty(), hard.toList(), soft.toList())
    }

    fun knownHookPackages(pm: PackageManager): List<String> {
        val packages = listOf("de.robv.android.xposed.installer","org.lsposed.manager","org.lsposed.lspatch",
            "com.saurik.substrate","com.topjohnwu.magisk","me.weishu.kernelsu","com.frida.console")
        return packages.filter { p -> runCatching { pm.getPackageInfo(p, 0); true }.getOrDefault(false) }
    }
}