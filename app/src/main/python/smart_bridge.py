import hashlib
import json
import os
import struct

ENGINE = "ALVSIA SMART TOOL / PYTHON CORE"
VERSION = "0.8.0"

def _head(path, n=131072):
    with open(path, "rb") as f:
        return f.read(n)

def analyze(path):
    size = os.path.getsize(path)
    h = _head(path)
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            sha.update(chunk)

    kind = "BINARY"
    if h[:4] == b"Lua\x1b":
        kind = "LUA"
    elif h[:4] == b"\x5a\x6f\x12\xe1":
        kind = "UE4_PAK"
    elif h[:2] == b"PK":
        kind = "ZIP_CONTAINER"
    elif h[:4] == b"\x7fELF":
        kind = "ELF"
    elif h[:2] == b"MZ":
        kind = "PE"
    elif h[:4] == b"dex\n":
        kind = "DEX"

    result = {
        "engine": ENGINE,
        "version": VERSION,
        "name": os.path.basename(path),
        "size": size,
        "sha256": sha.hexdigest(),
        "type": kind,
        "streaming": True,
        "stages": []
    }

    if kind == "LUA":
        result["stages"] = ["detect"]
        result["lua_version"] = "0x%02x" % h[4] if len(h) > 4 else "unknown"
        result["lua_format"] = h[5] if len(h) > 5 else None
    elif kind == "UE4_PAK":
        result["stages"] = ["detect", "footer-probe"]
    else:
        result["stages"] = ["detect"]

    return result

def run(path, operation="analyze", output=None):
    # Core adapters are loaded separately. This bridge never overwrites input.
    result = analyze(path)
    result["operation"] = operation
    result["input_untouched"] = True
    if output:
        os.makedirs(output, exist_ok=True)
        report = os.path.join(output, "smart_report.json")
        with open(report, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        result["report"] = report
    return result
