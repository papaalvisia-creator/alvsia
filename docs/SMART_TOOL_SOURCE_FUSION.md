# ALVSIA SMART TOOL — Source Fusion Manifest

## Audited source families

### IkramTool V130 4.7
Lua pipeline, mega Lua recovery, Tencent PAK, PakTool, UE/asset processing, custom SM4, Lua protection/compiler helpers, diagnosis and native/JAR backends.

### TOOL source
Combined unpack/decompile/batch-decompile/protek/info/all pipeline, crypto/compression, Lua bytecode handling, Lua protection, Lua-to-PAK injection and rebuild verification.

### RegulerResault regression corpus
Regression data only: successful Lua outputs, UE assets, LOCRES/UMAP and known malformed/failure cases. It is used for validation and is not copied wholesale into the APK.

## Recovered companion source logic integrated into the Android engine

- GRW.py — T24/BGMI Lua conversion and PAK injection/repack logic.
- UltimateEngineTool.py — Smart Lua analysis, T24 conversion, multi-XOR and PAK rebuild/protection helpers.
- GODXKAZUKI.py — full Tencent PAK/Lua/OBB engine family retained in the existing Android legacy engine.
- referensi.py — Lua bytecode parsing/patching, ZUC, AES/XOR recovery, SO/APK audit, URL and string recovery represented by the Android forensic adapter.
- alvsia_engine.py — Android Tencent PAK core.
- alvsia_forensics.py — Android forensic/recovery adapter.

## Implementation rule
A menu is not considered functional merely because the UI button exists. Every Smart Tool operation must resolve to a concrete backend or return a truthful backend-unavailable diagnostic. No fabricated success container is used.

The Lua protection route now uses the verified T24/BGMI bytecode transformation backend rather than the previous invented ALVSLUA2 container.