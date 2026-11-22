from __future__ import annotations
import hashlib, json, os, shutil, subprocess, tempfile, zipfile
from pathlib import Path

ENGINE = "ALVSIA SMART TOOL"
VERSION = "1.0.0"

def _sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def _head(path,n=131072):
    with open(path,"rb") as f: return f.read(n)

def _detect(path, head):
    n=path.lower()
    if head.startswith(b"\x1bLua"): return "LUA"
    if head.startswith(b"\x1bLJ"): return "LUAJIT"
    if head[:4] == b"\x5a\x6f\x12\xe1": return "UE4_PAK"
    if head[:4] == b"PK\x03\x04": return "ZIP_CONTAINER"
    if head[:4] == b"\x7fELF": return "ELF"
    if head[:2] == b"MZ": return "PE"
    if head[:4] == b"dex\n": return "DEX"
    if n.endswith((".lua",".luac",".slua",".lua.enc")): return "LUA"
    return "BINARY"

def analyze(path):
    p=Path(path); head=_head(p); typ=_detect(p.name,head)
    return {"engine":ENGINE,"version":VERSION,"name":p.name,"size":p.stat().st_size,"sha256":_sha256(p),"type":typ,
            "read_only":True,"stages":["detect","hash"],"capabilities":capabilities(typ)}

def capabilities(typ):
    if typ in ("LUA","LUAJIT"):
        return ["detect","normalize","BGMI/Lua conversion","decompile cascade","reconstruct/compile","roundtrip verify","batch"]
    if typ=="UE4_PAK":
        return ["detect","footer/index parse","AES/SM4/ZUC/SIMPLE decrypt","zlib/ZSTD/ZSTD-dict","extract","inject","repack","verify"]
    return ["analyze","hash","forensics","batch"]

def _lua(path,out):
    from alvsia_lua_core import normalize_lua,decompile_auto
    p=Path(path); data=p.read_bytes(); norm,meta=normalize_lua(data)
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    normalized=out/(p.stem+"_normalized.luac"); normalized.write_bytes(norm)
    result=decompile_auto(p,out)
    result["normalized"]=str(normalized); result["meta"]=meta
    return result

def _pak(path,operation,out=None,inject=None):
    from alvsia_engine import TencentPakFile
    p=Path(path); pak=TencentPakFile(p)
    info={"version":int(pak._pak_info.version),"index_encrypted":bool(pak._pak_info.index_encrypted),
          "index_offset":int(pak._pak_info.index_offset),"index_size":int(pak._pak_info.index_size),
          "file_count":sum(len(v) for v in pak._index.values()),
          "mount":str(pak._mount_point),"paths":pak.list_existing_paths()}
    if operation=="info": return info
    if out is None: raise ValueError("output required")
    out=Path(out); out.parent.mkdir(parents=True,exist_ok=True)
    if operation=="extract":
        pak.dump(out); return {**info,"output":str(out)}
    if operation=="extract_single":
        pak.dump_single_file(str(inject),out,"single"); return {**info,"output":str(out)}
    if operation=="inject":
        plan=inject or []
        pak.inject_files(plan,out); return {**info,"output":str(out),"injected":len(plan)}
    if operation=="repack":
        shutil.copy2(p,out)
        with open(out,"r+b") as fh: ok=pak.repack_inplace_from_modified_dir(fh)
        return {**info,"output":str(out),"repacked":bool(ok)}
    raise ValueError("unknown PAK operation")

def run(path,operation="analyze",output=None,options=None):\n    kwargs = options or {}
    p=Path(path)
    if operation=="analyze": return analyze(p)
    typ=_detect(p.name,_head(p))
    if typ in ("LUA","LUAJIT") and operation in ("lua","decompile","lua_decompile"):
        return _lua(p,output or (p.parent/"alvsia_output"))
    if typ=="UE4_PAK" and operation.startswith("pak_"):
        return _pak(p,operation[4:],output,kwargs.get("inject"))
    if operation=="zip_extract":
        out=Path(output or (p.parent/"alvsia_extract")); out.mkdir(parents=True,exist_ok=True)
        count=0
        with zipfile.ZipFile(p) as z:
            for name in z.namelist():
                target=(out/name).resolve()
                if not str(target).startswith(str(out.resolve())+os.sep) and target != out.resolve(): raise ValueError("zip-slip")
                if name.endswith("/"): target.mkdir(parents=True,exist_ok=True); continue
                target.parent.mkdir(parents=True,exist_ok=True)
                with z.open(name) as src, open(target,"wb") as dst: shutil.copyfileobj(src,dst,1024*1024)
                count+=1
        return {"output":str(out),"count":count}
    raise ValueError(f"operation {operation} unsupported for {typ}")

def forensic(path,mode="strings"):
    import alvsia_forensics as f
    data=Path(path).read_bytes()
    if mode=="strings" and hasattr(f,"recover_strings"): return f.recover_strings(data)
    if mode=="aes" and hasattr(f,"find_aes_keys"): return f.find_aes_keys(data)
    if mode=="so" and hasattr(f,"so_string_analysis"): return [e.__dict__ if hasattr(e,"__dict__") else str(e) for e in f.so_string_analysis(path,5,"")]
    return {"size":len(data),"sha256":hashlib.sha256(data).hexdigest()}

def self_test():
    checks={}
    try:
        import alvsia_engine as e
        checks["pak_core"]=all(hasattr(e,n) for n in ("TencentPakFile","PakCrypto","PakCompression","TencentPakEntry"))
        checks["sm4_keys"]=len(e.SM4_SECRET_NEW)>=22
    except Exception as x: checks["pak_core"]=False; checks["pak_error"]=str(x)
    try:
        import alvsia_lua_core as l
        checks["lua_core"]=all(hasattr(l,n) for n in ("bgmi_to_std","std_to_bgmi","normalize_lua","decompile_auto"))
    except Exception as x: checks["lua_core"]=False; checks["lua_error"]=str(x)
    return {"engine":ENGINE,"version":VERSION,"checks":checks,"ok":all(v is True for k,v in checks.items() if k.endswith("_core") or k=="sm4_keys")}
