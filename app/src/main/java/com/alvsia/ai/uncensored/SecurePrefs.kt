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
 * Stores provider credentials locally with Android Keystore AES-256-GCM.
 */
class SecurePrefs(context: Context) {
    private val prefs = context.getSharedPreferences("alvsia_ai_settings", Context.MODE_PRIVATE)

    fun providerKey(): String? = read("provider_key")
    fun setProviderKey(value: String?) = write("provider_key", value)

    fun providerEndpoint(): String =
        prefs.getString("provider_endpoint", DirectAiGateway.DEFAULT_ENDPOINT)
            ?: DirectAiGateway.DEFAULT_ENDPOINT

    fun setProviderEndpoint(value: String) {
        prefs.edit().putString("provider_endpoint", value).apply()
    }

    fun modelId(): String =
        prefs.getString("model_id", ModelCatalog.starter.first().id)
            ?: ModelCatalog.starter.first().id

    fun setModelId(value: String) {
        prefs.edit().putString("model_id", value).apply()
    }

    private fun read(name: String): String? {
        val stored = prefs.getString(name, null) ?: return null
        return runCatching { decrypt(stored) }.getOrNull()
    }

    private fun write(name: String, value: String?) {
        val editor = prefs.edit()
        if (value.isNullOrBlank()) editor.remove(name)
        else editor.putString(name, encrypt(value))
        editor.apply()
    }

    private fun key(): SecretKey {
        val store = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        val existing = store.getKey(KEY_ALIAS, null)
        if (existing is SecretKey) return existing

        val generator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
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
        return V2_PREFIX + Base64.encodeToString(cipher.iv + encrypted, Base64.NO_WRAP)
    }

    private fun decrypt(value: String): String {
        val raw = Base64.decode(value.removePrefix(V2_PREFIX), Base64.NO_WRAP)
        require(raw.size > IV_LENGTH + TAG_BYTES)
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(
            Cipher.DECRYPT_MODE,
            key(),
            GCMParameterSpec(TAG_BITS, raw.copyOfRange(0, IV_LENGTH))
        )
        cipher.updateAAD(AAD)
        return String(cipher.doFinal(raw.copyOfRange(IV_LENGTH, raw.size)), StandardCharsets.UTF_8)
    }

    private companion object {
        const val KEY_ALIAS = "alvsia_ai_provider_v1"
        const val TRANSFORMATION = "AES/GCM/NoPadding"
        const val IV_LENGTH = 12
        const val TAG_BITS = 128
        const val TAG_BYTES = TAG_BITS / 8
        const val V2_PREFIX = "v2:"
        val AAD = "com.alvsia.ai.uncensored|provider|v2"
            .toByteArray(StandardCharsets.UTF_8)
    }
}
