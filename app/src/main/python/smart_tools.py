from __future__ import annotations
import hashlib, json, math, re, zipfile
from pathlib import Path

PRINTABLE = set(range(32, 127)) | {9, 10, 13}

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def entropy(data):
    if not data: return 0.0
    freq=[0]*256
    for b in data: freq[b]+=1
    n=len(data)
    return round(-sum((c/n)*math.log2(c/n) for c in freq if c),5)

def strings(data,min_len=4,limit=5000):
    out=[]; cur=bytearray()
    for b in data:
        if b in PRINTABLE:
            cur.append(b)
        else:
            if len(cur)>=min_len: out.append(cur.decode("utf-8","replace"))
            cur.clear()
            if len(out)>=limit: break
    if len(cur)>=min_len and len(out)<limit: out.append(cur.decode("utf-8","replace"))
    return out

def hex_preview(path,limit=256):
    data=Path(path).read_bytes()[:limit]
    return {"offset":0,"length":len(data),"hex":data.hex(" "),"ascii":"".join(chr(b) if 32<=b<127 else "." for b in data)}

def signature(path):
    data=Path(path).read_bytes()[:64]
    sigs=[
        (b"PK\x03\x04","ZIP"),(b"\x1bLua","LUA"),(b"\x1bLJ","LUAJIT"),
        (b"\x7fELF","ELF"),(b"MZ","PE"),(b"dex\n","DEX"),(b"\x5a\x6f\x12\xe1","UE4_PAK")
    ]
    # literal escaped signatures above are intentionally corrected below
    if data.startswith(b"PK\x03\x04"): typ="ZIP"
    elif data.startswith(b"\x1bLua"): typ="LUA"
    elif data.startswith(b"\x1bLJ"): typ="LUAJIT"
    elif data.startswith(b"\x7fELF"): typ="ELF"
    elif data.startswith(b"MZ"): typ="PE"
    elif data.startswith(b"dex\n"): typ="DEX"
    elif data.startswith(b"\x5a\x6f\x12\xe1"): typ="UE4_PAK"
    else: typ="UNKNOWN"
    return {"type":typ,"magic":data[:16].hex()}

def run_tool(path,operation,options=None):
    p=Path(path); options=options or {}
    data=p.read_bytes()
    if operation=="strings":
        return {"operation":"strings","count":len(strings(data, int(options.get("min_len",4)))),"strings":strings(data, int(options.get("min_len",4)))}
    if operation=="entropy":
        return {"operation":"entropy","entropy":entropy(data),"size":len(data)}
    if operation=="hex":
        return {"operation":"hex","preview":hex_preview(p,int(options.get("limit",256)))}
    if operation=="file_report":
        return {"name":p.name,"size":p.stat().st_size,"sha256":sha256(p),"signature":signature(p),"entropy":entropy(data[:4*1024*1024])}
    if operation=="forensics":
        report=run_tool(p,"file_report",options)
        report["strings"]=strings(data, int(options.get("min_len",5)), int(options.get("limit",1000)))
        return report
    raise ValueError("unknown tool")

def safe_extract_zip(path,out=None):
    p=Path(path); out=Path(out or p.with_name(p.stem+"_extract")).resolve(); out.mkdir(parents=True,exist_ok=True)
    count=0
    with zipfile.ZipFile(p) as z:
        for name in z.namelist():
            target=(out/name).resolve()
            if target!=out and not str(target).startswith(str(out)+"/"):
                raise ValueError("zip-slip blocked")
            if name.endswith("/"): target.mkdir(parents=True,exist_ok=True); continue
            target.parent.mkdir(parents=True,exist_ok=True)
            with z.open(name) as src,target.open("wb") as dst:
                while True:
                    chunk=src.read(1024*1024)
                    if not chunk: break
                    dst.write(chunk)
            count+=1
    return {"output":str(out),"count":count,"verified":"zip-slip-safe"}

def _walk(root):
    p=Path(root)
    if p.is_file(): return [p]
    return [x for x in p.rglob("*") if x.is_file()]

def batch_audit(path,output=None,options=None):
    root=Path(path); files=_walk(root); rows=[]
    for p in files:
        try:
            data=p.read_bytes()
            rows.append({"path":str(p),"name":p.name,"size":len(data),"sha256":hashlib.sha256(data).hexdigest(),
                         "entropy":entropy(data[:4*1024*1024]),"signature":signature(p)["type"]})
        except Exception as e:
            rows.append({"path":str(p),"error":str(e)})
    report={"engine":"ALVSIA SMART TOOL","operation":"batch_audit","root":str(root),"count":len(rows),"files":rows}
    if output:
        out=Path(output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
        report["report"]=str(out)
    return report
