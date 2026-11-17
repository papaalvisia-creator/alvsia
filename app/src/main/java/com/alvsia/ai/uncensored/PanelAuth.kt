package com.alvsia.ai.uncensored

import android.content.Context
import android.provider.Settings
import android.util.Base64
import okhttp3.Cookie
import okhttp3.CookieJar
import okhttp3.HttpUrl
import okhttp3.HttpUrl.Companion.toHttpUrlOrNull
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.security.MessageDigest
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.TimeUnit
import javax.crypto.Cipher
import javax.crypto.spec.IvParameterSpec
import javax.crypto.spec.SecretKeySpec

data class PanelLoginResult(val token: String, val expiry: String, val product: String)

/**
 * AI adaptation of the proven SMART TOOL PanelClient transport:
 * - preserve cookies across requests
 * - solve the free-host __test/slowAES AES cookie gate
 * - retry captcha/connect after the gate cookie is stored
 * - retain the exact ALVSIA proto=2 captcha/encrypted-login contract
 */
class PanelAuth(private val baseUrl: String) {
    private val cookieStore = ConcurrentHashMap<String, MutableList<Cookie>>()
    private val jar = object : CookieJar {
        override fun saveFromResponse(url: HttpUrl, cookies: List<Cookie>) {
            val list = cookieStore.getOrPut(url.host) { mutableListOf() }
            synchronized(list) {
                cookies.forEach { cookie ->
                    list.removeAll { it.name == cookie.name }
                    list.add(cookie)
                }
            }
        }
        override fun loadForRequest(url: HttpUrl): List<Cookie> {
            val list = cookieStore[url.host] ?: return emptyList()
            synchronized(list) { return list.filter { it.matches(url) } }
        }
    }

    private val client = OkHttpClient.Builder()
        .cookieJar(jar)
        .certificatePinner(
            okhttp3.CertificatePinner.Builder()
                .add("alvsiapanel.unaux.com", "sha256/84+S6cn1vo+IjlQMR5mvqIe5XKMPh28WV9xYVtFKTkk=")
                .build()
        )
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(120, TimeUnit.SECONDS)
        .followRedirects(false)
        .followSslRedirects(false)
        .build()

    fun login(license: String, hwid: String): PanelLoginResult {
        require(baseUrl.startsWith("https://"))
        val root = baseUrl.trimEnd('/') + "/api/"
        val captchaText = openApi(root + "captcha.php")
            ?: error("Handshake panel tidak tersedia setelah pemeriksaan hosting.")
        check(!captchaText.trimStart().startsWith("<")) {
            "Panel masih mengembalikan HTML setelah pemeriksaan hosting. Login belum mencapai validasi license."
        }
        val captcha = JSONObject(captchaText)
        val cid = captcha.getString("cid")
        val nonce = captcha.getString("nonce")
        val seal = captcha.optString("seal", "")
        val mechanic = String(Base64.decode(captcha.getString("mechanic"), Base64.DEFAULT)).trim()
        val solution = solveMechanic(mechanic)
        val pow = solvePow(captcha.optString("pow_prefix", ""), captcha.optInt("pow_diff", 0))
        val payload = JSONObject()
            .put("license", license.trim())
            .put("game", "PYTHON")
            .put("hwid", hwid)
            .put("solution", solution)
            .put("pow_nonce", pow)
            .put("ts", System.currentTimeMillis() / 1000)
        val key = sha256("ALVSIA_V2|".toByteArray() + hex(nonce))
        val encrypted = aesEncrypt(key, nonce, payload.toString().toByteArray())
        val packet = JSONObject()
            .put("cid", cid)
            .put("packet", Base64.encodeToString(encrypted, Base64.NO_WRAP))
            .put("proto", 2)
            .apply { if (seal.isNotEmpty()) put("seal", seal) }
            .toString()

        val raw = postJson(root + "connect.php", packet)
            ?: error("Panel tidak mengirim respons login.")
        check(!raw.trimStart().startsWith("<")) {
            "Panel masih mengembalikan HTML setelah pemeriksaan hosting. License belum divalidasi."
        }
        val response = JSONObject(raw)
        check(response.optString("status") == "login") {
            response.optString("msg", "Login panel ditolak.")
        }
        val plain = aesDecrypt(
            key,
            Base64.decode(response.getString("ip"), Base64.DEFAULT),
            Base64.decode(response.getString("isp"), Base64.DEFAULT)
        )
        val data = JSONObject(String(plain))
        check(data.optString("status") == "success") {
            data.optString("msg", "Lisensi tidak valid.")
        }
        val token = data.optString("session_token")
        check(token.matches(Regex("^[0-9a-fA-F]{64}$"))) {
            "Panel tidak mengembalikan session token yang valid."
        }
        return PanelLoginResult(token, data.optString("expiry"), data.optString("product", "ALVSIA AI"))
    }

    private fun openApi(url: String): String? {
        var body = get(url) ?: return null
        if (body.contains("slowAES") || body.contains("__test")) {
            if (!solveTestCookie(body, url)) return body
            body = get(if (url.contains("?")) "$url&i=1" else "$url?i=1") ?: return null
        }
        return body
    }

    private fun solveTestCookie(html: String, pageUrl: String): Boolean {\n        return try {
        val re = Regex("""a=toNumbers\("([0-9a-f]+)"\),b=toNumbers\("([0-9a-f]+)"\),c=toNumbers\("([0-9a-f]+)"\)""")
        val m = re.find(html) ?: return false
        val key = hexToBytes(m.groupValues[1])
        val iv = hexToBytes(m.groupValues[2])
        val ct = hexToBytes(m.groupValues[3])
        val cipher = Cipher.getInstance("AES/CBC/NoPadding")
        cipher.init(Cipher.DECRYPT_MODE, SecretKeySpec(key, "AES"), IvParameterSpec(iv))
        val cookieValue = cipher.doFinal(ct).joinToString("") { "%02x".format(it) }
        val url = pageUrl.toHttpUrlOrNull() ?: return false
        val cookie = Cookie.Builder()
            .name("__test")
            .value(cookieValue)
            .domain(url.host)
            .path("/")
            .expiresAt(System.currentTimeMillis() + 6L * 60 * 60 * 1000)
            .build()
        jar.saveFromResponse(url, listOf(cookie))
        true
    } catch (_: Exception) { false }

    private fun get(url: String): String? {
        val request = Request.Builder().url(url)
            .header("User-Agent", "ALVSIA-PRO/5.5.2 (Android)")
            .header("Accept", "application/json, text/html, */*")
            .header("Accept-Language", "en-US,en;q=0.9")
            .get().build()
        client.newCall(request).execute().use { return it.body?.string() }
    }

    private fun postJson(url: String, json: String): String? {
        val body = json.toRequestBody("application/json; charset=utf-8".toMediaType())
        val request = Request.Builder().url(url)
            .header("User-Agent", "ALVSIA-PRO/5.5.2 (Android)")
            .header("Accept", "application/json, text/plain, */*")
            .header("Accept-Language", "en-US,en;q=0.9")
            .header("Content-Type", "application/json")
            .post(body).build()
        client.newCall(request).execute().use { response ->
            val text = response.body?.string() ?: return null
            if (text.contains("slowAES") || text.contains("__test")) {
                if (solveTestCookie(text, url)) {
                    client.newCall(request).execute().use { retry -> return retry.body?.string() }
                }
            }
            return text
        }
    }

    private fun solveMechanic(expr: String): Int {
        val m = Regex("^(-?\\d+)\\s*([+\\-*/])\\s*(-?\\d+)$").matchEntire(expr)
            ?: error("Challenge captcha panel tidak dikenali.")
        val a = m.groupValues[1].toInt()
        val b = m.groupValues[3].toInt()
        return when (m.groupValues[2]) {
            "+" -> a + b
            "-" -> a - b
            "*" -> a * b
            "/" -> if (b != 0) a / b else 0
            else -> error("Operator captcha tidak dikenal.")
        }
    }

    private fun solvePow(prefix: String, diff: Int): String {
        if (prefix.isEmpty() || diff <= 0) return "0"
        val target = "0".repeat(diff.coerceAtMost(6))
        for (i in 0 until 5_000_000) {
            val nonce = i.toString(16)
            if (sha256Hex(prefix + nonce).startsWith(target)) return nonce
        }
        error("Panel proof-of-work melewati batas percobaan.")
    }

    private fun sha256(bytes: ByteArray) = MessageDigest.getInstance("SHA-256").digest(bytes)
    private fun sha256Hex(value: String) = sha256(value.toByteArray()).joinToString("") { "%02x".format(it) }
    private fun hex(value: String): ByteArray {
        val normalized = if (value.length % 2 == 0) value else "0$value"
        return ByteArray(normalized.length / 2) { i ->
            normalized.substring(i * 2, i * 2 + 2).toInt(16).toByte()
        }
    }
    private fun hexToBytes(value: String): ByteArray = hex(value)

    private fun aesEncrypt(key: ByteArray, nonce: String, plain: ByteArray): ByteArray {
        val iv = nonce.take(16).padEnd(16, '0').toByteArray()
        return Cipher.getInstance("AES/CBC/PKCS5Padding").run {
            init(Cipher.ENCRYPT_MODE, SecretKeySpec(key, "AES"), IvParameterSpec(iv))
            doFinal(plain)
        }
    }
    private fun aesDecrypt(key: ByteArray, ivBytes: ByteArray, cipherBytes: ByteArray): ByteArray {
        val iv = if (ivBytes.size >= 16) ivBytes.copyOf(16) else ByteArray(16).also {
            System.arraycopy(ivBytes, 0, it, 0, ivBytes.size)
        }
        return Cipher.getInstance("AES/CBC/PKCS5Padding").run {
            init(Cipher.DECRYPT_MODE, SecretKeySpec(key, "AES"), IvParameterSpec(iv))
            doFinal(cipherBytes)
        }
    }

    companion object {
        fun deviceId(context: Context): String {
            val androidId = Settings.Secure.getString(context.contentResolver, Settings.Secure.ANDROID_ID).orEmpty()
            return MessageDigest.getInstance("SHA-256")
                .digest(("ALVSIA_AI|" + androidId + "|com.alvsia.ai.uncensored").toByteArray())
                .joinToString("") { "%02x".format(it) }
        }
    }
}
