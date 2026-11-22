# ALVSIA SMART TOOL — unified PAK/crypto core recovered from supplied sources
from __future__ import annotations
import os, struct, zlib, hashlib, math, itertools as it
from pathlib import Path, PurePath
from typing import List, Set, Dict, Tuple, Optional, Union
from functools import lru_cache
from collections import Counter
try:
    import gmalg
except Exception:
    gmalg = None
try:
    from Crypto.Cipher import AES
    from Crypto.Cipher.AES import MODE_CBC
    from Crypto.Hash import SHA1
    from Crypto.Util.Padding import unpad, pad
except Exception:
    AES = MODE_CBC = SHA1 = unpad = pad = None
try:
    from zstandard import ZstdDecompressor, ZstdCompressionDict, ZstdCompressor, DICT_TYPE_AUTO
except Exception:
    ZstdDecompressor = ZstdCompressionDict = ZstdCompressor = DICT_TYPE_AUTO = None
BASE_DIR = Path.cwd()
MAX_OVERFLOW_BYTES = 5
PAK_MAGIC = 0x5A6F12E1
MASK_32 = 0xFFFFFFFF
MSB_1 = 1 << 31
def _alv_require_operation(*args, **kwargs): return True
def _alv_pak_debug_display(value): return str(value)
def _log_path_debug(*args, **kwargs): return None
def to_long_path(path): return str(path)
def get_banner_color(): return "cyan"
def to_fancy(value): return str(value)
class _Console:
    def print(self, *args, **kwargs): return None
console = _Console()
try:
    from rich.panel import Panel
    from rich import box
except Exception:
    Panel = None
    box = None
ZUC_KEY = bytes.fromhex("01010101010101010101010101010101")
ZUC_IV = bytes.fromhex("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
RSA_MOD_1 = bytes.fromhex("CBE8B9F2504050EF9831B719E9A6249A6D238505ADE909BDE78C180DED6072A0C3347B8AF4780E1F212D952D82D4BF7F233C1ECA499E1F9D9A85B4FAD759F54BABC1666C5DE411EA9E4B2374425DD6C6F54333BBC8F2610FE6063E4D0D6C21A671A8F7C3740555E5DC06D4E1691C456DB4116C0C012BF7B206E8311AAAEC689952BF804EF638F09D5822B4117B114208F14DEB459E80CB770E5B0D7978E21F5E6CED4999D3583108221A7AB28B960277ADB5690A332784019D9C195BE4EA9EA0A09459010F236465DE0D59C3EF7324E954E1118D93EE19F299760C2CDB963CE87973EA5ECC9BBE81C27D4C7C8572AC07E9BCEAC9BD72AB7A56A3C0AD736ABCE4")
SIMPLE2_DECRYPT_KEY = bytes.fromhex("E55B4ED1")
SIMPLE1_DECRYPT_KEY = 0x79
SM4_SECRET_4 = "eb691efea914241317a8"
SM4_SECRET_2 = "Q0hVTKey$as*1ZFlQCiA"
