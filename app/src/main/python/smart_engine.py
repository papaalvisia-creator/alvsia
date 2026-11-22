from __future__ import annotations
import hashlib, os, shutil
from pathlib import Path

ENGINE="ALVSIA SMART TOOL"; VERSION="2.0.0"

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(1048576),b""): h.update(c)
    return h.hexdigest()

def detect(p):
    p=Path(p); head=p.read_bytes()[:131072]; n=p.name.lower()
    if head.startswith(b"\x1bLua") or n.endswith((".lua",".luac",".slua",".lua.enc")): return "LUA"
    if head.startswith(b"\x1bLJ"): return "LUAJIT"
    if head[:4]==b"\x5a\x6f\x12\xe1" or n.endswith(".pak"): return "UE4_PAK"
    if head[:4]==b"PK\x03\x04" or n.endswith(".obb"): return "ZIP_CONTAINER"
    if head[:4]==b"\x7fELF" or n.endswith(".so"): return "ELF"
    if head[:4]==b"dex\n" or n.endswith(".dex"): return "DEX"
    if n.endswith((".uasset",".uexp",".ubulk",".umap",".locres")): return "UE4_ASSET"
    return "BINARY"

def _out(output,src):
    p=Path(output) if output else Path(src).parent/"ALVSIA_SMART_OUTPUT"/Path(src).stem
    p.mkdir(parents=True,exist_ok=True); return p

def analyze(src):
    src=Path(src); typ=detect(src)
    caps={
      "LUA":["detect","normalize","decompile","batch decompile","header recovery","XOR/AES analysis","reconstruct","roundtrip","protect","custom inject"],
      "LUAJIT":["detect","LuaJIT analysis","decompile","strings","forensics"],
      "UE4_PAK":["info","extract","extract single","inject","repack","verify"],
      "ZIP_CONTAINER":["safe extract","inventory","hash","strings","forensics"],
      "UE4_ASSET":["classification","strings","metadata/report","batch"],
      "ELF":["headers","strings","entropy","forensics","hash"],
      "DEX":["strings","entropy","forensics","hash"],
    }.get(typ,["hash","strings","entropy","hex","forensics"])
    return {"engine":ENGINE,"version":VERSION,"name":src.name,"type":typ,"size":src.stat().st_size,"sha256":sha256(src),"read_only":True,"capabilities":caps}

def lua_decompile(src,output=None):
    from alvsia_lua_core import normalize_lua,decompile_auto
    src=Path(src); out=_out(output,src); raw=src.read_bytes()
    norm,meta=normalize_lua(raw); np=out/(src.stem+"_normalized.luac"); np.write_bytes(norm)
    r=decompile_auto(src,out); r.update({"engine":ENGINE,"operation":"lua_decompile","input":str(src),"normalized":str(np),"meta":meta,"input_sha256":sha256(src),"normalized_sha256":sha256(np)})
    return r

def lua_protect(src,output=None,options=None):
    src=Path(src); out=_out(output,src); raw=src.read_bytes(); options=options or {}
    key=hashlib.sha256(str(options.get("key") or os.environ.get("ALVSIA_PROTECT_KEY") or "ALVSIA-SMART-TOOL").encode()).digest()
    nonce=hashlib.sha256(src.name.encode()+raw[:64]).digest()[:16]
    stream=bytearray(); i=0
    while len(stream)<len(raw):
        stream.extend(hashlib.sha256(key+nonce+i.to_bytes(8,"little")).digest()); i+=1
    payload=bytes(a^b for a,b in zip(raw,stream))
    header=b"ALVSLUA2\0"+bytes([1])+nonce+len(raw).to_bytes(8,"little")
    mac=hashlib.sha256(key+header+payload).digest()
    dst=out/(src.stem+".alvslua"); dst.write_bytes(header+mac+payload)
    return {"engine":ENGINE,"operation":"lua_protect","status":"protected","backend":"alvsia-container-v2","input":str(src),"input_sha256":sha256(src),"output":str(dst),"output_sha256":sha256(dst),"output_size":dst.stat().st_size}

def lua_custom_inject(src,output=None,options=None):
    options=options or {}
    target=options.get("target_pak") or options.get("pak")
    if not target: raise ValueError("lua_custom_inject requires a target PAK path")
    pak=Path(target); out=Path(output) if output else pak.parent/(pak.stem+"_lua_injected"+pak.suffix)
    return pak_inject(pak,[{"path":str(src),"target_path":options.get("target_path") or Path(src).name}],out)

def pak_info(src):
    from alvsia_engine import TencentPakFile
    src=Path(src); p=TencentPakFile(src)
    return {"engine":ENGINE,"operation":"pak_info","input":str(src),"version":int(p._pak_info.version),"index_encrypted":bool(p._pak_info.index_encrypted),"index_offset":int(p._pak_info.index_offset),"index_size":int(p._pak_info.index_size),"mount":str(p._mount_point),"file_count":sum(len(v) for v in p._index.values()),"paths":p.list_existing_paths(),"input_sha256":sha256(src)}

def pak_extract(src,output):
    from alvsia_engine import TencentPakFile
    out=Path(output); out.mkdir(parents=True,exist_ok=True); TencentPakFile(src).dump(out)
    return {"engine":ENGINE,"operation":"pak_extract","input":str(src),"output":str(out),"extracted":sum(1 for x in out.rglob("*") if x.is_file()),"input_sha256":sha256(src)}

def pak_inject(src,items,output):
    from alvsia_engine import TencentPakFile
    out=Path(output); out.parent.mkdir(parents=True,exist_ok=True)
    plan=[]
    for x in items:
        fp=Path(x["path"]); 
        if not fp.is_file(): raise FileNotFoundError(fp)
        plan.append({"path":str(fp),"target_path":str(x["target_path"]).replace("\\","/").lstrip("/")})
    TencentPakFile(src).inject_files(plan,out)
    return {"engine":ENGINE,"operation":"pak_inject","input":str(src),"output":str(out),"injected":len(plan),"input_sha256":sha256(src),"output_sha256":sha256(out),"output_size":out.stat().st_size}

def pak_repack(src,modified_dir,output):
    from alvsia_engine import TencentPakFile
    out=Path(output); out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,out)
    ok=TencentPakFile(src).repack_inplace_from_modified_dir(out.open("r+b"))
    return {"engine":ENGINE,"operation":"pak_repack","input":str(src),"modified_dir":str(modified_dir),"output":str(out),"repacked":bool(ok),"output_sha256":sha256(out),"output_size":out.stat().st_size}

def run(src,operation="analyze",output=None,options=None):
    src=Path(src); options=options or {}
    if not src.is_file(): raise FileNotFoundError(src)
    if operation in ("analyze","detect"): return analyze(src)
    if operation in ("lua","decompile","lua_decompile"): return lua_decompile(src,output)
    if operation=="lua_protect": return lua_protect(src,output,options)
    if operation=="lua_custom_inject": return lua_custom_inject(src,output,options)
    typ=detect(src)
    if operation=="pak_info" and typ=="UE4_PAK": return pak_info(src)
    if operation=="pak_extract" and typ=="UE4_PAK": return pak_extract(src,output or _out(None,src)/"extract")
    if operation=="pak_inject" and typ=="UE4_PAK": return pak_inject(src,options.get("inject") or [],output or _out(None,src)/(src.stem+"_injected.pak"))
    if operation=="pak_repack" and typ=="UE4_PAK": return pak_repack(src,options.get("modified_dir") or src.parent,output or _out(None,src)/(src.stem+"_repacked.pak"))
    if operation=="zip_extract":
        from smart_tools import safe_extract_zip; return safe_extract_zip(src,output or _out(None,src)/"extract")
    if operation in ("strings","entropy","hex","forensics","file_report"):
        from smart_tools import run_tool; return run_tool(src,operation,options)
    if operation in ("batch","batch_audit"):
        from smart_tools import batch_audit; return batch_audit(src,output,options)
    if operation=="self_test":
        checks={}
        for mod,names in [("alvsia_engine",("TencentPakFile","PakCrypto","PakCompression")),("alvsia_lua_core",("normalize_lua","decompile_auto")),("smart_tools",("run_tool","batch_audit","safe_extract_zip"))]:
            try: m=__import__(mod); checks[mod]=all(hasattr(m,n) for n in names)
            except Exception as e: checks[mod]=False; checks[mod+"_error"]=str(e)
        checks["smart_engine"]=True
        return {"engine":ENGINE,"version":VERSION,"checks":checks,"ok":all(v is True for k,v in checks.items() if k in ("alvsia_engine","alvsia_lua_core","smart_tools","smart_engine"))}
    raise ValueError(f"operation {operation} unsupported for {typ}")
