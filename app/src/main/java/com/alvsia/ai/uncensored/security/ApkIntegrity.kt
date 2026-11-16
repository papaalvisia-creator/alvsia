package com.alvsia.ai.uncensored.security

import com.alvsia.ai.uncensored.BuildConfig

import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import java.io.File
import java.security.MessageDigest
import java.util.zip.ZipFile

data class ApkIntegrityReport(val valid: Boolean, val reasons: List<String>, val signerSha256: String?)

object ApkIntegrity {
    fun inspect(context: Context): ApkIntegrityReport {
        val reasons = mutableListOf<String>()
        if (context.packageName != "com.alvsia.ai.uncensored") reasons += "package_identity_mismatch"
        runCatching {
            val info = context.packageManager.getApplicationInfo(context.packageName, 0)
            if (info.flags and android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE != 0 && !BuildConfig.DEBUG) reasons += "release_debuggable"
            val apk = File(info.sourceDir)
            if (!apk.isFile || apk.length() !in 1_000_000L..150_000_000L) reasons += "apk_size_invalid"
            ZipFile(apk).use { zip ->
                val dex = zip.entries().asSequence().filter { it.name.matches(Regex("classes(\\d+)?\\.dex")) }.toList()
                if (dex.isEmpty() || dex.size > 32) reasons += "dex_inventory_invalid"
                if (zip.getEntry("AndroidManifest.xml") == null) reasons += "manifest_missing"
            }
        }.onFailure { reasons += "apk_inspection_failed" }
        val signer = signerSha256(context)
        val expected = BuildConfig.CERT_SHA256
        if (expected.isNotBlank() && signer != null && !signer.equals(expected, true)) reasons += "signer_mismatch"
        if (signer == null) reasons += "signer_unreadable"
        return ApkIntegrityReport(reasons.isEmpty(), reasons, signer)
    }

    private fun signerSha256(context: Context): String? = runCatching {
        val bytes = if (Build.VERSION.SDK_INT >= 28) {
            val pi = context.packageManager.getPackageInfo(context.packageName, PackageManager.GET_SIGNING_CERTIFICATES)
            val si = pi.signingInfo ?: error("no_signing_info")
            (if (si.hasMultipleSigners()) si.apkContentsSigners else si.signingCertificateHistory).first().toByteArray()
        } else {
            @Suppress("DEPRECATION")
            context.packageManager.getPackageInfo(context.packageName, PackageManager.GET_SIGNATURES).signatures?.firstOrNull()?.toByteArray() ?: error("no_legacy_signer")
        }
        MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it) }
    }.getOrNull()
}