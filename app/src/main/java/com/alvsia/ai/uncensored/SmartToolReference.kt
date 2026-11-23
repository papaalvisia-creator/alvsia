package com.alvsia.ai.uncensored

/**
 * Specification contract reconstructed from the supplied ALVSIA tool references.
 * An adapter is only marked available after it passes reference fixtures.
 */
object SmartToolReference {
    const val ENGINE_NAME = "ALVSIA SMART TOOL"
    const val PIPELINE_VERSION = "0.7.0"
    val luaStages = listOf("detect","normalize","decrypt","convert","decompile","reconstruct","verify","batch")
    val pakStages = listOf("detect","parse-index","decrypt-index","decompress","extract","modify","rebuild-index","repack","verify")
    val cryptoFamilies = listOf("AES","SM4","ZUC","XOR","zlib","zstd","zstd-dict")
}
