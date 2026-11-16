package com.alvsia.ai.uncensored

import android.content.Context
import android.provider.Settings
import android.util.Base64
import okhttp3.CertificatePinner
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.security.MessageDigest
import java.util.concurrent.TimeUnit
import javax.crypto.Cipher
import javax.crypto.spec.IvParameterSpec
import javax.crypto.spec.SecretKeySpec

data class PanelLoginResult(val token: String, val expiry: String, val product: String)

class PanelAuth(private val baseUrl: String) {
    private val client = OkHttpClient.Builder()
        .certificatePinner(
            CertificatePinner.Builder()
                .add("alvsiapanel.unaux.com", "sha256/84+S6cn1vo+IjlQMR5mvqIe5XKMPh28WV9xYVtFKTkk=")
                .build()
        )
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(120, TimeUnit.SECONDS)
        .build()

    fun login(license: String, hwid: String): PanelLoginResult {
        require(baseUrl.startsWith("https://"))
        val captchaText = request(baseUrl.trimEnd('/') + "/api/captcha.php", null)
        check(!captchaText.trimStart().startsWith("<")) { "Panel mengembalikan HTML, bukan JSON (captcha)." }
        val captcha = JSONObject(captchaText)
        val cid = captcha.getString("cid")
        val nonce = captcha.getString("nonce")
        val seal = captcha.optString("seal", "")
        val mechanic = String(Base64.decode(captcha.getString("mechanic"), Base64.DEFAULT)).trim()
        val solution = solveMechanic(mechanic)
        val prefix = captcha.optString("pow_prefix", "")
        val difficulty = captcha.optInt("pow_diff", 0)
        val pow = solvePow(prefix, difficulty)
        val payload = JSONObject()
            .put("license", license.trim())
            .put("game", "PYTHON")
            .put("hwid", hwid)
            .put("solution", solution)
            .put("pow_nonce", pow)
            .put("ts", System.currentTimeMillis() / 1000)
        val key = sha256("ALVSIA_V2|".toByteArray() + hex(nonce))
        val encrypted = aesEncrypt(key, nonce, payload.toString().toByteArray())
        val packet = JSONObject().put("cid", cid).put("packet", Base64.encodeToString(encrypted, Base64.NO_WRAP))
            .put("proto", 2).apply { if (seal.isNotEmpty()) put("seal", seal) }.toString()
        val raw = request(baseUrl.trimEnd('/') + "/api/connect.php", packet)
        check(!raw.trimStart().startsWith("<")) { "Panel mengembalikan halaman HTML, bukan respons login JSON." }
        val response = JSONObject(raw)
        check(response.optString("status") == "login") { response.optString("msg", "Login panel ditolak.") }
        val plain = aesDecrypt(key, Base64.decode(response.getString("ip"), Base64.DEFAULT), Base64.decode(response.getString("isp"), Base64.DEFAULT))
        val data = JSONObject(String(plain))
        check(data.optString("status") == "success") { data.optString("msg", "Lisensi tidak valid.") }
        val token = data.optString("session_token")
        check(token.matches(Regex("^[0-9a-fA-F]{64}$"))) { "Panel tidak mengembalikan session token yang valid." }
        return PanelLoginResult(token, data.optString("expiry"), data.optString("product", "ALVSIA AI"))
    }

    private fun request(url: String, json: String?): String {
        val builder = Request.Builder().url(url)
            .header("User-Agent", "ALVSIA-AI-UNCENSORED/0.3")
            .header("Accept", "application/json, text/plain, */*")
        if (json == null) builder.get() else builder.post(json.toRequestBody("application/json; charset=utf-8".toMediaType()))
        client.newCall(builder.build()).execute().use { response ->
            val body = response.body?.string().orEmpty()
            check(response.isSuccessful) { "Panel HTTP ${response.code}: ${body.take(180)}" }
            return body
        }
    }

    private fun solveMechanic(expr: String): Int {
        val m = Regex("^(-?\\d+)\\s*([+\\-*/])\\s*(-?\\d+)$").matchEntire(expr)
            ?: error("Challenge panel tidak dikenali.")
        val a=m.groupValues[1].toInt(); val b=m.groupValues[3].toInt()
        return when(m.groupValues[2]) { "+"->a+b; "-"->a-b; "*"->a*b; "/"->if(b!=0)a/b else 0; else->0 }
    }
    private fun solvePow(prefix: String, diff: Int): String {
        if(prefix.isEmpty() || diff<=0) return "0"
        val target="0".repeat(diff.coerceAtMost(6))
        for(i in 0 until 5_000_000) { val n=i.toString(16); if(sha256Hex(prefix+n).startsWith(target)) return n }
        error("Panel proof-of-work melewati batas waktu.")
    }
    private fun sha256(b:ByteArray)=MessageDigest.getInstance("SHA-256").digest(b)
    private fun sha256Hex(s:String)=sha256(s.toByteArray()).joinToString(""){"%02x".format(it)}
    private fun hex(s:String):ByteArray { val h=if(s.length%2==0)s else "0$s"; return ByteArray(h.length/2){i->h.substring(i*2,i*2+2).toInt(16).toByte()} }
    private fun aesEncrypt(key:ByteArray, nonce:String, plain:ByteArray):ByteArray {
        val iv=nonce.take(16).padEnd(16,'0').toByteArray()
        return Cipher.getInstance("AES/CBC/PKCS5Padding").run { init(Cipher.ENCRYPT_MODE,SecretKeySpec(key,"AES"),IvParameterSpec(iv)); doFinal(plain) }
    }
    private fun aesDecrypt(key:ByteArray, ivBytes:ByteArray, cipherBytes:ByteArray):ByteArray {
        val iv=if(ivBytes.size>=16)ivBytes.copyOf(16) else ByteArray(16).also{System.arraycopy(ivBytes,0,it,0,ivBytes.size)}
        return Cipher.getInstance("AES/CBC/PKCS5Padding").run { init(Cipher.DECRYPT_MODE,SecretKeySpec(key,"AES"),IvParameterSpec(iv)); doFinal(cipherBytes) }
    }
    companion object {
        fun deviceId(context: Context): String {
            val androidId=Settings.Secure.getString(context.contentResolver, Settings.Secure.ANDROID_ID).orEmpty()
            return MessageDigest.getInstance("SHA-256").digest(("ALVSIA_AI|"+androidId+"|com.alvsia.ai.uncensored").toByteArray()).joinToString(""){"%02x".format(it)}
        }
    }
}