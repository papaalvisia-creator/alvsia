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
SM4_SECRET_NEW = ["xG2qW5lP7lV2iN5fN5pG","xT1cJ6dL5wC0kK1rB4dK","qC4jS5bZ6fL5xE6nD4zA","gD4jQ2aL3bS3lC3xT0iW","xU1yQ8wE9zY3gZ3bT5aE","uQ3cO2dX7xY4xU7gH7iS","gW1fR0jK6wQ4oN0oK1kZ","aJ4pV7iZ7pU4wP2aC2cZ","cX6jT3cM2oT3vK0kJ1qN","iT2vS0cS6yT6cZ1sE1lO","hM1pH9iY8wM9hT4lN5uJ","kG6bC8jK0fL0dE4sH4mL","dB6lB3vE0eZ8wM8rI0aC","tP7sP7nI9rA2vQ4cV5yQ","aT0cL1yN4pT3sZ7eM2vY","uV6fU8fC9zN3mP5dH8mN","rT6aQ6oZ1yM0gO5tO1aN","jU5bH7lQ0fM9hK2kI0oF","iQ0eM0mJ7uT0kV6kL5zY","wD2rP3lP9xF4mE1eC5jS","rG0lR2rZ5vM6mW5lM1rR","fO3kW1fE6eD0pU1kY7xK"]
ZUC_KEY = bytes.fromhex('01010101010101010101010101010101')
ZUC_IV = bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
RSA_MOD_1 = bytes.fromhex('CBE8B9F2504050EF9831B719E9A6249A6D238505ADE909BDE78C180DED6072A0C3347B8AF4780E1F212D952D82D4BF7F233C1ECA499E1F9D9A85B4FAD759F54BABC1666C5DE411EA9E4B2374425DD6C6F54333BBC8F2610FE6063E4D0D6C21A671A8F7C3740555E5DC06D4E1691C456DB4116C0C012BF7B206E8311AAAEC689952BF804EF638F09D5822B4117B114208F14DEB459E80CB770E5B0D7978E21F5E6CED4999D3583108221A7AB28B960277ADB5690A332784019D9C195BE4EA9EA0A09459010F236465DE0D59C3EF7324E954E1118D93EE19F299760C2CDB963CE87973EA5ECC9BBE81C27D4C7C8572AC07E9BCEAC9BD72AB7A56A3C0AD736ABCE4')
RSA_MOD_2 = bytes.fromhex('7F58E8A39A4DA4E87357DDD650EAA16D3B5CE95B213D1030A662566444796A78A84AE9AC3DBFFDE7F41094896696835DAF13B89E6EC2B84963B1B1BAF7151DA245C3FBFAE2A6AE18B2684D03F9229DE2C91440F2A3A3BCDE1E5680C16722A88039C73560D5D43F4B6562C2EEA5B1D926D86B51108A2643C70FB74D6442CE3A08339B8FD8F660AE88129B7AB8C46F2FA58124485CCCB1E987B05A6DA65A01858ED3F89905449AE42BB07290FCB9994BF22E26610BCABB9804783A3B9587917F3D97316EDDA15C5E13F79066407B55A93B291B68A4AC42A98D6E35FED84B14A792D154E62028DDAD20FC301951E5924BE9AD62FB719DD94CC30CAB871BEC4377A8')
SIMPLE1_DECRYPT_KEY = 121
SIMPLE2_DECRYPT_KEY = bytes.fromhex('E55B4ED1')
SIMPLE2_BLOCK_SIZE = 4
SM4_SECRET_4 = 'eb691efea914241317a8'
SM4_SECRET_2 = 'Q0hVTKey$as*1ZFlQCiA'
SM4_SECRET_NEW = ['xG2qW5lP7lV2iN5fN5pG', 'xT1cJ6dL5wC0kK1rB4dK', 'qC4jS5bZ6fL5xE6nD4zA', 'gD4jQ2aL3bS3lC3xT0iW', 'xU1yQ8wE9zY3gZ3bT5aE', 'uQ3cO2dX7xY4xU7gH7iS', 'gW1fR0jK6wQ4oN0oK1kZ', 'aJ4pV7iZ7pU4wP2aC2cZ', 'cX6jT3cM2oT3vK0kJ1qN', 'iT2vS0cS6yT6cZ1sE1lO', 'hM1pH9iY8wM9hT4lN5uJ', 'kG6bC8jK0fL0dE4sH4mL', 'dB6lB3vE0eZ8wM8rI0aC', 'tP7sP7nI9rA2vQ4cV5yQ', 'aT0cL1yN4pT3sZ7eM2vY', 'uV6fU8fC9zN3mP5dH8mN', 'rT6aQ6oZ1yM0gO5tO1aN', 'jU5bH7lQ0fM9hK2kI0oF', 'iQ0eM0mJ7uT0kV6kL5zY']
EM_SIMPLE1 = 1
EM_SIMPLE2 = 16
EM_SM4_2 = 2
EM_SM4_4 = 4
EM_SM4_NEW_BASE = 31
EM_SM4_NEW_MASK = ~EM_SM4_NEW_BASE
EM_UNKNOWN_17 = 17
CM_NONE = 0
CM_ZLIB = 1
CM_ZSTD = 6
CM_ZSTD_DICT = 8
CM_MASK = 15


class SM4:
    """SM4 Algorithm Implementation."""
    _S_BOX = bytes([52, 102, 37, 116, 137, 120, 228, 169, 90, 65, 188, 122, 214, 22, 33, 35, 77, 97, 218, 148, 155, 223, 19, 60, 105, 58, 49, 10, 95, 215, 153, 149, 241, 174, 114, 61, 7, 96, 36, 182, 152, 238, 196, 162, 45, 136, 221, 141, 4, 234, 187, 17, 202, 62, 93, 161, 246, 63, 176, 151, 128, 71, 43, 166, 230, 247, 217, 177, 89, 192, 124, 190, 84, 40, 183, 126, 79, 248, 67, 110, 160, 80, 14, 245, 144, 184, 251, 163, 123, 98, 25, 70, 3, 42, 185, 143, 159, 119, 180, 91, 131, 135, 8, 235, 226, 30, 66, 240, 15, 232, 113, 106, 117, 173, 85, 31, 181, 171, 51, 250, 127, 21, 189, 133, 216, 6, 104, 179, 82, 48, 72, 11, 0, 237, 239, 178, 87, 142, 231, 108, 213, 229, 46, 83, 130, 5, 249, 129, 244, 86, 191, 140, 75, 227, 219, 74, 145, 76, 44, 211, 64, 41, 78, 32, 20, 54, 121, 9, 111, 209, 55, 224, 57, 12, 138, 146, 56, 18, 53, 109, 225, 253, 147, 154, 23, 212, 201, 156, 107, 132, 38, 157, 175, 118, 193, 158, 208, 150, 197, 203, 233, 115, 73, 210, 205, 100, 195, 199, 1, 125, 243, 172, 252, 222, 164, 68, 50, 27, 194, 186, 28, 2, 198, 39, 69, 139, 242, 24, 167, 16, 81, 29, 200, 207, 99, 255, 47, 13, 88, 206, 101, 165, 220, 26, 59, 134, 254, 34, 92, 168, 94, 103, 170, 236, 112, 204])
    _FK = [1184304796, 1270900830, 1493524870, 3164752158]
    _CK = [964907, 973793155, 2654690407, 2916866751, 2071233739, 1226140771, 3348805095, 2045549823, 388349611, 800627875, 612403927, 3721562911, 1195432523, 3150178931, 612053223, 2445162591, 67183755, 1174197155, 1393249511, 3331183455, 3822152747, 1332317203, 1804781383, 1990130463, 1282653851, 3376591251, 2910902311, 925872959, 332098219, 735840931, 396665415, 3588844719]

    @staticmethod
    def ROL32(x, n):
        return x << n & 4294967295 | x >> 32 - n

    @staticmethod
    def _BS(X):
        return SM4._S_BOX[X >> 24 & 255] << 24 | SM4._S_BOX[X >> 16 & 255] << 16 | SM4._S_BOX[X >> 8 & 255] << 8 | SM4._S_BOX[X & 255]

    @staticmethod
    def _T0(X):
        X = SM4._BS(X)
        return X ^ SM4.ROL32(X, 2) ^ SM4.ROL32(X, 10) ^ SM4.ROL32(X, 18) ^ SM4.ROL32(X, 24)

    @staticmethod
    def _T1(X):
        X = SM4._BS(X)
        return X ^ SM4.ROL32(X, 13) ^ SM4.ROL32(X, 23)

    @staticmethod
    def _key_expand(key: bytes, rkey: list):
        _s675e6878edf5 = int.from_bytes(key[0:4], 'big') ^ SM4._FK[0]
        _s76e8209e75a7 = int.from_bytes(key[4:8], 'big') ^ SM4._FK[1]
        _s37d5d30b5139 = int.from_bytes(key[8:12], 'big') ^ SM4._FK[2]
        _s8c360ca2c48a = int.from_bytes(key[12:16], 'big') ^ SM4._FK[3]
        for _sc04fd27b9cdf in range(0, 32, 4):
            _s675e6878edf5 = _s675e6878edf5 ^ SM4._T1(_s76e8209e75a7 ^ _s37d5d30b5139 ^ _s8c360ca2c48a ^ SM4._CK[_sc04fd27b9cdf])
            rkey[_sc04fd27b9cdf] = _s675e6878edf5
            _s76e8209e75a7 = _s76e8209e75a7 ^ SM4._T1(_s37d5d30b5139 ^ _s8c360ca2c48a ^ _s675e6878edf5 ^ SM4._CK[_sc04fd27b9cdf + 1])
            rkey[_sc04fd27b9cdf + 1] = _s76e8209e75a7
            _s37d5d30b5139 = _s37d5d30b5139 ^ SM4._T1(_s8c360ca2c48a ^ _s675e6878edf5 ^ _s76e8209e75a7 ^ SM4._CK[_sc04fd27b9cdf + 2])
            rkey[_sc04fd27b9cdf + 2] = _s37d5d30b5139
            _s8c360ca2c48a = _s8c360ca2c48a ^ SM4._T1(_s675e6878edf5 ^ _s76e8209e75a7 ^ _s37d5d30b5139 ^ SM4._CK[_sc04fd27b9cdf + 3])
            rkey[_sc04fd27b9cdf + 3] = _s8c360ca2c48a

    @classmethod
    def key_length(cls):
        return 16

    @classmethod
    def block_length(cls):
        return 16

    def __init__(self, key: bytes):
        if len(key) != self.key_length():
            raise ValueError(f'Key must be {self.key_length()} bytes')
        self._key = key
        self._rkey = [0] * 32
        SM4._key_expand(self._key, self._rkey)
        self._block_buffer = bytearray()

    def encrypt(self, block: bytes) -> bytes:
        if len(block) != self.block_length():
            raise ValueError(f'Block must be {self.block_length()} bytes')
        _sc1c516bb51fa = self._rkey
        _s575e5e04834a = int.from_bytes(block[0:4], 'big')
        _sdc8fde238313 = int.from_bytes(block[4:8], 'big')
        _s9ca2b966fe13 = int.from_bytes(block[8:12], 'big')
        _s4d48730788eb = int.from_bytes(block[12:16], 'big')
        for _s4db069a1d720 in range(0, 32, 4):
            _s575e5e04834a = _s575e5e04834a ^ SM4._T0(_sdc8fde238313 ^ _s9ca2b966fe13 ^ _s4d48730788eb ^ _sc1c516bb51fa[_s4db069a1d720])
            _sdc8fde238313 = _sdc8fde238313 ^ SM4._T0(_s9ca2b966fe13 ^ _s4d48730788eb ^ _s575e5e04834a ^ _sc1c516bb51fa[_s4db069a1d720 + 1])
            _s9ca2b966fe13 = _s9ca2b966fe13 ^ SM4._T0(_s4d48730788eb ^ _s575e5e04834a ^ _sdc8fde238313 ^ _sc1c516bb51fa[_s4db069a1d720 + 2])
            _s4d48730788eb = _s4d48730788eb ^ SM4._T0(_s575e5e04834a ^ _sdc8fde238313 ^ _s9ca2b966fe13 ^ _sc1c516bb51fa[_s4db069a1d720 + 3])
        _see62ae2378cb = self._block_buffer
        _see62ae2378cb.clear()
        _see62ae2378cb.extend(_s4d48730788eb.to_bytes(4, 'big'))
        _see62ae2378cb.extend(_s9ca2b966fe13.to_bytes(4, 'big'))
        _see62ae2378cb.extend(_sdc8fde238313.to_bytes(4, 'big'))
        _see62ae2378cb.extend(_s575e5e04834a.to_bytes(4, 'big'))
        return bytes(_see62ae2378cb)

    def decrypt(self, block: bytes) -> bytes:
        if len(block) != self.block_length():
            raise ValueError(f'Block must be {self.block_length()} bytes')
        _s4fac0e604588 = self._rkey
        _s9b8e65aabd3c = int.from_bytes(block[0:4], 'big')
        _s299d3838170f = int.from_bytes(block[4:8], 'big')
        _sc7c6fe8df4be = int.from_bytes(block[8:12], 'big')
        _s4b763ba958ab = int.from_bytes(block[12:16], 'big')
        for _sda06635f34a6 in range(0, 32, 4):
            _s9b8e65aabd3c = _s9b8e65aabd3c ^ SM4._T0(_s299d3838170f ^ _sc7c6fe8df4be ^ _s4b763ba958ab ^ _s4fac0e604588[31 - _sda06635f34a6])
            _s299d3838170f = _s299d3838170f ^ SM4._T0(_sc7c6fe8df4be ^ _s4b763ba958ab ^ _s9b8e65aabd3c ^ _s4fac0e604588[30 - _sda06635f34a6])
            _sc7c6fe8df4be = _sc7c6fe8df4be ^ SM4._T0(_s4b763ba958ab ^ _s9b8e65aabd3c ^ _s299d3838170f ^ _s4fac0e604588[29 - _sda06635f34a6])
            _s4b763ba958ab = _s4b763ba958ab ^ SM4._T0(_s9b8e65aabd3c ^ _s299d3838170f ^ _sc7c6fe8df4be ^ _s4fac0e604588[28 - _sda06635f34a6])
        _s0c55977ac20c = self._block_buffer
        _s0c55977ac20c.clear()
        _s0c55977ac20c.extend(_s4b763ba958ab.to_bytes(4, 'big'))
        _s0c55977ac20c.extend(_sc7c6fe8df4be.to_bytes(4, 'big'))
        _s0c55977ac20c.extend(_s299d3838170f.to_bytes(4, 'big'))
        _s0c55977ac20c.extend(_s9b8e65aabd3c.to_bytes(4, 'big'))
        return bytes(_s0c55977ac20c)

class Misc:

    @staticmethod
    def pad_to_n(data: bytes, n: int) -> bytes:
        assert n > 0
        _sdf8ea9172aca = n - len(data) % n
        if _sdf8ea9172aca == n:
            return data
        return data + b'\x00' * _sdf8ea9172aca

    @staticmethod
    def align_up(x: int, n: int) -> int:
        return (x + n - 1) // n * n

class PakReader:

    def __init__(self, buffer, cursor=0):
        self._buffer = buffer
        self._cursor = cursor

    def u1(self, move_cursor=True) -> int:
        return self.unpack('B', move_cursor=move_cursor)[0]

    def u4(self, move_cursor=True) -> int:
        return self.unpack('<I', move_cursor=move_cursor)[0]

    def u8(self, move_cursor=True) -> int:
        return self.unpack('<Q', move_cursor=move_cursor)[0]

    def i1(self, move_cursor=True) -> int:
        return self.unpack('b', move_cursor=move_cursor)[0]

    def i4(self, move_cursor=True) -> int:
        return self.unpack('<i', move_cursor=move_cursor)[0]

    def i8(self, move_cursor=True) -> int:
        return self.unpack('<q', move_cursor=move_cursor)[0]

    def s(self, n: int, move_cursor=True) -> bytes:
        return self.unpack(f'{n}s', move_cursor=move_cursor)[0]

    def unpack(self, f: Union[str, bytes], offset=0, move_cursor=True):
        _s6cb15be33ea2 = struct.unpack_from(f, self._buffer, self._cursor + offset)
        if move_cursor:
            self._cursor += struct.calcsize(f)
        return _s6cb15be33ea2

    def string(self, move_cursor=True) -> str:
        _s0cc99f169bdd = self.i4(move_cursor=move_cursor)
        if _s0cc99f169bdd == 0:
            return str()
        assert _s0cc99f169bdd > 0
        _s416c98aeba25 = 0 if move_cursor else 4
        return self.unpack(f'{_s0cc99f169bdd}s', offset=_s416c98aeba25, move_cursor=move_cursor)[0].rstrip(b'\x00').decode()

class PakInfo:

    def __init__(self, buffer, keystream: List[int]):

        def decrypt_index_encrypted(x: int) -> int:
            _s6bab90fc4ab8 = 255
            return (x ^ keystream[3]) & _s6bab90fc4ab8

        def decrypt_magic(x: int) -> int:
            return x ^ keystream[2]

        def decrypt_index_hash(x: bytes) -> bytes:
            key = struct.pack('<5I', *keystream[4:][:5])
            assert len(x) == len(key)
            return bytes((a ^ b for a, b in zip(x, key)))

        def decrypt_index_size(x: int) -> int:
            return x ^ (keystream[10] << 32 | keystream[11])

        def decrypt_index_offset(x: int) -> int:
            return x ^ (keystream[0] << 32 | keystream[1])
        reader = PakReader(buffer[-PakInfo._mem_size(-1):])
        self.index_encrypted: bool = decrypt_index_encrypted(reader.u1()) == 1
        self.magic: int = decrypt_magic(reader.u4())
        self.version: int = reader.u4()
        self.index_hash: bytes = decrypt_index_hash(reader.s(20)) if self.version >= 6 else bytes()
        self.index_size: int = decrypt_index_size(reader.u8())
        self.index_offset: int = decrypt_index_offset(reader.u8())
        if self.version <= 3:
            self.index_encrypted = False

    @staticmethod
    def _mem_size(_: int) -> int:
        return 1 + 4 + 4 + 20 + 8 + 8

class TencentPakInfo(PakInfo):

    def __init__(self, buffer, keystream: List[int]):

        def decrypt_unk(x: bytes) -> bytes:
            key = struct.pack('<8I', *keystream[7:][:8])
            assert len(x) == len(key)
            return bytes((a ^ b for a, b in zip(x, key)))

        def decrypt_stem_hash(x: int) -> int:
            return x ^ keystream[8]

        def decrypt_unk_hash(x: int) -> int:
            return x ^ keystream[9]
        super().__init__(buffer, keystream)
        reader = PakReader(buffer[-TencentPakInfo._mem_size(self.version):])
        self.unk1: bytes = decrypt_unk(reader.s(32)) if self.version >= 7 else bytes()
        self.packed_key: bytes = reader.s(256) if self.version >= 8 else bytes()
        self.packed_iv: bytes = reader.s(256) if self.version >= 8 else bytes()
        self.packed_index_hash: bytes = reader.s(256) if self.version >= 8 else bytes()
        self.stem_hash: int = decrypt_stem_hash(reader.u4()) if self.version >= 9 else 0
        self.unk2: int = decrypt_unk_hash(reader.u4()) if self.version >= 9 else 0
        self.content_org_hash: bytes = reader.s(20) if self.version >= 12 else bytes()

    @staticmethod
    def _mem_size(version: int) -> int:
        _s2d9696b0690f = 32 if version >= 7 else 0
        _s4d01566231cb = 256 * 3 if version >= 8 else 0
        _s5e8c6b2d84ca = 4 * 2 if version >= 9 else 0
        _s6f8f7c152ca5 = 20 if version >= 12 else 0
        return PakInfo._mem_size(version) + _s2d9696b0690f + _s4d01566231cb + _s5e8c6b2d84ca + _s6f8f7c152ca5

class PakCompressedBlock:

    def __init__(self, reader: PakReader):
        self.start: int = reader.u8()
        self.end: int = reader.u8()

class TencentPakEntry:

    def __init__(self, reader: PakReader, version: int):
        self.content_hash: bytes = reader.s(20)
        if version <= 1:
            _ = reader.u8()
        self.offset: int = reader.u8()
        self.uncompressed_size: int = reader.u8()
        self.compression_method: int = reader.u4() & CM_MASK
        self.size: int = reader.u8()
        self.unk1: int = reader.u1() if version >= 5 else 0
        self.unk2: bytes = reader.s(20) if version >= 5 else bytes()
        self.compressed_blocks: List[PakCompressedBlock] = [PakCompressedBlock(reader) for _ in range(reader.u4())] if self.compression_method != 0 and version >= 3 else []
        self.compression_block_size: int = reader.u4() if version >= 4 else 0
        self.encrypted: bool = reader.u1() == 1 if version >= 4 else False
        self.encryption_method: int = reader.u4() if version >= 12 else 0
        self.index_new_sep: int = reader.u4() if version >= 12 else 0

    def _mem_size(self, version: int) -> int:
        _sc406064ed7f7 = 20 + 8 + 8 + 4 + 8 + (8 if version == 1 else 0)
        _s7729abb79481 = 4 + 1 if version >= 4 else 0
        _sdf708330ae6c = 4 + len(self.compressed_blocks) * 16 if self.compressed_blocks else 0
        _sb82161dbd1a7 = 1 + 20 if version >= 5 else 0
        _s7d6502d56c25 = 4 if version >= 12 else 0
        return _sc406064ed7f7 + _s7729abb79481 + _sb82161dbd1a7 + _s7d6502d56c25 + _sdf708330ae6c

class PakCrypto:

    class _LCG:

        def __init__(self, seed: int):
            self.state = seed

        def next(self) -> int:
            MASK_32 = 4294967295
            MSB_1 = 1 << 31

            def wrap(x: int) -> int:
                x &= MASK_32
                if not x & MSB_1:
                    return x
                else:
                    return (x + MSB_1 & MASK_32) - MSB_1
            x1 = wrap(1103515245 * self.state)
            self.state = wrap(x1 + 12345)
            x2 = wrap(x1 + 77880) if self.state < 0 else self.state
            return (x2 >> 16 & MASK_32) % 32767

    @staticmethod
    def zuc_keystream() -> List[int]:
        zuc = gmalg.ZUC(ZUC_KEY, ZUC_IV)
        return [struct.unpack('>I', zuc.generate())[0] for _ in range(16)]

    @staticmethod
    def _xorxor(buffer, x) -> bytes:
        return bytes((buffer[i] ^ x[i % len(x)] for i in range(len(buffer))))

    @staticmethod
    def _hashhash(buffer, n: int) -> bytes:
        _s59baeeaef8af = bytes()
        for _s6af6e5bfddf7 in range(math.ceil(n / SHA1.digest_size)):
            _s59baeeaef8af += SHA1.new(buffer).digest()
        if len(_s59baeeaef8af) >= n:
            _s59baeeaef8af = _s59baeeaef8af[:n]
        else:
            _s59baeeaef8af += b'\x00' * (n - len(_s59baeeaef8af))
        return _s59baeeaef8af

    @staticmethod
    def _meowmeow(buffer) -> bytes:

        def unpad(x):
            skip = 1 + next((i for i in range(len(x)) if x[i] != 0))
            return x[skip:]
        if len(buffer) < 43:
            return bytes()
        x1 = buffer[1:][:SHA1.digest_size]
        x2 = buffer[SHA1.digest_size + 1:]
        x1 = PakCrypto._xorxor(x1, PakCrypto._hashhash(x2, len(x1)))
        x2 = PakCrypto._xorxor(x2, PakCrypto._hashhash(x1, len(x2)))
        part1, m = (x2[:SHA1.digest_size], x2[SHA1.digest_size:])
        if part1 != SHA1.new(b'\x00' * SHA1.digest_size).digest():
            return bytes()
        return unpad(m)

    @staticmethod
    def rsa_extract(signature: bytes, modulus: bytes) -> bytes:
        _s111eea9de461 = int.from_bytes(signature, 'little')
        _s55ed6d4fd331 = int.from_bytes(modulus, 'little')
        _s095c3755c6f0 = 65537
        _se1fe0c965606 = pow(_s111eea9de461, _s095c3755c6f0, _s55ed6d4fd331).to_bytes(256, 'little').rstrip(b'\x00')
        return PakCrypto._meowmeow(Misc.pad_to_n(_se1fe0c965606, 4))

    @staticmethod
    def _decrypt_simple1(ciphertext) -> bytes:
        return bytes((x ^ SIMPLE1_DECRYPT_KEY for x in ciphertext))

    @staticmethod
    def _decrypt_simple2(ciphertext) -> bytes:

        class RollingKey:

            def __init__(self, initial_value: int):
                self._value = initial_value

            def update(self, x: int) -> int:
                self._value ^= x
                return self._value
        assert len(ciphertext) % SIMPLE2_BLOCK_SIZE == 0
        initial_key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
        rolling_key = RollingKey(initial_key)
        plaintext = (struct.pack('<I', rolling_key.update(x)) for x in struct.unpack(f'<{len(ciphertext) // 4}I', ciphertext))
        return bytes(it.chain.from_iterable(plaintext))

    @staticmethod
    @lru_cache(maxsize=1)
    def _derive_sm4_key(file_path: PurePath, encryption_method: int) -> bytes:
        _s5faefbac755f = file_path.stem.lower()
        if encryption_method == EM_SM4_2:
            _sbd281f3d3181 = SM4_SECRET_2
        elif encryption_method == EM_SM4_4:
            _sbd281f3d3181 = SM4_SECRET_4
        elif encryption_method == EM_UNKNOWN_17:
            _s2b8e7b87d9f2 = (encryption_method - EM_SM4_NEW_BASE) % len(SM4_SECRET_NEW)
            _sbd281f3d3181 = SM4_SECRET_NEW[_s2b8e7b87d9f2]
        else:
            _s2b8e7b87d9f2 = (encryption_method - EM_SM4_NEW_BASE) % len(SM4_SECRET_NEW)
            _sbd281f3d3181 = f'{SM4_SECRET_NEW[_s2b8e7b87d9f2]}{encryption_method}'
        return SHA1.new(str(_s5faefbac755f + _sbd281f3d3181).encode()).digest()[:SM4.key_length()]

    @staticmethod
    @lru_cache(maxsize=1)
    def _sm4_context_for_key(key: bytes) -> SM4:
        return SM4(key)

    @staticmethod
    def _decrypt_sm4(ciphertext, file_path: PurePath, encryption_method: int) -> bytes:
        assert len(ciphertext) % SM4.block_length() == 0
        key = PakCrypto._derive_sm4_key(file_path, encryption_method)
        sm4 = PakCrypto._sm4_context_for_key(key)
        block_size = SM4.block_length()
        return b''.join(
            sm4.decrypt(ciphertext[i:i + block_size])
            for i in range(0, len(ciphertext), block_size)
        )

    @staticmethod
    def decrypt_index(ciphertext, pak_info: TencentPakInfo) -> bytes:
        _sf57f815e306f = BASE_DIR / 'index_debug.txt'
        if pak_info.version > 7:
            _s6d658520201a = PakCrypto.rsa_extract(pak_info.packed_key, RSA_MOD_1)
            _s7df51ea341e1 = PakCrypto.rsa_extract(pak_info.packed_iv, RSA_MOD_1)
            _sdfce38baa9ff = f'\n=== AES INDEX DEBUG ===\nPAK version       : {pak_info.version}\nIndex encrypted   : {pak_info.index_encrypted}\nCiphertext length : {len(ciphertext)}\nCiphertext % 16   : {len(ciphertext) % 16}\nAES key length    : {len(_s6d658520201a)}\nIV length         : {len(_s7df51ea341e1)}\n=======================\n'
            print(_sdfce38baa9ff, flush=True)
            try:
                BASE_DIR.mkdir(parents=True, exist_ok=True)
                with open(_sf57f815e306f, 'a', encoding='utf-8') as _s110c157ac958:
                    _s110c157ac958.write(_sdfce38baa9ff)
            except Exception as e:
                print('Debug file write error:', e, flush=True)
            if len(_s6d658520201a) != 32:
                raise ValueError(f'Invalid AES key length: {len(_s6d658520201a)}')
            if len(_s7df51ea341e1) < 16:
                raise ValueError(f'Invalid IV length: {len(_s7df51ea341e1)}')
            if len(ciphertext) % AES.block_size != 0:
                raise ValueError(f'Encrypted index length is not aligned to AES block size: {len(ciphertext)} bytes')
            _scb460bac2d84 = AES.new(_s6d658520201a, MODE_CBC, _s7df51ea341e1[:16])
            _s970428e04040 = _scb460bac2d84.decrypt(ciphertext)
            _s285ad5d1da15 = f'\n=== AES DECRYPT RESULT ===\nDecrypted length  : {len(_s970428e04040)}\nFirst 16 bytes    : {_s970428e04040[:16].hex()}\nLast 16 bytes     : {_s970428e04040[-16:].hex()}\n==========================\n'
            print(_s285ad5d1da15, flush=True)
            try:
                with open(_sf57f815e306f, 'a', encoding='utf-8') as _s110c157ac958:
                    _s110c157ac958.write(_s285ad5d1da15)
            except Exception:
                pass
            try:
                _s0aecf0486bd3 = SHA1.new(_s970428e04040).digest()
                _s13f9d17236b6 = pak_info.index_hash
                _sf6b6965d0240 = _s0aecf0486bd3 == _s13f9d17236b6
                _sceb8ace10522 = None
                _s2599eac6ebec = None
                if len(_s970428e04040) >= 4:
                    _sceb8ace10522 = struct.unpack_from('<i', _s970428e04040, 0)[0]
                    if 0 < _sceb8ace10522 < 1024 and len(_s970428e04040) >= 4 + _sceb8ace10522:
                        _sce7a66c51c13 = _s970428e04040[4:4 + _sceb8ace10522]
                        _s2599eac6ebec = _sce7a66c51c13.rstrip(b'\\x00').decode('utf-8', errors='replace')
                _s8202ab0c7d3c = f'\n=== RAW INDEX CHECK ===\nExpected SHA1     : {_s13f9d17236b6.hex()}\nRaw SHA1          : {_s0aecf0486bd3.hex()}\nHASH MATCH        : {_sf6b6965d0240}\nFirst length      : {_sceb8ace10522}\nFirst string      : {_s2599eac6ebec}\n=======================\n'
                print(_s8202ab0c7d3c, flush=True)
                try:
                    with open(_sf57f815e306f, 'a', encoding='utf-8') as _s110c157ac958:
                        _s110c157ac958.write(_s8202ab0c7d3c)
                except Exception:
                    pass
            except Exception as e:
                _s955ef3f2949b = f'\n=== RAW INDEX CHECK ERROR ===\n{type(e).__name__}: {e}\n=============================\n'
                print(_s955ef3f2949b, flush=True)
                try:
                    with open(_sf57f815e306f, 'a', encoding='utf-8') as _s110c157ac958:
                        _s110c157ac958.write(_s955ef3f2949b)
                except Exception:
                    pass
            try:
                _sf9a1a1bab682 = unpad(_s970428e04040, AES.block_size)
            except ValueError as e:
                _s0aecf0486bd3 = SHA1.new(_s970428e04040).digest()
                _s13f9d17236b6 = pak_info.index_hash
                if _s0aecf0486bd3 == _s13f9d17236b6:
                    _s0cf61c10ae02 = f'\n=== PADDING FALLBACK ===\nUnpad error       : {e}\nRaw SHA1 matches expected index hash.\nUsing raw decrypted index without PKCS#7 unpad.\n========================\n'
                    print(_s0cf61c10ae02, flush=True)
                    try:
                        with open(_sf57f815e306f, 'a', encoding='utf-8') as _s110c157ac958:
                            _s110c157ac958.write(_s0cf61c10ae02)
                    except Exception:
                        pass
                    _sf9a1a1bab682 = _s970428e04040
                else:
                    _se3c61c4c947e = _s970428e04040[-1] if _s970428e04040 else None
                    _sb71dc219a486 = f'\n=== DECRYPT FAILURE ===\nError             : {e}\nDecrypted length  : {len(_s970428e04040)}\nLast byte         : {_se3c61c4c947e}\nLast 16 bytes     : {_s970428e04040[-16:].hex()}\nExpected SHA1     : {_s13f9d17236b6.hex()}\nRaw SHA1          : {_s0aecf0486bd3.hex()}\n=======================\n'
                    print(_sb71dc219a486, flush=True)
                    try:
                        with open(_sf57f815e306f, 'a', encoding='utf-8') as _s110c157ac958:
                            _s110c157ac958.write(_sb71dc219a486)
                    except Exception:
                        pass
                    raise
            _sbe3b813d7bcd = f'\n=== DECRYPT SUCCESS ===\nResult length     : {len(_sf9a1a1bab682)}\n=======================\n'
            print(_sbe3b813d7bcd, flush=True)
            try:
                with open(_sf57f815e306f, 'a', encoding='utf-8') as _s110c157ac958:
                    _s110c157ac958.write(_sbe3b813d7bcd)
            except Exception:
                pass
            return _sf9a1a1bab682
        return bytes(PakCrypto._decrypt_simple1(ciphertext))

    @staticmethod
    def _is_simple1_method(encryption_method: int) -> bool:
        return encryption_method == EM_SIMPLE1

    @staticmethod
    def _is_simple2_method(encryption_method: int) -> bool:
        return encryption_method == EM_SIMPLE2 or encryption_method == 17

    @staticmethod
    def _is_sm4_method(encryption_method: int) -> bool:
        return encryption_method == EM_SM4_2 or encryption_method == EM_SM4_4 or encryption_method == EM_UNKNOWN_17 or (encryption_method & EM_SM4_NEW_MASK != 0)

    @staticmethod
    def align_encrypted_content_size(n: int, encryption_method: int) -> int:
        if PakCrypto._is_simple2_method(encryption_method):
            return Misc.align_up(n, SIMPLE2_BLOCK_SIZE)
        elif PakCrypto._is_sm4_method(encryption_method):
            return Misc.align_up(n, SM4.block_length())
        else:
            return n

    @staticmethod
    def decrypt_block(ciphertext, file: PurePath, encryption_method: int) -> bytes:
        if PakCrypto._is_simple1_method(encryption_method):
            return PakCrypto._decrypt_simple1(ciphertext)
        elif PakCrypto._is_simple2_method(encryption_method):
            return PakCrypto._decrypt_simple2(ciphertext)
        elif PakCrypto._is_sm4_method(encryption_method):
            return PakCrypto._decrypt_sm4(ciphertext, file, encryption_method)
        else:
            raise ValueError(f'Unknown encryption method: {encryption_method}')

    @staticmethod
    @lru_cache(maxsize=33)
    def generate_block_indices(n: int, encryption_method: int) -> List[int]:
        if not PakCrypto._is_sm4_method(encryption_method):
            return list(range(n))
        _s3a075bc662d9 = []
        _s6e382a72ca37 = PakCrypto._LCG(n)
        while len(_s3a075bc662d9) != n:
            _sfe84feb5bf53 = _s6e382a72ca37.next() % n
            if _sfe84feb5bf53 not in _s3a075bc662d9:
                _s3a075bc662d9.append(_sfe84feb5bf53)
        _sba12f1c4fab3 = [0] * len(_s3a075bc662d9)
        for _sc2e19a16b623, _sfe84feb5bf53 in enumerate(_s3a075bc662d9):
            _sba12f1c4fab3[_sfe84feb5bf53] = _sc2e19a16b623
        return _sba12f1c4fab3

    def _encrypt_simple1(plaintext: bytes) -> bytes: return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in plaintext)

    def _encrypt_simple2(plaintext: bytes) -> bytes:
            initial_key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY); out_words = []; current = initial_key
            for w in struct.unpack(f'<{len(plaintext)//4}I', plaintext): c = current ^ w; out_words.append(c); current = w
            return struct.pack(f'<{len(out_words)}I', *out_words)

    def _encrypt_sm4(plaintext: bytes, file_path: PurePath, encryption_method: int) -> bytes:
            key = PakCrypto._derive_sm4_key(file_path, encryption_method); sm4 = PakCrypto._sm4_context_for_key(key)
            return b''.join(sm4.encrypt(plaintext[i:i+SM4.block_length()]) for i in range(0, len(plaintext), SM4.block_length()))

class PakCompression:

    @staticmethod
    @lru_cache(maxsize=33)
    def _zstd_decompressor(dict: ZstdCompressionDict) -> ZstdDecompressor:
        return ZstdDecompressor(dict)

    @staticmethod
    def zstd_dictionary(dict_data) -> ZstdCompressionDict:
        return ZstdCompressionDict(dict_data, DICT_TYPE_AUTO)

    @staticmethod
    def decompress_block(block, dict: Optional[ZstdCompressionDict], compression_method: int) -> bytes:
        if compression_method == CM_NONE:
            return block
        if compression_method == CM_ZLIB:
            try:
                return zlib.decompress(block)
            except zlib.error:
                return block
        elif compression_method == CM_ZSTD or compression_method == CM_ZSTD_DICT:
            if compression_method != CM_ZSTD_DICT:
                dict = None
            return PakCompression._zstd_decompressor(dict).decompress(block)
        else:
            raise ValueError(f'Unknown compression method: {compression_method}')

    def compress_block(plain_block: bytes, compression_method: int, zstd_dict: ZstdCompressionDict | None, target_len: int | None) -> bytes:
            if compression_method == CM_NONE: return plain_block
            if compression_method == CM_ZLIB:
                for level in range(6, 10):
                    comp = zlib.compress(plain_block, level)
                    if target_len is None or len(comp) <= target_len: return comp
                return zlib.compress(plain_block)
            if compression_method == CM_ZSTD or compression_method == CM_ZSTD_DICT:
                for level in range(18, 23):
                    cctx = ZstdCompressor(level=level, dict_data=zstd_dict) if compression_method == CM_ZSTD_DICT and zstd_dict else ZstdCompressor(level=level)
                    comp = cctx.compress(plain_block)
                    if target_len is None or len(comp) <= target_len: return comp
                return cctx.compress(plain_block)
            raise RuntimeError('Unsupported compression')

class TencentPakFile:

    def __init__(self, file_path: PurePath, is_od=True):
        _alv_require_operation(('pak.unpack', 'pak.repack', 'pak.unpack_single', 'pak.repack_single', 'pak.diagnostics', 'pak.delete_entry', 'pak.delete_all', 'advanced.inject_any', 'advanced.inject_brplayer', 'advanced.same_size_hashfix', 'advanced.zsdic_hashfix', 'asset.unpack', 'obb.unpack', 'obb.repack', 'lab.editor.auto_pak', 'lab.playerpawn.auto_pak'))
        self._file_path = file_path
        with open(file_path, 'rb') as _sb1e9a39131ae:
            self._file_content = memoryview(_sb1e9a39131ae.read())
        self._is_od = is_od
        self._mount_point = PurePath()
        self._is_zstd_with_dict = 'zsdic' in str(self._file_path)
        self._zstd_dict = None
        self._files: List[TencentPakEntry] = []
        self._index: Dict[PurePath, Dict[str, TencentPakEntry]] = {}
        self._pak_info = TencentPakInfo(self._file_content, PakCrypto.zuc_keystream())
        self._verify_stem_hash()
        self._tencent_load_index()

    def _verify_stem_hash(self) -> None:
        if not self._is_od and self._pak_info.version >= 9:
            assert self._pak_info.stem_hash == zlib.crc32(self._file_path.stem.encode('utf-32le'))

    def _tencent_load_index(self) -> None:
        _s348b5384ebf7 = BASE_DIR / 'index_debug.txt'
        _sa051e2872adf = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]
        _s76e0849234b7 = len(self._file_content)
        _sa8818ce51f00 = self._pak_info.index_offset + self._pak_info.index_size
        _scc798660995b = f'\n=================================\n        PAK INDEX DEBUG\n=================================\nPAK file          : {self._file_path}\nPAK file size     : {_s76e0849234b7}\nPAK version       : {self._pak_info.version}\nIndex encrypted   : {self._pak_info.index_encrypted}\nIndex offset      : {self._pak_info.index_offset}\nIndex size        : {self._pak_info.index_size}\nRaw index length  : {len(_sa051e2872adf)}\nIndex end         : {_sa8818ce51f00}\n=================================\n'
        print(_scc798660995b, flush=True)
        try:
            BASE_DIR.mkdir(parents=True, exist_ok=True)
            with open(_s348b5384ebf7, 'w', encoding='utf-8') as _s4bc868e5e0cb:
                _s4bc868e5e0cb.write(_scc798660995b)
        except Exception as e:
            print('Debug file write error:', e, flush=True)
        if self._pak_info.index_offset < 0 or self._pak_info.index_size < 0 or _sa8818ce51f00 > _s76e0849234b7:
            _s8808166cce94 = f'\n=== INDEX RANGE ERROR ===\nFile size         : {_s76e0849234b7}\nIndex offset      : {self._pak_info.index_offset}\nIndex size        : {self._pak_info.index_size}\nIndex end         : {_sa8818ce51f00}\n=========================\n'
            print(_s8808166cce94, flush=True)
            try:
                with open(_s348b5384ebf7, 'a', encoding='utf-8') as _s4bc868e5e0cb:
                    _s4bc868e5e0cb.write(_s8808166cce94)
            except Exception:
                pass
            raise ValueError('PAK index offset/size is outside the file.')
        if self._pak_info.index_encrypted:
            print('Index encryption detected.', flush=True)
            try:
                _sa051e2872adf = PakCrypto.decrypt_index(_sa051e2872adf, self._pak_info)
            except Exception as e:
                _s9fa7d45d95f7 = f'\n=== INDEX DECRYPT ERROR ===\n{type(e).__name__}: {e}\n===========================\n'
                print(_s9fa7d45d95f7, flush=True)
                try:
                    with open(_s348b5384ebf7, 'a', encoding='utf-8') as _s4bc868e5e0cb:
                        _s4bc868e5e0cb.write(_s9fa7d45d95f7)
                except Exception:
                    pass
                raise
        else:
            print('Index is not encrypted.', flush=True)
        _s63b65c85941d = f'\n=== INDEX AFTER DECRYPT ===\nIndex length      : {len(_sa051e2872adf)}\nFirst 16 bytes    : {bytes(_sa051e2872adf[:16]).hex()}\n===========================\n'
        print(_s63b65c85941d, flush=True)
        try:
            with open(_s348b5384ebf7, 'a', encoding='utf-8') as _s4bc868e5e0cb:
                _s4bc868e5e0cb.write(_s63b65c85941d)
        except Exception:
            pass
        try:
            self._verify_index_hash(_sa051e2872adf)
        except Exception as e:
            _s9f7c93207141 = f'\n=== INDEX HASH ERROR ===\n{type(e).__name__}: {e}\n========================\n'
            print(_s9f7c93207141, flush=True)
            try:
                with open(_s348b5384ebf7, 'a', encoding='utf-8') as _s4bc868e5e0cb:
                    _s4bc868e5e0cb.write(_s9f7c93207141)
            except Exception:
                pass
            raise
        try:
            self._load_index(_sa051e2872adf)
        except Exception as e:
            _s619995a82fa4 = f'\n=== INDEX LOAD ERROR ===\n{type(e).__name__}: {e}\n========================\n'
            print(_s619995a82fa4, flush=True)
            try:
                with open(_s348b5384ebf7, 'a', encoding='utf-8') as _s4bc868e5e0cb:
                    _s4bc868e5e0cb.write(_s619995a82fa4)
            except Exception:
                pass
            raise
        _s571239371976 = '\n=================================\n INDEX LOAD COMPLETED SUCCESSFULLY\n=================================\n'
        print(_s571239371976, flush=True)
        try:
            with open(_s348b5384ebf7, 'a', encoding='utf-8') as _s4bc868e5e0cb:
                _s4bc868e5e0cb.write(_s571239371976)
        except Exception:
            pass

    def _verify_index_hash(self, index_data) -> None:
        _s860f9b0ab543 = self._pak_info.index_hash
        if not self._is_od and self._pak_info.version >= 8:
            assert _s860f9b0ab543 == PakCrypto.rsa_extract(self._pak_info.packed_index_hash, RSA_MOD_2)
        assert _s860f9b0ab543 == SHA1.new(index_data).digest()

    @staticmethod
    def _construct_mount_point(mount_point: str) -> PurePath:
        _s618c3a7399cb = PurePath()
        for _s683bf62df053 in PurePath(mount_point).parts:
            if _s683bf62df053 != '..':
                _s618c3a7399cb /= _s683bf62df053
        return _s618c3a7399cb

    def _peek_content(self, offset: int, size: int, encryption_method: int) -> memoryview:
        size = PakCrypto.align_encrypted_content_size(size, encryption_method)
        return self._file_content[offset:][:size]

    def _peek_block_content(self, block: PakCompressedBlock, encryption_method: int) -> memoryview:
        _sef994aeed7fb = PakCrypto.align_encrypted_content_size(block.end - block.start, encryption_method)
        return self._file_content[block.start:][:_sef994aeed7fb]

    def _construct_zstd_dict(self, dict_entry: TencentPakEntry) -> None:
        assert not self._zstd_dict
        assert not dict_entry.encrypted
        assert dict_entry.compression_method == CM_NONE
        _s41bb931c4a96 = PakReader(self._peek_content(dict_entry.offset, dict_entry.size, 0))
        _scc7cac6d6f06 = _s41bb931c4a96.u8()
        _s2ce972b6572e = _s41bb931c4a96.u4()
        assert _scc7cac6d6f06 == _s41bb931c4a96.u4()
        _s086160e11595 = _s41bb931c4a96.s(_scc7cac6d6f06)
        self._zstd_dict = PakCompression.zstd_dictionary(_s086160e11595)

    def _load_index(self, index_data) -> None:
        if self._pak_info.version <= 10:
            raise ValueError(f'Unsupported version: {self._pak_info.version}')
        debug_path = BASE_DIR / 'index_debug.txt'
        reader = PakReader(index_data)
        self._mount_point = self._construct_mount_point(reader.string())
        file_count = reader.u4()
        self._files = [TencentPakEntry(reader, self._pak_info.version) for _ in range(file_count)]
        dir_count = reader.u8()
        skipped_bad_refs = 0
        skipped_bad_paths = 0

        def log_skip(message: str) -> None:
            _s540ed156ec16 = _alv_pak_debug_display(message)
            print(_s540ed156ec16, flush=True)
            try:
                with open(debug_path, 'a', encoding='utf-8') as _s7a74957a9147:
                    _s7a74957a9147.write(_s540ed156ec16 + '\n')
            except Exception:
                pass
        for dir_no in range(dir_count):
            raw_dir = reader.string()
            entry_count = reader.u8()
            parsed_entries = []
            for entry_no in range(entry_count):
                file_name = reader.string()
                raw_file_index = reader.i4()
                mapped_index = ~raw_file_index
                parsed_entries.append((entry_no, file_name, raw_file_index, mapped_index))
            dir_obj = PurePath(raw_dir)
            dir_parts = dir_obj.parts
            unsafe_dir = '\x00' in raw_dir or dir_obj.is_absolute() or '..' in dir_parts or ('\\' in raw_dir)
            if unsafe_dir:
                skipped_bad_paths += 1
                log_skip(f'[INDEX SKIP] dir={dir_no} unsafe path: {raw_dir!r}')
                continue
            e = {}
            for entry_no, file_name, raw_file_index, mapped_index in parsed_entries:
                unsafe_name = '\x00' in file_name or '/' in file_name or '\\' in file_name or (file_name in ('.', '..'))
                if unsafe_name:
                    skipped_bad_paths += 1
                    log_skip(f'[INDEX SKIP] dir={dir_no} entry={entry_no} unsafe filename: {file_name!r}')
                    continue
                if not 0 <= mapped_index < len(self._files):
                    skipped_bad_refs += 1
                    log_skip(f'[INDEX SKIP] dir={dir_no} entry={entry_no} file={file_name!r} raw_ref={raw_file_index} mapped_ref={mapped_index} files={len(self._files)}')
                    continue
                e[file_name] = self._files[mapped_index]
            if self._is_zstd_with_dict and dir_obj.name == 'zstddic':
                if len(e) == 1:
                    self._construct_zstd_dict(next(iter(e.values())))
                elif e:
                    log_skip(f'[INDEX SKIP] zstddic directory has {len(e)} valid entries; expected exactly 1')
                continue
            if e:
                self._index[dir_obj] = e
        self._index_parse_stats = {'file_entries': len(self._files), 'directory_records': dir_count, 'loaded_directories': len(self._index), 'skipped_bad_refs': skipped_bad_refs, 'skipped_bad_paths': skipped_bad_paths, 'reader_cursor': reader._cursor, 'index_length': len(index_data)}
        summary = f'\n=== INDEX PARSE SUMMARY ===\nFile entries       : {len(self._files)}\nDirectory records  : {dir_count}\nLoaded directories : {len(self._index)}\nSkipped bad refs   : {skipped_bad_refs}\nSkipped bad paths  : {skipped_bad_paths}\nPakReader cursor      : {reader._cursor}/{len(index_data)}\n===========================\n'
        print(summary, flush=True)
        try:
            with open(debug_path, 'a', encoding='utf-8') as f:
                f.write(summary)
        except Exception:
            pass

    def detect_dominant_style(self) -> dict:
        comp_counter = Counter()
        enc_counter = Counter()
        blk_counter = Counter()
        enc_flag_counter = Counter()
        total = len(self._files)
        if total == 0:
            return {'comp_method': CM_ZSTD, 'enc_method': 0, 'encrypted': False, 'block_size': 65536}
        for entry in self._files:
            comp_counter[entry.compression_method] += 1
            if entry.encrypted:
                enc_counter[entry.encryption_method] += 1
                enc_flag_counter['encrypted'] += 1
            else:
                enc_flag_counter['plain'] += 1
            if entry.compression_block_size:
                blk_counter[entry.compression_block_size] += 1
        non_none = [(m, c) for m, c in comp_counter.items() if m != CM_NONE]
        comp_method = max(non_none, key=lambda x: x[1])[0] if non_none else CM_NONE
        encrypted = enc_flag_counter.get('encrypted', 0) > enc_flag_counter.get('plain', 0)
        enc_method = enc_counter.most_common(1)[0][0] if encrypted and enc_counter else 0
        block_size = blk_counter.most_common(1)[0][0] if blk_counter else 65536
        return {'comp_method': comp_method, 'enc_method': enc_method, 'encrypted': encrypted, 'block_size': block_size}

    def list_existing_paths(self) -> List[str]:
        _s923c21165935 = []
        for _s0ae1e3cd5262, _s68f1c0e6347e in self._index.items():
            for _s9bb2390cf2a1 in _s68f1c0e6347e.keys():
                _s923c21165935.append(str(_s0ae1e3cd5262 / _s9bb2390cf2a1).replace('\\', '/').lstrip('/'))
        return _s923c21165935

    @staticmethod
    def _extract_entry_plain(pak_buffer: memoryview, entry: TencentPakEntry, file_path_for_crypto: PurePath, zstd_dict) -> bytes:
        """Extract a single entry's plaintext (decrypted + decompressed) bytes."""
        if entry.compression_method == CM_NONE:
            _se741c9e5b336 = PakCrypto.align_encrypted_content_size(entry.size, entry.encryption_method)
            _s2c1f87975662 = bytes(pak_buffer[entry.offset:][:_se741c9e5b336])
            if entry.encrypted:
                _s2c1f87975662 = PakCrypto.decrypt_block(_s2c1f87975662, file_path_for_crypto, entry.encryption_method)
            return _s2c1f87975662
        _sa2b725aa04a1 = []
        for _s233f3b8af19b in PakCrypto.generate_block_indices(len(entry.compressed_blocks), entry.encryption_method):
            _s352a9973d0a5 = entry.compressed_blocks[_s233f3b8af19b]
            _se51624ae001c = PakCrypto.align_encrypted_content_size(_s352a9973d0a5.end - _s352a9973d0a5.start, entry.encryption_method)
            _s3ab48815ace4 = bytes(pak_buffer[_s352a9973d0a5.start:][:_se51624ae001c])
            if entry.encrypted:
                _s3ab48815ace4 = PakCrypto.decrypt_block(_s3ab48815ace4, file_path_for_crypto, entry.encryption_method)
            _sbe77522f0741 = PakCompression.decompress_block(_s3ab48815ace4, zstd_dict, entry.compression_method)
            _sa2b725aa04a1.append(_sbe77522f0741)
        return b''.join(_sa2b725aa04a1)

    def inject_files(self, inject_plan: list, output_pak: Path) -> None:
        """Inject new files into this PAK, producing a new PAK at output_pak."""
        if not inject_plan:
            raise ValueError('inject_plan is empty — nothing to inject')
        console.print('[bold magenta]💉 CUSTOM INJECT[/bold magenta]')
        console.print(f'[white]Source PAK:[/] [yellow]{self._file_path.name}[/yellow]')
        console.print(f'[white]Output    :[/] [cyan]{output_pak.name}[/cyan]')
        console.print(f'[white]Injecting :[/] [green]{len(inject_plan)} new file(s)[/green]')
        console.print('[green]AUTO-INSERT: OFF — only files selected by the user are added.[/green]')
        console.print('\n[bold magenta]━━ STEP 1/5 : LOADING INJECT FILES ━━[/bold magenta]')
        work_items = []
        for i, item in enumerate(inject_plan):
            if item.get('plain_bytes') is not None:
                plain = item['plain_bytes']
            elif item.get('src_path') is not None:
                try:
                    plain = Path(item['src_path']).read_bytes()
                except Exception as e:
                    console.print(f"   [red]✗ Cannot read {item['src_path']}: {e} — skipping[/red]")
                    continue
            else:
                console.print(f'   [red]✗ Inject item {i} has no src_path or plain_bytes — skipping[/red]')
                continue
            internal = item['internal_path'].replace('\\', '/').lstrip('/')
            if not internal:
                console.print(f'   [red]✗ Empty internal_path for item {i} — skipping[/red]')
                continue
            parts = internal.rsplit('/', 1)
            if len(parts) == 2:
                dir_str, file_name = (parts[0], parts[1])
            else:
                dir_str, file_name = ('', parts[0])
            work_items.append({'dir_str': dir_str, 'file_name': file_name, 'internal_path': internal, 'plain': plain, 'comp_method': item['comp_method'], 'enc_method': item['enc_method'], 'encrypted': bool(item['encrypted']), 'block_size': item['block_size'], 'comp_level': item.get('comp_level', 19)})
            console.print(f'   [blue]✨[/] {internal} [dim]({len(plain):,} bytes)[/dim]')
        if not work_items:
            raise RuntimeError('No valid inject items after loading')
        console.print(f'[green]✔ Loaded {len(work_items)} file(s)[/green]')
        console.print('\n[bold magenta]━━ STEP 2/5 : ENCODING INJECT FILES ━━[/bold magenta]')
        keystream = PakCrypto.zuc_keystream()
        version = self._pak_info.version
        header_size = TencentPakInfo._mem_size(version)
        PAK_MAGIC = self._pak_info.magic
        orig_index_offset = self._pak_info.index_offset
        current_new_offset = orig_index_offset
        new_data_region = bytearray()
        new_injected_entries = []
        preferred_level = 19

        def _encrypt_plaintext(plaintext, pak_relative_path, encryption_method):
            if PakCrypto._is_simple1_method(encryption_method):
                return bytes((b ^ SIMPLE1_DECRYPT_KEY for b in plaintext))
            elif PakCrypto._is_simple2_method(encryption_method):
                pad = -len(plaintext) % SIMPLE2_BLOCK_SIZE
                plaintext += b'\x00' * pad
                key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
                rolling = key
                out = []
                for x, in struct.iter_unpack('<I', plaintext):
                    c = rolling ^ x
                    out.append(c)
                    rolling ^= c
                return struct.pack(f'<{len(out)}I', *out)
            elif PakCrypto._is_sm4_method(encryption_method):
                key = PakCrypto._derive_sm4_key(pak_relative_path, encryption_method)
                sm4 = PakCrypto._sm4_context_for_key(key)
                pad_len = -len(plaintext) % 16
                if pad_len > 0:
                    plaintext = plaintext + b'\x00' * pad_len
                out = bytearray()
                for i in range(0, len(plaintext), 16):
                    block = plaintext[i:i + 16]
                    if len(block) < 16:
                        block = block.ljust(16, b'\x00')
                    out.extend(sm4.encrypt(block))
                return bytes(out)
            return plaintext
        for item in work_items:
            plain = item['plain']
            comp_method = item['comp_method']
            enc_method = item['enc_method']
            encrypted = item['encrypted']
            block_size_val = item['block_size']
            file_path_for_crypto = PurePath(item['file_name'])
            if len(plain) == 0:
                new_injected_entries.append({'content_hash': SHA1.new(b'').digest(), 'offset': current_new_offset, 'uncompressed_size': 0, 'size': 0, 'comp_method': CM_NONE, 'enc_method': 0, 'encrypted': False, 'block_size_val': 0, 'compressed_blocks': [], 'unk1': 0, 'unk2': b'\x00' * 20, 'index_new_sep': 0, '_dir_path': PurePath(item['dir_str']) if item['dir_str'] else PurePath(), '_file_name': item['file_name']})
                continue
            if comp_method == CM_NONE:
                if encrypted:
                    aligned_size = PakCrypto.align_encrypted_content_size(len(plain), enc_method)
                    padded = plain + b'\x00' * (aligned_size - len(plain))
                    stored_data = _encrypt_plaintext(padded, file_path_for_crypto, enc_method)
                else:
                    stored_data = plain
                new_size = len(stored_data)
                new_compressed_blocks = []
            else:
                chunks = [plain[i:i + block_size_val] for i in range(0, len(plain), block_size_val)]
                if not chunks:
                    chunks = [b'']
                compressed_chunks = []
                for chunk in chunks:
                    comp = None
                    if comp_method in (CM_ZSTD, CM_ZSTD_DICT):
                        zstd_dict = self._zstd_dict if comp_method == CM_ZSTD_DICT else None
                        for lvl in range(22, 0, -1):
                            try:
                                c = ZstdCompressor(level=lvl, dict_data=zstd_dict, threads=1)
                                comp = c.compress(chunk)
                                break
                            except:
                                continue
                    elif comp_method == CM_ZLIB:
                        comp = zlib.compress(chunk, level=9)
                    if comp is None:
                        comp = chunk
                    compressed_chunks.append(comp)
                encrypted_chunks = []
                for comp_data in compressed_chunks:
                    if encrypted:
                        comp_data = _encrypt_plaintext(comp_data, file_path_for_crypto, enc_method)
                    encrypted_chunks.append(comp_data)
                n_blocks = len(encrypted_chunks)
                indices = PakCrypto.generate_block_indices(n_blocks, enc_method)
                physical_blocks = [None] * n_blocks
                for j, chunk_data in enumerate(encrypted_chunks):
                    physical_blocks[indices[j]] = chunk_data
                physical_offsets = []
                block_cursor = current_new_offset
                for phys_block in physical_blocks:
                    physical_offsets.append((block_cursor, block_cursor + len(phys_block)))
                    block_cursor += len(phys_block)
                new_compressed_blocks = physical_offsets
                stored_data = b''.join(physical_blocks)
                new_size = len(stored_data)
                if encrypted:
                    aligned_total = PakCrypto.align_encrypted_content_size(new_size, enc_method)
                    if aligned_total > new_size:
                        stored_data = stored_data + b'\x00' * (aligned_total - new_size)
                        new_size = aligned_total
            new_content_hash = SHA1.new(stored_data).digest()
            new_data_region.extend(stored_data)
            new_injected_entries.append({'content_hash': new_content_hash, 'offset': current_new_offset, 'uncompressed_size': len(plain), 'size': new_size, 'comp_method': comp_method, 'enc_method': enc_method if encrypted else 0, 'encrypted': encrypted, 'block_size_val': block_size_val, 'compressed_blocks': new_compressed_blocks, 'unk1': 0, 'unk2': b'\x00' * 20, 'index_new_sep': 0, '_dir_path': PurePath(item['dir_str']) if item['dir_str'] else PurePath(), '_file_name': item['file_name']})
            current_new_offset += new_size
        console.print(f'[green]✔ Encoded {len(new_injected_entries)} file(s)[/green]')
        new_entries = []
        entry_to_path = {}
        for dir_path, files in self._index.items():
            for fname, entry in files.items():
                entry_to_path[id(entry)] = (dir_path, fname)
        for i, entry in enumerate(self._files):
            dir_path, fname = entry_to_path.get(id(entry), (PurePath(), f'unknown_{i}'))
            new_entries.append({'content_hash': entry.content_hash, 'offset': entry.offset, 'uncompressed_size': entry.uncompressed_size, 'size': entry.size, 'comp_method': entry.compression_method, 'enc_method': entry.encryption_method if entry.encrypted else 0, 'encrypted': entry.encrypted, 'block_size_val': entry.compression_block_size, 'compressed_blocks': [(b.start, b.end) for b in entry.compressed_blocks], 'unk1': entry.unk1, 'unk2': entry.unk2, 'index_new_sep': entry.index_new_sep})
        new_entries.extend(new_injected_entries)
        index_data = bytearray()
        raw_orig_index = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]
        if self._pak_info.index_encrypted:
            orig_index_decoded = PakCrypto.decrypt_index(bytes(raw_orig_index), self._pak_info)
        else:
            orig_index_decoded = bytes(raw_orig_index)
        orig_reader = PakReader(orig_index_decoded)
        orig_mount_len = orig_reader.i4()
        orig_mount_bytes = bytes(orig_reader.s(orig_mount_len))
        index_data.extend(struct.pack('<I', orig_mount_len))
        index_data.extend(orig_mount_bytes)
        index_data.extend(struct.pack('<I', len(new_entries)))
        for item in new_entries:
            index_data.extend(item['content_hash'])
            if version <= 1:
                index_data.extend(struct.pack('<Q', 0))
            index_data.extend(struct.pack('<Q', item['offset']))
            index_data.extend(struct.pack('<Q', item['uncompressed_size']))
            index_data.extend(struct.pack('<I', item['comp_method'] & CM_MASK))
            index_data.extend(struct.pack('<Q', item['size']))
            if version >= 5:
                index_data.extend(struct.pack('<B', item['unk1']))
                index_data.extend(item['unk2'] if item['unk2'] else b'\x00' * 20)
            if item['comp_method'] != CM_NONE and version >= 3:
                index_data.extend(struct.pack('<I', len(item['compressed_blocks'])))
                for start, end in item['compressed_blocks']:
                    index_data.extend(struct.pack('<Q', start))
                    index_data.extend(struct.pack('<Q', end))
            if version >= 4:
                index_data.extend(struct.pack('<I', item['block_size_val']))
                index_data.extend(struct.pack('<B', 1 if item['encrypted'] else 0))
            if version >= 12:
                index_data.extend(struct.pack('<I', item['enc_method']))
                index_data.extend(struct.pack('<I', item['index_new_sep']))
        file_to_dirname = {}
        for dir_path, files_dict in self._index.items():
            dir_str = dir_path.as_posix()
            for fname, entry in files_dict.items():
                for i, fe in enumerate(self._files):
                    if id(fe) == id(entry):
                        file_to_dirname[i] = (dir_str, fname)
                        break
        for i, item in enumerate(new_entries):
            if i not in file_to_dirname:
                if '_dir_path' in item:
                    file_to_dirname[i] = (item['_dir_path'].as_posix(), item['_file_name'])
                else:
                    file_to_dirname[i] = ('', f'file_{i}')
        all_dirs = []
        dir_to_files = {}
        for dir_path in self._index.keys():
            ds = dir_path.as_posix()
            all_dirs.append(ds)
            dir_to_files[ds] = []
        for i, item in enumerate(new_entries):
            ds, fn = file_to_dirname[i]
            if ds not in dir_to_files:
                dir_to_files[ds] = []
                all_dirs.append(ds)
            dir_to_files[ds].append((fn, i))
        index_data.extend(struct.pack('<Q', len(all_dirs)))
        for dir_str in all_dirs:
            files_list = dir_to_files[dir_str]
            if not dir_str or dir_str == '.':
                index_data.extend(struct.pack('<I', 0))
            else:
                if not dir_str.endswith('/'):
                    dir_str_with_slash = dir_str + '/'
                else:
                    dir_str_with_slash = dir_str
                dir_bytes = dir_str_with_slash.encode('utf-8') + b'\x00'
                index_data.extend(struct.pack('<I', len(dir_bytes)))
                index_data.extend(dir_bytes)
            index_data.extend(struct.pack('<Q', len(files_list)))
            for file_name, fi in files_list:
                name_bytes = file_name.encode('utf-8') + b'\x00'
                index_data.extend(struct.pack('<I', len(name_bytes)))
                index_data.extend(name_bytes)
                index_data.extend(struct.pack('<i', -fi - 1))
        index_data.extend(b'\x1d\x00\x00\x00..')
        index_hash = SHA1.new(bytes(index_data)).digest()
        if version > 7 and self._pak_info.index_encrypted:
            key = PakCrypto.rsa_extract(self._pak_info.packed_key, RSA_MOD_1)
            iv = PakCrypto.rsa_extract(self._pak_info.packed_iv, RSA_MOD_1)
            assert len(key) == 32 and len(iv) == 32
            padded = pad(bytes(index_data), AES.block_size)
            aes = AES.new(key, MODE_CBC, iv[:16])
            encrypted_index = aes.encrypt(padded)
        elif self._pak_info.index_encrypted:
            encrypted_index = bytes((b ^ SIMPLE1_DECRYPT_KEY for b in bytes(index_data)))
        else:
            encrypted_index = bytes(index_data)
        index_size = len(encrypted_index)
        new_index_offset = orig_index_offset + len(new_data_region)
        encrypted_magic = self._pak_info.magic ^ keystream[2]
        key_stream_hash = struct.pack('<5I', *keystream[4:][:5])
        encrypted_index_hash = bytes((a ^ b for a, b in zip(index_hash, key_stream_hash)))
        encrypted_index_size = index_size ^ (keystream[10] << 32 | keystream[11])
        encrypted_index_offset = new_index_offset ^ (keystream[0] << 32 | keystream[1])
        encrypted_flag_byte = (1 if self._pak_info.index_encrypted else 0) ^ keystream[3] & 255
        orig_data_region = bytearray(self._file_content[0:orig_index_offset])
        output_pak.parent.mkdir(parents=True, exist_ok=True)
        with open(output_pak, 'wb') as f:
            f.write(bytes(orig_data_region))
            f.write(bytes(new_data_region))
            f.write(encrypted_index)
            if version >= 7:
                key_unk1 = struct.pack('<8I', *keystream[7:][:8])
                unk1_plain = self._pak_info.unk1 if self._pak_info.unk1 else b'\x00' * 32
                encrypted_unk1 = bytes((a ^ b for a, b in zip(unk1_plain, key_unk1)))
                f.write(encrypted_unk1)
            if version >= 8:
                f.write(self._pak_info.packed_key if self._pak_info.packed_key else b'\x00' * 256)
                f.write(self._pak_info.packed_iv if self._pak_info.packed_iv else b'\x00' * 256)
                f.write(self._pak_info.packed_index_hash if self._pak_info.packed_index_hash else b'\x00' * 256)
            if version >= 9:
                f.write(struct.pack('<I', (self._pak_info.stem_hash or 0) ^ keystream[8]))
                f.write(struct.pack('<I', (self._pak_info.unk2 or 0) ^ keystream[9]))
            if version >= 12:
                f.write(self._pak_info.content_org_hash if self._pak_info.content_org_hash else b'\x00' * 20)
            f.write(struct.pack('<B', encrypted_flag_byte))
            f.write(struct.pack('<I', encrypted_magic))
            f.write(struct.pack('<I', version))
            if version >= 6:
                f.write(encrypted_index_hash)
            else:
                f.write(b'\x00' * 20)
            f.write(struct.pack('<Q', encrypted_index_size))
            f.write(struct.pack('<Q', encrypted_index_offset))
        console.print('[bold green]🎉 INJECT COMPLETE![/bold green]')
        console.print(f'[white]Output  :[/] [cyan]{output_pak.name}[/cyan]')

    def _write_to_disk(self, file_path: PurePath, entry: TencentPakEntry) -> None:
        _se33e912f7767 = entry.encryption_method
        _s5206fe150a33 = entry.compression_method
        console.print(f'[#00CCFF]{file_path.name}[/#00CCFF] - Encryption: {_se33e912f7767}, Compression: {_s5206fe150a33}, Blocks: {len(entry.compressed_blocks)}')
        if _se33e912f7767 == 17:
            with open(file_path, 'wb') as _sbb61cc6b3e63:
                for _s576e50701491 in entry.compressed_blocks:
                    _s366d3d829edf = self._file_content[_s576e50701491.start:_s576e50701491.end]
                    _sbb61cc6b3e63.write(_s366d3d829edf)
            return
        with open(file_path, 'wb') as _sbb61cc6b3e63:
            if _s5206fe150a33 == CM_NONE:
                _sb96393f68f4d = self._peek_content(entry.offset, entry.size, _se33e912f7767)
                if entry.encrypted:
                    _sb96393f68f4d = PakCrypto.decrypt_block(bytes(_sb96393f68f4d), file_path, _se33e912f7767)
                _sbb61cc6b3e63.write(_sb96393f68f4d)
                return
            for _s1f6d01ab75cb in PakCrypto.generate_block_indices(len(entry.compressed_blocks), _se33e912f7767):
                _sb96393f68f4d = self._peek_block_content(entry.compressed_blocks[_s1f6d01ab75cb], _se33e912f7767)
                if entry.encrypted:
                    _sb96393f68f4d = PakCrypto.decrypt_block(bytes(_sb96393f68f4d), file_path, _se33e912f7767)
                _sb96393f68f4d = PakCompression.decompress_block(_sb96393f68f4d, self._zstd_dict, _s5206fe150a33)
                _sbb61cc6b3e63.write(_sb96393f68f4d)

    def dump(self, out_path: PurePath) -> None:
        debug_path = BASE_DIR / 'index_debug.txt'

        def _log_path_debug(title, **values):
            try:
                BASE_DIR.mkdir(parents=True, exist_ok=True)
                _se78e1dce92b0 = ['', f'=== {title} ===']
                for _s07c75bc1b558, _s0c49bd2ad1c0 in values.items():
                    _se78e1dce92b0.append(f'{_s07c75bc1b558:<20}: {_s0c49bd2ad1c0!r}')
                _se78e1dce92b0.append('=' * (8 + len(title)))
                _scb74e83bd4bb = '\n'.join(_se78e1dce92b0) + '\n'
                print(_scb74e83bd4bb, flush=True)
                with open(debug_path, 'a', encoding='utf-8') as _s17c5d36b0ad1:
                    _s17c5d36b0ad1.write(_scb74e83bd4bb)
            except Exception:
                pass
        mount_text = str(self._mount_point)
        if '\x00' in mount_text:
            _log_path_debug('INVALID MOUNT POINT', mount_point=mount_text, output_root=str(out_path))
            raise ValueError('PAK mount point contains an embedded NUL character.')
        out_path /= self._mount_point
        skipped_dirs = 0
        skipped_files = 0
        for dir_path, dir in self._index.items():
            dir_text = str(dir_path)
            if '\x00' in dir_text:
                skipped_dirs += 1
                _log_path_debug('INVALID DIRECTORY PATH', directory=dir_text, output_root=str(out_path), reason='embedded NUL character')
                continue
            current_out_path = Path(out_path / dir_path)
            if '\x00' in str(current_out_path):
                skipped_dirs += 1
                _log_path_debug('INVALID OUTPUT DIRECTORY', directory=dir_text, output_path=str(current_out_path), reason='embedded NUL character')
                continue
            try:
                if not current_out_path.exists():
                    current_out_path.mkdir(parents=True, exist_ok=True)
            except (ValueError, OSError) as e:
                skipped_dirs += 1
                _log_path_debug('DIRECTORY CREATE ERROR', directory=dir_text, output_path=str(current_out_path), error=f'{type(e).__name__}: {e}')
                continue
            for file_name, entry in dir.items():
                file_text = str(file_name)
                if '\x00' in file_text:
                    skipped_files += 1
                    _log_path_debug('INVALID FILE NAME', directory=dir_text, file_name=file_text, reason='embedded NUL character')
                    continue
                file_out_path = current_out_path / file_name
                if '\x00' in str(file_out_path):
                    skipped_files += 1
                    _log_path_debug('INVALID FILE OUTPUT PATH', directory=dir_text, file_name=file_text, output_path=str(file_out_path), reason='embedded NUL character')
                    continue
                try:
                    self._write_to_disk(file_out_path, entry)
                except (ValueError, OSError) as e:
                    skipped_files += 1
                    _log_path_debug('FILE WRITE ERROR', directory=dir_text, file_name=file_text, output_path=str(file_out_path), error=f'{type(e).__name__}: {e}')
                    continue
        _log_path_debug('DUMP PATH SUMMARY', skipped_directories=skipped_dirs, skipped_files=skipped_files)

    def dump_filtered(self, out_path: PurePath, extensions) -> dict:
        """
        Extract only entries whose filename ends with one of `extensions`.
        Internal directory structure is preserved under out_path.
        """
        normalized = tuple((ext.lower() if str(ext).startswith('.') else '.' + str(ext).lower() for ext in extensions))
        stats = {'matched': 0, 'extracted': 0, 'failed': 0, 'errors': []}
        for dir_path, files in self._index.items():
            for file_name, entry in files.items():
                if not str(file_name).lower().endswith(normalized):
                    continue
                stats['matched'] += 1
                target_dir = Path(out_path / dir_path)
                target_dir.mkdir(parents=True, exist_ok=True)
                target_file = target_dir / file_name
                try:
                    self._write_to_disk(target_file, entry)
                    stats['extracted'] += 1
                except Exception as e:
                    stats['failed'] += 1
                    stats['errors'].append({'file': str(dir_path / file_name).replace('\\', '/'), 'error': str(e)})
                    console.print(f'[yellow]⚠ Skip {str(dir_path / file_name)}: {str(e)}[/yellow]')
        return stats

    def dump_single_file(self, target_file_name: str, out_path_base: Path, single_file_dir_name: str) -> None:
            entry_found = None
            dir_of_file = None
            for dir_path, dir in self._index.items():
                if target_file_name in dir:
                    entry_found = dir[target_file_name]
                    dir_of_file = dir_path.relative_to(self._mount_point) if dir_path.parts and dir_path.parts[0] == self._mount_point.name else dir_path
                    break
            if entry_found is None:
                console.print(Panel(f"[red]Error: Target file '[bold yellow]{to_fancy(target_file_name)}[/bold yellow]' not found in the PAK index.[/red]"))
                return
            pak_stem = Path(self._file_path).stem
            current_out_path = out_path_base / single_file_dir_name / pak_stem / dir_of_file
            os.makedirs(to_long_path(current_out_path), exist_ok=True)
            target_path = current_out_path / target_file_name
        
            console.print(f"[dim]|[/] [bold white]{to_fancy('SINGLE UNPACK')}:[/bold white] [green]{to_fancy(target_file_name)}[/] [dim]from {self._file_path.name}[/dim]")
            try:
                self._write_to_disk(target_path, entry_found)
                console.print(Panel(f"[green]{to_fancy('Successfully extracted')}: {to_fancy(target_file_name)} -> {target_path.resolve()}[/green]"))
            except Exception as e:
                console.print(Panel(f"[red]Error writing {target_file_name}: {e}[/red]"))

    def find_entry_for_modified(self, relative_path_to_mod_dir: PurePath, is_repack=False):
            dir_part = relative_path_to_mod_dir.parent
            name = relative_path_to_mod_dir.name
        
            if dir_part in self._index:
                for fname, entry in self._index[dir_part].items():
                    if fname.lower() == name.lower() and entry is not None:
                        return dir_part, name, entry
        
            if len(relative_path_to_mod_dir.parts) == 1:
                candidates = []
                for dir_path, dir in self._index.items():
                    for fname, entry in dir.items():
                        if fname.lower() == name.lower() and entry is not None:
                            candidates.append((dir_path, fname, entry))
            
                if len(candidates) == 1:
                
                    return candidates[0]
                elif len(candidates) > 1:
                    return candidates[0]
        
            return None

    def repack_inplace_from_modified_dir(self, pak_file_handle=None) -> bool:
            mod_root = Path(self.MODIFIED_DIR)
            if not os.path.exists(to_long_path(mod_root)):
                console.print(Panel(f"[red]Modified_files folder.{mod_root}[/red]"))
                return False
            need_close = False
            if pak_file_handle is None:
                pak_file_handle = open_long(self._file_path, 'r+b')
                need_close = True
            try:
                any_ok = False
                for root, _, files in os.walk(to_long_path(mod_root)):
                    for fname in files:
                        mpath = Path(os.path.join(root, fname))
                        try:
                            relative_path_for_search = Path(mpath).relative_to(self.MODIFIED_DIR)
                        except ValueError:
                            relative_path_for_search = Path(fname) 
                    
                        match = self.find_entry_for_modified(relative_path_for_search, is_repack=True) 
                        if not match: continue
                    
                        dir_path, name, entry = match
                        target_full_path = (dir_path / name).as_posix()
                    
                        try:
                            ok = self._repack_single_file(pak_file_handle, mpath, entry)
                            if ok:
                                # 👇 Sirf 'Auto-Detected Location:' print hoga, aage ka path hata diya
                                console.print(f"[bold {get_banner_color()}]✓ {to_fancy('Auto-Detected Location')}:[/bold {get_banner_color()}]")
                            
                                # Premium Green Box
                                panel_text = (
                                    f"[bold cyan]Repacking:[/] [bold white]{name}[/]\n"
                                    f"[bold yellow]Target Entry:[/] [bold green]{target_full_path}[/]\n"
                                    f"[bold bright_blue]Encryption Method Applied: {entry.encryption_method}[/]"
                                )
                                from rich import box
                                console.print(Panel(panel_text, border_style=get_banner_color(), box=box.SQUARE))
                            
                                any_ok = True
                            else:
                                console.print(Panel(f"[yellow]{to_fancy('Failed to repack (in-place not possible)')}: {to_fancy(name)}[/yellow]", border_style="yellow"))
                        except Exception as e:
                            console.print(Panel(f"[red]Error repacking {name}: {e}[/red]", border_style="red"))
                return any_ok
            finally:
                if need_close: pak_file_handle.close()

    def _apply_encrypt_for_entry(self, data: bytes, file_path: PurePath, encryption_method: int) -> bytes:
            if encryption_method == 17: return data 
            if PakCrypto._is_simple1_method(encryption_method): return PakCrypto._encrypt_simple1(data)
            if PakCrypto._is_simple2_method(encryption_method):
                data = Misc.pad_to_n(data, SIMPLE2_BLOCK_SIZE)
                assert len(data) % SIMPLE2_BLOCK_SIZE == 0
                return PakCrypto._encrypt_simple2(data)
            if PakCrypto._is_sm4_method(encryption_method):
                bl = SM4.block_length()
                data_aligned = data
                if len(data_aligned) % bl != 0: data_aligned = data_aligned + b'\x00' * (bl - (len(data_aligned) % bl))
                return PakCrypto._encrypt_sm4(data_aligned, file_path, encryption_method)
            raise RuntimeError('Unknown encryption method')

    def _repack_single_file(self, pak_file_handle, modified_file_path: Path, entry: TencentPakEntry) -> bool:
            try:
                with open_long(modified_file_path, 'rb') as f: modified_data = f.read()
            except Exception as e: return False
            encryption_method = entry.encryption_method
            compression_method = entry.compression_method
            if compression_method == CM_NONE:
                out = modified_data
                if entry.encrypted: out = self._apply_encrypt_for_entry(out, modified_file_path, encryption_method)
                aligned_len = PakCrypto.align_encrypted_content_size(len(out), encryption_method)
                if aligned_len > entry.size:
                    diff = aligned_len - entry.size
                    if diff <= MAX_OVERFLOW_BYTES:
                        pak_file_handle.seek(entry.offset)
                        pak_file_handle.write(out)
                        return True
                    else: return False
                pak_file_handle.seek(entry.offset)
                pak_file_handle.write(out)
                if entry.size > aligned_len: pak_file_handle.write(b'\x00' * (entry.size - aligned_len))
                return True
            if entry.compressed_blocks:
                block_size = entry.compression_block_size
                blocks_plain = [modified_data[i:i+block_size] for i in range(0, len(modified_data), block_size)]
                max_blocks = min(len(blocks_plain), len(entry.compressed_blocks))
                blocks_plain = blocks_plain[:max_blocks]
                produced_blocks = [None] * len(entry.compressed_blocks)
                indices = PakCrypto.generate_block_indices(len(entry.compressed_blocks), encryption_method)
                for i_plain, plain in enumerate(blocks_plain):
                    stored_index = indices[i_plain]
                    target_block = entry.compressed_blocks[stored_index]
                    target_len = target_block.end - target_block.start
                    try: comp = PakCompression.compress_block(plain, compression_method, self._zstd_dict, target_len)
                    except Exception as e: return False
                    if len(comp) > target_len:
                        produced_blocks[stored_index] = None; continue
                    if len(comp) < target_len: comp = comp + b'\x00' * (target_len - len(comp))
                    if entry.encrypted: comp = self._apply_encrypt_for_entry(comp, modified_file_path, encryption_method)
                    comp = comp.ljust(PakCrypto.align_encrypted_content_size(len(comp), encryption_method), b'\x00')
                    produced_blocks[stored_index] = comp
                for idx, block in enumerate(entry.compressed_blocks):
                    data_bytes = produced_blocks[idx]
                    if data_bytes is None: continue
                    pak_file_handle.seek(block.start)
                    pak_file_handle.write(data_bytes)
                return True
            return False

def alv_build_pak_filename_map(pak_file):
    """Build safe filename → full pak path map"""
    _se7f3ca17d472 = {}
    for _s7e683b8ac5c2, _se352e8c8e360 in pak_file._index.items():
        for _s36b96ef37a21 in _se352e8c8e360.keys():
            _sb2fd256adcad = str(PurePath(_s7e683b8ac5c2) / _s36b96ef37a21).replace('\\', '/')
            _s0787b701de33 = Path(_s36b96ef37a21).stem.lower()
            _s255a5bcfbd89 = Path(_s36b96ef37a21).suffix.lower()
            _s838b26bde2d8 = _s36b96ef37a21.lower()
            _s38f204919472 = f'{_s0787b701de33}{_s255a5bcfbd89}'
            _s947b4016c945 = _s0787b701de33
            for _sad3366e40b68 in (_s838b26bde2d8, _s38f204919472, _s947b4016c945):
                _se7f3ca17d472.setdefault(_sad3366e40b68, []).append(_sb2fd256adcad)
    return _se7f3ca17d472

def alv_dump_unpacking_log(pak_file, output_log_path: Path):
    """Dump detailed unpacking log"""
    with open(output_log_path, 'w', encoding='utf-8') as log_file:
        log_file.write('=' * 80 + '\n')