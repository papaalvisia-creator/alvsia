package com.alvsia.ai.uncensored

import android.app.Application
import app.talsec.rasp.security.api.SuspiciousAppInfo
import app.talsec.rasp.security.api.Talsec
import app.talsec.rasp.security.api.TalsecConfig
import app.talsec.rasp.security.api.ThreatListener
import com.alvsia.ai.uncensored.security.ThreatReporter

/**
 * Starts freeRASP in the background. Signals are telemetry-only at this stage:
 * legitimate rooted/developer devices must not lose AI access because of a low-confidence
 * environment signal.
 */
class AlvsiaApplication : Application() {
    private val threatListener = object : ThreatListener.ThreatDetected() {
        override fun onPrivilegedAccess() = report("privileged_access")
        override fun onDebug() = report("debugger_detected")
        override fun onSimulator() = report("simulator_detected")
        override fun onAppIntegrity() = report("app_integrity")
        override fun onUnofficialStore() = report("unofficial_install_source")
        override fun onHooks() = report("hook_framework")
        override fun onDeviceBinding() = report("device_binding")
        override fun onObfuscationIssues() = report("obfuscation_issue")
        override fun onAutomation() = report("automation_detected")
        override fun onBootloader() = report("bootloader_unlocked")
        override fun onMalware(suspiciousApps: List<SuspiciousAppInfo>) {
            report("malware_detected_count_${suspiciousApps.size}")
        }
    }

    override fun onCreate() {
        super.onCreate()
        runCatching {
            val config = TalsecConfig.Builder(
                EXPECTED_PACKAGE_NAME,
                EXPECTED_SIGNING_CERTIFICATE_HASH_BASE64
            )
                .prod(!BuildConfig.DEBUG)
                .killOnBypass(false)
                .build()
            ThreatListener(threatListener).registerListener(this)
            Talsec.start(this, config)
        }.onFailure {
            // RASP initialization must never crash login or AI chat.
            report("rasp_initialization_unavailable")
        }
    }

    private fun report(signal: String) {
        ThreatReporter.report("FREERASP", listOf(signal))
    }

    private companion object {
        const val EXPECTED_PACKAGE_NAME = "com.alvsia.ai.uncensored"
        val EXPECTED_SIGNING_CERTIFICATE_HASH_BASE64 = arrayOf(
            "mbM4FciKF6u8/iK+FSUDY/bfx5wR/8mA5xtit0sfKVw="
        )
    }
}
