package com.alvsia.ai.uncensored

object SmartToolReference {
    const val referenceFiles = 2141
    const val reconstructionFiles = 2080
    const val toolPackageFiles = 61
    const val reconstructionOk = 345
    const val reconstructionFailed = 32
    const val reconstructionLines = 603547
    const val selfTestOk = 9
    const val selfTestWarn = 1
    const val selfTestFail = 0

    val supportedConcepts = listOf(
        "PAK: UNPACK / REPACK / REBUILD / INJEK / APK protection / detection / carve",
        "LUA: detect / dump / decrypt candidates / decompile backend / reconstruct / verify / validate",
        "BATCH: per-container output + master reports + hash ledger",
        "UTILITIES: hash / hexdump / entropy / diff / text search / backup / restore / statistics",
        "PROTEK: layered obfuscation + checksum + mirror verification + runtime validation",
        "GAME BYTECODE: modified Lua 5.3 detection and game-to-vanilla conversion path",
        "PAK CRYPTO: custom SM4 / DYN_SM4 / SM4_NEW / SIMPLE1 / SIMPLE2 / ZUC / AES index paths",
        "COMPRESSION: zlib / zstd / zstd-dict",
        "NON-DESTRUCTIVE: original input is never overwritten; zip-slip is rejected"
    )

    val knownReferenceFailures = listOf(
        "pengujian10 ui_util.lua — parse: nli 0 != ncode 7",
        "pengujian12 BRPlayerCharacterBase.lua — unknown format",
        "pengujian12 BYPASS_4.7.lua — unknown format",
        "pengujian3 GameStateBase.lua — parse: nli 0 != ncode 1442",
        "pengujian8 — 27 parse failures with nli 0 != ncode 33..36",
        "test CharacterBase.lua — parse: nli 0 != ncode 6066",
        "_loose 03704831068.lua — parse: nli 0 != ncode 29"
    )
}
