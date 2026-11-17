package com.alvsia.ai.uncensored

import android.content.Context
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.Base64
import java.nio.charset.StandardCharsets
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

/**
 * Stores the panel session token encrypted with an Android Keystore AES-256-GCM key.
 * Version 2 binds ciphertext to this preference purpose using authenticated AAD.
 * Legacy v1 ciphertext remains readable and is migrated on the next token read.
 */
class SecurePrefs(context: Context) {
    private val prefs = context.getSharedPreferences("alvsia_ai_session", Context.MODE_PRIVATE)

    fun token(): String? {
        val stored = prefs.getString("session_token", null) ?: return null
        if (stored.isBlank()) return null

        val decoded = runCatching { decryptStored(stored) }.getOrNull()
        if (decoded == null) {
            clearSession()
            return null
        }

        if (!stored.startsWith(V2_PREFIX)) {
            // Best-effort migration; keep the current session usable if migration
            // cannot complete on this device during this read.
            runCatching { setToken(decoded) }
        }
        return decoded
    }

    fun setToken(value: String?) {
        if (value == null) {
            clearSession()
            return
        }
        prefs.edit().putString("session_token", encrypt(value)).apply()
    }

    fun clearSession() {
        prefs.edit().remove("session_token").apply()
    }

    fun modelId(): String =
        prefs.getString("model_id", ModelCatalog.starter.first().id)
            ?: ModelCatalog.starter.first().id

    fun setModelId(value: String) {
        prefs.edit().putString("model_id", value).apply()
    }

    private fun key(): SecretKey {
        val store = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        val existing = store.getKey(KEY_ALIAS, null)
        if (existing is SecretKey) return existing

        val generator = KeyGenerator.getInstance(
            KeyProperties.KEY_ALGORITHM_AES,
            "AndroidKeyStore"
        )
        generator.init(
            KeyGenParameterSpec.Builder(
                KEY_ALIAS,
                KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
            )
                .setKeySize(256)
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .setRandomizedEncryptionRequired(true)
                .build()
        )
        return generator.generateKey()
    }

    private fun encrypt(value: String): String {
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.ENCRYPT_MODE, key())
        cipher.updateAAD(AAD)
        val encrypted = cipher.doFinal(value.toByteArray(StandardCharsets.UTF_8))
        return V2_PREFIX + Base64.encodeToString(
            cipher.iv + encrypted,
            Base64.NO_WRAP
        )
    }

    private fun decryptStored(value: String): String {
        val isV2 = value.startsWith(V2_PREFIX)
        val encoded = if (isV2) value.removePrefix(V2_PREFIX) else value
        val raw = Base64.decode(encoded, Base64.NO_WRAP)
        require(raw.size > GCM_IV_LENGTH + GCM_TAG_LENGTH_BYTES)

        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(
            Cipher.DECRYPT_MODE,
            key(),
            GCMParameterSpec(
                GCM_TAG_LENGTH_BITS,
                raw.copyOfRange(0, GCM_IV_LENGTH)
            )
        )
        if (isV2) cipher.updateAAD(AAD)
        val plain = cipher.doFinal(raw.copyOfRange(GCM_IV_LENGTH, raw.size))
        return String(plain, StandardCharsets.UTF_8)
    }

    private companion object {
        const val KEY_ALIAS = "alvsia_ai_session_v1"
        const val TRANSFORMATION = "AES/GCM/NoPadding"
        const val GCM_IV_LENGTH = 12
        const val GCM_TAG_LENGTH_BITS = 128
        const val GCM_TAG_LENGTH_BYTES = GCM_TAG_LENGTH_BITS / 8
        const val V2_PREFIX = "v2:"
        val AAD = "com.alvsia.ai.uncensored|session_token|v2"
            .toByteArray(StandardCharsets.UTF_8)
    }
}
