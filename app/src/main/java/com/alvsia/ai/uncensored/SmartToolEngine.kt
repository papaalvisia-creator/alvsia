package com.alvsia.ai.uncensored

import android.content.ContentResolver
import android.net.Uri
import java.io.BufferedInputStream
import java.io.File
import java.io.FileOutputStream
import java.security.MessageDigest
import java.util.zip.ZipInputStream

data class SmartFileReport(
    val name: String,
    val type: String,
    val size: Long,
    val sha256: String,
    val detail: String,
    val warnings: List<String> = emptyList()
)

data class LuaReport(
    val kind: String,
    val version: String,
    val header: String,
    val xorCandidates: List<String>,
    val detail: String
)

object SmartToolEngine {
    private const val BUF = 1024 * 1024

    fun analyze(resolver: ContentResolver, uri: Uri): SmartFileReport {
        val name = queryName(resolver, uri)
        val size = querySize(resolver, uri)
        val md = MessageDigest.getInstance("SHA-256")
        val head = ByteArray(64 * 1024)
        var headLen = 0
        resolver.openInputStream(uri).use { raw ->
            requireNotNull(raw) { "Tidak dapat membuka file." }
            BufferedInputStream(raw, BUF).use { input ->
                val buf = ByteArray(BUF)
                while (true) {
                    val n = input.read(buf)
                    if (n < 0) break
                    md.update(buf, 0, n)
                    if (headLen < head.size) {
                        val take = minOf(n, head.size - headLen)
                        System.arraycopy(buf, 0, head, headLen, take)
                        headLen += take
                    }
                }
            }
        }
        val h = head.copyOf(headLen)
        val type = detectType(name, h)
        val detail = when (type) {
            "LUA" -> {
                val lr = inspectLua(h)
                "Lua kind=${lr.kind}; ${lr.detail}"
            }
            "UE4 PAK" -> "UE4 PAK magic terdeteksi. Parsing indeks/enkripsi spesifik memerlukan backend PAK yang sesuai; file asli tidak disentuh."
            "ZIP/APK/JAR/AAB" -> "ZIP container terdeteksi; ekstraksi aman dapat dilakukan ke folder output baru."
            "ELF" -> "ELF binary terdeteksi."
            "PE" -> "Windows PE/MZ binary terdeteksi."
            "DEX" -> "DEX bytecode terdeteksi."
            "IMAGE" -> "Format gambar terdeteksi."
            else -> "Format belum dikenali; metadata + SHA-256 tetap tersedia."
        }
        return SmartFileReport(name, type, size, md.digest().toHex(), detail)
    }

    fun inspectLua(bytes: ByteArray): LuaReport {
        if (bytes.size >= 4 && bytes.copyOfRange(0, 4).contentEquals(byteArrayOf(0x1B,0x4C,0x75,0x61))) {
            val version = if (bytes.size > 4) "0x%02X".format(bytes[4]) else "unknown"
            val fmt = if (bytes.size > 5) "format=0x%02X".format(bytes[5]) else "format=?"
            return LuaReport("Lua bytecode", version, "${bytes.take(8).toByteArray().toHex()} \$fmt", emptyList(), "Header Lua valid.")
        }
        val text = bytes.toString(Charsets.UTF_8)
        if (looksLikeLuaSource(text)) {
            return LuaReport("Lua source", "text", bytes.take(32).toByteArray().toHex(), emptyList(), "Source Lua terdeteksi.")
        }
        val candidates = mutableListOf<String>()
        for (k in 1..255) {
            var printable = 0
            val limit = minOf(bytes.size, 4096)
            for (i in 0 until limit) {
                val v = (bytes[i].toInt() xor k) and 0xFF
                if (v in 32..126 || v == 10 || v == 13 || v == 9) printable++
            }
            if (limit > 0 && printable.toDouble() / limit > 0.82) {
                candidates += "xor-0x%02X".format(k)
                if (candidates.size >= 8) break
            }
        }
        val kind = when {
            bytes.size >= 2 && bytes[0] == 0x1F.toByte() && bytes[1] == 0x8B.toByte() -> "gzip/lua"
            bytes.size >= 2 && bytes[0] == 0x78.toByte() -> "zlib?/lua"
            candidates.isNotEmpty() -> "encrypted/obfuscated candidate"
            else -> "unknown"
        }
        return LuaReport(kind, "unknown", bytes.take(16).toByteArray().toHex(), candidates, "Tidak ada header Lua standar; lanjutkan diagnostic/dekripsi bertahap.")
    }

    fun extractZip(resolver: ContentResolver, uri: Uri, outDir: File): Int {
        outDir.mkdirs()
        var count = 0
        resolver.openInputStream(uri).use { raw ->
            requireNotNull(raw)
            ZipInputStream(BufferedInputStream(raw, BUF)).use { zin ->
                val buffer = ByteArray(BUF)
                while (true) {
                    val e = zin.nextEntry ?: break
                    val target = safeResolve(outDir, e.name)
                    if (e.isDirectory) target.mkdirs()
                    else {
                        target.parentFile?.mkdirs()
                        FileOutputStream(target).use { out ->
                            while (true) {
                                val n = zin.read(buffer)
                                if (n < 0) break
                                out.write(buffer, 0, n)
                            }
                        }
                        count++
                    }
                    zin.closeEntry()
                }
            }
        }
        return count
    }

    fun batchClassify(resolver: ContentResolver, uri: Uri): String {
        val r = analyze(resolver, uri)
        return buildString {
            appendLine("ALVSIA SMART TOOL REPORT")
            appendLine("FILE  : ${r.name}")
            appendLine("TYPE  : ${r.type}")
            appendLine("SIZE  : ${r.size}")
            appendLine("SHA256: ${r.sha256}")
            appendLine("DETAIL: ${r.detail}")
            r.warnings.forEach { appendLine("WARN  : $it") }
        }
    }

    private fun queryName(r: ContentResolver, u: Uri): String =
        r.query(u, arrayOf(android.provider.OpenableColumns.DISPLAY_NAME), null, null, null)?.use {
            if (it.moveToFirst()) it.getString(0) else u.lastPathSegment ?: "input"
        } ?: (u.lastPathSegment ?: "input")

    private fun querySize(r: ContentResolver, u: Uri): Long =
        r.query(u, arrayOf(android.provider.OpenableColumns.SIZE), null, null, null)?.use {
            if (it.moveToFirst() && !it.isNull(0)) it.getLong(0) else -1L
        } ?: -1L

    private fun detectType(name: String, b: ByteArray): String {
        val lower = name.lowercase()
        if (b.size >= 4 && b[0] == 0x5A.toByte() && b[1] == 0x6F.toByte() && b[2] == 0x12.toByte() && b[3] == 0xE1.toByte()) return "UE4 PAK"
        if (b.size >= 4 && b[0] == 0x50.toByte() && b[1] == 0x4B.toByte()) return "ZIP/APK/JAR/AAB"
        if (b.size >= 4 && b[0] == 0x7F.toByte() && b[1] == 'E'.code.toByte() && b[2] == 'L'.code.toByte() && b[3] == 'F'.code.toByte()) return "ELF"
        if (b.size >= 2 && b[0] == 'M'.code.toByte() && b[1] == 'Z'.code.toByte()) return "PE"
        if (b.size >= 4 && b[0] == 'd'.code.toByte() && b[1] == 'e'.code.toByte() && b[2] == 'x'.code.toByte() && b[3] == 0x0A.toByte()) return "DEX"
        if (b.size >= 8 && b[0] == 0x89.toByte() && b[1] == 0x50.toByte() && b[2] == 0x4E.toByte() && b[3] == 0x47.toByte()) return "IMAGE"
        if (lower.endsWith(".lua") || lower.endsWith(".luac") || lower.endsWith(".lua.enc")) return "LUA"
        return "BINARY"
    }

    private fun looksLikeLuaSource(s: String): Boolean {
        val t = s.trimStart()
        if (t.startsWith("--") || t.startsWith("local ") || t.startsWith("function ") || t.startsWith("return ")) return true
        val score = listOf("function", "local", "end", "then", "return").count { s.contains(it) }
        return score >= 2 && s.count { it == '\u0000' } < 3
    }

    private fun safeResolve(root: File, entry: String): File {
        val base = root.canonicalFile
        val target = File(base, entry).canonicalFile
        require(target.path == base.path || target.path.startsWith(base.path + File.separator)) { "ZIP entry ditolak (zip-slip): $entry" }
        return target
    }

    private fun ByteArray.toHex(): String = joinToString("") { "%02x".format(it.toInt() and 0xFF) }
}
