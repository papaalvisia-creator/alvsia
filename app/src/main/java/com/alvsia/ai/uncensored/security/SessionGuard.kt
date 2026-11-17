package com.alvsia.ai.uncensored.security

import android.os.SystemClock
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.security.KeyStore
import java.security.MessageDigest
import javax.crypto.KeyGenerator
import javax.crypto.Mac
import javax.crypto.SecretKey
import javax.crypto.spec.SecretKeySpec

/**
 * Process-bound session integrity gate.
 *
 * The panel remains authoritative for license validity and revocation. This
 * local guard only detects stale or modified in-process session state.
 */
class SessionGuard {
    private var tokenDigest: ByteArray? = null
    private var mac: ByteArray? = null
    private var startedAtElapsed: Long = 0L
    private var fallbackKey: SecretKey? = null

    @Synchronized
    fun activate(sessionToken: String) {
        require(sessionToken.matches(Regex("^[0-9a-fA-F]{64}$"))) {
            "Invalid panel session token"
        }
        clear()
        val digest = MessageDigest.getInstance("SHA-256")
            .digest(sessionToken.toByteArray(Charsets.UTF_8))
        tokenDigest = digest
        mac = compute(digest)
        startedAtElapsed = SystemClock.elapsedRealtime()
    }

    @Synchronized
    fun isActive(): Boolean {
        val digest = tokenDigest ?: return false
        val expectedMac = mac ?: return false
        val age = SystemClock.elapsedRealtime() - startedAtElapsed
        if (age < 0L || age > SESSION_TTL_MS) return false
        return runCatching {
            MessageDigest.isEqual(expectedMac, compute(digest))
        }.getOrDefault(false)
    }

    @Synchronized
    fun clear() {
        tokenDigest?.fill(0)
        mac?.fill(0)
        tokenDigest = null
        mac = null
        startedAtElapsed = 0L
    }

    private fun compute(data: ByteArray): ByteArray {
        val hmac = Mac.getInstance("HmacSHA256")
        hmac.init(key())
        return hmac.doFinal(data)
    }

    private fun key(): SecretKey = runCatching {
        val store = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        (store.getKey(KEY_ALIAS, null) as? SecretKey) ?: run {
            val generator = KeyGenerator.getInstance(
                KeyProperties.KEY_ALGORITHM_HMAC_SHA256,
                "AndroidKeyStore"
            )
            generator.init(
                KeyGenParameterSpec.Builder(
                    KEY_ALIAS,
                    KeyProperties.PURPOSE_SIGN or KeyProperties.PURPOSE_VERIFY
                )
                    .setKeySize(256)
                    .setDigests(KeyProperties.DIGEST_SHA256)
                    .build()
            )
            generator.generateKey()
        }
    }.getOrElse {
        // One process-only fallback key; never regenerate between activate/isActive.
        fallbackKey ?: SecretKeySpec(
            ByteArray(32).also(java.security.SecureRandom()::nextBytes),
            "HmacSHA256"
        ).also { fallbackKey = it }
    }

    private companion object {
        const val KEY_ALIAS = "alvsia.ai.session.hmac.v1"
        const val SESSION_TTL_MS = 8L * 60L * 60L * 1000L
    }
}
