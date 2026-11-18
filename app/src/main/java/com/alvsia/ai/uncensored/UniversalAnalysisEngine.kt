package com.alvsia.ai.uncensored

import android.content.ContentResolver
import android.net.Uri
import android.provider.OpenableColumns
import java.io.BufferedInputStream
import java.security.MessageDigest
import java.util.Locale

data class UniversalAnalysisResult(
    val name: String,
    val extension: String,
    val typeLabel: String,
    val sizeBytes: Long,
    val sha256: String,
    val summary: String,
    val detectedSignatures: List<String>
)

object UniversalAnalysisEngine {
    private const val BUFFER_SIZE = 1024 * 1024
    private const val HEADER_SIZE = 64 * 1024

    fun analyze(resolver: ContentResolver, uri: Uri): UniversalAnalysisResult {
        val name = queryName(resolver, uri)
        val size = querySize(resolver, uri)
        val extension = name.substringAfterLast('.', "").lowercase(Locale.ROOT)
        val header = resolver.openInputStream(uri)?.use { input ->
            val buffer = ByteArray(HEADER_SIZE)
            val read = input.read(buffer)
            if (read <= 0) ByteArray(0) else buffer.copyOf(read)
        } ?: ByteArray(0)

        val detection = detect(extension, header)
        val hash = sha256(resolver, uri)

        return UniversalAnalysisResult(
            name = name,
            extension = if (extension.isBlank()) "unknown" else ".$extension",
            typeLabel = detection.first,
            sizeBytes = size,
            sha256 = hash,
            summary = detection.second,
            detectedSignatures = detection.third
        )
    }

    private fun queryName(resolver: ContentResolver, uri: Uri): String {
        resolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)?.use { c ->
            if (c.moveToFirst()) return c.getString(0) ?: "selected-file"
        }
        return uri.lastPathSegment?.substringAfterLast('/') ?: "selected-file"
    }

    private fun querySize(resolver: ContentResolver, uri: Uri): Long {
        resolver.query(uri, arrayOf(OpenableColumns.SIZE), null, null, null)?.use { c ->
            if (c.moveToFirst() && !c.isNull(0)) return c.getLong(0)
        }
        return resolver.openAssetFileDescriptor(uri, "r")?.use { afd -> afd.length.coerceAtLeast(0L) } ?: -1L
    }

    private fun sha256(resolver: ContentResolver, uri: Uri): String {
        val digest = MessageDigest.getInstance("SHA-256")
        resolver.openInputStream(uri)?.use { raw ->
            BufferedInputStream(raw, BUFFER_SIZE).use { input ->
                val buffer = ByteArray(BUFFER_SIZE)
                while (true) {
                    val read = input.read(buffer)
                    if (read < 0) break
                    if (read == 0) continue
                    digest.update(buffer, 0, read)
                }
            }
        } ?: error("File cannot be opened for streaming analysis")
        return digest.digest().joinToString("") { "%02x".format(it) }
    }

    private fun detect(extension: String, bytes: ByteArray): Triple<String, String, List<String>> {
        fun ascii(offset: Int, length: Int): String {
            if (offset >= bytes.size) return ""
            return bytes.copyOfRange(offset, minOf(bytes.size, offset + length)).toString(Charsets.US_ASCII)
        }
        fun has(vararg values: Int): Boolean =
            values.isNotEmpty() && values.size <= bytes.size &&
                values.indices.all { bytes[it].toInt() and 0xff == values[it] }

        return when {
            has(0x50, 0x4B, 0x03, 0x04) -> {
                val label = when (extension) {
                    "apk" -> "Android APK / ZIP"
                    "jar" -> "Java JAR / ZIP"
                    "aab" -> "Android App Bundle / ZIP"
                    "zip" -> "ZIP ARCHIVE"
                    else -> "ZIP-CONTAINER"
                }
                Triple(label, "ZIP-compatible container detected; entries can be indexed without loading the entire file into RAM.", listOf("ZIP"))
            }
            has(0x7F, 0x45, 0x4C, 0x46) ->
                Triple("ELF BINARY", "ELF executable format detected; metadata and sections can be inspected without execution.", listOf("ELF"))
            has(0x4D, 0x5A) ->
                Triple("PE / DOS EXECUTABLE", "MZ executable header detected; PE metadata can be indexed without executing the file.", listOf("MZ"))
            has(0xCA, 0xFE, 0xBA, 0xBE) || has(0xCA, 0xFE, 0xD0, 0x0D) ->
                Triple("MACH-O BINARY", "Mach-O executable header detected.", listOf("MACH-O"))
            ascii(0, 4) == "dex\n" ->
                Triple("DEX BYTECODE", "Dalvik/ART executable bytecode detected.", listOf("DEX"))
            ascii(0, 4) == "\u001bLua" ->
                Triple("LUA BYTECODE", "Lua bytecode header detected; version-specific parsing can be selected next.", listOf("LUA"))
            extension in setOf("png") -> Triple("PNG IMAGE", "PNG image container detected.", listOf("PNG"))
            extension in setOf("jpg", "jpeg") -> Triple("JPEG IMAGE", "JPEG image detected.", listOf("JPEG"))
            extension in setOf("json") -> Triple("JSON TEXT", "Structured JSON document candidate.", listOf("TEXT"))
            extension in setOf("xml") -> Triple("XML TEXT", "Structured XML document candidate.", listOf("TEXT"))
            extension in setOf("txt", "log", "md", "csv", "ini", "cfg", "yaml", "yml") ->
                Triple("TEXT DOCUMENT", "Text-oriented document detected from extension.", listOf("TEXT"))
            else ->
                Triple("UNKNOWN / GENERIC BINARY", "No known magic signature matched. The universal engine keeps the file as a stream and can route it to a suitable analyzer later.", emptyList())
        }
    }
}
