package com.alvsia.ai.uncensored.security

import okhttp3.ResponseBody
import java.io.ByteArrayOutputStream
import java.io.IOException
import java.nio.charset.StandardCharsets

/**
 * Reads network bodies with a strict byte ceiling before decoding/parsing.
 * Prevents unexpectedly large or unbounded gateway responses from exhausting
 * the app process while preserving the existing JSON wire format.
 */
internal object HttpBodyGuard {
    fun readUtf8(body: ResponseBody?, maxBytes: Int): String {
        require(maxBytes > 0) { "Invalid response size limit" }
        if (body == null) return ""
        if (body.contentLength() > maxBytes.toLong()) {
            throw IOException("Response exceeded the configured size limit")
        }

        val output = ByteArrayOutputStream(minOf(maxBytes, 8 * 1024))
        val input = body.byteStream()
        val buffer = ByteArray(8 * 1024)
        var total = 0

        while (true) {
            val remainingWithOverflowProbe = maxBytes - total + 1
            val count = input.read(
                buffer,
                0,
                minOf(buffer.size, remainingWithOverflowProbe)
            )
            if (count < 0) break
            total += count
            if (total > maxBytes) {
                throw IOException("Response exceeded the configured size limit")
            }
            output.write(buffer, 0, count)
        }

        return String(output.toByteArray(), StandardCharsets.UTF_8)
    }
}
