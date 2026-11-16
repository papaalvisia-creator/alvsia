package com.alvsia.ai.uncensored.security

import android.util.Log

/** Local, privacy-preserving security event adapter. Never logs tokens, licenses, HWIDs or file paths. */
object ThreatReporter {
    private val sensitive = Regex("(?i)(token|password|license|hwid|api[_-]?key)\\s*[:=]\\s*[^\\s,;]+")
    fun report(kind: String, details: List<String>) {
        val safe = details.joinToString(",").replace(sensitive, "$1=[REDACTED]").take(800)
        Log.w("ALVSIA_SECURITY", "${kind.take(48)}:$safe")
    }
}