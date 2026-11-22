import struct
from pathlib import Path

LUA_XOR_KEY = b""
BGMI_STD = {0:13,1:14,2:15,3:16,4:17,5:18,14:27,16:29,17:0,18:1,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:12,30:30,31:31,32:32,33:33,34:34,36:36,37:37,38:38,39:39,40:40,41:41,42:42,43:43,44:44,45:45}
STD_BGMI = {v:k for k,v in BGMI_STD.items()}
STD_FMT = [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,2,0,2,0,1,0,3]

def process_lua_file(data, is_encrypt=False):
    class W:
        def __init__(self): self.b=bytearray()
        def byte(self,v): self.b.append(int(v)&255)
        def u32(self,v): self.b.extend(struct.pack("<I",int(v)&0xffffffff))
        def i32(self,v): self.b.extend(struct.pack("<i",int(v)))
        def raw(self,d): self.b.extend(d)
    class R:
        def __init__(self,d): self.d=bytes(d); self.p=0
        def need(self,n,what="data"):
            if n<0 or self.p+n>len(self.d): raise ValueError(f"truncated: {what} at {self.p}")
        def byte(self): self.need(1,"byte"); v=self.d[self.p]; self.p+=1; return v
        def u32(self): self.need(4,"u32"); v=struct.unpack_from("<I",self.d,self.p)[0]; self.p+=4; return v
        def i32(self): self.need(4,"i32"); v=struct.unpack_from("<i",self.d,self.p)[0]; self.p+=4; return v
        def raw(self,n): self.need(n,f"raw({n})"); v=self.d[self.p:self.p+n]; self.p+=n; return v
    if len(data)<4 or data[:4]!=b"\x1bLua": raise ValueError("Not a Lua bytecode file")
    ver=data[4]
    if ver in (0x51,0x52,0x54): return data
    if ver!=0x53: raise ValueError(f"Unsupported Lua version byte: 0x{ver:02x}")
    size_t=data[13]
    if size_t!=4: return data
    r=R(data); w=W(); hdr=bytearray(r.raw(33)); hdr[13]=4 if is_encrypt else 8; w.raw(hdr); w.byte(r.byte())
    key=LUA_XOR_KEY
    def r_t24():
        sz=r.byte()
        if sz==255: sz=r.u32()
        if sz==0:return None
        if sz<1: raise ValueError("invalid T24 string size")
        e=r.raw(sz-1)
        return bytes(e[i]^key[i%len(key)] for i in range(len(e))) if key else e
    def r_std():
        sz=r.byte()
        if sz==255:
            r.need(8,"size_t"); sz=struct.unpack_from("<Q",r.d,r.p)[0]; r.p+=8
        if sz==0:return None
        if sz<1: raise ValueError("invalid standard string size")
        return r.raw(sz-1)
    def w_t24(s):
        if s is None:w.byte(0);return
        e=bytes(s)
        if key:e=bytes(e[i]^key[i%len(key)] for i in range(len(e)))
        sz=len(e)+1
        if sz<255:w.byte(sz)
        else:w.byte(255);w.u32(sz)
        w.raw(e)
    def w_std(s):
        if s is None:w.byte(0);return
        e=bytes(s);sz=len(e)+1
        if sz<255:w.byte(sz)
        else:w.byte(255);w.raw(struct.pack("<Q",sz))
        w.raw(e)
    def rs(): return r_std() if is_encrypt else r_t24()
    def ws(s): return w_t24(s) if is_encrypt else w_std(s)
    def translate(raw):
        op=raw&63; A=(raw>>6)&255; C=(raw>>14)&511; B=(raw>>23)&511; Bx=(raw>>14)&0x3ffff; Ax=(raw>>6)&0x3ffffff
        dop=(STD_BGMI if is_encrypt else BGMI_STD).get(op,op)
        if dop<0 or dop>=64:dop=op
        fmt=STD_FMT[dop] if dop<len(STD_FMT) else 0
        if fmt==0:return (dop&63)|(A<<6)|(C<<14)|(B<<23)
        if fmt in (1,2):return (dop&63)|(A<<6)|(Bx<<14)
        if fmt==3:return (dop&63)|(Ax<<6)
        return (dop&63)|(A<<6)|(Bx<<14)
    MAX_COUNT=2_000_000
    def proto(depth=0):
        if depth>50: raise ValueError("Nested prototype too deep")
        ws(rs()); w.i32(r.i32()); ldef=r.i32(); w.i32(ldef)
        w.byte(r.byte());w.byte(r.byte());w.byte(r.byte())
        n=r.u32()
        if n>MAX_COUNT:raise ValueError("invalid code count")
        w.u32(n)
        for _ in range(n):w.u32(translate(r.u32()))
        n=r.u32()
        if n>MAX_COUNT:raise ValueError("invalid constant count")
        w.u32(n)
        for _ in range(n):
            tag=r.byte();w.byte(tag)
            if tag==0:continue
            if tag==1:w.byte(r.byte())
            elif tag in (3,19):w.raw(r.raw(8))
            elif tag in (4,20):ws(rs())
            else:raise ValueError(f"unsupported constant type 0x{tag:02x}")
        n=r.u32()
        if n>MAX_COUNT:raise ValueError("invalid upvalue count")
        w.u32(n)
        for _ in range(n):w.byte(r.byte());w.byte(r.byte())
        n=r.u32()
        if n>MAX_COUNT:raise ValueError("invalid prototype count")
        w.u32(n)
        for _ in range(n):proto(depth+1)
        n=r.u32()
        if n>MAX_COUNT:raise ValueError("invalid line-info count")
        if is_encrypt:
            lines=[r.i32() for _ in range(n)];w.u32(n);prev=ldef
            for ln in lines:w.byte((ln-prev)&255);prev=ln
            w.u32(0)
        else:
            cur=ldef;lines=[]
            for _ in range(n):
                d=r.byte();cur+=d if d<=127 else d-256;lines.append(cur)
            nab=r.u32()
            if nab>MAX_COUNT:raise ValueError("invalid absolute-line count")
            for _ in range(nab):
                pc=r.u32();ln=r.i32()
                if pc<n:lines[pc]=ln
            w.u32(n)
            for ln in lines:w.i32(ln)
        n=r.u32()
        if n>MAX_COUNT:raise ValueError("invalid local count")
        w.u32(n)
        for _ in range(n):ws(rs());w.i32(r.i32());w.i32(r.i32())
        n=r.u32()
        if n>MAX_COUNT:raise ValueError("invalid upvalue-name count")
        w.u32(n)
        for _ in range(n):ws(rs())
    proto()
    return bytes(w.b)

def run_lua_multi_xor(luac_path, out_dir):
    src=Path(luac_path); out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    keys_file=Path(__file__).resolve().parent/"WORK"/"xor_keys.txt"
    keys=[]
    if keys_file.exists():
        for line in keys_file.read_text(errors="ignore").splitlines():
            line=line.strip()
            if line:
                try:keys.append(bytes.fromhex(line))
                except ValueError:keys.append(line.encode())
    if not keys:return {"ok":False,"msg":"No XOR candidates configured in WORK/xor_keys.txt"}
    raw=src.read_bytes();results=[]
    for key in keys:
        dec=bytes(raw[i]^key[i%len(key)] for i in range(len(raw)))
        printable=sum(1 for b in dec[:8192] if 32<=b<127)
        magic=1000 if dec[:4]==b"\x1bLua" or dec[:3]==b"\x1bLJ" else 0
        results.append((printable+magic,key,dec))
    results.sort(key=lambda x:x[0],reverse=True);saved=[]
    for i,(score,key,dec) in enumerate(results[:5]):
        p=out/(src.stem+f"_mxor_{i}_{key.hex()[:8]}.bin");p.write_bytes(dec);saved.append(str(p))
    return {"ok":True,"msg":f"{len(results)} keys tried","out":saved[0] if saved else None,"candidates":saved}
