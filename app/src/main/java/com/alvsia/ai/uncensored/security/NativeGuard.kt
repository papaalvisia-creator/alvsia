package com.alvsia.ai.uncensored.security

import java.io.File

/** Native RASP bridge ported from ALVSIA SMART TOOL; no Smart Tool keys or payload seeds are copied. */
object NativeGuard {
    @Volatile private var loaded = false
    init { try { System.loadLibrary("rasp_guard"); loaded = true } catch (_: Throwable) { loaded = false } }

    private external fun nativeScanFlags(): Int
    private external fun nativeWipe(buf: ByteArray)
    private external fun nativeAntiDump(): Int
    private external fun nativeSealSeed(): ByteArray?
    private external fun nativeSealBuildId(): String?
    private external fun nativeVmFlags(): Int

    fun isLoaded() = loaded
    fun scanFlags(): Int = if (loaded) runCatching { nativeScanFlags() }.getOrElse { fallbackFlags() } else fallbackFlags()
    fun antiDump(): Int = if (loaded) runCatching { nativeAntiDump() }.getOrDefault(0) else 0
    fun vmFlags(): Int = if (loaded) runCatching { nativeVmFlags() }.getOrDefault(-1) else -1
    fun wipe(bytes: ByteArray) { if (loaded) runCatching { nativeWipe(bytes) }.onFailure { bytes.fill(0) } else bytes.fill(0) }

    private fun fallbackFlags(): Int {
        var flags = 0
        runCatching {
            val status = File("/proc/self/status").readText()
            val pid = status.lineSequence().firstOrNull { it.startsWith("TracerPid:") }?.substringAfter(":")?.trim()?.toIntOrNull() ?: 0
            if (pid > 0) flags = flags or 1
        }
        runCatching {
            File("/proc/self/maps").forEachLine { line ->
                val fields = line.trim().split(Regex("\\s+"), limit = 6)
                if (fields.size >= 2 && 'x' in fields[1]) {
                    val name = fields.getOrNull(5)?.lowercase().orEmpty()
                    if (listOf("frida-agent","frida-gadget","libfrida","libgadget","linjector").any { it in name }) flags = flags or 2
                }
            }
        }
        return flags
    }

    fun reasons(flags: Int): List<String> = buildList {
        if (flags and 1 != 0) add("tracer_pid")
        if (flags and 2 != 0) add("active_instrumentation_map")
        if (flags and 0x40 != 0) add("native_integrity_mismatch")
        if (flags and 0x100 != 0) add("ptrace_wchan")
        if (flags and 0x200 != 0) add("late_hook_library")
        if (flags and 0x400 != 0) add("jni_prologue")
        if (flags and 0x800 != 0) add("active_instrumentation_artifact")
    }
}