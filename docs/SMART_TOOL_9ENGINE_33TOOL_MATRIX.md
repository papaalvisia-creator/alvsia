# ALVSIA SMART TOOL — 9 Engine / 33 Tool Matrix

1. HOME
- Universal File Detect → analyze
- Workspace Report → file_report
- Engine Health → self_test

2. LUA
- Smart Analyze → lua_smart_analyze
- Recovery / Normalize → lua_decompile
- T24 / BGMI Convert → lua_t24_convert
- Multi-XOR → lua_multi_xor
- Protect / Transform → lua_protect
- Custom Lua→PAK Inject → lua_custom_inject

3. PAK / OBB
- PAK Info → pak_info
- Extract → pak_extract
- Lua Inject → lua_custom_inject
- Repack Modified Tree → pak_repack

4. ASSET / UE
- UAsset Classify → analyze
- UExp / UBULK Classify → analyze
- LOCRES / UMAP Classify → analyze
- Asset Report → file_report

5. APK / DEX
- APK Structural Audit → apk_audit
- DEX / Bytecode Report → file_report
- URL / Endpoint Scan → url_scan
- Package / Signature Audit → apk_audit

6. NATIVE
- ELF / SO Audit → so_audit
- Native Strings → strings
- ABI / Dependency Report → file_report

7. CRYPTO / RECOVERY
- AES Candidate Scan → aes_scan
- ZUC Decrypt → zuc_decrypt
- String Recovery → string_recover
- URL / Endpoint Recovery → url_scan

8. FORENSIC / STRING
- File Report → file_report
- Strings → strings
- Entropy → entropy
- Hex Preview → hex

9. BATCH / DEV LAB
- Batch Audit → batch_audit
- Regression / Compare → batch_audit
- Self Test → self_test

## Backend rule
All listed routes are concrete operation IDs. UI labels are not treated as implementation. If a required optional native/JAR backend is not present on-device, the operation must return a truthful diagnostic rather than a fake success.

## Source mapping
- IkramTool V130 4.7: Lua pipeline, mega Lua recovery, Tencent PAK, PakTool, UE/asset, SM4, compiler/protection helpers, native/JAR backend families.
- TOOL source: combined unpack/decompile/batch/protek/info/all pipeline, crypto/compression, Lua protection, Lua→PAK injection and rebuild verification.
- RegulerResault corpus: regression/evidence data only; used to validate failure and success classes, not shipped wholesale.
- GRW / UltimateEngineTool / GODXKAZUKI / referensi: recovered executable source logic now routed through the Android adapters.
