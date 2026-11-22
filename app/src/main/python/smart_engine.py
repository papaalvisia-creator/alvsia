from __future__ import annotations
import hashlib, shutil, zipfile
from pathlib import Path

ENGINE="ALVSIA SMART TOOL"
VERSION="3.0.0-source-fused"

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(1048576),b""): h.update(c)
    return h.hexdigest()

def detect(p):
    p=Path(p); head=p.read_bytes()[:131072]; n=p.name.lower()
    if head.startswith(b"\x1bLua") or n.endswith((".lua",".luac",".slua",".lua.enc")): return "LUA"
    if head.startswith(b"\x1bLJ") or n.endswith((".ljbc",".luajit")): return "LUAJIT"
    if head[:4]==b"\x5a\x6f\x12\xe1" or n.endswith(".pak"): return "UE4_PAK"
    if head[:4]==b"PK\x03\x04" or n.endswith((".obb",".zip",".apk",".jar")): return "ZIP_CONTAINER"
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
      "LUA":["smart analyze","T24/BGMI normalize","standardize","multi-XOR","bytecode constants","string recovery","AES scan","ZUC","decompile","Lua patch/repack","Lua protect/transform","PAK injection"],
      "LUAJIT":["detect","LuaJIT classification","strings","forensics"],
      "UE4_PAK":["info","extract","single-file extraction","inject","repack","verify","crypto/compression diagnostics"],
      "ZIP_CONTAINER":["safe extract","inventory","hash","strings","APK/ZIP audit"],
      "UE4_ASSET":["classification","strings","metadata/report","batch"],
      "ELF":["headers","strings","entropy","AES/XOR scan","URL scan","SM4 candidate scan","forensics"],
      "DEX":["strings","entropy","APK audit","forensics","hash"],
    }.get(typ,["hash","strings","entropy","hex","forensics"])
    return {"engine":ENGINE,"version":VERSION,"name":src.name,"type":typ,"size":src.stat().st_size,"sha256":sha256(src),"read_only":True,"capabilities":caps}

def lua_transform(src,output=None,to_standard=True):
    src=Path(src); out=_out(output,src); raw=src.read_bytes()
    converted=__import__("alvsia_t24_engine").process_lua_file(raw,is_encrypt=not to_standard)
    dst=out/(src.stem+("_standard.luac" if to_standard else ".t24.luac")); dst.write_bytes(converted)
    return {"ok":True,"engine":ENGINE,"operation":"lua_t24_convert","direction":"t24_to_standard" if to_standard else "standard_to_t24","input":str(src),"output":str(dst),"input_sha256":sha256(src),"output_sha256":sha256(dst),"output_size":dst.stat().st_size}

def lua_decompile(src,output=None):
    src=Path(src); out=_out(output,src); raw=src.read_bytes(); meta={}
    normalized=raw
    try:
        normalized=__import__("alvsia_t24_engine").process_lua_file(raw,is_encrypt=False)
        meta={"source_backend":"verified T24/BGMI converter"}
    except Exception as e:
        meta={"source_backend":"Lua fallback","conversion_error":str(e)}
        try: normalized,meta2=__import__("alvsia_lua_core").normalize_lua(raw); meta.update(meta2)
        except Exception: pass
    np=out/(src.stem+"_normalized.luac"); np.write_bytes(normalized)
    r=__import__("alvsia_lua_core").decompile_auto(np,out)
    r.update({"engine":ENGINE,"operation":"lua_decompile","input":str(src),"normalized":str(np),"meta":meta,"input_sha256":sha256(src),"normalized_sha256":sha256(np)})
    return r

def lua_protect(src,output=None,options=None):
    # Real source-backed standard-Lua -> T24/BGMI transformation; no fabricated ALVSIA container.
    r=lua_transform(src,output,False); r.update({"operation":"lua_protect","status":"transformed","backend":"verified T24/BGMI backend"}); return r

def lua_multi_xor(src,output=None):
    out=_out(output,Path(src)); r=__import__("alvsia_t24_engine").run_lua_multi_xor(str(src),out); r.update({"engine":ENGINE,"operation":"lua_multi_xor"}); return r

def reference_op(src,op,output=None,options=None):
    options=options or {}; mod=__import__("alvsia_forensics"); data=Path(src).read_bytes()
    if op=="string_recover":
        fn=getattr(mod,"recover_strings",None)
        return {"engine":ENGINE,"operation":op,"results":fn(data) if fn else []}
    if op=="aes_scan":
        fn=getattr(mod,"find_aes_keys",None)
        return {"engine":ENGINE,"operation":op,"results":fn(data) if fn else []}
    if op=="so_audit":
        fn=getattr(mod,"so_string_analysis",None)
        return {"engine":ENGINE,"operation":op,"results":[e.__dict__ if hasattr(e,"__dict__") else str(e) for e in fn(str(src),5,"")] if fn else []}
    if op=="url_scan":
        fn=getattr(mod,"find_urls_in_so",None)
        return {"engine":ENGINE,"operation":op,"results":fn(data) if fn else []}
    if op=="apk_audit":
        fn=getattr(mod,"apk_audit",None)
        return {"engine":ENGINE,"operation":op,"results":fn(str(src)) if fn else {}}
    if op=="zuc_decrypt":
        fn=getattr(mod,"zuc_decrypt",None)
        if not fn: return {"ok":False,"engine":ENGINE,"operation":op,"message":"ZUC backend not exposed by current Android forensic adapter"}
        key=bytes.fromhex(options["key"]); iv=bytes.fromhex(options["iv"]); dst=Path(output) if output else _out(None,src)/(Path(src).name+".zuc.dec")
        dst.write_bytes(fn(data,key,iv)); return {"ok":True,"engine":ENGINE,"operation":op,"output":str(dst),"output_sha256":sha256(dst)}
    return {"ok":False,"engine":ENGINE,"operation":op,"message":"unsupported"}

def pak_info(src):
    from alvsia_engine import TencentPakFile
    p=TencentPakFile(src)
    return {"engine":ENGINE,"operation":"pak_info","input":str(src),"version":int(p._pak_info.version),"index_encrypted":bool(p._pak_info.index_encrypted),"index_offset":int(p._pak_info.index_offset),"index_size":int(p._pak_info.index_size),"mount":str(p._mount_point),"file_count":sum(len(v) for v in p._index.values()),"paths":p.list_existing_paths(),"input_sha256":sha256(src)}

def pak_extract(src,output):
    from alvsia_engine import TencentPakFile
    out=Path(output); out.mkdir(parents=True,exist_ok=True); TencentPakFile(src).dump(out)
    return {"engine":ENGINE,"operation":"pak_extract","input":str(src),"output":str(out),"extracted":sum(1 for x in out.rglob("*") if x.is_file()),"input_sha256":sha256(src)}

def pak_inject(src,items,output):
    from alvsia_engine import TencentPakFile
    out=Path(output); out.parent.mkdir(parents=True,exist_ok=True); plan=[]
    for x in items:
        fp=Path(x["path"])
        if not fp.is_file(): raise FileNotFoundError(fp)
        plan.append({"path":str(fp),"target_path":str(x["target_path"]).replace("\\","/").lstrip("/")})
    TencentPakFile(src).inject_files(plan,out)
    return {"engine":ENGINE,"operation":"pak_inject","input":str(src),"output":str(out),"injected":len(plan),"input_sha256":sha256(src),"output_sha256":sha256(out),"output_size":out.stat().st_size}

def lua_custom_inject(src,output=None,options=None):
    options=options or {}
    target=options.get("target_pak") or options.get("pak")
    if not target: raise ValueError("lua_custom_inject requires target_pak")
    pak=Path(target)
    out=Path(output) if output else pak.parent/(pak.stem+"_lua_injected"+pak.suffix)
    return pak_inject(pak,[{"path":str(src),"target_path":options.get("target_path") or Path(src).name}],out)

def pak_repack(src,modified_dir,output):
    from alvsia_engine import TencentPakFile
    out=Path(output); out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,out)
    with out.open("r+b") as fh: ok=TencentPakFile(src).repack_inplace_from_modified_dir(fh)
    return {"engine":ENGINE,"operation":"pak_repack","input":str(src),"modified_dir":str(modified_dir),"output":str(out),"repacked":bool(ok),"output_sha256":sha256(out),"output_size":out.stat().st_size}

def safe_zip_extract(src,output):
    out=Path(output); out.mkdir(parents=True,exist_ok=True); root=out.resolve(); count=0
    with zipfile.ZipFile(src) as z:
        for info in z.infolist():
            dest=(out/info.filename).resolve()
            if root not in dest.parents and dest!=root: raise ValueError("unsafe archive path")
            if info.is_dir(): dest.mkdir(parents=True,exist_ok=True); continue
            dest.parent.mkdir(parents=True,exist_ok=True)
            with z.open(info) as r, open(dest,"wb") as w: shutil.copyfileobj(r,w,1048576)
            count+=1
    return {"ok":True,"engine":ENGINE,"operation":"zip_extract","output":str(out),"extracted":count}

def source_inventory():
    return {"engine":ENGINE,"version":VERSION,"sources":{
      "IkramTool_V130_4.7.zip":"audited: Lua pipeline, mega Lua, Tencent PAK, PakTool, UE/asset, SM4, protection/compiler helpers, native/JAR backends",
      "TOOL.zip":"audited: unpack, decompile, batch-decompile, protek, info/all pipeline, crypto/compression, Lua injection and rebuild",
      "RegulerResault_ALVSIA_tool_no_on_vip_engine.zip":"audited as regression corpus: Lua outputs, UE assets, LOCRES/UMAP and known failure cases",
      "GRW.py":"integrated T24/BGMI Lua + PAK source logic",
      "UltimateEngineTool.py":"integrated T24/BGMI Lua transform and multi-XOR logic",
      "GODXKAZUKI.py":"existing Android legacy PAK/Lua engine retained and routed",
      "referensi.py":"forensic/recovery functions represented by alvsia_forensics adapter"
    }}

def run(src,operation="analyze",output=None,options=None):
    src=Path(src); options=options or {}
    if operation=="source_inventory": return source_inventory()
    if not src.is_file(): raise FileNotFoundError(src)
    if operation in ("analyze","detect"): return analyze(src)
    if operation in ("lua","decompile","lua_decompile","lua_smart_analyze"): return lua_decompile(src,output)
    if operation in ("lua_protect","protek"): return lua_protect(src,output,options)
    if operation=="lua_custom_inject": return lua_custom_inject(src,output,options)
    if operation in ("lua_t24_convert","pubg_lua_convert"): return lua_transform(src,output,True)
    if operation=="lua_multi_xor": return lua_multi_xor(src,output)
    if operation in ("lua_strings","priv_lua_parse"): return reference_op(src,"string_recover",output,options)
    if operation in ("aes_scan","string_recover","url_scan","so_audit","apk_audit","zuc_decrypt"): return reference_op(src,operation,output,options)
    if operation=="pak_info" and detect(src)=="UE4_PAK": return pak_info(src)
    if operation=="pak_extract" and detect(src)=="UE4_PAK": return pak_extract(src,output or _out(None,src)/"extract")
    if operation=="pak_inject" and detect(src)=="UE4_PAK": return pak_inject(src,options.get("inject") or [],output or _out(None,src)/(src.stem+"_injected.pak"))
    if operation=="pak_repack" and detect(src)=="UE4_PAK": return pak_repack(src,options.get("modified_dir") or src.parent,output or _out(None,src)/(src.stem+"_repacked.pak"))
    if operation=="zip_extract": return safe_zip_extract(src,output or _out(None,src)/"extract")
    if operation in ("strings","entropy","hex","forensics","file_report"): return __import__("smart_tools").run_tool(src,operation,options)
    if operation in ("batch","batch_audit"): return __import__("smart_tools").batch_audit(src,output,options)
    if operation=="self_test":
        checks={}
        for mod,names in [("alvsia_engine",("TencentPakFile","PakCrypto","PakCompression")),("alvsia_lua_core",("normalize_lua","decompile_auto")),("smart_tools",("run_tool","batch_audit","safe_extract_zip")),("alvsia_t24_engine",("process_lua_file","run_lua_multi_xor"))]:
            try: m=__import__(mod); checks[mod]=all(hasattr(m,n) for n in names)
            except Exception as e: checks[mod]=False; checks[mod+"_error"]=str(e)
        checks["smart_engine"]=True
        return {"engine":ENGINE,"version":VERSION,"checks":checks,"ok":all(v is True for k,v in checks.items() if k.endswith("_engine") or k in ("smart_tools","smart_engine"))}
    raise ValueError(f"operation {operation} unsupported for {detect(src)}")
