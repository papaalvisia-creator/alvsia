# ALVSIA SMART TOOL — Lua conversion/decode core
from __future__ import annotations
import os,struct
def _load_xor_key() -> bytes:
    env_key = os.environ.get('BGMI_XOR_KEY')
    if env_key:
        try:
            key_bytes = bytes.fromhex(env_key.replace(' ', '').replace(':', '').replace('-', ''))
            if len(key_bytes) == 32: return key_bytes
        except ValueError: pass
    return bytes([0x11, 0x21, 0x36, 0x47, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84, 0x90, 0xD8, 0xAB, 0x00, 0x8C, 0x35, 0x26, 0x1A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x15, 0x07, 0xD0, 0x2C, 0x1E, 0x8F, 0xF6, 0xC8])

STRING_XOR_KEY = _load_xor_key()

_BGMI_TO_STD = [13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,0,1,2,3,4,5,6,7,8,9,10,11,12,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46]
BGMI_TO_STD = _BGMI_TO_STD + [i for i in range(len(_BGMI_TO_STD), 64)]
STD_TO_BGMI = {v: k for k, v in enumerate(BGMI_TO_STD) if k < len(BGMI_TO_STD)}
STD_FMT = [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,2,0,2,0,1,0,3]
iABC, iABx, iAsBx, iAx = 0, 1, 2, 3
HEADER_SIZE = 33

class BinaryReader:
    def __init__(self, data: bytes, sizet: int = 4):
        self.data = bytearray(data); self.pos = 0; self.sizet = sizet
    def byte(self) -> int:
        if self.pos >= len(self.data): raise EOFError()
        v = self.data[self.pos]; self.pos += 1; return v
    def int32(self) -> int:
        if self.pos + 4 > len(self.data): raise EOFError()
        v = struct.unpack_from('<i', self.data, self.pos)[0]; self.pos += 4; return v
    def uint32(self) -> int:
        if self.pos + 4 > len(self.data): raise EOFError()
        v = struct.unpack_from('<I', self.data, self.pos)[0]; self.pos += 4; return v
    def double(self) -> float:
        if self.pos + 8 > len(self.data): raise EOFError()
        v = struct.unpack_from('<d', self.data, self.pos)[0]; self.pos += 8; return v
    def int64(self) -> int:
        if self.pos + 8 > len(self.data): raise EOFError()
        v = struct.unpack_from('<q', self.data, self.pos)[0]; self.pos += 8; return v
    def bytes(self, n: int) -> bytes:
        if self.pos + n > len(self.data): raise EOFError()
        v = self.data[self.pos:self.pos+n]; self.pos += n; return bytes(v)
    def pubg_string(self) -> Optional[str]:
        sz = self.byte()
        if sz == 0xFF: sz = self.uint32()
        if sz == 0: return None
        sz -= 1
        enc = self.bytes(sz)
        dec = bytes(enc[i] ^ STRING_XOR_KEY[i % 32] for i in range(len(enc)))
        try: return dec.decode('utf-8', errors='replace')
        except Exception: return dec.decode('latin-1')
    def std_string(self) -> Optional[str]:
        sz = self.byte()
        if sz == 0xFF:
            if self.sizet == 8:
                if self.pos + 8 > len(self.data): raise EOFError()
                sz = struct.unpack_from('<Q', self.data, self.pos)[0]; self.pos += 8
            else: sz = self.uint32()
        if sz == 0: return None
        sz -= 1
        raw = self.bytes(sz)
        try: return raw.decode('utf-8', errors='replace')
        except Exception: return raw.decode('latin-1')

class BinaryWriter:
    def __init__(self): self.buf = bytearray()
    def byte(self, v): self.buf.append(v & 0xFF)
    def int32(self, v): self.buf.extend(struct.pack('<i', v))
    def uint32(self, v): self.buf.extend(struct.pack('<I', v))
    def int64(self, v): self.buf.extend(struct.pack('<q', v))
    def double(self, v): self.buf.extend(struct.pack('<d', v))
    def raw(self, data): self.buf.extend(data)
    def lua_string(self, s: Optional[str], is_pubg: bool = False):
        if s is None: self.byte(0); return
        e = s.encode('utf-8') if isinstance(s, str) else s
        sz = len(e) + 1
        if sz < 0xFF: self.byte(sz)
        else: self.byte(0xFF); self.uint32(sz)
        if is_pubg:
            enc = bytes(e[i] ^ STRING_XOR_KEY[i % 32] for i in range(len(e)))
            self.raw(enc)
        else: self.raw(e)
    def lua_inst(self, op, A, B, C, Bx, sBx, Ax, fmt):
        op &= 0x3F
        if   fmt == iABC:  r = op | ((A & 0xFF)<<6) | ((C & 0x1FF)<<14) | ((B & 0x1FF)<<23)
        elif fmt == iABx:  r = op | ((A & 0xFF)<<6) | ((Bx & 0x3FFFF)<<14)
        elif fmt == iAsBx: r = op | ((A & 0xFF)<<6) | (((sBx+131071) & 0x3FFFF)<<14)
        elif fmt == iAx:   r = op | ((Ax & 0x3FFFFFF)<<6)
        else: r = 0
        self.uint32(r)
    def get_data(self) -> bytes: return bytes(self.buf)

def _convert_function(reader: BinaryReader, writer: BinaryWriter, to_std: bool = True):
    src = reader.pubg_string() if to_std else reader.std_string()
    writer.lua_string(src, is_pubg=(not to_std))
    linedefined = reader.int32(); writer.int32(linedefined)
    writer.int32(reader.int32())
    writer.byte(reader.byte()); writer.byte(reader.byte()); writer.byte(reader.byte())
    csz = reader.uint32(); writer.uint32(csz)
    opmap = BGMI_TO_STD if to_std else STD_TO_BGMI
    for _ in range(csz):
        raw = reader.uint32()
        bop = raw & 0x3F; A = (raw >> 6) & 0xFF; B = (raw >> 23) & 0x1FF; C = (raw >> 14) & 0x1FF
        Bx = (raw >> 14) & 0x3FFFF; sBx = Bx - 131071; Ax = (raw >> 6) & 0x3FFFFFF
        sop = opmap[bop] if bop < len(opmap) else bop
        fmt = STD_FMT[sop] if sop < len(STD_FMT) else iABC
        writer.lua_inst(sop, A, B, C, Bx, sBx, Ax, fmt)
    nk = reader.uint32(); writer.uint32(nk)
    for _ in range(nk):
        t = reader.byte(); writer.byte(t)
        if t == 0: pass
        elif t == 1: writer.byte(reader.byte())
        elif t == 3: writer.double(reader.double())
        elif t == 19: writer.int64(reader.int64())
        elif t in (4, 20):
            s = reader.pubg_string() if to_std else reader.std_string()
            writer.lua_string(s, is_pubg=(not to_std))
        else: raise ValueError(f"Unknown constant type 0x{t:02X}")
    nups = reader.uint32(); writer.uint32(nups)
    for _ in range(nups): writer.byte(reader.byte()); writer.byte(reader.byte())
    npts = reader.uint32(); writer.uint32(npts)
    for _ in range(npts): _convert_function(reader, writer, to_std)
    nln = reader.uint32()
    if to_std:
        lines = []; cur = linedefined
        for _ in range(nln):
            d = reader.byte()
            cur += d if d <= 127 else d - 256
            lines.append(cur)
        writer.uint32(len(lines))
        for ln in lines: writer.int32(ln)
        nab = reader.uint32()
        for _ in range(nab): reader.uint32(); reader.uint32()
    else:
        lines = [reader.int32() for _ in range(nln)]
        writer.uint32(len(lines))
        prev = linedefined
        for ln in lines:
            delta = ln - prev
            if -128 <= delta <= 127: writer.byte(delta & 0xFF)
            else: writer.byte(0x00); writer.int32(delta)
            prev = ln
        writer.uint32(0)
    nloc = reader.uint32(); writer.uint32(nloc)
    for _ in range(nloc):
        s = reader.pubg_string() if to_std else reader.std_string()
        writer.lua_string(s, is_pubg=(not to_std))
        writer.int32(reader.int32()); writer.int32(reader.int32())
    nupn = reader.uint32(); writer.uint32(nupn)
    for _ in range(nupn):
        s = reader.pubg_string() if to_std else reader.std_string()
        writer.lua_string(s, is_pubg=(not to_std))

def bgmi_to_std(data: bytes) -> bytes:
    if data[:4] != b'\x1bLua': raise ValueError("Not a valid Lua bytecode file")
    reader = BinaryReader(data, sizet=4); writer = BinaryWriter()
    hdr = bytearray(data[:HEADER_SIZE]); hdr[13] = 4
    writer.raw(hdr); reader.pos = HEADER_SIZE
    nibble_flag = reader.byte(); writer.byte(nibble_flag)
    _convert_function(reader, writer, to_std=True)
    return writer.get_data()

def std_to_bgmi(data: bytes) -> bytes:
    if data[:4] != b'\x1bLua': raise ValueError("Not a valid Lua bytecode file")
    sizet = data[13] if data[13] in (4, 8) else 4
    reader = BinaryReader(data, sizet=sizet); writer = BinaryWriter()
    hdr = bytearray(data[:HEADER_SIZE]); hdr[13] = 4
    writer.raw(hdr); reader.pos = HEADER_SIZE
    nibble_flag = reader.byte(); writer.byte(nibble_flag)
    _convert_function(reader, writer, to_std=False)
    return writer.get_data()


import os, subprocess, shutil, tempfile
from pathlib import Path

def _run_external(cmd, timeout=180):
    try:
        p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout,check=False)
        return p.returncode, p.stdout.decode('utf-8','replace')
    except Exception as e:
        return -1, str(e)

def validate_lua_bytes(data):
    if data.startswith(b'\x1bLua'):
        v=data[4] if len(data)>4 else 0
        return {'valid':True,'family':'lua','version':'0x%02x'%v,'format':data[5] if len(data)>5 else None}
    if data.startswith(b'\x1bLJ'):
        return {'valid':True,'family':'luajit','version':'0x%02x'%(data[3] if len(data)>3 else 0)}
    return {'valid':False,'family':'unknown','version':'unknown'}

def normalize_lua(data):
    meta=validate_lua_bytes(data)
    if not meta['valid']: return data, meta
    if data.startswith(b'\x1bLua') and len(data)>=33 and data[13] == 4:
        try: return bgmi_to_std(data), {**meta,'converted':'bgmi_to_standard'}
        except Exception: pass
    return data, {**meta,'converted':None}

def decompile_auto(src, out_dir):
    src=Path(src); out_dir=Path(out_dir); out_dir.mkdir(parents=True,exist_ok=True)
    data=src.read_bytes(); normalized,meta=normalize_lua(data)
    if normalized != data:
        tmp=out_dir/(src.stem+'.standard.luac'); tmp.write_bytes(normalized); target=tmp
    else: target=src
    if meta.get('family')=='lua' and data.startswith(b'--'):
        out=out_dir/(src.stem+'.lua'); out.write_bytes(data); return {'ok':True,'status':'source','out':str(out),'meta':meta}
    candidates=[]
    root=Path(__file__).resolve().parent
    for name in ('luadec.fresh','luadec','unluac_rs'):
        p=root/name
        if p.exists(): candidates.append(p)
    for tool in candidates:
        out=out_dir/(src.stem+'_decompiled.lua')
        rc,text=_run_external([str(tool),str(target)],180)
        if rc==0 and text.strip(): out.write_text(text,encoding='utf-8'); return {'ok':True,'status':'decompiled','out':str(out),'tool':tool.name,'meta':meta}
    # Java decompiler is optional; use it only when a runtime and jar are actually bundled.
    jar=root/'unluac.jar'; java=shutil.which('java')
    if jar.exists() and java:
        rc,text=_run_external([java,'-jar',str(jar),str(target)],180)
        out=out_dir/(src.stem+'_decompiled.lua')
        if rc==0 and text.strip(): out.write_text(text,encoding='utf-8'); return {'ok':True,'status':'decompiled','out':str(out),'tool':'bundled-java','meta':meta}
    return {'ok':False,'status':'unsupported','out':None,'meta':meta,'message':'No compatible decompiler runtime bundled; normalized bytecode is available for the next tier.'}
