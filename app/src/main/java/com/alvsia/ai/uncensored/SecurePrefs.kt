package com.alvsia.ai.uncensored

import android.content.Context
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.Base64
import java.nio.charset.StandardCharsets
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

class SecurePrefs(context: Context) {
    private val prefs = context.getSharedPreferences("alvsia_ai_session", Context.MODE_PRIVATE)
    fun token(): String? = decrypt(prefs.getString("session_token", null))
    fun setToken(value: String?) = prefs.edit().putString("session_token", value?.let(::encrypt)).apply()
    fun clearSession() = prefs.edit().remove("session_token").apply()
    fun modelId(): String = prefs.getString("model_id", ModelCatalog.starter.first().id) ?: ModelCatalog.starter.first().id
    fun setModelId(value: String) = prefs.edit().putString("model_id", value).apply()

    private fun key(): SecretKey {
        val ks = java.security.KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        val existing = ks.getKey(KEY_ALIAS, null)
        if (existing is SecretKey) return existing
        val generator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
        generator.init(KeyGenParameterSpec.Builder(KEY_ALIAS, KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
            .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
            .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
            .setRandomizedEncryptionRequired(true).build())
        return generator.generateKey()
    }

    private fun encrypt(value: String): String {
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.ENCRYPT_MODE, key())
        return Base64.encodeToString(cipher.iv + cipher.doFinal(value.toByteArray(StandardCharsets.UTF_8)), Base64.NO_WRAP)
    }

    private fun decrypt(value: String?): String? = runCatching {
        if (value.isNullOrBlank()) return null
        val raw = Base64.decode(value, Base64.NO_WRAP)
        require(raw.size > GCM_IV_LENGTH)
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.DECRYPT_MODE, key(), GCMParameterSpec(128, raw.copyOfRange(0, GCM_IV_LENGTH)))
        String(cipher.doFinal(raw.copyOfRange(GCM_IV_LENGTH, raw.size)), StandardCharsets.UTF_8)
    }.getOrNull()

    private companion object {
        const val KEY_ALIAS = "alvsia_ai_session_v1"
        const val TRANSFORMATION = "AES/GCM/NoPadding"
        const val GCM_IV_LENGTH = 12
    }
}
