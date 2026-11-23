from __future__ import annotations
import hashlib
from pathlib import Path

ENGINE="ALVSIA SMART TOOL"; VERSION="2.0.0"

def _sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(1048576),b""): h.update(c)
    return h.hexdigest()

def _detect(path,head):
    n=str(path).lower()
    if head.startswith(b"\x1bLua") or n.endswith((".lua",".luac",".slua",".lua.enc")): return "LUA"
    if head.startswith(b"\x1bLJ"): return "LUAJIT"
    if head[:4]==b"\x5a\x6f\x12\xe1" or n.endswith(".pak"): return "UE4_PAK"
    if head[:4]==b"PK\x03\x04" or n.endswith(".obb"): return "ZIP_CONTAINER"
    if head[:4]==b"\x7fELF" or n.endswith(".so"): return "ELF"
    if head[:4]==b"dex\n" or n.endswith(".dex"): return "DEX"
    return "BINARY"

def analyze(path):
    from smart_engine import analyze as _analyze
    return _analyze(Path(path))

def run(path,operation="analyze",output=None,options=None):
    from smart_engine import run as _run
    result=_run(Path(path),operation,output,options or {})
    if isinstance(result,dict):
        result.setdefault("engine",ENGINE); result.setdefault("version",VERSION)
    return result

def forensic(path,mode="strings"):
    import alvsia_forensics as f
    data=Path(path).read_bytes()
    if mode=="strings" and hasattr(f,"recover_strings"): return f.recover_strings(data)
    if mode=="aes" and hasattr(f,"find_aes_keys"): return f.find_aes_keys(data)
    if mode=="so" and hasattr(f,"so_string_analysis"):
        return [e.__dict__ if hasattr(e,"__dict__") else str(e) for e in f.so_string_analysis(path,5,"")]
    return {"size":len(data),"sha256":hashlib.sha256(data).hexdigest()}

def self_test():
    from smart_engine import run
    return run(__file__,"self_test") if False else __import__("smart_engine").run(__file__,"self_test")
