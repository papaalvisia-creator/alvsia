package com.alvsia.ai.uncensored.security

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.security.KeyStore
import javax.crypto.KeyGenerator
import javax.crypto.Mac
import javax.crypto.SecretKey
import javax.crypto.spec.SecretKeySpec

/** Process-bound session integrity gate. Panel remains the authority for license validity/revocation. */
class SessionGuard {
    @Volatile private var tokenDigest: ByteArray? = null
    @Volatile private var mac: ByteArray? = null
    @Volatile private var startedAt: Long = 0L
    private val ttlMs = 8L * 60L * 60L * 1000L

    @Synchronized fun activate(sessionToken: String) {
        require(sessionToken.matches(Regex("^[0-9a-fA-F]{64}$"))) { "Invalid panel session token" }
        tokenDigest = java.security.MessageDigest.getInstance("SHA-256").digest(sessionToken.toByteArray())
        mac = compute(tokenDigest!!)
        startedAt = System.currentTimeMillis()
    }

    @Synchronized fun isActive(): Boolean {
        val d = tokenDigest ?: return false
        val m = mac ?: return false
        val age = System.currentTimeMillis() - startedAt
        if (age !in 0..ttlMs) return false
        return java.security.MessageDigest.isEqual(m, compute(d))
    }

    @Synchronized fun clear() { tokenDigest?.fill(0); mac?.fill(0); tokenDigest=null; mac=null; startedAt=0L }

    private fun compute(data: ByteArray): ByteArray {
        val key = key()
        val h = Mac.getInstance("HmacSHA256")
        h.init(key)
        return h.doFinal(data)
    }

    private fun key(): SecretKey = runCatching {
        val ks = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        (ks.getKey("alvsia.ai.session.hmac.v1", null) as? SecretKey) ?: run {
            val gen = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_HMAC_SHA256, "AndroidKeyStore")
            gen.init(KeyGenParameterSpec.Builder("alvsia.ai.session.hmac.v1",
                KeyProperties.PURPOSE_SIGN or KeyProperties.PURPOSE_VERIFY).setKeySize(256)
                .setDigests(KeyProperties.DIGEST_SHA256).build())
            gen.generateKey()
        }
    }.getOrElse {
        // Process-only fallback: still binds the session for this process, but is not hardware-backed.
        SecretKeySpec(ByteArray(32).also(java.security.SecureRandom()::nextBytes), "HmacSHA256")
    }
}