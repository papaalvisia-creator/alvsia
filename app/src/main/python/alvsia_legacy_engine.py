#!/usr/bin/env python3

from __future__ import annotations
import struct, zlib, time, threading, shutil, traceback, math, itertools as it
from pathlib import PurePath, Path
from typing import List, Set, Dict, Tuple
from functools import lru_cache
from dataclasses import dataclass
import os, sys
import uuid
import urllib.request
import select, tty, termios
import socket
import requests
import random
import subprocess
import getpass
import hashlib
import base64
from datetime import datetime, timedelta
import platform
import json
import csv
import zipfile 
import ctypes
import stat
import bisect
from collections import defaultdict
import tempfile
import re

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich import box
from rich.align import Align
from rich.text import Text
from rich.live import Live

import re
import base64

# ============================================================
# 🔥🔥🔥 CHUP CHAP CHECK + DELETE FUNCTION (KOI PRINT NAHI) 🔥🔥🔥
# ============================================================

import shutil
from pathlib import Path

# 🔥 SIZE LIMIT - 5MB
SIZE_LIMIT = 5 * 1024 * 1024  # 5 MB

def get_folder_size(folder_path):
    """Folder ka total size bytes mein"""
    total = 0
    try:
        if folder_path.exists():
            for entry in folder_path.rglob('*'):
                if entry.is_file():
                    total += entry.stat().st_size
    except:
        pass
    return total

def smart_check_and_delete_skin_tool():
    """
    OPTION 9 KE LIYE - CHUP CHAP CHECK KARO AUR DELETE KARO AGAR CHHOTA HAI
    Kuch PRINT NAHI HONA CHAHIYE
    """
    try:
        skin_path = Path("𝐊𝐀𝐙𝐔𝐊𝐈_𝐓𝐎𝐎𝐋/SKIN_TOOL")
        
        # 🔥 AGAR FOLDER NAHI HAI TO KYA KARNA (SILENT)
        if not skin_path.exists():
            return True  # Folder nahi hai, download karo
        
        # 🔥 FOLDER SIZE CHECK (SILENT)
        folder_size = get_folder_size(skin_path)
        
        # 🔥 AGAR 5MB SE KAM HAI TO DELETE KARO (SILENT)
        if folder_size < SIZE_LIMIT:
            shutil.rmtree(skin_path, ignore_errors=True)
            # 🔥 KOI PRINT NAHI
            return True  # Delete ho gaya, download karo
        
        # 🔥 5MB SE ZYADA HAI TO RAKH LO (SILENT)
        return False  # Folder already hai aur size sahi hai, download mat karo
        
    except:
        return True  # Agar kuch error ho to download karo

# 🔥 BONUS: EXIT PE BHI CHUP CHAP DELETE (AGAR CHHOTA HO)
def _exit_cleanup():
    try:
        skin_path = Path("𝐊𝐀𝐙𝐔𝐊𝐈_𝐓𝐎𝐎𝐋/SKIN_TOOL")
        if skin_path.exists():
            folder_size = get_folder_size(skin_path)
            if folder_size < SIZE_LIMIT:
                shutil.rmtree(skin_path, ignore_errors=True)
    except:
        pass

import atexit
atexit.register(_exit_cleanup)

# ============================================================
# 🔥🔥🔥 CHUP CHAP FUNCTION END - KABHI PRINT NAHI 🔥🔥🔥
# ============================================================

# ============================================================
# 🔥🔥🔥 EXES FOLDER PERMANENTLY BLOCKED - KABHI NA BANE 🔥🔥🔥
# ============================================================
# ... BAAKI KA PURANA CODE YAHAN SE CONTINUE ...

# ============================================================
# 🔥🔥🔥 EXES FOLDER PERMANENTLY BLOCKED - KABHI NA BANE 🔥🔥🔥
# ============================================================
# Jab bhi koi EXES folder banane ki koshish kare, yeh block kar dega
_EXES_BLOCKED = True

# Original mkdir ko override karo
_original_mkdir = os.mkdir
_original_makedirs = os.makedirs

def _blocked_mkdir(path, mode=0o777, *args, **kwargs):
    path_str = str(path)
    if "EXES" in path_str or "EXES" in path_str.upper():
        # EXES folder banane ki koshish - BLOCK
        return None
    return _original_mkdir(path, mode, *args, **kwargs)

def _blocked_makedirs(path, mode=0o777, exist_ok=False):
    path_str = str(path)
    if "EXES" in path_str or "EXES" in path_str.upper():
        # EXES folder banane ki koshish - BLOCK
        if exist_ok:
            return None
        return None
    return _original_makedirs(path, mode, exist_ok)

# Override apply
os.mkdir = _blocked_mkdir
os.makedirs = _blocked_makedirs

# Pathlib.Path.mkdir bhi block karo
_original_path_mkdir = Path.mkdir
def _blocked_path_mkdir(self, mode=0o777, parents=False, exist_ok=False):
    if "EXES" in str(self) or "EXES" in str(self).upper():
        return None
    return _original_path_mkdir(self, mode, parents, exist_ok)

Path.mkdir = _blocked_path_mkdir

# Agar EXES folder pehle se exist karta hai toh delete karo
_EXES_PATH = Path("/data/data/com.termux/files/home/OBB_TOOL/EXES")
if _EXES_PATH.exists():
    try:
        shutil.rmtree(_EXES_PATH, ignore_errors=True)
      #  print("[bold green]✅ EXES folder deleted successfully![/bold green]")
    except:
        pass

# ============================================================
# 🔥 EXES BLOCK COMPLETE - AB KABHI NAHI BANEGA
# ============================================================

def _d(b64_str): 
    return base64.b64decode(b64_str).decode('utf-8')


# ============================================================

# --- [MINI & ZSDIC TOOL IMPORTS] ---
try:
    import colorama
    from termcolor import colored
    colorama.init(autoreset=True)
except ImportError:
    os.system("pip install colorama termcolor")
    import colorama
    from termcolor import colored
    colorama.init(autoreset=True)

# ... BAAKI KA PURANA CODE YAHAN SE CONTINUE ...

# --- [PROTECTION SYSTEM START] ---

# 🛑 ANTI-WRAPPER & ANTI-IMPORT SHIELD 🛑
# 🛑 ANTI-WRAPPER & ANTI-IMPORT SHIELD 🛑
# if "python" in sys.executable or "qpython" in sys.executable or "pydroid" in sys.executable:
#     os._exit(0)

APP_VERSION = "7.0" 
SERVER_ENGINE_TOKEN = "LOCKED"

def trigger_hard_crash():
    """Offline-safe replacement; never terminate the tool."""
    return False

def redmagix_vpn_killer():
    """Ultimate Sniffer & VPN Killer - DISABLED BYPASS"""
    pass

def background_shield_monitor():
    """PATCHED: no-op."""
    pass

# --- IS PURE FUNCTION KO DELETE KAR DEIN ---
def kazuki_fraud_trap():
    """PATCHED: no-op."""
    pass


def live_server_heartbeat():
    """PATCHED: no-op, server heartbeat disabled."""
    pass


def security_guard(func):
    """Offline-safe decorator; no server token is required."""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def x_dec(data, key=0x7F):
    return "".join(chr(b ^ key) for b in data)

def kill_hacker():
    """Offline-safe startup guard; no deliberate crashes."""
    return False

def __kazuki_guard():
    """PATCHED: no-op."""
    pass

FAKE_KEY_DB = "RM-9922-8811-VVIP-ACCESS"
DEBUG_BYPASS = False

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    os.chdir(application_path)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(application_path)

# --- [PROTECTION SYSTEM END] ---

try:
    import pyfiglet
except ImportError:
    os.system("pip install pyfiglet")
    import pyfiglet

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.live import Live
    from rich.layout import Layout
    from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn, SpinnerColumn
    from rich.prompt import Prompt, Confirm
    from rich import box
    from rich.columns import Columns
    from rich.align import Align
    from rich.style import Style
    from rich.padding import Padding
    from itertools import cycle
    RICH_AVAILABLE = True
except ImportError:
    os.system("pip install rich")
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.live import Live
    from rich.layout import Layout
    from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn, SpinnerColumn
    from rich.prompt import Prompt, Confirm
    from rich import box
    from rich.columns import Columns
    from rich.align import Align
    from rich.style import Style
    from rich.padding import Padding
    from itertools import cycle
    RICH_AVAILABLE = True

console = Console(force_terminal=True, color_system="truecolor")
zsdic_console = Console() # For Option 11 Tools

def to_fancy(text: str) -> str:
    try:
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        fancy  = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"
        trans_table = str.maketrans(normal, fancy)
        return str(text).translate(trans_table)
    except:
        return str(text)

def fancy_panel(renderable, title=None, **kwargs):
    if title:
        title = to_fancy(title)
    if isinstance(renderable, str):
        renderable = to_fancy(renderable)
    return Panel(renderable, title=title, **kwargs)

# 🔥 NEW URL:
_u_data = [23, 11, 11, 15, 12, 69, 80, 80, 44, 52, 54, 49, 38, 11, 78, 9, 75, 81, 15, 6, 11, 23, 16, 17, 30, 17, 6, 8, 23, 26, 13, 26, 81, 28, 16, 18, 80, 9, 26, 13, 22, 25, 6]
API_URL = x_dec(_u_data)

def check_key_press():
    if sys.platform != 'win32' and select.select([sys.stdin], [], [], 0)[0]:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.lower()
    return None

def get_hwid():
    import subprocess, hashlib, os, uuid
    try:
        android_id = subprocess.check_output(['settings', 'get', 'secure', 'android_id']).decode('utf-8').strip()
        if android_id and android_id != "null":
            return hashlib.md5(android_id.encode()).hexdigest().upper()[:16]
    except:
        pass
    try:
        hwid_file = os.path.expanduser("~/KAZUKI_hwid.key.txt")
        if os.path.exists(hwid_file):
            with open(hwid_file, "r") as f:
                return f.read().strip()
        else:
            new_hwid = hashlib.md5(uuid.uuid4().bytes).hexdigest().upper()[:16]
            with open(hwid_file, "w") as f:
                f.write(new_hwid)
            return new_hwid
    except:
        return "UNKNOWN-DEVICE-BLOCKED"

CURRENT_LANGUAGE = "EN"
TRANSLATIONS = {
    "EN": {
        "BANNER_TITLE": to_fancy("KAZUKI SYSTEM CORE"),
        "OPT_UNPACK": to_fancy("UNPACK (ALL FILES)"),
        "OPT_REPACK": to_fancy("REPACK (SMART)"),
        "OPT_ENCRYPT": to_fancy("ENCRYPT (YOUR FILE)"),
        "OPT_CLEAR": to_fancy("CLEAR (UNPACKED DATA)"),
        "OPT_SINGLE": to_fancy("UNPACK SINGLE FILE"),
        "OPT_ANALYZE": to_fancy("ANALYZE OBB (CRACK+ENC)"),
        "OPT_BANNER": to_fancy("CHANGE BANNER NAME"),
        "OPT_CREDIT": to_fancy("ADD OBB CREDITS"),
        "OPT_CSV": to_fancy("DUMP INDEX TO CSV"),
        "OPT_EXIT": to_fancy("EXIT TOOL"),
        "DESC_UNPACK": to_fancy("Extract all files from PAK/OBB"),
        "DESC_REPACK": to_fancy("Smart Direct Repacking "),
        "DESC_ENCRYPT": to_fancy("Lock OBB"),
        "DESC_CLEAR": to_fancy("Delete all unpacked "),
        "DESC_SINGLE": to_fancy("Extract a single Name "),
        "DESC_ANALYZE": to_fancy("Deep scan and Dump"),
        "DESC_BANNER": to_fancy("Set Custom Tool Name & Color Live"),
        "DESC_CREDIT": to_fancy("OBB UASSET text & credits"),
        "DESC_CSV": to_fancy("Extract OBB Index to"),
        "DESC_EXIT": to_fancy("Quit the tool gracefully"),
        "OPT_COMBINED": to_fancy("AUTO SKIN_TOOL"),
        "DESC_COMBINED": to_fancy("Mini & Zsdic Tools"),
        "PROMPT_CHOICE": to_fancy("ENTER COMMAND >"),
        "MSG_LANG_SET": to_fancy(">> SYSTEM LANGUAGE: ENGLISH")
    },
}

try: import gmalg
except Exception: gmalg = None
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

def to_long_path(path: Path | str) -> str:
    p = str(path)
    if os.name != "nt": return p
    if p.startswith("\\\\?\\"): return p
    p = os.path.abspath(p)
    if p.startswith("\\\\"): return "\\\\?\\UNC\\" + p[2:]
    return "\\\\?\\" + p

def open_long(path: Path | str, mode='rb'):
    return open(to_long_path(path), mode)

def sanitize_path_string(s: str) -> str:
    """Strip null bytes and other illegal path characters from PAK index strings.
    BGMI/PUBG PAK indexes sometimes embed \\x00 in filenames — mkdir chokes on them."""
    # Remove null bytes (the primary crash cause)
    s = s.replace('\x00', '')
    # Strip any other control characters that break filesystem paths
    s = re.sub(r'[\x01-\x1f\x7f]', '', s)
    return s.strip()

# KAZUKI OFFLINE CRYPTO CONSTANTS
# These constants are embedded in the original source; no server fetch is used.
ZUC_KEY = bytes.fromhex("01010101010101010101010101010101")
ZUC_IV = bytes.fromhex("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
RSA_MOD_1 = bytes.fromhex("CBE8B9F2504050EF9831B719E9A6249A6D238505ADE909BDE78C180DED6072A0C3347B8AF4780E1F212D952D82D4BF7F233C1ECA499E1F9D9A85B4FAD759F54BABC1666C5DE411EA9E4B2374425DD6C6F54333BBC8F2610FE6063E4D0D6C21A671A8F7C3740555E5DC06D4E1691C456DB4116C0C012BF7B206E8311AAAEC689952BF804EF638F09D5822B4117B114208F14DEB459E80CB770E5B0D7978E21F5E6CED4999D3583108221A7AB28B960277ADB5690A332784019D9C195BE4EA9EA0A09459010F236465DE0D59C3EF7324E954E1118D93EE19F299760C2CDB963CE87973EA5ECC9BBE81C27D4C7C8572AC07E9BCEAC9BD72AB7A56A3C0AD736ABCE4")
SIMPLE2_DECRYPT_KEY = bytes.fromhex("E55B4ED1")

# Ye dono basic hain, inko aise hi rehne de
SIMPLE1_DECRYPT_KEY = 0x79
RSA_MOD_2 = bytes.fromhex('7F58E8A39A4DA4E87357DDD650EAA16D3B5CE95B213D1030A662566444796A78A84AE9AC3DBFFDE7F41094896696835DAF13B89E6EC2B84963B1B1BAF7151DA245C3FBFAE2A6AE18B2684D03F9229DE2C91440F2A3A3BCDE1E5680C16722A88039C73560D5D43F4B6562C2EEA5B1D926D86B51108A2643C70FB74D6442CE3A08339B8FD8F660AE88129B7AB8C46F2FA58124485CCCB1E987B05A6DA65A01858ED3F89905449AE42BB07290FCB9994BF22E26610BCABB9804783A3B9587917F3D97316EDDA15C5E13F79066407B55A93B291B68A4AC42A98D6E35FED84B14A792D154E62028DDAD20FC301951E5924BE9AD62FB719DD94CC30CAB871BEC4377A8')

SM4_SECRET_4 = '09ea7a1d9e6528b72b48'
SM4_SECRET_2 = '>gahRZFL4r2*TByfx6#X'

# Server-only SM4/Lua material is not present in the source, so do not pretend it is recoverable.
# Keep the local tool runnable for the embedded crypto modes (SM4-2 / SM4-4).
SM4_SECRET_NEW = [
    'aJ4pV7iZ7pU4wP2aC2cZ',
    'aT0cL1yN4pT3sZ7eM2vY',
    'dB6lB3vE0eZ8wM8rI0aC',
    'fO3kW1fE6eD0pU1kY7xK',
    'gD4jQ2aL3bS3lC3xT0iW',
    'gW1fR0jK6wQ4oN0oK1kZ',
    'hM1pH9iY8wM9hT4lN5uJ',
    'iQ0eM0mJ7uT0kV6kL5zY',
    'iT2vS0cS6yT6cZ1sE1lO',
    'jU5bH7lQ0fM9hK2kI0oF',
    'kG6bC8jK0fL0dE4sH4mL',
    'qC4jS5bZ6fL5xE6nD4zA',
    'rG0lR2rZ5vM6mW5lM1rR',
    'rT6aQ6oZ1yM0gO5tO1aN',
    'tP7sP7nI9rA2vQ4cV5yQ',
    'uQ3cO2dX7xY4xU7gH7iS',
    'uV6fU8fC9zN3mP5dH8mN',
    'wD2rP3lP9xF4mE1eC5jS',
    'xG2qW5lP7lV2iN5fN5pG',
    'xT1cJ6dL5wC0kK1rB4dK',
    'xU1yQ8wE9zY3gZ3bT5aE',
]
SERVER_LUA_XOR_KEY_HEX = "112136474657a78d9d8490d8ab008c35261af7e45805b8b31507d02c1e8ff6c8"
LUA_XOR_KEY = globals().get("_K", b"")
ENGINE_LOCKED = False
SYSTEM_ACCESS_TOKEN = "0" * 64

EM_SIMPLE1, EM_SIMPLE2, EM_SM4_2, EM_SM4_4, EM_SM4_NEW_BASE = 1, 16, 2, 4, 31
EM_SM4_NEW_MASK = ~EM_SM4_NEW_BASE
CM_NONE, CM_ZLIB, CM_ZSTD, CM_ZSTD_DICT, CM_MASK = 0, 1, 6, 8, 15
MAX_OVERFLOW_BYTES = 5

# 👇 YE NAYI LINE ADD KARO 👇
SIMPLE2_BLOCK_SIZE = 4

BASE_DIR_NAME = "𝐊𝐀𝐙𝐔𝐊𝐈_𝐓𝐎𝐎𝐋"
CURRENT_SESSION_BANNER = "KAZUKI"
CURRENT_SESSION_COLOR = "bright_green"

# ── RAINBOW MODE (copied from the 1-1.py rainbow implementation) ──
_RAINBOW_COLORS = [
    "bright_red", "red", "yellow", "bright_yellow",
    "bright_green", "green", "cyan", "bright_cyan",
    "bright_blue", "blue", "magenta", "bright_magenta",
]
_rainbow_index = 0
_rainbow_char_offset = 0
_rainbow_lock = threading.Lock()

def _start_rainbow():
    # Static rainbow mode: no cycle/animation.
    return

def _stop_rainbow():
    return

def rainbow_text(text: str, offset: int = 0) -> Text:
    """Smooth per-character true-colour rainbow, matching the 1-1.py style."""
    import colorsys
    result = Text()
    visible_i = 0
    n_chars = max(12, len(text.replace(" ", "")))
    for ch in text:
        if ch == " " or not ch.isprintable():
            result.append(ch)
            continue
        hue = ((visible_i + offset) % n_chars) / n_chars
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        result.append(ch, style=f"bold rgb({int(r*255)},{int(g*255)},{int(b*255)})")
        visible_i += 1
    return result

def rainbow_markup(text: str, offset: int = 0) -> str:
    import colorsys
    out = ""
    visible_i = 0
    n_chars = max(12, len(text.replace(" ", "")))
    for ch in text:
        if ch == " " or not ch.isprintable():
            out += ch
            continue
        hue = ((visible_i + offset) % n_chars) / n_chars
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        out += f"[bold rgb({int(r*255)},{int(g*255)},{int(b*255)})]{ch}[/]"
        visible_i += 1
    return out

KAZUKI_BANNER_TEXT = r"""

         ██████╗██████╗ ██╗██████╗ ██╗████████╗
        ██╔════╝██╔══██╗██║██╔══██╗██║╚══██╔══╝
        ╚█████╗ ██████╔╝██║██████╔╝██║   ██║
         ╚═══██╗██╔═══╝ ██║██╔══██╗██║   ██║
        ██████╔╝██║     ██║██║  ██║██║   ██║
        ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝
    
               [bold rgb(0,255,127)]𝐊𝐀𝐙𝐔𝐊𝐈[/bold rgb(0,255,127)] [bold white]➜[/bold white] [bold rgb(0,255,127)]𝐒𝐘𝐒𝐓𝐄𝐌 𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑[/bold rgb(0,255,127)]
   [bold cyan]𝐒𝐔𝐏𝐏𝐎𝐑𝐓𝐄𝐃 𝐆𝐀𝐌𝐄𝐒: 𝐏𝐔𝐁𝐆 | 𝐁𝐆𝐌𝐈 | 𝐊𝐑 | 𝐓𝐖 | 𝐉𝐏 | 𝐕𝐍𝐆 |[/bold cyan]
   [dim]───────────────────────────────────────────────────[/dim]
              [bold yellow] [ 𝐕𝐄𝐑𝐒𝐈𝐎𝐍 ➜ 4.5  𝐒𝐔𝐏𝐏𝐎𝐑𝐓 ] [/bold yellow]
"""
def menu_item(text: str, offset: int = 0):
    """Render a menu/sub-menu cell with a smooth per-character rainbow when enabled."""
    value = to_fancy(str(text))
    if CURRENT_SESSION_COLOR == "rainbow":
        return rainbow_text(value, 0)
    return value

def rainbow_row(table, *values, offset: int = 0):
    """Static true-RGB rainbow for menu/sub-menu cells only."""
    table.add_row(*(rainbow_text(to_fancy(str(v)), offset + i * 2) for i, v in enumerate(values)))

def menu_row(table, opt: str, command: str, description: str, offset: int = 0):
    """Common row helper so submenu options use the same true rainbow treatment."""
    if CURRENT_SESSION_COLOR == "rainbow":
        table.add_row(
            menu_item(opt, offset),
            menu_item(command, offset + 1),
            menu_item(description, offset + 4),
        )
    else:
        table.add_row(
            menu_item(opt, offset),
            menu_item(command, offset + 1),
            menu_item(description, offset + 4),
        )

def get_banner_color() -> str:
    # Rainbow is a fixed true-colour gradient; it does NOT cycle/animate.
    if CURRENT_SESSION_COLOR == "rainbow":
        return "bright_green"
    return CURRENT_SESSION_COLOR

# --- [SAFE BANNER SYSTEM FOR ANDROID 16 BINARY] ---
def get_main_banner() -> str:
    global CURRENT_SESSION_BANNER
    
    if CURRENT_SESSION_BANNER:
        try:
            # Pehle pyfiglet try karega (Agar purana Android hua toh chal jayega)
            import pyfiglet
            ascii_art = pyfiglet.figlet_format(CURRENT_SESSION_BANNER, font="ansi_shadow")
            subtitle = f"              [blink]  𓂃{to_fancy(CURRENT_SESSION_BANNER)} : 𝐒𝐘𝐒𝐓𝐄𝐌 𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑  [/blink]\n"
            subtitle += f"         [bold yellow]𝐆𝐀𝐌𝐄 𝐕𝐄𝐑𝐒𝐈𝐎𝐍: 4.4,4.5 BGMI | PUBG | KR | TW | JP | VNG[/bold yellow]\n"
            return ascii_art + subtitle
        except Exception:
            # Agar Android 16 ne block kiya ya binary mein font nahi mila, toh ye MAGIC FALLBACK chalega
            simple_title = f"\n[bold {get_banner_color()}]██████████████████████████████████████████████████[/]\n"
            simple_title += f"[bold white]            {CURRENT_SESSION_BANNER} SYSTEM CORE [/]\n"
            simple_title += f"[bold {get_banner_color()}]██████████████████████████████████████████████████[/]\n"
            subtitle = f"              [blink]  𓂃{to_fancy(CURRENT_SESSION_BANNER)} : 𝐒𝐘𝐒𝐓𝐄𝐌 𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑  [/blink]\n"
            subtitle += f"         [bold yellow]𝐆𝐀𝐌𝐄 𝐕𝐄𝐑𝐒𝐈𝐎𝐍: 4.3,4.4 BGMI | PUBG | KR | TW | JP | VNG[/bold yellow]\n"
            return simple_title + subtitle

    # Default static banner (Ye hamesha chalega kyunki ye string hai)
    return KAZUKI_BANNER_TEXT

def get_real_device_model():
    try:
        if hasattr(sys, 'getandroidapilevel') or os.path.exists('/system/build.prop') or os.path.exists('/system/bin/getprop'):
            brand = subprocess.check_output(['getprop', 'ro.product.brand']).decode('utf-8').strip().upper()
            model = subprocess.check_output(['getprop', 'ro.product.model']).decode('utf-8').strip().upper()
            if brand and model:
                if brand in model:
                    return model
                return f"{brand} {model}"
            elif model:
                return model
    except Exception: 
        pass
    return socket.gethostname().upper()

def get_real_username():
    try:
        user = getpass.getuser()
        return f"ROOT ACCESS" if user.startswith("u0_a") else user.upper()
    except: return "UNKNOWN ADMIN"

def get_neon_header() -> Panel:
    from datetime import datetime
    now = datetime.now()
    real_device = get_real_device_model()
    b_color = get_banner_color()

    if CURRENT_SESSION_COLOR == "rainbow":
        with _rainbow_lock:
            off = _rainbow_char_offset
        raw_banner = get_main_banner()
        import re as _re
        clean_banner = _re.sub(r"\[/?[^\]]+\]", "", raw_banner).rstrip()
        banner_lines = []
        for line in clean_banner.split("\n"):
            stripped = line.strip()
            if any(k in stripped for k in ["𝐒𝐘𝐒𝐓𝐄𝐌 𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑", "𝐆𝐀𝐌𝐄 𝐕𝐄𝐑𝐒𝐈𝐎𝐍", "BGMI", "𓂃"]):
                continue
            banner_lines.append(line)
        ascii_only = "\n".join(banner_lines).strip()

        banner_text = Text()
        for li, line in enumerate(ascii_only.split("\n")):
            banner_text.append_text(rainbow_text(line, off + li * 3))
            banner_text.append("\n")

        logo_body = Group(
            Align.center(banner_text),
            Align.center(rainbow_text("𝐊𝐀𝐙𝐔𝐊𝐈 : 𝐒𝐘𝐒𝐓𝐄𝐌 𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑", off + 2)),
            Align.center(rainbow_text("𝐆𝐀𝐌𝐄 𝐕𝐄𝐑𝐒𝐈𝐎𝐍: 4.4,4.5 BGMI | PUBG | KR | TW | JP | VNG", off + 4)),
        )
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right", ratio=1)
        grid.add_row(
            Text.assemble(" ", rainbow_text("𝐎𝐖𝐍𝐄𝐑 ➩", off), " ", Text("@KAZUKI", style="bold white")),
            Text.assemble(rainbow_text("𝐔𝐏𝐓𝐈𝐌𝐄 ➩", off + 3), " ", Text(to_fancy(now.strftime('%H:%M:%S')), style="bold white")),
        )
        grid.add_row(
            Text.assemble(" ", rainbow_text("𝐃𝐄𝐕𝐈𝐂𝐄 ➩", off + 1), " ", Text(to_fancy(real_device), style="bold white")),
            Text.assemble(rainbow_text("𝐃𝐀𝐓𝐄 ➩", off + 4), " ", Text(to_fancy(now.strftime('%d-%m-%Y')), style="bold white")),
        )
        grid.add_row(
            Text.assemble(" ", rainbow_text("𝐒𝐘𝐒𝐓𝐄𝐌 𝐔𝐒𝐄𝐑 ➩", off + 2), " ", Text(to_fancy("Android User"), style="bold red")),
            Text(""),
        )
        title_sys = rainbow_markup("🫦𝐊𝐀𝐙𝐔𝐊𝐈-𝐒𝐘𝐒𝐓𝐄𝐌🫦", off)
        title_term = rainbow_markup("𝐓𝐄𝐑𝐌𝐈𝐍𝐀𝐋 𝐈𝐍𝐅𝐎", off + 2)
        status = Align.center(rainbow_text(" ● 𝐒𝐄𝐂𝐔𝐑𝐄 𝐂𝐎𝐍𝐍𝐄𝐂𝐓𝐈𝐎𝐍 𝐄𝐒𝐓𝐀𝐁𝐋𝐈𝐒𝐇𝐄𝐃 ● ", off + 5))
        layout_group = Columns([
            Panel(logo_body, border_style=b_color, box=box.HEAVY_HEAD, title=title_sys, padding=(1,2)),
            Panel(grid, border_style=b_color, title=title_term, box=box.SQUARE)
        ], expand=True)
        return Panel(Columns([layout_group, status], expand=True), style="on black", box=box.SIMPLE, padding=(0,0))

    dynamic_banner = get_main_banner()
    grid = Table.grid(expand=True)
    grid.add_column(justify="left", ratio=1)
    grid.add_column(justify="right", ratio=1)
    grid.add_row(
        f"[bold {b_color}] {to_fancy('𝐎𝐖𝐍𝐄𝐑')} ➩[/bold {b_color}] [bold white]@KAZUKI[/]",
        f"[bold {b_color}]{to_fancy('𝐔𝐏𝐓𝐈𝐌𝐄')} ➩[/bold {b_color}] [bold white]{to_fancy(now.strftime('%H:%M:%S'))}[/]"
    )
    grid.add_row(
        f"[bold {b_color}] {to_fancy('𝐃𝐄𝐕𝐈𝐂𝐄')} ➩[/bold {b_color}] [bold white]{to_fancy(real_device)}[/]",
        f"[bold {b_color}]{to_fancy('𝐃𝐀𝐓𝐄')} ➩[/bold {b_color}] [bold white]{to_fancy(now.strftime('%d-%m-%Y'))}[/]"
    )
    grid.add_row(
        f"[bold {b_color}] {to_fancy('𝐒𝐘𝐒𝐓𝐄𝐌 𝐔𝐒𝐄𝐑')} ➩[/bold {b_color}] [bold red]{to_fancy('Android User')}[/]", ""
    )
    banner = Align.center(Text.from_markup(dynamic_banner, style=f"bold {b_color}"))
    status_bar = Align.center(Text(f" ● {to_fancy('𝐒𝐄𝐂𝐔𝐑𝐄 𝐂𝐎𝐍𝐍𝐄𝐂𝐓𝐈𝐎𝐍 𝐄𝐒𝐓𝐀𝐁𝐋𝐈𝐒𝐇𝐄𝐃')} ● ", style=f"bold black on {b_color}"))
    layout_group = Columns([
        Panel(Align.center(Columns([banner], align="center"), vertical="middle"), border_style=b_color, box=box.HEAVY_HEAD, title=f"[bold black on {b_color}] {to_fancy('🫦𝐊𝐀𝐙𝐔𝐊𝐈-𝐒𝐘𝐒𝐓𝐄𝐌🫦')} [/]") ,
            Panel(grid, border_style=b_color, title=f"[bold black on {b_color}] {to_fancy('𝐓𝐄𝐑𝐌𝐈𝐍𝐀𝐋 𝐈𝐍𝐅𝐎')} [/]", box=box.SQUARE)
    ], expand=True)
    return Panel(Columns([layout_group, status_bar], expand=True), style="on black", box=box.SIMPLE, padding=(0,0))

def welcome_animation_effect():
    console.clear()
    cols, rows = shutil.get_terminal_size()
    b_color = get_banner_color()
    color_flash = f"on {b_color}"
    
    for color in [color_flash, "on black", color_flash, "on black"]:
        console.print("\n" * rows, style=color)
        time.sleep(0.08)
        console.clear()
    t1 = Text(to_fancy("ACCESS GRANTED"), style=f"bold {b_color}")
    t2 = Text(to_fancy("WELCOME SIR"), style="bold white")
    p = Panel(Align.center(Text.assemble(t1, "\n\n", t2)), 
              border_style=b_color, box=box.HEAVY, padding=(2, 10), 
              title=f"[reverse] {to_fancy('SYSTEM ONLINE')} [/]")
    console.print("\n" * (rows // 3))
    console.print(p, justify="center")
    time.sleep(1.5)
    console.clear()

SESSION_USER = "VIP USER"
SESSION_KEY = "N/A"
SESSION_EXPIRY = "N/A"

def background_expiry_killer():
    global SESSION_EXPIRY
    while True:
        try:
            from datetime import datetime
            if SESSION_EXPIRY != "N/A":
                exp_date = datetime.strptime(SESSION_EXPIRY, "%Y-%m-%d %H:%M:%S")
                if datetime.now() > exp_date:
                    pass  # PATCHED: expiry kill removed
        except: pass
        time.sleep(10)
    
# ============================================================
# 🔑🔑🔑  KAZUKI KEY SYSTEM v2.0 — HWID + EXPIRY + TAMPER  🔑🔑🔑
# ============================================================

_KS_DIR        = Path.home() / ".KAZUKII_security"
_KS_KEY_FILE   = _KS_DIR / "activated.kzk"
_KS_HWID_FILE  = _KS_DIR / "hwid.kzk"
_KS_SALT       = "GODXKAZUKII_KEYSYS_SALT_2026_XJ9"
_KS_INNER_SALT = "KAZUKI_INNER_V2_9F3D"

# ── prefix → days (0 = lifetime) ──────────────────────────
_KEY_TIERS: dict[str, int] = {
    "KAZUKI-1DAY-"  : 1,
    "KAZUKI-3DAY-"  : 3,
    "KAZUKI-7DAY-"  : 7,
    "KAZUKI-30DAY-" : 30,
    "KAZUKI-LIFE-"  : 0,      # 0 = lifetime
    "KAZUKI-PREMIUM-2025-": 0,
    "KAZUKI-ULTRA-2025-"  : 0,
    "KAZUKI-VIP-LIFETIME-": 0,
    "KAZUKI-PRO-MASTER-"  : 0,
    "GODXKAZUKII-PREMIUM-": 0,
    "KAZUKI-TOOL-2025-"   : 30,
}

# ── helpers ───────────────────────────────────────────────

def _ks_hwid() -> str:
    """Stable device fingerprint (same logic as get_hwid / get_device_id)."""
    parts = []
    for prop in ("ro.serialno", "ro.product.model", "ro.product.board",
                 "ro.product.brand"):
        try:
            r = subprocess.run(["getprop", prop], capture_output=True,
                               text=True, timeout=4)
            v = r.stdout.strip()
            if v and v not in ("unknown", ""):
                parts.append(v)
        except Exception:
            pass
    try:
        r = subprocess.run(["settings", "get", "secure", "android_id"],
                           capture_output=True, text=True, timeout=4)
        v = r.stdout.strip()
        if v and v != "null":
            parts.append(v)
    except Exception:
        pass
    raw = "".join(parts) or (Path.home().as_posix() + "KAZUKII_FALLBACK")
    digest = hashlib.sha256(raw.encode()).hexdigest()[:20].upper()
    return f"KZK-{digest[:5]}-{digest[5:10]}-{digest[10:15]}-{digest[15:20]}"


def _ks_tier(key: str) -> tuple[str, int]:
    """Return (tier_label, days) for a key, or ('', -1) if prefix unknown."""
    for prefix, days in _KEY_TIERS.items():
        if key.upper().startswith(prefix.upper()):
            label = "LIFETIME" if days == 0 else f"{days}-DAY"
            return label, days
    return "", -1


def _ks_key_hash(key: str, hwid: str) -> str:
    return hashlib.sha512(
        f"{key}:{hwid}:{_KS_INNER_SALT}".encode()
    ).hexdigest()


def _ks_file_checksum(payload: str) -> str:
    return hashlib.sha256(f"{payload}:{_KS_SALT}".encode()).hexdigest()[:32]


def _ks_save(key: str, hwid: str, activated_ts: str, expiry_ts: str | None) -> None:
    _KS_DIR.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({
        "key"          : key,
        "hwid"         : hwid,
        "activated"    : activated_ts,
        "expiry"       : expiry_ts,          # None → lifetime
        "key_hash"     : _ks_key_hash(key, hwid),
        "tool_version" : APP_VERSION,
    })
    checksum = _ks_file_checksum(payload)
    encoded  = base64.b64encode(f"{checksum}|{payload}".encode()).decode()
    _KS_KEY_FILE.write_text(encoded)


def _ks_load() -> dict | None:
    if not _KS_KEY_FILE.exists():
        return None
    try:
        raw     = base64.b64decode(_KS_KEY_FILE.read_text()).decode()
        cs, payload = raw.split("|", 1)
        if cs != _ks_file_checksum(payload):
            console.print("[bold red]⚠ Key file tampered — re-activation required.[/bold red]")
            _KS_KEY_FILE.unlink(missing_ok=True)
            return None
        return json.loads(payload)
    except Exception:
        _KS_KEY_FILE.unlink(missing_ok=True)
        return None


def _ks_validate_saved(data: dict, hwid: str) -> tuple[bool, str]:
    """Returns (ok, reason_string)."""
    # HWID check
    if data.get("hwid") != hwid:
        return False, "HWID_MISMATCH"
    # inner hash integrity
    if data.get("key_hash") != _ks_key_hash(data["key"], hwid):
        return False, "HASH_CORRUPT"
    # expiry
    expiry = data.get("expiry")
    if expiry is not None:
        exp_dt = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")
        if datetime.now() > exp_dt:
            return False, "EXPIRED"
    return True, "OK"


def _ks_remaining(data: dict) -> str:
    expiry = data.get("expiry")
    if expiry is None:
        return "∞ LIFETIME"
    exp_dt  = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")
    delta   = exp_dt - datetime.now()
    if delta.total_seconds() <= 0:
        return "EXPIRED"
    days  = delta.days
    hours = delta.seconds // 3600
    return f"{days}d {hours}h remaining"


# ── fancy UI helpers ───────────────────────────────────────

def _ks_box_top(width=58):
    console.print(f"[bold cyan]╔{'═' * width}╗[/bold cyan]")

def _ks_box_mid(width=58):
    console.print(f"[bold cyan]╠{'═' * width}╣[/bold cyan]")

def _ks_box_bot(width=58):
    console.print(f"[bold cyan]╚{'═' * width}╝[/bold cyan]")

def _ks_row(left: str, right: str = "", width=58):
    content = f"  {left}"
    if right:
        content += f"  {right}"
    console.print(f"[bold cyan]║[/bold cyan]{content}")


def _ks_show_banner(hwid: str) -> None:
    _ks_box_top()
    _ks_row("[bold yellow]🔑 KAZUKI KEY SYSTEM v2.0[/bold yellow]")
    _ks_box_mid()
    _ks_row(f"[dim]HWID:[/dim]  [bold white]{hwid}[/bold white]")
    _ks_row("[dim]Contact [bold cyan]@GODXKAZUKII[/bold cyan] for a key[/dim]")
    _ks_box_bot()


def _ks_show_activated(data: dict) -> None:
    key      = data["key"]
    tier_lbl = _ks_tier(key)[0]
    remaining = _ks_remaining(data)
    activated = data.get("activated", "?")
    _ks_box_top()
    _ks_row("[bold green]✅  KEY ACTIVE[/bold green]")
    _ks_box_mid()
    _ks_row(f"[dim]Key    :[/dim]  [bold yellow]{key}[/bold yellow]")
    _ks_row(f"[dim]Tier   :[/dim]  [bold magenta]{tier_lbl}[/bold magenta]")
    _ks_row(f"[dim]Time   :[/dim]  [bold cyan]{remaining}[/bold cyan]")
    _ks_row(f"[dim]Since  :[/dim]  [white]{activated}[/white]")
    _ks_box_bot()


def _ks_prompt_key(hwid: str) -> bool:
    """
    Interactive key entry loop.
    Returns True if the user successfully activates a key.
    """
    for attempt in range(3):
        console.print()
        try:
            raw = Prompt.ask(
                f"[bold cyan]🔑 Enter your KAZUKI key[/bold cyan] "
                f"[dim](attempt {attempt+1}/3)[/dim]"
            ).strip()
        except (KeyboardInterrupt, EOFError):
            return False

        if not raw:
            console.print("[bold red]❌ No key entered.[/bold red]")
            continue

        tier_lbl, days = _ks_tier(raw)
        if tier_lbl == "":
            console.print("[bold red]❌ Invalid key format.[/bold red]")
            console.print("[dim]Keys look like: KAZUKI-7DAY-XXXXX or KAZUKI-LIFE-XXXXX[/dim]")
            continue

        # Key format accepted — activate
        now_str    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        expiry_str = None if days == 0 else (
            (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        )
        _ks_save(raw, hwid, now_str, expiry_str)

        console.print()
        console.print(Panel(
            f"[bold green]✅ KEY ACTIVATED![/bold green]\n"
            f"[bold yellow]Tier    :[/bold yellow] [cyan]{tier_lbl}[/cyan]\n"
            f"[bold yellow]Expires :[/bold yellow] [cyan]{'Never (LIFETIME)' if expiry_str is None else expiry_str}[/cyan]",
            title="[bold white on green] 🔓 ACTIVATION SUCCESS [/]",
            border_style="green",
            box=box.HEAVY,
        ))
        time.sleep(1.5)
        return True

    # 3 failed attempts
    console.print()
    console.print(Panel(
        "[bold red]❌ Too many invalid attempts.[/bold red]\n"
        "[yellow]Contact [bold cyan]@GODXKAZUKII[/bold cyan] to get a valid key.[/yellow]",
        title="[bold white on red] 🚫 ACCESS DENIED [/]",
        border_style="red",
        box=box.HEAVY,
    ))
    time.sleep(2)
    os._exit(1)


# ── public entry point (replaces the old stub) ─────────────

def check_password_login():
    """
    Full key-gate.  Runs once at startup; returns an auth string
    compatible with the rest of the tool's SESSION_KEY usage.
    """
    global SESSION_USER, SESSION_KEY, SESSION_EXPIRY, ENGINE_LOCKED, \
           SERVER_ENGINE_TOKEN, SYSTEM_ACCESS_TOKEN

    # Boilerplate token setup (keeps shield-monitor happy)
    SERVER_ENGINE_TOKEN = "0" * 64
    SYSTEM_ACCESS_TOKEN = "0" * 64
    ENGINE_LOCKED       = False

    hwid = _ks_hwid()

    # ── Step 1: show banner ───────────────────────────────
    console.clear()
    _ks_show_banner(hwid)

    # ── Step 2: try to load an existing activation ────────
    data = _ks_load()

    if data is not None:
        ok, reason = _ks_validate_saved(data, hwid)

        if ok:
            _ks_show_activated(data)
            time.sleep(1.2)
            SESSION_USER   = data["key"]
            SESSION_KEY    = f"KZK-{_ks_tier(data['key'])[0]}"
            SESSION_EXPIRY = data.get("expiry") or "LIFETIME"
            return "KAZUKI_KEYED"

        # ── expired or hwid mismatch ──────────────────────
        if reason == "EXPIRED":
            console.print()
            console.print(Panel(
                "[bold red]⏰ Your key has expired![/bold red]\n"
                "[yellow]Enter a new key to continue.[/yellow]",
                title="[bold white on red] ⏰ KEY EXPIRED [/]",
                border_style="red", box=box.HEAVY,
            ))
            _KS_KEY_FILE.unlink(missing_ok=True)
            time.sleep(1)

        elif reason == "HWID_MISMATCH":
            console.print()
            console.print(Panel(
                "[bold red]🚫 This key is locked to a different device![/bold red]\n"
                "[yellow]Contact [bold cyan]@GODXKAZUKII[/bold cyan] to transfer.[/yellow]",
                title="[bold white on red] 🚫 DEVICE MISMATCH [/]",
                border_style="red", box=box.HEAVY,
            ))
            time.sleep(2)
            os._exit(1)

        elif reason == "HASH_CORRUPT":
            _KS_KEY_FILE.unlink(missing_ok=True)

    # ── Step 3: no valid saved key → prompt ──────────────
    _ks_prompt_key(hwid)

    # Reload after activation
    data = _ks_load()
    if data:
        ok, _ = _ks_validate_saved(data, hwid)
        if ok:
            SESSION_USER   = data["key"]
            SESSION_KEY    = f"KZK-{_ks_tier(data['key'])[0]}"
            SESSION_EXPIRY = data.get("expiry") or "LIFETIME"
            return "KAZUKI_KEYED"

    # Shouldn't reach here, but safety exit
    os._exit(1)

def ROL32(x: int, n: int) -> int: return ((x << n) & 0xFFFFFFFF) | ((x & 0xFFFFFFFF) >> (32 - n))
class Misc:
    @staticmethod
    def pad_to_n(data: bytes, n: int) -> bytes:
        padding = n - (len(data) % n)
        if padding == n: return data
        return data + b'\x00' * padding
    @staticmethod
    def align_up(x: int, n: int) -> int: return ((x + n - 1) // n) * n

_S_BOX = bytes.fromhex('346625748978E4A95A41BC7AD61621234D61DA949BDF133C693A310A5FD79995F1AE723D076024B698EEC4A22D88DD8D04EABB11CA3E5DA1F63FB09780472BA6E6F7D9B159C07CBE5428B77E4FF8436EA0500EF590B8FBA37B621946032AB98F9F77B45B838708EBE21E42F00FE8716A75AD551FB5AB33FA7F15BD85D80668B35230480B00EDEFB2578EE76CD5E52E538205F981F456BF8C4BE3DB4A914C2CD340294E20143679096FD137E0390C8A923812356DE1FD939A17D4C99C6B84269DAF76C19ED096C5CBE97349D2CD64C3C7017DF3ACFCDEA444321BC2BA1C02C627458BF218A710511DC8CF63FF2F0D58CE65A5DC1A3B86FE225CA85E67AAEC70CC')
_FK = [0x46970E9C, 0x4BC0685E, 0x59056186, 0xBCA2491E]
_CK = [0x000EB92B,0x3A0AE783,0x9E3B5C67,0xADDBDABF,0x7B7484CB,0x49156C63,0xC79AB5E7,0x79EC9CFF,0x1725BEAB,0x2FB89CA3,0x24808AD7,0xDDD28B1F,0x4740DA4B,0xBBC3EA73,0x247B30E7,0x91BE385F,0x0401248B,0x45FCD3A3,0x530B4CE7,0xC68DD35F,0xE3D16C2B,0x4F698C13,0x6B92C747,0x769EFB1F,0x4C73BE9B,0xC942B193,0xAD80D827,0x372FB33F,0x13CB6AAB,0x2BDC0AA3,0x17A4A247,0xD5E96CAF]
def _BS(X: int) -> int: return ((_S_BOX[(X >> 24) & 0xff] << 24) | (_S_BOX[(X >> 16) & 0xff] << 16) | (_S_BOX[(X >> 8) & 0xff] << 8) | (_S_BOX[X & 0xff]))
def _T0(X: int) -> int: X = _BS(X); return X ^ ROL32(X, 2) ^ ROL32(X, 10) ^ ROL32(X, 18) ^ ROL32(X, 24)
def _T1(X: int) -> int: X = _BS(X); return X ^ ROL32(X, 13) ^ ROL32(X, 23)
def _key_expand(key: bytes, rkey: List[int]):
    K0 = int.from_bytes(key[0:4], "big") ^ _FK[0]; K1 = int.from_bytes(key[4:8], "big") ^ _FK[1]
    K2 = int.from_bytes(key[8:12], "big") ^ _FK[2]; K3 = int.from_bytes(key[12:16], "big") ^ _FK[3]
    for i in range(0, 32, 4):
        K0 = K0 ^ _T1(K1 ^ K2 ^ K3 ^ _CK[i]); rkey[i] = K0
        K1 = K1 ^ _T1(K2 ^ K3 ^ K0 ^ _CK[i + 1]); rkey[i + 1] = K1
        K2 = K2 ^ _T1(K3 ^ K0 ^ K1 ^ _CK[i + 2]); rkey[i + 2] = K2
        K3 = K3 ^ _T1(K0 ^ K1 ^ K2 ^ _CK[i + 3]); rkey[i + 3] = K3

class SM4:
    @classmethod
    def key_length(cls) -> int: return 16
    @classmethod
    def block_length(cls) -> int: return 16
    def __init__(self, key: bytes) -> None:
        self._key = key; self._rkey: List[int] = [0] * 32; _key_expand(self._key, self._rkey); self._block_buffer = bytearray()
    def encrypt(self, block: bytes) -> bytes:
        RK = self._rkey
        X0 = int.from_bytes(block[0:4], "big"); X1 = int.from_bytes(block[4:8], "big"); X2 = int.from_bytes(block[8:12], "big"); X3 = int.from_bytes(block[12:16], "big")
        for i in range(0, 32, 4):
            X0 = X0 ^ _T0(X1 ^ X2 ^ X3 ^ RK[i]); X1 = X1 ^ _T0(X2 ^ X3 ^ X0 ^ RK[i + 1]); X2 = X2 ^ _T0(X3 ^ X0 ^ X1 ^ RK[i + 2]); X3 = X3 ^ _T0(X0 ^ X1 ^ X2 ^ RK[i + 3])
        BUFFER = self._block_buffer; BUFFER.clear(); BUFFER.extend(X3.to_bytes(4, "big")); BUFFER.extend(X2.to_bytes(4, "big")); BUFFER.extend(X1.to_bytes(4, "big")); BUFFER.extend(X0.to_bytes(4, "big"))
        return bytes(BUFFER)
    def decrypt(self, block: bytes) -> bytes:
        RK = self._rkey
        X0 = int.from_bytes(block[0:4], "big"); X1 = int.from_bytes(block[4:8], "big"); X2 = int.from_bytes(block[8:12], "big"); X3 = int.from_bytes(block[12:16], "big")
        for i in range(0, 32, 4):
            X0 = X0 ^ _T0(X1 ^ X2 ^ X3 ^ RK[31 - i]); X1 = X1 ^ _T0(X2 ^ X3 ^ X0 ^ RK[30 - i]); X2 = X2 ^ _T0(X3 ^ X0 ^ X1 ^ RK[29 - i]); X3 = X3 ^ _T0(X0 ^ X1 ^ X2 ^ RK[28 - i])
        BUFFER = self._block_buffer; BUFFER.clear(); BUFFER.extend(X3.to_bytes(4, "big")); BUFFER.extend(X2.to_bytes(4, "big")); BUFFER.extend(X1.to_bytes(4, "big")); BUFFER.extend(X0.to_bytes(4, "big"))
        return bytes(BUFFER)

class Reader:
    def __init__(self, buffer, cursor=0): self._buffer = buffer; self._cursor = cursor
    def u1(self, move_cursor=True) -> int: return self.unpack('B', move_cursor=move_cursor)[0]
    def u4(self, move_cursor=True) -> int: return self.unpack('<I', move_cursor=move_cursor)[0]
    def u8(self, move_cursor=True) -> int: return self.unpack('<Q', move_cursor=move_cursor)[0]
    def i1(self, move_cursor=True) -> int: return self.unpack('b', move_cursor=move_cursor)[0]
    def i4(self, move_cursor=True) -> int: return self.unpack('<i', move_cursor=move_cursor)[0]
    def i8(self, move_cursor=True) -> int: return self.unpack('<q', move_cursor=move_cursor)[0]
    def s(self, n: int, move_cursor=True) -> bytes: return self.unpack(f'{n}s', move_cursor=move_cursor)[0]
    def unpack(self, f: str | bytes, offset=0, move_cursor=True):
        x = struct.unpack_from(f, self._buffer, self._cursor + offset)
        if move_cursor: self._cursor += struct.calcsize(f)
        return x
    def string(self, move_cursor=True) -> str:
        length = self.i4(move_cursor=move_cursor)
        if length == 0: return str()
        return self.unpack(f'{length}s', offset=(0 if move_cursor else 4), move_cursor=move_cursor)[0].rstrip(b'\x00').decode(errors='ignore')

class PakInfo:
    def __init__(self, buffer, keystream: list[int]):
        def decrypt_index_encrypted(x: int) -> int: return (x ^ keystream[3]) & 0xFF
        def decrypt_magic(x: int) -> int: return x ^ keystream[2]
        def decrypt_index_hash(x: bytes) -> bytes:
            key = struct.pack('<5I', *keystream[4:][:5])
            return bytes(a ^ b for a, b in zip(x, key))
        def decrypt_index_size(x: int) -> int: return x ^ ((keystream[10] << 32) | keystream[11])
        def decrypt_index_offset(x: int) -> int: return x ^ ((keystream[0] << 32) | keystream[1])
        reader = Reader(buffer[-PakInfo._mem_size(-1):])
        self.index_encrypted: bool = decrypt_index_encrypted(reader.u1()) == 1
        self.magic: int = decrypt_magic(reader.u4())
        self.version: int = reader.u4()
        self.index_hash: bytes = decrypt_index_hash(reader.s(20)) if self.version >= 6 else bytes()
        self.index_size: int = decrypt_index_size(reader.u8())
        self.index_offset: int = decrypt_index_offset(reader.u8())
        if self.version <= 3: self.index_encrypted = False
    @staticmethod
    def _mem_size(_: int) -> int: return 1 + 4 + 4 + 20 + 8 + 8

class TencentPakInfo(PakInfo):
    def __init__(self, buffer, keystream: list[int]):
        def decrypt_unk(x: bytes) -> bytes:
            key = struct.pack('<8I', *keystream[7:][:8])
            return bytes(a ^ b for a, b in zip(x, key))
        def decrypt_stem_hash(x: int) -> int: return x ^ keystream[8]
        def decrypt_unk_hash(x: int) -> int: return x ^ keystream[9]
        super().__init__(buffer, keystream)
        reader = Reader(buffer[-TencentPakInfo._mem_size(self.version):])
        self.unk1: bytes = decrypt_unk(reader.s(32)) if self.version >= 7 else bytes()
        self.packed_key: bytes = reader.s(256) if self.version >= 8 else bytes()
        self.packed_iv: bytes = reader.s(256) if self.version >= 8 else bytes()
        self.packed_index_hash: bytes = reader.s(256) if self.version >= 8 else bytes()
        self.stem_hash: int = decrypt_stem_hash(reader.u4()) if self.version >= 9 else 0
        self.unk2: int = decrypt_unk_hash(reader.u4()) if self.version >= 9 else 0
        self.content_org_hash: bytes = reader.s(20) if self.version >= 12 else bytes()
    @staticmethod
    def _mem_size(version: int) -> int:
        return PakInfo._mem_size(version) + (32 if version >= 7 else 0) + (256 * 3 if version >= 8 else 0) + (4 * 2 if version >= 9 else 0) + (20 if version >= 12 else 0)

class PakCompressedBlock:
    def __init__(self, reader: Reader):
        self.start: int = reader.u8()
        self.end: int = reader.u8()

@dataclass
class TencentPakEntry:
    def __init__(self, reader: Reader, version: int):
        self.content_hash: bytes = reader.s(20)
        if version <= 1: _ = reader.u8()
        self.offset: int = reader.u8()
        self.uncompressed_size: int = reader.u8()
        self.compression_method: int = reader.u4() & CM_MASK
        self.size: int = reader.u8()
        self.unk1: int = reader.u1() if version >= 5 else 0
        self.unk2: bytes = reader.s(20) if version >= 5 else bytes()
        self.compressed_blocks: list[PakCompressedBlock] = [PakCompressedBlock(reader) for _ in range(reader.u4())] if self.compression_method != 0 and version >= 3 else []
        self.compression_block_size: int = reader.u4() if version >= 4 else 0
        self.encrypted: bool = reader.u1() == 1 if version >= 4 else False
        self.encryption_method: int = reader.u4() if version >= 12 else 0
        self.index_new_sep: int = reader.u4() if version >= 12 else 0

class PakCrypto:
    class _LCG:
        def __init__(self, seed: int): self.state = seed
        def next(self) -> int:
            MASK_32 = 0xFFFFFFFF; MSB_1 = 1 << 31
            def wrap(x: int) -> int:
                x &= MASK_32
                if not x & MSB_1: return x
                return ((x + MSB_1) & MASK_32) - MSB_1
            x1 = wrap(0x41C64E6D * self.state)
            self.state = wrap(x1 + 12345)
            x2 = wrap(x1 + 77880) if self.state < 0 else self.state 
            return ((x2 >> 16) & MASK_32) % 0x7FFF
    @staticmethod
    def zuc_keystream() -> list[int]:
        if gmalg:
            zuc = gmalg.ZUC(ZUC_KEY, ZUC_IV)
            return [struct.unpack('>I', zuc.generate())[0] for _ in range(16)]
        raise RuntimeError('gmalg.ZUC not available')
    @staticmethod
    def _xorxor(buffer, x) -> bytes: return bytes(buffer[i] ^ x[i % len(x)] for i in range(len(buffer)))
    @staticmethod
    def _hashhash(buffer, n: int) -> bytes:
        result = bytes()
        for i in range(math.ceil(n / (SHA1.digest_size if SHA1 else 20))): result += (SHA1.new(buffer).digest() if SHA1 else b'\x00' * 20)
        return result[:n] if len(result) >= n else result + b'\x00' * (n - len(result))
    @staticmethod
    def _meowmeow(buffer) -> bytes:
        def unpad(x):
            skip = 1 + next((i for i in range(len(x)) if x[i] != 0))
            return x[skip:]
        if len(buffer) < 43: return bytes()
        x1 = buffer[1:][:SHA1.digest_size if SHA1 else 20]; x2 = buffer[(SHA1.digest_size if SHA1 else 20) + 1:]
        x1 = PakCrypto._xorxor(x1, PakCrypto._hashhash(x2, len(x1))); x2 = PakCrypto._xorxor(x2, PakCrypto._hashhash(x1, len(x2)))
        part1, m = (x2[:(SHA1.digest_size if SHA1 else 20)], x2[(SHA1.digest_size if SHA1 else 20):])
        if part1 != (SHA1.new(b'\x00' * (SHA1.digest_size if SHA1 else 20)).digest() if SHA1 else b'\x00' * (SHA1.digest_size if SHA1 else 20)): return bytes()
        return unpad(m)
    @staticmethod
    def rsa_extract(signature: bytes, modulus: bytes) -> bytes:
        c = int.from_bytes(signature, 'little'); n = int.from_bytes(modulus, 'little'); e = 0x10001
        m = pow(c, e, n).to_bytes(256, 'little').rstrip(b'\x00')
        return PakCrypto._meowmeow(Misc.pad_to_n(m, 4))
    @staticmethod
    def _decrypt_simple1(ciphertext) -> bytes: return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in ciphertext)
    @staticmethod
    def _decrypt_simple2(ciphertext) -> bytes:
        class RollingKey:
            def __init__(self, initial_value: int): self._value = initial_value
            def update(self, x: int) -> int: self._value ^= x; return self._value
        initial_key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY); rolling_key = RollingKey(initial_key)
        plaintext = (struct.pack('<I', rolling_key.update(x)) for x in struct.unpack(f'<{len(ciphertext) // 4}I', ciphertext))
        return bytes(it.chain.from_iterable(plaintext))
    @staticmethod
    def _derive_sm4_key(file_path: PurePath, encryption_method: int) -> bytes:
        part1 = file_path.stem.lower()
        if encryption_method == EM_SM4_2: secret = SM4_SECRET_2
        elif encryption_method == EM_SM4_4: secret = SM4_SECRET_4
        else: index = (encryption_method - EM_SM4_NEW_BASE) % len(SM4_SECRET_NEW); secret = f'{SM4_SECRET_NEW[index]}{encryption_method}'
        return (SHA1.new(str(part1 + secret).encode()).digest()[:SM4.key_length()] if SHA1 else b'\x00' * SM4.key_length())
    @staticmethod
    def _sm4_context_for_key(key: bytes) -> SM4: return SM4(key)
    @staticmethod
    def _decrypt_sm4(ciphertext, file_path: PurePath, encryption_method: int) -> bytes:
        key = PakCrypto._derive_sm4_key(file_path, encryption_method); sm4 = PakCrypto._sm4_context_for_key(key)
        return bytes(it.chain.from_iterable(sm4.decrypt(bytes(x)) for x in it.batched(ciphertext, SM4.block_length())))
    @staticmethod
    def decrypt_index(ciphertext, pak_info: TencentPakInfo) -> bytes:
        if pak_info.version > 7:
            for mod in [RSA_MOD_1, RSA_MOD_2]:
                try:
                    key = PakCrypto.rsa_extract(pak_info.packed_key, mod)
                    iv  = PakCrypto.rsa_extract(pak_info.packed_iv,  mod)
                    if not key or not iv or len(key) < 16 or len(iv) < 16:
                        continue
                    aes = AES.new(key, MODE_CBC, iv[:16])
                    dec = aes.decrypt(bytes(ciphertext))
                    try:
                        result = unpad(dec, AES.block_size)
                    except Exception:
                        result = dec.rstrip(b'\x00')
                    if result:
                        return result
                except Exception:
                    continue
            return bytes(ciphertext)
        else:
            return bytes(PakCrypto._decrypt_simple1(ciphertext))
    @staticmethod
    def _is_simple1_method(encryption_method: int) -> bool: return encryption_method == EM_SIMPLE1
    @staticmethod
    def _is_simple2_method(encryption_method: int) -> bool: return encryption_method == EM_SIMPLE2
    @staticmethod
    def _is_sm4_method(encryption_method: int) -> bool: return (encryption_method == EM_SM4_2 or encryption_method == EM_SM4_4 or encryption_method & EM_SM4_NEW_MASK != 0)
    
    @staticmethod
    def align_encrypted_content_size(n: int, encryption_method: int) -> int:
        if PakCrypto._is_simple2_method(encryption_method): return Misc.align_up(n, SIMPLE2_BLOCK_SIZE)
        elif PakCrypto._is_sm4_method(encryption_method): return Misc.align_up(n, SM4.block_length())
        else: return n

    @staticmethod
    def decrypt_block(ciphertext, file: PurePath, encryption_method: int) -> bytes:
        if False:  # PATCHED: bypass ENGINE_LOCKED / SYSTEM_ACCESS_TOKEN crash
            import os, random
            os._exit(random.randint(1, 255))
        if encryption_method == 17: return ciphertext
        elif PakCrypto._is_simple1_method(encryption_method): return PakCrypto._decrypt_simple1(ciphertext)
        elif PakCrypto._is_simple2_method(encryption_method): return PakCrypto._decrypt_simple2(ciphertext)
        elif PakCrypto._is_sm4_method(encryption_method): return PakCrypto._decrypt_sm4(ciphertext, file, encryption_method)
        else: assert False

    @staticmethod
    def _encrypt_simple1(plaintext: bytes) -> bytes: return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in plaintext)
    @staticmethod
    def _encrypt_simple2(plaintext: bytes) -> bytes:
        initial_key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY); out_words = []; current = initial_key
        for w in struct.unpack(f'<{len(plaintext)//4}I', plaintext): c = current ^ w; out_words.append(c); current = w
        return struct.pack(f'<{len(out_words)}I', *out_words)
    @staticmethod
    def _encrypt_sm4(plaintext: bytes, file_path: PurePath, encryption_method: int) -> bytes:
        key = PakCrypto._derive_sm4_key(file_path, encryption_method); sm4 = PakCrypto._sm4_context_for_key(key)
        return b''.join(sm4.encrypt(plaintext[i:i+SM4.block_length()]) for i in range(0, len(plaintext), SM4.block_length()))
    @staticmethod
    @lru_cache(maxsize=33)
    def generate_block_indices(n: int, encryption_method: int) -> list[int]:
        if n <= 0: return []
        if not PakCrypto._is_sm4_method(encryption_method): return list(range(n))
        permutation = []; lcg = PakCrypto._LCG(n)
        while len(permutation) != n:
            x = lcg.next() % n
            if x not in permutation: permutation.append(x)
        inverse = [0] * len(permutation)
        for i, x in enumerate(permutation): inverse[x] = i
        return inverse

class PakCompression:
    @staticmethod
    def decompress_block(block, dict: ZstdCompressionDict | None, compression_method: int) -> bytes:
        if compression_method == CM_ZLIB: 
            try:
                return zlib.decompress(block)
            except Exception as e:
                return block
                
        elif compression_method == CM_ZSTD or compression_method == CM_ZSTD_DICT:
            if compression_method != CM_ZSTD_DICT: dict = None
            try:
                return ZstdDecompressor(dict_data=dict).decompress(block)
            except Exception as e:
                if "could not determine content size" in str(e):
                    try:
                        return ZstdDecompressor(dict_data=dict).decompress(block, max_output_size=5242880)
                    except:
                        return block
                return block 
        else: 
            return block

    @staticmethod
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
    INPUT_DIR = None
    OUTPUT_BASE = None
    MODIFIED_DIR = None

    def __init__(self, file_path: PurePath, is_od=False, silent=False): 
        self._silent = silent 
        self._file_path = file_path
        with open_long(file_path, 'rb') as file:
            self._file_content = memoryview(file.read())
        self._is_od = is_od
        self._mount_point = PurePath()
        self._is_zstd_with_dict = True 
        self._zstd_dict = None
        self._files: list[TencentPakEntry] = []
        self._index: dict[PurePath, dict[str, TencentPakEntry]] = {}
        try:
            ks = PakCrypto.zuc_keystream()
        except Exception as e:
            ks = [0]*16
        self._pak_info = TencentPakInfo(self._file_content, ks)
        self._verify_stem_hash()
        self._tencent_load_index()

    def _verify_stem_hash(self) -> None:
        if not self._is_od and self._pak_info.version >= 9:
            try:
                assert self._pak_info.stem_hash == zlib.crc32(self._file_path.stem.encode('utf-32le'))
            except AssertionError:
                pass

    def _tencent_load_index(self) -> None:
        raw_index = bytes(self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size])

        def _try_aes_decrypt(data, mod):
            """Try AES-CBC decrypt with given RSA mod. Return plaintext or None."""
            try:
                key = PakCrypto.rsa_extract(self._pak_info.packed_key, mod)
                iv  = PakCrypto.rsa_extract(self._pak_info.packed_iv,  mod)
                if not key or not iv or len(key) < 16 or len(iv) < 16:
                    return None
                aes = AES.new(key, MODE_CBC, iv[:16])
                decrypted = aes.decrypt(data)
                # Safe unpad — catch padding errors
                try:
                    result = unpad(decrypted, AES.block_size)
                except Exception:
                    # Try manual strip of trailing zeros/padding
                    result = decrypted.rstrip(b'\x00')
                    if not result:
                        return None
                # Sanity: try parsing mount point
                r = Reader(result)
                r.string()
                n = r.u4()
                if 0 <= n <= 200000:
                    return result
                return None
            except Exception:
                return None

        candidates = []

        if self._pak_info.index_encrypted:
            # 1. RSA_MOD_1
            d = _try_aes_decrypt(raw_index, RSA_MOD_1)
            if d: candidates.append(d)
            # 2. RSA_MOD_2
            d = _try_aes_decrypt(raw_index, RSA_MOD_2)
            if d: candidates.append(d)
            # 3. Simple1 XOR fallback
            try:
                candidates.append(PakCrypto._decrypt_simple1(raw_index))
            except Exception:
                pass

        # 4. Always try raw (unencrypted)
        candidates.append(raw_index)

        # Try each candidate until _load_index succeeds with non-empty index
        for data in candidates:
            try:
                self._files = []
                self._index = {}
                self._load_index(data)
                if self._index:
                    return
            except Exception:
                continue

        # Nothing worked
        if not self._silent:
            custom_msg = (
                "[bold cyan]MODDER BY @KAZUKI YT[/bold cyan]\n"
                "[bold yellow]Note  = KYA LAGATA THA ENC LGA  KE BACH JAOOGE NA MUNA NA NICHE DEKH 👇😂[/bold yellow]"
            )
            console.print(Panel(custom_msg, border_style="red",
                                title="[bold white on red] WARNING [/bold white on red]",
                                box=box.HEAVY))
        self._files = []
        self._index = {}

    @staticmethod
    def _construct_mount_point(mount_point: str) -> PurePath:
        result = PurePath()
        for part in PurePath(mount_point).parts:
            if part != '..': result /= part
        return result

    def _peek_content(self, offset: int, size: int, encryption_method: int) -> memoryview:
        size = PakCrypto.align_encrypted_content_size(size, encryption_method)
        return self._file_content[offset:][:size]

    def _peek_block_content(self, block: PakCompressedBlock, encryption_method: int) -> memoryview:
        size = PakCrypto.align_encrypted_content_size(block.end - block.start, encryption_method)
        return self._file_content[block.start:][:size]

    def _construct_zstd_dict(self, dict_entry: TencentPakEntry) -> None:
        try:
            data = self._peek_content(dict_entry.offset, dict_entry.size, dict_entry.encryption_method)
            if dict_entry.encrypted:
                data = PakCrypto.decrypt_block(data, PurePath("zstddic"), dict_entry.encryption_method)
            reader = Reader(data)
            dict_size = reader.u8()
            _ = reader.u4()
            _ = reader.u4()
            dict_data = reader.s(dict_size)
            if ZstdCompressionDict: 
                self._zstd_dict = ZstdCompressionDict(dict_data, DICT_TYPE_AUTO)
        except Exception as e:
            console.print(f"[red]Dictionary Load Error: {e}[/red]")

    def _load_index(self, index_data) -> None:
        global SYSTEM_ACCESS_TOKEN
        if False:  # PATCHED: bypass SYSTEM_ACCESS_TOKEN check
            console.clear()
            console.print(Panel(
                "[blink bold red]☠️ FATAL SECURITY BREACH & DATA LEAK IN PROGRESS ☠️[/blink bold red]\n\n"
                "[bold yellow]>> INITIATING LEVEL-4 COUNTER-MEASURES...[/bold yellow]\n"
                "[white]Bhai, Tune Login Page toh bypass kar liya, par asli OBB Engine ka HASH token kahan se layega? Teri aukaat yahin tak thi Beta aur Tera Data tak lick ho gya Banchhod Samjaa..😂[/white]\n\n"
                "[bold red]⚠️ WARNING: ILLEGAL TAMPERING DETECTED![/bold red]\n"
                "[cyan]Extracting Device IP, MAC Address, and Network Identity...[/cyan]\n"
                "[cyan]Uploading Hacker Data to KAZUKI Servers... [ ▓▓▓▓▓▓▓▓▓▓ ] 100%[/cyan]\n\n"
                "[bold white on red] YOUR DEVICE IS NOW PERMANENTLY BLACKLISTED [/bold white on red]\n"
                "[dim white]RedMagix System is destroying current process and corrupting local cache...[/dim white]", 
                border_style="red", box=box.HEAVY
            ))
            time.sleep(4)
            try:
                junk_data = []
                while True: junk_data.append('0' * 1000000) 
            except: pass
            os._exit(0)
            
        reader = Reader(index_data)
        self._mount_point = self._construct_mount_point(reader.string())
        n_files = min(reader.u4(), 200000)
        self._files = [TencentPakEntry(reader, self._pak_info.version) for _ in range(n_files)]
        dirs_count = min(reader.u8(), 200000)
        for _ in range(dirs_count):
            dir_path = PurePath(sanitize_path_string(reader.string()))
            file_count = min(reader.u8(), 200000)
            e = {}
            for _ in range(file_count):
                name = sanitize_path_string(reader.string())
                idx = reader.i4()
                mapped = ~idx
                if 0 <= mapped < len(self._files): e[name] = self._files[mapped]
                else: e[name] = None
            if self._is_zstd_with_dict and dir_path.name == 'zstddic':
                self._construct_zstd_dict(e[[*e.keys()][0]])
                continue
            self._index.update({PurePath(dir_path): e})

    def _write_to_disk(self, file_path: Path, entry: TencentPakEntry) -> None:
        encryption_method = entry.encryption_method
        compression_method = entry.compression_method
        # Sanitize every path component — null bytes in PAK index strings crash makedirs
        file_path = Path(*[sanitize_path_string(p) for p in Path(file_path).parts])
        parent_dir = file_path.parent
        os.makedirs(to_long_path(parent_dir), exist_ok=True)
        
        with open_long(file_path, 'wb') as file:
            if compression_method == CM_NONE:
                data = self._peek_content(entry.offset, entry.size, encryption_method)
                if entry.encrypted: 
                    data = PakCrypto.decrypt_block(data, file_path, encryption_method)
                file.write(data)
                return
                
            # Some PAK indexes contain compressed entries with zero block records.
            # Do not call generate_block_indices(0, ...): its modulo operation would
            # raise ZeroDivisionError and abort extraction of that file.
            if not entry.compressed_blocks:
                if entry.size:
                    data = self._peek_content(entry.offset, entry.size, encryption_method)
                    if entry.encrypted:
                        data = PakCrypto.decrypt_block(data, file_path, encryption_method)
                    data = PakCompression.decompress_block(data, self._zstd_dict, compression_method)
                    file.write(data)
                return

            for x in PakCrypto.generate_block_indices(len(entry.compressed_blocks), encryption_method):
                data = self._peek_block_content(entry.compressed_blocks[x], encryption_method)
                if entry.encrypted: 
                    data = PakCrypto.decrypt_block(data, file_path, encryption_method)
                data = PakCompression.decompress_block(data, self._zstd_dict, compression_method)
                file.write(data)

    def dump(self, out_path: PurePath) -> bool:
        total_files = sum(len(files) for files in self._index.values())
        if total_files == 0:
            console.print(Panel("[yellow]No files found in PAK index.[/yellow]", border_style="yellow"))
            return False

        b_color = get_banner_color()
        console.print(f"\n[bold {b_color}] 🚀 {to_fancy('UNPACKING')}: {self._file_path.name} [/bold {b_color}]\n")

        from rich.console import Group
        from rich.live import Live
        from rich.align import Align

        control_text = (
            "[bold black on {get_banner_color()}] S [/] [bold {get_banner_color()}]PAUSE / RESUME[/]   [bold white]❖[/]   [bold black on bright_red]         B [/] [bold bright_red]BACK (CANCEL)[/]"
        )
        control_panel = Panel(
            Align.center(control_text), 
            title="[bold bright_blue]⚡ KAZUKI LIVE ENGINE ⚡[/]", 
            border_style="bright_blue", 
            box=box.HEAVY
        )

        progress = Progress(
            SpinnerColumn("dots", style="bright_blue"),
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(bar_width=40, style="dim blue", complete_style="bold bright_blue"),
            TextColumn("[bold white]{task.percentage:>3.0f}%[/]"),
            TimeElapsedColumn(),
        )
        task = progress.add_task(f"{to_fancy('Extracting Files')}...", total=total_files)

        is_paused = False
        is_cancelled = False

        live_group = Group(progress, control_panel)

        with Live(live_group, console=console, refresh_per_second=15):
            for dir_path, files in self._index.items():
                if is_cancelled: break
                for name, entry in files.items():
                    if is_cancelled: break
                    
                    while True:
                        key = check_key_press()
                        if key == 's':
                            is_paused = not is_paused
                            if is_paused:
                                progress.update(task, description=f"[blink bold red]⏸️  SYSTEM PAUSED... (Press S to Resume)[/]")
                            else:
                                progress.update(task, description=f"[bold cyan]▶️  {to_fancy('Extracting Files')}...[/]")
                        elif key == 'b':
                            is_cancelled = True
                            break
                        
                        if not is_paused:
                            break
                        time.sleep(0.1) 

                    if entry is None:
                        progress.advance(task)
                        continue

                    if dir_path.parts and dir_path.parts[0] == self._mount_point.name:
                        relative_dir = dir_path.relative_to(self._mount_point)
                    else:
                        relative_dir = dir_path

                    pak_stem = Path(self._file_path).stem
                    dest_dir = out_path / pak_stem / relative_dir
                    os.makedirs(to_long_path(dest_dir), exist_ok=True)
                    dest_file = dest_dir / name

                    short_name = name if len(name) < 45 else name[:20] + "..." + name[-20:]

                    try:
                        self._write_to_disk(dest_file, entry)
                        enc_info = f" [dim white]- Encryption: {entry.encryption_method}, Compression: {entry.compression_method}, Blocks: {len(entry.compressed_blocks) if entry.compressed_blocks else 0}[/]"
                        console.print(f"[bold {get_banner_color()}]✔ {to_fancy('OK')}:[/] [bold bright_blue]{short_name}[/]{enc_info}")
                    except Exception as e:
                        console.print(f"[bold red]❌ {to_fancy('FAIL')}:[/] [bold bright_blue]{short_name}[/] [dim]({e})[/dim]")

                    progress.advance(task)

        if is_cancelled:
            console.print("\n")
            console.print(Panel("[bold red]🛑 EXTRACTION CANCELLED BY USER![/bold red]\n[white]Returning to Main Menu...[/white]", border_style="red", box=box.HEAVY))
            return False

        console.print(Panel(f"[bold green]✅ {to_fancy('Successfully Unpacked')} [white]{total_files}[/white] {to_fancy('files from')} {self._file_path.name}![/]", border_style="green", box=box.DOUBLE_EDGE))
        return True

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

# ---------------------------
# DIRECTORY MANAGEMENT
# ---------------------------
# ======================================================================
#                    DIRECTORY MANAGEMENT
# ======================================================================

# ======================================================================
#                    DIRECTORY MANAGEMENT
# ======================================================================

ORGNAL_DIR = "ORGNAL"
EDITED_DIR = "Modified_files"
UNPACK_DIR = "UNPACK"
REPACK_DIR = "REPACK"
SINGLE_DIR = "UNPACKED_SINGLE"

ENCRYPT_INPUT_DIR = Path(BASE_DIR_NAME) / "Enc_pak" / "Input"
ENCRYPT_OUTPUT_DIR = Path(BASE_DIR_NAME) / "Enc_pak" / "Output"

ANLAISH_DIR = Path(BASE_DIR_NAME) / "OBB Anlaish"
ANLAISH_ORG = ANLAISH_DIR / "ORGNAL"
ANLAISH_MOD = ANLAISH_DIR / "MOD"
ANLAISH_RESULT = ANLAISH_DIR / "RESULT"

# ======================================================================
#                    MINI & ZSDIC TOOL GLOBALS
# ======================================================================

# 🔥 BASE DIRECTORIES (Game specific paths will be set in run_combined_modding_tool)
BASE_DIR = os.path.join("𝐊𝐀𝐙𝐔𝐊𝐈_𝐓𝐎𝐎𝐋", "SKIN_TOOL")
MINI_BASE = os.path.join(BASE_DIR, "MINI")
ZSDIC_BASE = os.path.join(BASE_DIR, "ZSDIC")
FINAL_DIR = os.path.join(BASE_DIR, "FINAL")

# 🔥 MINI PATHS (Will be overridden in run_combined_modding_tool)
mini_BASE_DIR = MINI_BASE
mini_MINI_ICON_DIR = os.path.join(mini_BASE_DIR, "MINI_ICON")
mini_INPUT_DIR = os.path.join(mini_MINI_ICON_DIR, "INPUT")
mini_OUTPUT_DIR = os.path.join(mini_MINI_ICON_DIR, "OUTPUT")
mini_TXTS_DIR = os.path.join(mini_MINI_ICON_DIR, "TXTS")
mini_MODSKIN_FILE = os.path.join(mini_BASE_DIR, "modskin.txt")
mini_CHANGELOG_PATH = os.path.join(mini_BASE_DIR, "changelog.txt")
mini_NULL_TXT_PATH = os.path.join(mini_TXTS_DIR, "null.txt")
mini_NULLED_TXT_PATH = os.path.join(mini_BASE_DIR, "nulled.txt")
mini_ALL_TXT_PATH = os.path.join(mini_TXTS_DIR, "ALL.txt")
mini_INDEX_FILE_PATH = os.path.join(mini_TXTS_DIR, "index.txt")

mini_AUTO_THEME_BASE = os.path.join(mini_BASE_DIR, "AUTO_THEME")
mini_AUTO_THEME_FILES = os.path.join(mini_AUTO_THEME_BASE, "FILES")
mini_AUTO_THEME_RESULT = os.path.join(mini_AUTO_THEME_BASE, "MODIFIED")
mini_AUTO_THEME_TXT = os.path.join(mini_AUTO_THEME_BASE, "TXT")
mini_LOBBY_FILE = os.path.join(mini_AUTO_THEME_TXT, "lobby.txt")

mini_HIT_EFFECT_DIR = os.path.join(mini_BASE_DIR, "HIT EFFECT")
mini_LOOTCRATES_DIR = os.path.join(mini_BASE_DIR, "LOOTCRATES")
mini_HIT_ORIG = os.path.join(mini_HIT_EFFECT_DIR, "org")
mini_HIT_MODIFIED = os.path.join(mini_HIT_EFFECT_DIR, "modified")
mini_LOOT_ORIG = os.path.join(mini_LOOTCRATES_DIR, "org")
mini_LOOT_MODIFIED = os.path.join(mini_LOOTCRATES_DIR, "modified")
mini_HIT_TXT_PATH = os.path.join(mini_BASE_DIR, "hit.txt")

mini_changelog_entries = []
mini_modified_blocks_map = {}  
mini_BLOCK_SIZE = 65536

# 🔥 ZSDIC PATHS (Will be overridden in run_combined_modding_tool)
zsdic_DEFAULT_MAX_NULLS = 40
zsdic_ENABLE_UTF16LE_ID_SCAN = False

zsdic_GAME_DIRS = {"BGMI": os.path.join(ZSDIC_BASE, "BGMI")}
zsdic_OUTPUT_DIR_NAME = "skindats"
zsdic_EDITED_DIR_NAME = "edited"
zsdic_SIZE_DIR_NAME = "size"
zsdic_MODSKIN_TXT = os.path.join(ZSDIC_BASE, "modskin.txt")
zsdic_OUTFITS_TXT = os.path.join(ZSDIC_BASE, "outfits.txt")
zsdic_NULL_TXT = os.path.join(ZSDIC_BASE, "null.txt")
zsdic_CHANGELOG_TXT = os.path.join(ZSDIC_BASE, "changelog.txt")
zsdic_NULLED_LOG_TXT = os.path.join(ZSDIC_BASE, "nulled.txt")
zsdic_SWAP_OFFSETS_TXT = os.path.join(ZSDIC_BASE, "swap_offsets.txt")
zsdic_OUTFITS_FILES = {"AvatarSuitsTable.uasset", "GoldClothBattleEffect.uasset"}
zsdic_ID_ASCII_RE = re.compile(rb"(?<![0-9])[0-9]{3,}(?![0-9])")
zsdic_ID_UTF16LE_RE = re.compile(rb"(?:(?:[0-9]\x00){3,})")

# 🔥 STAND POSH PATHS (Will be overridden in run_combined_modding_tool)
STAND_POSH_BASE = os.path.join(BASE_DIR, "STAND_POSH")
sp_INPUT = os.path.join(STAND_POSH_BASE, "INPUT")
sp_OUTPUT = os.path.join(STAND_POSH_BASE, "OUTPUT")
sp_DUMP = os.path.join(STAND_POSH_BASE, "dump.txt")
sp_MODSKIN = os.path.join(STAND_POSH_BASE, "modskin.txt")
sp_NULL = os.path.join(STAND_POSH_BASE, "null.txt")

# ======================================================================
#                    CREATE DIRS FUNCTION
# ======================================================================

def create_dirs(base: Path):
    os.makedirs(to_long_path(base), exist_ok=True)
    obb_unpacker = base / "OBB_UNPACKER"
    os.makedirs(to_long_path(obb_unpacker / ORGNAL_DIR), exist_ok=True)
    os.makedirs(to_long_path(obb_unpacker / EDITED_DIR), exist_ok=True)
    os.makedirs(to_long_path(obb_unpacker / UNPACK_DIR), exist_ok=True)
    os.makedirs(to_long_path(obb_unpacker / REPACK_DIR), exist_ok=True)
    os.makedirs(to_long_path(obb_unpacker / SINGLE_DIR), exist_ok=True)
    os.makedirs(to_long_path(ENCRYPT_INPUT_DIR), exist_ok=True)
    os.makedirs(to_long_path(ENCRYPT_OUTPUT_DIR), exist_ok=True)
    os.makedirs(to_long_path(ANLAISH_ORG), exist_ok=True)
    os.makedirs(to_long_path(ANLAISH_MOD), exist_ok=True)
    os.makedirs(to_long_path(ANLAISH_RESULT), exist_ok=True)
    
    credit_tool = base / "CREDIT_TOOL"
    os.makedirs(to_long_path(credit_tool / "ORGNAL"), exist_ok=True)
    os.makedirs(to_long_path(credit_tool / "MODDED FILE"), exist_ok=True)
    
  #  obbzip_root = base / "OBBZIP"
  #  os.makedirs(to_long_path(obbzip_root / "ORGNAL_OBB"), exist_ok=True)
   # os.makedirs(to_long_path(obbzip_root / "UNPACKED_OBB"), exist_ok=True)
   # os.makedirs(to_long_path(obbzip_root / "REPACK_OBB"), exist_ok=True)
   # os.makedirs(to_long_path(obbzip_root / "Modified_pak"), exist_ok=True)
    
    # 🔥 SKIN TOOL FOLDERS (BGMI & PUBG)
    skin_tool = base / "SKIN_TOOL"
    for game in ["BGMI_SKIN", "PUBG_SKIN"]:
        game_base = skin_tool / game
        
        # MINI
        mini_base = game_base / "MINI"
        os.makedirs(mini_base / "MINI_ICON" / "INPUT", exist_ok=True)
        os.makedirs(mini_base / "MINI_ICON" / "OUTPUT", exist_ok=True)
        os.makedirs(mini_base / "TXTS", exist_ok=True)
        os.makedirs(mini_base / "AUTO_THEME" / "FILES", exist_ok=True)
        os.makedirs(mini_base / "AUTO_THEME" / "MODIFIED", exist_ok=True)
        os.makedirs(mini_base / "AUTO_THEME" / "TXT", exist_ok=True)
        os.makedirs(mini_base / "HIT EFFECT" / "org", exist_ok=True)
        os.makedirs(mini_base / "HIT EFFECT" / "modified", exist_ok=True)
        os.makedirs(mini_base / "LOOTCRATES" / "org", exist_ok=True)
        os.makedirs(mini_base / "LOOTCRATES" / "modified", exist_ok=True)
        
        # ZSDIC
        game_key = "BGMI" if game == "BGMI_SKIN" else "PUBG"
        zsdic_base = game_base / "ZSDIC"
        os.makedirs(zsdic_base / game_key / "skindats", exist_ok=True)
        os.makedirs(zsdic_base / game_key / "edited", exist_ok=True)
        os.makedirs(zsdic_base / game_key / "size", exist_ok=True)
        
        # STAND POSH
        stand_posh = game_base / "STAND_POSH"
        os.makedirs(stand_posh / "INPUT", exist_ok=True)
        os.makedirs(stand_posh / "OUTPUT", exist_ok=True)
        
        # FINAL
        os.makedirs(game_base / "FINAL", exist_ok=True)

# ======================================================================
# 🔥 AUTO DOWNLOAD SKIN_TOOL FROM GITHUB (SAME UI AS SCREENSHOT)
# ======================================================================

# ======================================================================
# 🔥 AUTO DOWNLOAD SKIN_TOOL FROM GITHUB (SIRF DOWNLOAD DIKHE)
# ======================================================================

import requests
import zipfile
from pathlib import Path
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TransferSpeedColumn
from rich.panel import Panel
from rich.console import Console
from rich import box

console = Console()

def download_skin_tool():
    """GitHub se download + extract (Sirf download dikhe, extract background mein)"""
    
    GITHUB_URL = "https://raw.githubusercontent.com/sellacountvinay-creator/SKIN_TOOL/main/SKIN_TOOL.zip"
    
    base_dir = Path("𝐊𝐀𝐙𝐔𝐊𝐈_𝐓𝐎𝐎𝐋")
    skin_tool_dir = base_dir / "SKIN_TOOL"
    zip_path = base_dir / "SKIN_TOOL.zip"
    
    if skin_tool_dir.exists():
        return True
    
    os.makedirs(base_dir, exist_ok=True)
    
    # ============================================================
    # 🔥 SIRF DOWNLOADING PANEL (EK BAAR)
    # ============================================================
    console.print()
    console.print(Panel(
        "[bold bright_cyan]📥 Downloading SKIN_TOOL.zip...[/]\n"
        "[dim]Please wait...[/]",
        title="[bold black on bright_cyan] DOWNLOADING [/]",
        border_style="bright_cyan",
        box=box.HEAVY
    ))
    console.print()
    
    try:
        # ============================================================
        # 🔥 DOWNLOAD PROGRESS (SIRF YAHI DIKHEGA)
        # ============================================================
        with Progress(
            TextColumn("[bold cyan]⬇️ {task.description}"),
            BarColumn(bar_width=50, complete_style=f"bold {get_banner_color()}", finished_style="bold green"),
            TextColumn("[bold white]{task.percentage:>3.0f}%"),
            TextColumn("[dim]({task.fields[file_size]})"),
            TransferSpeedColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            response = requests.get(GITHUB_URL, stream=True, timeout=60)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            task = progress.add_task(
                f"Downloading",
                total=total_size,
                file_size=""
            )
            
            with open(zip_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            file_size_mb = downloaded / (1024 * 1024)
                            progress.update(
                                task,
                                completed=downloaded,
                                file_size=f"{file_size_mb:.2f} MB"
                            )
        
        # 🔥 DOWNLOAD COMPLETE
        console.print()
        console.print("[bold {get_banner_color()}]✔ Download complete![/]")
        
        # ============================================================
        # 🔥 EXTRACT (BACKGROUND MEIN - KUCH DIKHAO MAT)
        # ============================================================
       # console.print("[dim]📦 Extracting... (Please wait)[/]")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(base_dir)
        
        # 🔥 ZIP DELETE (CHUP CHAP)
        if zip_path.exists():
            zip_path.unlink()
        
        # ============================================================
        # 🔥 SUCCESS (SIRF EK PANEL)
        # ============================================================
        console.print()
        console.print(Panel(
            f"[bold {get_banner_color()}]✅ SKIN_TOOL ready![/]",
            title= f"[bold black on {get_banner_color()}] ✓ COMPLETE [/]",
            border_style=get_banner_color(),
            box=box.ROUNDED
        ))
        
        # 🔥 PRESS ENTER
        from rich.prompt import Prompt
        Prompt.ask("[bold bright_cyan]Press Enter to continue...[/bold bright_cyan]", default="")
        return True
        
    except Exception as e:
        console.print()
        console.print(Panel(
            f"[bold red]❌ Download failed![/]\n"
            f"[yellow]Error: {e}[/]",
            title="[bold red] ⚠️ ERROR [/]",
            border_style="red",
            box=box.HEAVY
        ))
        return False
        
# ======================================================================
# 🔥 YAHAN SE EXISTING CODE CONTINUE HOTA HAI 🔥
# ======================================================================

def files_available_panel(pak_files: List[Path], folder_label: str = "Files available") -> Panel:
    b_color = get_banner_color()
    tbl = Table(box=box.SQUARE, expand=True, border_style=b_color)
    
    tbl.add_column("No.", style="bold cyan", width=4, justify="right")
    tbl.add_column("Filename", style=f"bold {b_color}")
    tbl.add_column("Size", style=f"bold {b_color}", justify="right")
    
    for i, p in enumerate(pak_files, start=1):
        try:
            size = os.stat(to_long_path(p)).st_size
            size_str = f"{size:,} bytes"
        except Exception: 
            size_str = "?"
        
        tbl.add_row(
            to_fancy(str(i)), 
            Text(to_fancy(p.name), style=f"bold {b_color}"), 
            Text(to_fancy(size_str), style=f"bold {b_color}")
        )
        
    return Panel(
        tbl, 
        title=f"[bold black on {b_color}]{to_fancy(folder_label)}[/]", 
        border_style=b_color, 
        box=box.HEAVY # Charo kone acche se lock ho jayenge
    )

def list_paks_in_folder(folder: Path) -> List[Path]:
    folder_str = to_long_path(folder)
    if not os.path.exists(folder_str): return []
    try: names = sorted(os.listdir(folder_str))
    except Exception: return []
    results: List[Path] = []
    for name in names:
        try:
            full = Path(folder) / name
            if os.path.isfile(to_long_path(full)) and (full.suffix.lower() == '.pak' or full.suffix.lower() == '.obb'):
                results.append(full)
        except Exception: continue
    return results

# ---------------------------
# TOOLS (RedMagix Core)
# ---------------------------
def encrypt_file(input_path: Path, output_path: Path) -> bool:
    try:
        shutil.copy2(to_long_path(input_path), to_long_path(output_path))
        with open_long(output_path, "r+b") as f:
            f.seek(0, 2)
            file_size = f.tell()
            seek_pos = max(0, file_size - 45)
            f.seek(seek_pos)
            f.write(b'\x00' * 40)
        return True
    except Exception as e:
        console.print(f"[red]Error encrypting {input_path.name}: {e}[/red]")
        return False


# ══════════════════════════════════════════════════════════════════════════════
# 🔒 OPTION 15 — PAK ENCRYPT SUBMENU
# Sub-options: 1=Normal Enc  2=Custom Enc  3=Decrypt Restore  0=Back
# ══════════════════════════════════════════════════════════════════════════════

def run_pak_encrypt_submenu():
    """Option 15 – PAK Encryption Tool with Normal / Custom / Decrypt submenu."""

    # ── folder layout (mirrors Enc_pak already used by run_encrypt_tool) ──────
    enc_base   = Path(BASE_DIR_NAME) / "Enc_pak"
    input_dir  = enc_base / "Input"
    output_dir = enc_base / "Output"
    os.makedirs(to_long_path(input_dir),  exist_ok=True)
    os.makedirs(to_long_path(output_dir), exist_ok=True)

    b_color = get_banner_color()

    # ── helpers ───────────────────────────────────────────────────────────────
    def _header():
        console.clear()
        print_banner_and_header()
        print_user_profile()

    def _get_files():
        return [f for f in input_dir.iterdir()
                if f.is_file() and f.suffix.lower() in ('.pak', '.obb')]

    def _no_files_panel():
        console.print(Panel(
            f"[red]No .pak / .obb files found in:[/red]\n"
            f"[yellow]{input_dir.resolve()}[/yellow]\n\n"
            f"[white]Place your files there and try again.[/white]",
            title="❗ No Files", border_style="red", box=box.HEAVY
        ))
        Prompt.ask("\nPress Enter to continue", default="")

    # ── Normal Encryption (last-45-bytes sig kill, same as encrypt_file) ──────
    def _normal_enc():
        _header()
        console.print(Panel(
            f"[bold {b_color}]🔒 NORMAL ENCRYPTION[/bold {b_color}]\n"
            f"[dim]Standard MINI OBB sig kill — zeroes last 45 bytes[/dim]",
            border_style=b_color, box=box.HEAVY
        ))
        files = _get_files()
        if not files:
            _no_files_panel(); return

        console.print(f"[green]Found {len(files)} file(s).[/green]\n")
        ok = 0
        with Progress(
            SpinnerColumn("bouncingBar", style=f"bold {b_color}"),
            TextColumn(f"[bold {b_color}]{{task.description}}"),
            BarColumn(),
            TextColumn("[bold white]{task.percentage:>3.0f}%"),
            console=console
        ) as prog:
            task = prog.add_task("Normal Encrypting...", total=len(files))
            for f in files:
                out = output_dir / f.name
                try:
                    shutil.copy2(to_long_path(f), to_long_path(out))
                    with open_long(out, "r+b") as fh:
                        fh.seek(0, 2)
                        sz = fh.tell()
                        fh.seek(max(0, sz - 45))
                        fh.write(b'\x00' * 40)
                    ok += 1
                    prog.console.print(f"[bold green]✔ Encrypted:[/bold green] {f.name}")
                except Exception as e:
                    prog.console.print(f"[red]✘ {f.name}: {e}[/red]")
                prog.advance(task)

        console.print(Panel(
            f"[bold {b_color}]✔ {ok}/{len(files)} files encrypted successfully![/bold {b_color}]\n"
            f"[white]Output:[/white] [cyan]{output_dir.resolve()}[/cyan]",
            border_style=b_color, box=box.HEAVY
        ))
        Prompt.ask("\nPress Enter to continue", default="")

    # ── Custom Encryption (level 1-10 + optional custom XOR key) ─────────────
    def _custom_enc():
        _header()
        console.print(Panel(
            f"[bold {b_color}]🔐 CUSTOM ENCRYPTION[/bold {b_color}]\n"
            f"[dim]Level 1-10 intensity + optional custom XOR key[/dim]",
            border_style=b_color, box=box.HEAVY
        ))
        files = _get_files()
        if not files:
            _no_files_panel(); return

        # Level selection
        level_table = Table(show_header=True, header_style=f"bold black on {b_color}",
                            box=box.DOUBLE_EDGE, border_style=b_color, expand=True)
        level_table.add_column("LEVEL", style="bold white", justify="center", width=8)
        level_table.add_column("BYTES ZEROED", style=f"bold {b_color}")
        level_table.add_column("DESCRIPTION", style="dim white")
        level_defs = [
            ("1",  20,  "Light — last 20 bytes"),
            ("2",  30,  "Mild  — last 30 bytes"),
            ("3",  40,  "Standard — last 40 bytes"),
            ("4",  45,  "Normal — last 45 bytes (default)"),
            ("5",  64,  "Medium — last 64 bytes"),
            ("6",  80,  "Strong — last 80 bytes"),
            ("7",  100, "Heavy — last 100 bytes"),
            ("8",  128, "Aggressive — last 128 bytes"),
            ("9",  200, "Extreme — last 200 bytes"),
            ("10", 256, "MAX — last 256 bytes"),
        ]
        for lv, nb, desc in level_defs:
            level_table.add_row(f"[bold cyan]{lv}[/bold cyan]",
                                f"[bold {b_color}]{nb}[/bold {b_color}]",
                                f"[white]{desc}[/white]")
        console.print(Panel(level_table, border_style=b_color, box=box.HEAVY))

        raw_level = Prompt.ask(f"\n[bold {b_color}]Select Level (1-10)[/bold {b_color}]", default="4")
        try:
            level_idx = max(0, min(9, int(raw_level) - 1))
        except ValueError:
            level_idx = 3
        _, zero_bytes, _ = level_defs[level_idx]

        # Optional custom XOR key
        custom_key_str = Prompt.ask(
            f"[bold {b_color}]Custom XOR key as HEX (leave blank to skip)[/bold {b_color}]",
            default=""
        ).strip()
        custom_key = b""
        if custom_key_str:
            try:
                custom_key = bytes.fromhex(custom_key_str)
                console.print(f"[green]✔ Custom key loaded ({len(custom_key)} bytes)[/green]")
            except ValueError:
                console.print("[yellow]⚠ Invalid hex — skipping custom key[/yellow]")

        console.print(f"\n[green]Found {len(files)} file(s). Level {level_idx+1} — {zero_bytes} bytes.[/green]\n")
        ok = 0
        with Progress(
            SpinnerColumn("bouncingBar", style=f"bold {b_color}"),
            TextColumn(f"[bold {b_color}]{{task.description}}"),
            BarColumn(),
            TextColumn("[bold white]{task.percentage:>3.0f}%"),
            console=console
        ) as prog:
            task = prog.add_task("Custom Encrypting...", total=len(files))
            for f in files:
                out = output_dir / f.name
                try:
                    shutil.copy2(to_long_path(f), to_long_path(out))
                    with open_long(out, "r+b") as fh:
                        fh.seek(0, 2)
                        sz = fh.tell()
                        seek_pos = max(0, sz - zero_bytes)
                        fh.seek(seek_pos)
                        if custom_key:
                            # XOR the tail with rolling custom key
                            fh.seek(seek_pos)
                            tail = bytearray(fh.read(zero_bytes))
                            kl = len(custom_key)
                            tail = bytearray(tail[i] ^ custom_key[i % kl] for i in range(len(tail)))
                            fh.seek(seek_pos)
                            fh.write(bytes(tail))
                        else:
                            fh.seek(seek_pos)
                            fh.write(b'\x00' * zero_bytes)
                    ok += 1
                    prog.console.print(f"[bold green]✔ Encrypted:[/bold green] {f.name}  [dim](level {level_idx+1})[/dim]")
                except Exception as e:
                    prog.console.print(f"[red]✘ {f.name}: {e}[/red]")
                prog.advance(task)

        console.print(Panel(
            f"[bold {b_color}]✔ {ok}/{len(files)} files encrypted (Level {level_idx+1})![/bold {b_color}]\n"
            f"[white]Output:[/white] [cyan]{output_dir.resolve()}[/cyan]",
            border_style=b_color, box=box.HEAVY
        ))
        Prompt.ask("\nPress Enter to continue", default="")

    # ── Decrypt Restore (restore MINI OBB / ZSDIC signature from original) ────
    def _decrypt_restore():
        _header()
        console.print(Panel(
            f"[bold {b_color}]🔓 DECRYPT RESTORE[/bold {b_color}]\n"
            f"[dim]Restore MINI OBB / ZSDIC signature from an original reference file[/dim]",
            border_style=b_color, box=box.HEAVY
        ))

        # Expect: Input/ has the encrypted files, Output/ will get restored files
        # User must also supply an original (unencrypted) reference in Input/original/
        orig_dir = input_dir / "original"
        os.makedirs(to_long_path(orig_dir), exist_ok=True)

        enc_files = _get_files()
        orig_files = [f for f in orig_dir.iterdir()
                      if f.is_file() and f.suffix.lower() in ('.pak', '.obb')] if orig_dir.exists() else []

        if not enc_files:
            _no_files_panel(); return

        if not orig_files:
            console.print(Panel(
                f"[red]No original reference file found![/red]\n"
                f"[yellow]Place the unencrypted original .pak/.obb in:[/yellow]\n"
                f"[cyan]{orig_dir.resolve()}[/cyan]\n\n"
                f"[white]The last 45 bytes of the original will be used to restore the signature.[/white]",
                border_style="red", box=box.HEAVY
            ))
            Prompt.ask("\nPress Enter to continue", default="")
            return

        # Map originals by filename for fast lookup
        orig_map = {f.name: f for f in orig_files}

        console.print(f"[green]Found {len(enc_files)} encrypted file(s).[/green]\n")
        ok = 0
        with Progress(
            SpinnerColumn("bouncingBar", style=f"bold {b_color}"),
            TextColumn(f"[bold {b_color}]{{task.description}}"),
            BarColumn(),
            TextColumn("[bold white]{task.percentage:>3.0f}%"),
            console=console
        ) as prog:
            task = prog.add_task("Restoring signatures...", total=len(enc_files))
            for f in enc_files:
                out = output_dir / f.name
                try:
                    if f.name not in orig_map:
                        prog.console.print(f"[yellow]⚠ No matching original for {f.name} — skipped[/yellow]")
                        prog.advance(task); continue

                    orig_path = orig_map[f.name]

                    # Read last 45 bytes from original
                    with open_long(orig_path, "rb") as fh:
                        fh.seek(0, 2)
                        orig_sz = fh.tell()
                        sig_seek = max(0, orig_sz - 45)
                        fh.seek(sig_seek)
                        original_sig = fh.read(45)

                    # Copy encrypted file → output, then patch signature back
                    shutil.copy2(to_long_path(f), to_long_path(out))
                    with open_long(out, "r+b") as fh:
                        fh.seek(0, 2)
                        out_sz = fh.tell()
                        patch_seek = max(0, out_sz - 45)
                        fh.seek(patch_seek)
                        fh.write(original_sig)

                    ok += 1
                    prog.console.print(f"[bold green]✔ Restored:[/bold green] {f.name}")
                except Exception as e:
                    prog.console.print(f"[red]✘ {f.name}: {e}[/red]")
                prog.advance(task)

        console.print(Panel(
            f"[bold {b_color}]✔ {ok}/{len(enc_files)} signatures restored![/bold {b_color}]\n"
            f"[white]Output:[/white] [cyan]{output_dir.resolve()}[/cyan]",
            border_style=b_color, box=box.HEAVY
        ))
        Prompt.ask("\nPress Enter to continue", default="")

    # ── Sub-menu loop ─────────────────────────────────────────────────────────
    while True:
        _header()

        sub_table = Table(
            show_header=True,
            header_style=f"bold black on {b_color}",
            box=box.DOUBLE_EDGE,
            border_style=b_color,
            expand=True,
            title=(rainbow_markup("  🔒 PAK ENCRYPTION TOOL  ") if CURRENT_SESSION_COLOR == "rainbow" else f"[reverse]  🔒 {to_fancy('PAK ENCRYPTION TOOL')}  [/]")
        )
        if CURRENT_SESSION_COLOR == "rainbow":
            sub_table.add_column(rainbow_text("𝐎𝐏𝐓"), justify="center", width=6)
            sub_table.add_column(rainbow_text("𝐎𝐏𝐄𝐑𝐀𝐓𝐈𝐎𝐍"))
            sub_table.add_column(rainbow_text("𝐃𝐄𝐒𝐂𝐑𝐈𝐏𝐓𝐈𝐎𝐍"))
        else:
            sub_table.add_column("𝐎𝐏𝐓",       style="bold white",  justify="center", width=6)
            sub_table.add_column("𝐎𝐏𝐄𝐑𝐀𝐓𝐈𝐎𝐍", style=f"bold {b_color}")
            sub_table.add_column("𝐃𝐄𝐒𝐂𝐑𝐈𝐏𝐓𝐈𝐎𝐍", style="dim white")

        if CURRENT_SESSION_COLOR == "rainbow":
            menu_row(sub_table, "1", "🔒 Normal Encryption", "Standard MINI OBB sig kill (last 45 bytes)")
            menu_row(sub_table, "2", "🔐 Custom Encryption", "Level 1-10 + Optional Custom XOR Key")
            menu_row(sub_table, "3", "🔓 Decrypt Restore", "Restore MINI OBB / ZSDIC signature")
            menu_row(sub_table, "0", "↩ Back", "Return to Main Menu")
        else:
            sub_table.add_row(
            "[bold cyan]1[/bold cyan]",
            f"[bold {b_color}]🔒 Normal Encryption[/bold {b_color}]",
            "[white]Standard MINI OBB sig kill (last 45 bytes)[/white]"
        )
        sub_table.add_row(
            "[bold cyan]2[/bold cyan]",
            f"[bold {b_color}]🔐 Custom Encryption[/bold {b_color}]",
            "[white]Level 1-10 + Optional Custom XOR Key[/white]"
        )
        sub_table.add_row(
            "[bold yellow]3[/bold yellow]",
            "[bold yellow]🔓 Decrypt Restore[/bold yellow]",
            "[white]Restore MINI OBB / ZSDIC signature[/white]"
        )
        sub_table.add_row(
            "[bold red]0[/bold red]",
            "[bold red]↩ Back[/bold red]",
            "[dim red]Return to Main Menu[/dim red]"
        )

        console.print(Panel(sub_table, border_style=b_color, box=box.HEAVY))
        sub_choice = Prompt.ask(f"[bold {b_color}]Select option (1-3, 0 = Back)[/bold {b_color}]")

        if sub_choice == "1":
            _normal_enc()
        elif sub_choice == "2":
            _custom_enc()
        elif sub_choice == "3":
            _decrypt_restore()
        elif sub_choice == "0":
            break
        else:
            console.print(Panel("[bold red]❌ Invalid option![/bold red]", border_style="red", box=box.HEAVY))
            time.sleep(1)

@security_guard
def run_encrypt_tool():
    console.clear()
    console.print(get_neon_header())
    b_color = get_banner_color()
    console.print(Panel(f"[bold {b_color}]{to_fancy('ENCRYPTION TOOL')}[/bold {b_color}]\n[dim]Lock .pak/.obb files (signature kill).[/dim]", border_style=b_color))

    create_dirs(Path(BASE_DIR_NAME))
    input_files = [f for f in ENCRYPT_INPUT_DIR.iterdir() if f.is_file() and f.suffix.lower() in ('.pak', '.obb')]
    if not input_files:
        console.print(Panel(f"[red]No .pak/.obb files found in[/red]\n[yellow]{ENCRYPT_INPUT_DIR.resolve()}[/yellow]\n\n[white]Please place your files there and try again.[/white]", title="❗ No Files", border_style="red"))
        Prompt.ask("\nPress Enter to continue", default="")
        return

    console.print(f"[green]Found {len(input_files)} file(s) to process.[/green]")
    success_count = 0

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), console=console) as progress:
        task = progress.add_task(f"[{b_color}]Encrypting...", total=len(input_files))
        for f in input_files:
            out_path = ENCRYPT_OUTPUT_DIR / f.name
            if encrypt_file(f, out_path):
                success_count += 1
            progress.advance(task)

    console.print("\n")
    if success_count == len(input_files):
        console.print(Panel(f"[bold {b_color}]✔ {to_fancy('ALL FILES ENCRYPTED SUCCESSFULLY')}![/bold {b_color}]\n[white]Output folder:[/white] [cyan]{ENCRYPT_OUTPUT_DIR.resolve()}[/cyan]", border_style=b_color))
    else:
        console.print(Panel(f"[yellow]Encryption completed with {success_count}/{len(input_files)} successes.[/yellow]\n[white]Check errors above. Output folder:[/white] [cyan]{ENCRYPT_OUTPUT_DIR.resolve()}[/cyan]", border_style="yellow"))
    Prompt.ask("\nPress Enter to return to menu", default="")

@security_guard
def run_obb_analysis_tool():
    console.clear()
    console.print(get_neon_header())
    b_color = get_banner_color()
    console.print(Panel(f"[bold {b_color}]{to_fancy('DEEP SCAN & EXTRACT (PRO AUTO-SINGLE)')}[/bold {b_color}]\n[dim]Scanning OBBs and auto-extracting modified .uasset/.uexp to RESULT folder...[/dim]", border_style=b_color))

    org_files = list_paks_in_folder(ANLAISH_ORG)
    mod_files = list_paks_in_folder(ANLAISH_MOD)

    if not org_files or not mod_files:
        console.print(Panel(f"[red]Error: Files missing![/red]\n[white]Please put Original OBB in: {ANLAISH_ORG}\nPlease put Mod OBB in: {ANLAISH_MOD}[/white]"))
        Prompt.ask("Press Enter to go back...")
        return

    total_processed = 0

    for org_path in org_files:
        mod_path = next((f for f in mod_files if f.name == org_path.name), None)
        if not mod_path:
            console.print(Panel(f"[yellow]Skipping {org_path.name}: Not found in MOD folder![/yellow]"))
            continue

        console.print(f"\n[bold {b_color}]==================================================[/]")
        console.print(f"[{b_color}]{to_fancy('Original:')}[/{b_color}] {to_fancy(org_path.name)}")
        console.print(f"[magenta]{to_fancy('Modded:')}[/magenta]   {to_fancy(mod_path.name)}")
        console.print(Panel(f"[yellow]{to_fancy('LOADING FILES INTO MEMORY')}...[/yellow]"))
        
        current_result_dir = ANLAISH_RESULT / org_path.name
        os.makedirs(to_long_path(current_result_dir), exist_ok=True)

        try:
            pak_org = TencentPakFile(org_path)
            pak_mod = TencentPakFile(mod_path)

            console.print("[bold yellow]🔥POWER BY- @KAZUKI...👇[/bold yellow]")
            if not pak_mod._index:
                console.print("[bold cyan]..[/bold cyan]")
                pak_mod._index = pak_org._index
                pak_mod._pak_info = pak_org._pak_info
                pak_mod._mount_point = pak_org._mount_point
                pak_mod._zstd_dict = pak_org._zstd_dict
            else:
                console.print("[bold green][/bold green]")

            def flatten_index(pak_obj):
                flat = {}
                for dir_path, files in pak_obj._index.items():
                    for name, entry in files.items():
                        if entry:
                            full_p = str(dir_path / name).replace("\\", "/")
                            flat[full_p] = entry
                return flat

            flat_org = flatten_index(pak_org)
            flat_mod = flatten_index(pak_mod)

            extracted_count = 0
            
            with Progress(
                SpinnerColumn(), 
                TextColumn("[progress.description]{task.description}"), 
                BarColumn(), 
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), 
                TimeElapsedColumn(),
                console=console
            ) as progress:
                task = progress.add_task(f"[{b_color}]Scanning & Extracting...", total=len(flat_mod))
                
                for f_path, mod_entry in flat_mod.items():
                    valid_exts = ('.uasset', '.uexp', '.lua', '.json', '.ini')
                    if f_path.lower().endswith(valid_exts) or 'luatool' in f_path.lower():
                        is_modified = False
                        
                        if f_path in flat_org:
                            org_entry = flat_org[f_path]
                            if mod_entry.size != org_entry.size:
                                is_modified = True
                            else:
                                try:
                                    org_data = pak_org._peek_content(org_entry.offset, org_entry.size, org_entry.encryption_method)
                                    mod_data = pak_mod._peek_content(mod_entry.offset, mod_entry.size, mod_entry.encryption_method)
                                    if org_data != mod_data:
                                        is_modified = True
                                except Exception: pass
                        else:
                            is_modified = True 

                        if is_modified:
                            relative_path = Path(f_path)
                            dest_file = current_result_dir / relative_path
                            
                            os.makedirs(to_long_path(dest_file.parent), exist_ok=True)
                            
                            try:
                                pak_mod._write_to_disk(dest_file, mod_entry)
                                extracted_count += 1
                                
                                file_name_only = relative_path.name
                                
                                # 1. Auto-Detected Location in Green (Bina aage ke path ke)
                                progress.console.print(f"[bold {get_banner_color()}]✓ {to_fancy('Auto-Detected Location')}:[/bold {get_banner_color()}]")
                                
                                # 2. Premium Green Box with Blue Encryption Text
                                panel_text = (
                                    f"[bold cyan]Extracted:[/] [bold white]{file_name_only}[/]\n"
                                    f"[bold yellow]Target Entry:[/] [bold green]{relative_path.as_posix()}[/]\n"
                                    f"[bold bright_blue]Encryption Method Applied: {mod_entry.encryption_method}[/]"
                                )
                                progress.console.print(Panel(panel_text, border_style=get_banner_color(), box=box.SQUARE))
                                
                            except Exception as e:
                                progress.console.print(f"[bold red]❌ FAILED:[/] {f_path} - [dim]{e}[/dim]")

                    progress.advance(task)

            total_processed += 1
        except Exception as e:
            console.print(Panel(f"[red]Analysis Failed for {org_path.name}: {e}[/red]"))

    MOD_REPACK_BASE = ANLAISH_DIR / "MOD_REPACK"
    os.makedirs(to_long_path(MOD_REPACK_BASE), exist_ok=True)

    if total_processed > 0:
        console.print(Panel(f"[bold {b_color}]🎉 {to_fancy('ALL FILES ANALYZED & EXTRACTED SUCCESSFULLY')}![/bold {b_color}]\n[white]Total OBBs Processed: {total_processed}[/white]", border_style=b_color))
    
    while True:
        console.print("\n")
        pro_menu = Table(show_header=False, box=box.SIMPLE, expand=True)
        if CURRENT_SESSION_COLOR == "rainbow":
            pro_menu.add_column(rainbow_text("𝐎𝐏𝐓"), width=4)
            pro_menu.add_column(rainbow_text("DESC"))
            pro_menu.add_row(rainbow_text("1"), rainbow_text("AUTO REMOVE CRDIT"))
            pro_menu.add_row(rainbow_text("2"), rainbow_text("ADD YOUR CREDIT"))
            pro_menu.add_row(rainbow_text("3"), rainbow_text("PRO REPACK"))
            pro_menu.add_row(rainbow_text("0"), rainbow_text("BACK"))
        else:
            pro_menu.add_column("𝐎𝐏𝐓", style="bold white", width=4)
            pro_menu.add_column("DESC", style=f"bold {b_color}")
            pro_menu.add_row("1", to_fancy("AUTO REMOVE CRDIT"))
            pro_menu.add_row("2", to_fancy("ADD YOUR CREDIT"))
            pro_menu.add_row("3", to_fancy("PRO REPACK"))
            pro_menu.add_row("0", f"[red]{to_fancy('BACK')}[/red]")
        
        console.print(Panel(pro_menu, title=f"[bold yellow]🔥 {to_fancy('USE PRO MODE')} 🔥[/bold yellow]", border_style="yellow"))
        
        pro_choice = Prompt.ask(f"[bold {b_color}]Select PRO Option[/bold {b_color}]", choices=["1", "2", "3", "0"])
        
        if pro_choice == "1":
            console.print(f"\n[bold cyan]🔍 Purana kachra saaf kar rahe hain aur ShadowTrackerExtra nikal rahe hain...[/bold cyan]")
            
            dest_shadow_dir = MOD_REPACK_BASE / "ShadowTrackerExtra"
            files_to_delete = ["SplashScreen_BH.uexp", "LocalizationText_en.uexp"]
            source_dumps = ["mini_obb.pak", "mini_obbzsdic_obb.pak"]
            
            import shutil
            moved_any = False

            for dump_name in source_dumps:
                source_shadow_dir = ANLAISH_RESULT / dump_name / "ShadowTrackerExtra"
                
                if source_shadow_dir.exists():
                    console.print(f"\n[bold yellow]📦 Processing:[/] {dump_name}")
                    
                    for file_path in source_shadow_dir.rglob("*"):
                        if file_path.is_file() and file_path.name in files_to_delete:
                            try: 
                                file_path.unlink()
                                console.print(f"[bold green]✅ KILLED:[/] {file_path.name}")
                            except: pass
                    
                    console.print(f"[cyan]📂 Merging {dump_name} assets to MOD_REPACK...[/cyan]")
                    try:
                        os.makedirs(to_long_path(dest_shadow_dir), exist_ok=True)
                        for item in os.listdir(to_long_path(source_shadow_dir)):
                            s = source_shadow_dir / item
                            d = dest_shadow_dir / item
                            if s.is_dir():
                                if d.exists(): shutil.rmtree(to_long_path(d))
                                shutil.copytree(to_long_path(s), to_long_path(d))
                            else:
                                shutil.copy2(to_long_path(s), to_long_path(d))
                        moved_any = True
                        console.print(f"[bold green]✔ Merged Successfully![/bold green]")
                    except Exception as e:
                        console.print(f"[red]Error copying {dump_name}: {e}[/red]")
                else:
                    console.print(f"[dim]Skip: {dump_name} not found in RESULT.[/dim]")

            if moved_any:
                console.print(f"\n[bold {get_banner_color()}]🚀 BOOM! RESULT ka sara data MOD_REPACK me aa gaya![/bold {get_banner_color()}]")
                console.print(f"[white]Target:[/] {dest_shadow_dir.resolve()}")
            else:
                console.print(f"\n[red]❌ Error: RESULT folder me koi ShadowTrackerExtra nahi mila! Pehle Analyze karo.[/red]")
            
            time.sleep(2)
                
        elif pro_choice == "2":
            black_tool_main()
            console.clear()
            print_banner_and_header()
            
        elif pro_choice == "3":
            import shutil
            global EDITED_DIR 
            
            console.print(f"\n[bold cyan]🔨 Initiating PRO REPACK (Target: MOD_REPACK/RESULT)...[/bold cyan]")
            
            original_mod_dir = EDITED_DIR
            MOD_REPACK_path = ANLAISH_DIR / "MOD_REPACK"
            final_repack_dir = MOD_REPACK_path / "RESULT"
            
            if not MOD_REPACK_path.exists() or not any(os.scandir(to_long_path(MOD_REPACK_path))):
                console.print(Panel("[bold red]❌ Error: MOD_REPACK folder khali hai![/bold red]"))
                continue

            try:
                os.makedirs(to_long_path(final_repack_dir), exist_ok=True)
                EDITED_DIR = MOD_REPACK_path
                TencentPakFile.MODIFIED_DIR = MOD_REPACK_path
                
                base_org = Path(BASE_DIR_NAME) / "OBB_UNPACKER" / ORGNAL_DIR
                pak_files = list_paks_in_folder(base_org)
                selected = auto_detect_repack_candidates(pak_files, MOD_REPACK_path)
                
                if not selected:
                    console.print("[yellow]⚠️ MOD_REPACK ke assets ke liye koi matching OBB nahi mila.[/yellow]")
                else:
                    for pak_path in selected:
                        repacked_copy = final_repack_dir / pak_path.name
                        if repacked_copy.exists(): 
                            repacked_copy.unlink()
                            
                        shutil.copy2(to_long_path(pak_path), to_long_path(repacked_copy))
                        
                        console.print(f"[cyan]📦 Repacking:[/] {pak_path.name}")
                        pak = TencentPakFile(pak_path)
                        with open_long(repacked_copy, 'r+b') as fh:
                            pak.repack_inplace_from_modified_dir(fh)
                        
                        console.print(f"[bold green]✔ Saved in RESULT folder:[/] {repacked_copy.resolve()}")

                EDITED_DIR = original_mod_dir
                console.print(f"\n[bold green]✅ PRO REPACK COMPLETE! Pak file 'MOD_REPACK/RESULT' me save ho gayi hai.[/bold green]")
            except Exception as e:
                EDITED_DIR = original_mod_dir
                console.print(f"[red]Repack Error: {e}[/red]")

            Prompt.ask("\nPress Enter to continue...")

        elif pro_choice == "0":
            break

@security_guard
def run_obbzip_tool():
    """12.py KA EXACT COPY - SIRF SM4 KEYS SERVER SE + DIVISION BY ZERO FIX"""
    
    import os, sys, subprocess, shutil, zipfile
    from pathlib import Path
    import struct
    import tempfile
    import zlib
    import hashlib
    from dataclasses import dataclass
    from functools import lru_cache
    from typing import List, Optional
    import itertools as it
    import math
    from pathlib import PurePath
    from Crypto.Cipher import AES
    from Crypto.Cipher.AES import MODE_CBC
    from Crypto.Hash import SHA1
    from Crypto.Util.Padding import unpad, pad
    from zstandard import ZstdDecompressor, ZstdCompressor, ZstdCompressionDict, DICT_TYPE_AUTO
    from rich.box import ROUNDED
    from rich.align import Align
    from rich.console import Console  # ✅ YEH ADD KARO
    from rich.panel import Panel     # ✅ YEH ADD KARO
    from rich.table import Table     # ✅ YEH ADD KARO
    from rich.prompt import Prompt   # ✅ YEH ADD KARO
    
    
    try:
        import gmalg
        from gmalg import SM4, ZUC
    except ImportError:
        print('gmalg not found, installing...')
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'gmalg'], check=True)
        import gmalg
        from gmalg import SM4, ZUC
    
    console = Console()
    
    # ============================================================
    # OFFLINE CRYPTO MODE
    # ============================================================
    global SM4_SECRET_NEW
    # No network key fetch. Embedded SM4-2 / SM4-4 constants remain usable.
    
    # ============================================================
    # DIRECTORY SETUP
    # ============================================================
    KGF_BASE = Path("/data/data/com.termux/files/home/𝐊𝐀𝐙𝐔𝐊𝐈_𝐓𝐎𝐎𝐋")
    
    PAK_BASE = KGF_BASE / 'ANTIRESET_OBB'
    EDITED_FILES_DIR = PAK_BASE / 'EDITTED_FILES'
    REPACKED_PAK_DIR = PAK_BASE / 'REPACKED_PAK'
    
    OBB_BASE = KGF_BASE / 'ANTIRESET_OBB'
    ORIGINAL_OBB = OBB_BASE / 'Original_obb'
    UNPACKED_OBB = OBB_BASE / 'unpacked_obb'
    REPACKED_OBB = OBB_BASE / 'Repacked_obb'
    INPUT_FILE = UNPACKED_OBB / 'ShadowTrackerExtra' / 'Content' / 'Paks'
    
    EXES_DIR = KGF_BASE / 'EXES'
    
    def set_executable_permissions():
        if os.name == 'nt':
            return None
        if not EXES_DIR.exists():
            return None
        for item in EXES_DIR.iterdir():
            if item.is_file():
                try:
                    item.chmod(item.stat().st_mode | 0o111)
                except Exception:
                    pass
    
    def ensure_dirs():
        dirs_list = [
            EDITED_FILES_DIR, REPACKED_PAK_DIR, EXES_DIR, 
            ORIGINAL_OBB, UNPACKED_OBB, REPACKED_OBB, INPUT_FILE
        ]
        for d in dirs_list:
            if not d.exists():
                d.mkdir(parents=True, exist_ok=True)
        set_executable_permissions()
    
    ensure_dirs()

    # ============================================================
    # XOR KEY & SM4 SECRETS - SERVER SE
    # ============================================================
    _K = b'\x11!6GFW\xa7\x8d\x9d\x84\x90\xd8\xab\x00\x8c5&\x1a\xf7\xe4X\x05\xb8\xb3\x15\x07\xd0,\x1e\x8f\xf6\xc8'
    
    def xor_game_crypt(data: bytes) -> bytes:
        return bytes(b ^ _K[i % len(_K)] for i, b in enumerate(data))
    
    def ensure_sm4_secrets() -> bool:
        return SM4_SECRET_NEW is not None and len(SM4_SECRET_NEW) > 0

    # ============================================================
    # CRYPTO CONSTANTS
    # ============================================================
    ZUC_KEY = bytes.fromhex('01010101010101010101010101010101')
    ZUC_IV = bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
    RSA_MOD_1 = bytes.fromhex('CBE8B9F2504050EF9831B719E9A6249A6D238505ADE909BDE78C180DED6072A0C3347B8AF4780E1F212D952D82D4BF7F233C1ECA499E1F9D9A85B4FAD759F54BABC1666C5DE411EA9E4B2374425DD6C6F54333BBC8F2610FE6063E4D0D6C21A671A8F7C3740555E5DC06D4E1691C456DB4116C0C012BF7B206E8311AAAEC689952BF804EF638F09D5822B4117B114208F14DEB459E80CB770E5B0D7978E21F5E6CED4999D3583108221A7AB28B960277ADB5690A332784019D9C195BE4EA9EA0A09459010F236465DE0D59C3EF7324E954E1118D93EE19F299760C2CDB963CE87973EA5ECC9BBE81C27D4C7C8572AC07E9BCEAC9BD72AB7A56A3C0AD736ABCE4')
    RSA_MOD_2 = bytes.fromhex('7F58E8A39A4DA4E87357DDD650EAA16D3B5CE95B213D1030A662566444796A78A84AE9AC3DBFFDE7F41094896696835DAF13B89E6EC2B84963B1B1BAF7151DA245C3FBFAE2A6AE18B2684D03F9229DE2C91440F2A3A3BCDE1E5680C16722A88039C73560D5D43F4B6562C2EEA5B1D926D86B51108A2643C70FB74D6442CE3A08339B8FD8F660AE88129B7AB8C46F2FA58124485CCCB1E987B05A6DA65A01858ED3F89905449AE42BB07290FCB9994BF22E26610BCABB9804783A3B9587917F3D97316EDDA15C5E13F79066407B55A93B291B68A4AC42A98D6E35FED84B14A792D154E62028DDAD20FC301951E5924BE9AD62FB719DD94CC30CAB871BEC4377A8')
    SIMPLE1_DECRYPT_KEY = 121
    SIMPLE2_DECRYPT_KEY = bytes.fromhex('E55B4ED1')
    SIMPLE2_BLOCK_SIZE = 16
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

    _S_BOX = bytes([0x34,0x66,0x25,0x74,0x89,0x78,0xE4,0xA9,0x5A,0x41,0xBC,0x7A,0xD6,0x16,0x21,0x23,0x4D,0x61,0xDA,0x94,0x9B,0xDF,0x13,0x3C,0x69,0x3A,0x31,0x0A,0x5F,0xD7,0x99,0x95,0xF1,0xAE,0x72,0x3D,0x07,0x60,0x24,0xB6,0x98,0xEE,0xC4,0xA2,0x2D,0x88,0xDD,0x8D,0x04,0xEA,0xBB,0x11,0xCA,0x3E,0x5D,0xA1,0xF6,0x3F,0xB0,0x97,0x80,0x47,0x2B,0xA6,0xE6,0xF7,0xD9,0xB1,0x59,0xC0,0x7C,0xBE,0x54,0x28,0xB7,0x7E,0x4F,0xF8,0x43,0x6E,0xA0,0x50,0x0E,0xF5,0x90,0xB8,0xFB,0xA3,0x7B,0x62,0x19,0x46,0x03,0x2A,0xB9,0x8F,0x9F,0x77,0xB4,0x5B,0x83,0x87,0x08,0xEB,0xE2,0x1E,0x42,0xF0,0x0F,0xE8,0x71,0x6A,0x75,0xAD,0x55,0x1F,0xB5,0xAB,0x33,0xFA,0x7F,0x15,0xBD,0x85,0xD8,0x06,0x68,0xB3,0x52,0x30,0x48,0x0B,0x00,0xED,0xEF,0xB2,0x57,0x8E,0xE7,0x6C,0xD5,0xE5,0x2E,0x53,0x82,0x05,0xF9,0x81,0xF4,0x56,0xBF,0x8C,0x4B,0xE3,0xDB,0x4A,0x91,0x4C,0x2C,0xD3,0x40,0x29,0x4E,0x20,0x14,0x36,0x79,0x09,0x6F,0xD1,0x37,0xE0,0x39,0x0C,0x8A,0x92,0x38,0x12,0x35,0x6D,0xE1,0xFD,0x93,0x9A,0x17,0xD4,0xC9,0x9C,0x6B,0x84,0x26,0x9D,0xAF,0x76,0xC1,0x9E,0xD0,0x96,0xC5,0xCB,0xE9,0x73,0x49,0xD2,0xCD,0x64,0xC3,0xC7,0x01,0x7D,0xF3,0xAC,0xFC,0xDE,0xA4,0x44,0x32,0x1B,0xC2,0xBA,0x1C,0x02,0xC6,0x27,0x45,0x8B,0xF2,0x18,0xA7,0x10,0x51,0x1D,0xC8,0xCF,0x63,0xFF,0x2F,0x0D,0x58,0xCE,0x65,0xA5,0xDC,0x1A,0x3B,0x86,0xFE,0x22,0x5C,0xA8,0x5E,0x67,0xAA,0xEC,0x70,0xCC])

    _FK = [0x46970E9C, 0x4BC0685E, 0x59056186, 0xBCA2491E]

    _CK = [0x000EB92B, 0x3A0AE783, 0x9E3B5C67, 0xADDBDABF, 0x7B7484CB, 0x49156C63, 0xC79AB5E7, 0x79EC9CFF,
           0x1725BEAB, 0x2FB89CA3, 0x24808AD7, 0xDDD28B1F, 0x4740DA4B, 0xBBC3EA73, 0x247B30E7, 0x91BE385F,
           0x0401248B, 0x45FCD3A3, 0x530B4CE7, 0xC68DD35F, 0xE3D16C2B, 0x4F698C13, 0x6B92C747, 0x769EFB1F,
           0x4C73BE9B, 0xC942B193, 0xAD80D827, 0x372FB33F, 0x13CB6AAB, 0x2BDC0AA3, 0x17A4A247, 0xD5E96CAF]

    def ROL32(x, n):
        return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))

    def _BS(X):
        return (_S_BOX[(X >> 24) & 0xFF] << 24 |
                _S_BOX[(X >> 16) & 0xFF] << 16 |
                _S_BOX[(X >> 8) & 0xFF] << 8 |
                _S_BOX[X & 0xFF])

    def _T0(X):
        X = _BS(X)
        return X ^ ROL32(X, 2) ^ ROL32(X, 10) ^ ROL32(X, 18) ^ ROL32(X, 24)

    def _T1(X):
        X = _BS(X)
        return X ^ ROL32(X, 13) ^ ROL32(X, 23)

    def _key_expand(key: bytes) -> List[int]:
        rkey = [0] * 32
        K0 = int.from_bytes(key[0:4], 'big') ^ _FK[0]
        K1 = int.from_bytes(key[4:8], 'big') ^ _FK[1]
        K2 = int.from_bytes(key[8:12], 'big') ^ _FK[2]
        K3 = int.from_bytes(key[12:16], 'big') ^ _FK[3]
        for i in range(0, 32, 4):
            K0 = K0 ^ _T1(K1 ^ K2 ^ K3 ^ _CK[i])
            rkey[i] = K0
            K1 = K1 ^ _T1(K2 ^ K3 ^ K0 ^ _CK[i + 1])
            rkey[i + 1] = K1
            K2 = K2 ^ _T1(K3 ^ K0 ^ K1 ^ _CK[i + 2])
            rkey[i + 2] = K2
            K3 = K3 ^ _T1(K0 ^ K1 ^ K2 ^ _CK[i + 3])
            rkey[i + 3] = K3
        return rkey

    class SM4:
        _rkey: List[int]
        
        def __init__(self, key: bytes):
            self._rkey = _key_expand(key)
        
        def encrypt(self, block: bytes) -> bytes:
            RK = self._rkey
            X0 = int.from_bytes(block[0:4], 'big')
            X1 = int.from_bytes(block[4:8], 'big')
            X2 = int.from_bytes(block[8:12], 'big')
            X3 = int.from_bytes(block[12:16], 'big')
            for i in range(0, 32, 4):
                X0 = X0 ^ _T0(X1 ^ X2 ^ X3 ^ RK[i])
                X1 = X1 ^ _T0(X2 ^ X3 ^ X0 ^ RK[i + 1])
                X2 = X2 ^ _T0(X3 ^ X0 ^ X1 ^ RK[i + 2])
                X3 = X3 ^ _T0(X0 ^ X1 ^ X2 ^ RK[i + 3])
            return (X3.to_bytes(4, 'big') + X2.to_bytes(4, 'big') +
                    X1.to_bytes(4, 'big') + X0.to_bytes(4, 'big'))
        
        def decrypt(self, block: bytes) -> bytes:
            RK = self._rkey
            X0 = int.from_bytes(block[0:4], 'big')
            X1 = int.from_bytes(block[4:8], 'big')
            X2 = int.from_bytes(block[8:12], 'big')
            X3 = int.from_bytes(block[12:16], 'big')
            for i in range(0, 32, 4):
                X0 = X0 ^ _T0(X1 ^ X2 ^ X3 ^ RK[31 - i])
                X1 = X1 ^ _T0(X2 ^ X3 ^ X0 ^ RK[30 - i])
                X2 = X2 ^ _T0(X3 ^ X0 ^ X1 ^ RK[29 - i])
                X3 = X3 ^ _T0(X0 ^ X1 ^ X2 ^ RK[28 - i])
            return (X3.to_bytes(4, 'big') + X2.to_bytes(4, 'big') +
                    X1.to_bytes(4, 'big') + X0.to_bytes(4, 'big'))

    class Misc:
        @staticmethod
        def pad_to_n(data: bytes, n: int) -> bytes:
            padding = n - (len(data) % n)
            if padding == n:
                return data
            return data + b'\x00' * padding
        
        @staticmethod
        def align_up(x: int, n: int) -> int:
            return ((x + n - 1) // n) * n

    class Reader_pak:
        _buffer: bytes
        _cursor: int
        
        def __init__(self, buffer: bytes, cursor: int = 0):
            self._buffer = buffer
            self._cursor = cursor
        
        def u1(self, move_cursor: bool = True) -> int:
            return self.unpack('B', move_cursor=move_cursor)[0]
        
        def u4(self, move_cursor: bool = True) -> int:
            return self.unpack('<I', move_cursor=move_cursor)[0]
        
        def u8(self, move_cursor: bool = True) -> int:
            return self.unpack('<Q', move_cursor=move_cursor)[0]
        
        def i1(self, move_cursor: bool = True) -> int:
            return self.unpack('b', move_cursor=move_cursor)[0]
        
        def i4(self, move_cursor: bool = True) -> int:
            return self.unpack('<i', move_cursor=move_cursor)[0]
        
        def i8(self, move_cursor: bool = True) -> int:
            return self.unpack('<q', move_cursor=move_cursor)[0]
        
        def s(self, n: int, move_cursor: bool = True) -> bytes:
            return self.unpack(f'{n}s', move_cursor=move_cursor)[0]
        
        def unpack(self, f: str, offset: int = 0, move_cursor: bool = True):
            x = struct.unpack_from(f, self._buffer, self._cursor + offset)
            if move_cursor:
                self._cursor += struct.calcsize(f)
            return x
        
        def string(self, move_cursor: bool = True) -> str:
            length = self.i4(move_cursor=move_cursor)
            if length == 0:
                return ''
            offset = 0 if move_cursor else 4
            return self.unpack(f'{length}s', offset=offset, move_cursor=move_cursor)[0].rstrip(b'\x00').decode()

    def serialize_string(s: str) -> bytes:
        if not s:
            return struct.pack('<i', 0)
        b = s.encode('utf-8')
        return struct.pack('<i', len(b) + 1) + b + b'\x00'

    class PakIndexWriter:
        data: bytearray
        
        def __init__(self):
            self.data = bytearray()
        
        def write_bytes(self, b: bytes):
            self.data.extend(b)
        
        def write_u8(self, v: int):
            self.data.extend(struct.pack('<Q', v))
        
        def write_u4(self, v: int):
            self.data.extend(struct.pack('<I', v))
        
        def write_u1(self, v: int):
            self.data.extend(struct.pack('<B', v))
        
        def write_string(self, s: str):
            self.write_bytes(serialize_string(s))

    class PakInfo:
        index_encrypted: bool
        index_hash: bytes
        index_offset: int
        index_size: int
        magic: int
        version: int
        
        def __init__(self, buffer: bytes, keystream: list):
            def decrypt_index_encrypted(x: int) -> int:
                return (x ^ keystream[3]) & 0xFF
            
            def decrypt_magic(x: int) -> int:
                return x ^ keystream[2]
            
            def decrypt_index_hash(x: bytes) -> bytes:
                key = struct.pack('<5I', *keystream[4:9])
                return bytes(a ^ b for a, b in zip(x, key))
            
            def decrypt_index_size(x: int) -> int:
                return x ^ ((keystream[10] << 32) | keystream[11])
            
            def decrypt_index_offset(x: int) -> int:
                return x ^ ((keystream[0] << 32) | keystream[1])
            
            reader = Reader_pak(buffer[-PakInfo._mem_size(-1):])
            self.index_encrypted = decrypt_index_encrypted(reader.u1()) == 1
            self.magic = decrypt_magic(reader.u4())
            self.version = reader.u4()
            self.index_hash = decrypt_index_hash(reader.s(20)) if self.version >= 6 else bytes()
            self.index_size = decrypt_index_size(reader.u8())
            self.index_offset = decrypt_index_offset(reader.u8())
            if self.version <= 3:
                self.index_encrypted = False
        
        @staticmethod
        def _mem_size(_) -> int:
            return 45

    class TencentPakInfo(PakInfo):
        unk1: bytes
        packed_key: bytes
        packed_iv: bytes
        packed_index_hash: bytes
        stem_hash: int
        unk2: int
        content_org_hash: bytes
        
        def __init__(self, buffer: bytes, keystream: list):
            def decrypt_unk(x: bytes) -> bytes:
                key = struct.pack('<8I', *keystream[7:15])
                return bytes(a ^ b for a, b in zip(x, key))
            
            def decrypt_stem_hash(x: int) -> int:
                return x ^ keystream[8]
            
            def decrypt_unk_hash(x: int) -> int:
                return x ^ keystream[9]
            
            super().__init__(buffer, keystream)
            footer_size = TencentPakInfo._mem_size(self.version)
            reader = Reader_pak(buffer[-footer_size:])
            self.unk1 = decrypt_unk(reader.s(32)) if self.version >= 7 else bytes()
            self.packed_key = reader.s(256) if self.version >= 8 else bytes()
            self.packed_iv = reader.s(256) if self.version >= 8 else bytes()
            self.packed_index_hash = reader.s(256) if self.version >= 8 else bytes()
            self.stem_hash = decrypt_stem_hash(reader.u4()) if self.version >= 9 else 0
            self.unk2 = decrypt_unk_hash(reader.u4()) if self.version >= 9 else 0
            self.content_org_hash = reader.s(20) if self.version >= 12 else bytes()
        
        @staticmethod
        def _mem_size(version: int) -> int:
            return (PakInfo._mem_size(version) +
                    (32 if version >= 7 else 0) +
                    (768 if version >= 8 else 0) +
                    (8 if version >= 9 else 0) +
                    (20 if version >= 12 else 0))

    class PakCompressedBlock:
        start: int
        end: int
        
        def __init__(self, reader: Reader_pak = None, start: int = 0, end: int = 0):
            if reader is not None:
                self.start = reader.u8()
                self.end = reader.u8()
            else:
                self.start = start
                self.end = end
        
        def write(self, writer: PakIndexWriter):
            writer.write_u8(self.start)
            writer.write_u8(self.end)

    @dataclass
    class TencentPakEntry:
        content_hash: bytes = b'\x00' * 20
        offset: int = 0
        uncompressed_size: int = 0
        compression_method: int = 0
        size: int = 0
        unk1: int = 0
        unk2: bytes = b'\x00' * 20
        compressed_blocks: List[PakCompressedBlock] = None
        compression_block_size: int = 0
        encrypted: bool = False
        encryption_method: int = 0
        unk3: int = 0
        
        def __post_init__(self):
            if self.compressed_blocks is None:
                self.compressed_blocks = []
        
        def __init__(self, reader: Reader_pak, version: int):
            self.content_hash = reader.s(20)
            if version <= 1:
                reader.u8()
            self.offset = reader.u8()
            self.uncompressed_size = reader.u8()
            self.compression_method = reader.u4() & CM_MASK
            self.size = reader.u8()
            self.unk1 = reader.u1() if version >= 5 else 0
            self.unk2 = reader.s(20) if version >= 5 else b'\x00' * 20
            block_count = 0
            if self.compression_method != 0 and version >= 3:
                block_count = reader.u4()
                if block_count > 10000:
                    block_count = 0
                self.compressed_blocks = [PakCompressedBlock(reader) for _ in range(block_count)]
            else:
                self.compressed_blocks = []
            self.compression_block_size = reader.u4() if version >= 4 else 0
            self.encrypted = reader.u1() == 1 if version >= 4 else False
            self.encryption_method = reader.u4() if version >= 12 else 0
            self.unk3 = reader.u4() if version >= 14 else 0
        
        def write(self, writer: PakIndexWriter, version: int):
            writer.write_bytes(self.content_hash)
            if version <= 1:
                writer.write_u8(0)
            writer.write_u8(self.offset)
            writer.write_u8(self.uncompressed_size)
            writer.write_u4(self.compression_method)
            writer.write_u8(self.size)
            if version >= 5:
                writer.write_u1(self.unk1)
                writer.write_bytes(self.unk2)
            if self.compression_method != 0 and version >= 3:
                writer.write_u4(len(self.compressed_blocks))
                for block in self.compressed_blocks:
                    block.write(writer)
            if version >= 4:
                writer.write_u4(self.compression_block_size)
                writer.write_u1(1 if self.encrypted else 0)
            if version >= 12:
                writer.write_u4(self.encryption_method)
            if version >= 14:
                writer.write_u4(self.unk3)

    class PakCrypto:
        
        class _LCG:
            state: int
            
            def __init__(self, seed: int):
                self.state = seed
            
            def next(self) -> int:
                MASK_32 = 0xFFFFFFFF
                MSB_1 = 1 << 31
                
                def wrap(x):
                    x &= MASK_32
                    return x if not (x & MSB_1) else ((x + MSB_1) & MASK_32) - MSB_1
                
                x1 = wrap(0x41C64E6D * self.state)
                self.state = wrap(x1 + 12345)
                x2 = wrap(x1 + 0x13038) if self.state < 0 else self.state
                return ((x2 >> 16) & MASK_32) % 0x7FFF
        
        @staticmethod
        def zuc_keystream() -> list:
            zuc = gmalg.ZUC(ZUC_KEY, ZUC_IV)
            return [struct.unpack('>I', zuc.generate())[0] for _ in range(16)]
        
        @staticmethod
        def _xorxor(buffer: bytes, x: bytes) -> bytes:
            return bytes(buffer[i] ^ x[i % len(x)] for i in range(len(buffer)))
        
        @staticmethod
        def _hashhash(buffer: bytes, n: int) -> bytes:
            result = bytes()
            for _ in range(math.ceil(n / SHA1.digest_size)):
                result += SHA1.new(buffer).digest()
            if len(result) >= n:
                result = result[:n]
            else:
                result += b'\x00' * (n - len(result))
            return result
        
        @staticmethod
        def _meowmeow(buffer: bytes) -> bytes:
            def unpad(x):
                skip = 1 + next(i for i in range(len(x)) if x[i] != 0)
                return x[skip:]
            
            if len(buffer) < 43:
                return bytes()
            x1 = buffer[1:SHA1.digest_size + 1]
            x2 = buffer[SHA1.digest_size + 1:]
            x1 = PakCrypto._xorxor(x1, PakCrypto._hashhash(x2, len(x1)))
            x2 = PakCrypto._xorxor(x2, PakCrypto._hashhash(x1, len(x2)))
            m, part1 = x2[SHA1.digest_size:], x2[:SHA1.digest_size]
            if part1 != SHA1.new(b'\x00' * SHA1.digest_size).digest():
                return bytes()
            return unpad(m)
        
        @staticmethod
        def rsa_extract(signature: bytes, modulus: bytes) -> bytes:
            c = int.from_bytes(signature, 'little')
            n = int.from_bytes(modulus, 'little')
            m = pow(c, 0x10001, n).to_bytes(256, 'little').rstrip(b'\x00')
            return PakCrypto._meowmeow(Misc.pad_to_n(m, 4))
        
        @staticmethod
        def _encrypt_simple1(pt: bytes) -> bytes:
            return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in pt)
        
        @staticmethod
        def _decrypt_simple1(ct: bytes) -> bytes:
            return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in ct)
        
        @staticmethod
        def _encrypt_simple2(pt: bytes) -> bytes:
            class RollingKey:
                _value: int
                def __init__(self, iv: int):
                    self._value = iv
                def update(self, x: int) -> int:
                    orig = self._value
                    self._value = x
                    return orig ^ x
            
            initial_key = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)[0]
            rk = RollingKey(initial_key)
            ciphertext = (struct.pack('<I', rk.update(x)) for x in struct.unpack(f'<{len(pt) // 4}I', pt))
            return bytes(it.chain.from_iterable(ciphertext))
        
        @staticmethod
        def _decrypt_simple2(ct: bytes) -> bytes:
            class RollingKey:
                _value: int
                def __init__(self, iv: int):
                    self._value = iv
                def update(self, x: int) -> int:
                    self._value ^= x
                    return self._value
            
            initial_key = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)[0]
            rk = RollingKey(initial_key)
            plaintext = (struct.pack('<I', rk.update(x)) for x in struct.unpack(f'<{len(ct) // 4}I', ct))
            return bytes(it.chain.from_iterable(plaintext))
        
        @staticmethod
        @lru_cache(maxsize=33)
        def _derive_sm4_key(file_path: PurePath, encryption_method: int) -> bytes:
            part1 = file_path.stem.lower()
            if encryption_method == EM_SM4_2:
                secret = SM4_SECRET_2
            elif encryption_method == EM_SM4_4:
                secret = SM4_SECRET_4
            else:
                index = (encryption_method - EM_SM4_NEW_BASE) % len(SM4_SECRET_NEW)
                secret = f'{SM4_SECRET_NEW[index]}{encryption_method}'
            return SHA1.new(str(part1 + secret).encode()).digest()[:16]
        
        @staticmethod
        @lru_cache(maxsize=33)
        def _sm4_context_for_key(key: bytes) -> SM4:
            return SM4(key)
        
        @staticmethod
        def _encrypt_sm4(plaintext: bytes, file_path: PurePath, encryption_method: int) -> bytes:
            padded = pad(plaintext, 16)
            key = PakCrypto._derive_sm4_key(file_path, encryption_method)
            sm4 = PakCrypto._sm4_context_for_key(key)
            return b''.join(sm4.encrypt(padded[i:i + 16]) for i in range(0, len(padded), 16))
        
        @staticmethod
        def _decrypt_sm4(ciphertext: bytes, file_path: PurePath, encryption_method: int) -> bytes:
            key = PakCrypto._derive_sm4_key(file_path, encryption_method)
            sm4 = PakCrypto._sm4_context_for_key(key)
            return b''.join(sm4.decrypt(ciphertext[i:i + 16]) for i in range(0, len(ciphertext), 16))
        
        @staticmethod
        def decrypt_index(ciphertext: bytes, pak_info: TencentPakInfo) -> bytes:
            if pak_info.version > 7:
                key = PakCrypto.rsa_extract(pak_info.packed_key, RSA_MOD_1)
                iv = PakCrypto.rsa_extract(pak_info.packed_iv, RSA_MOD_1)
                assert len(key) == 32 and len(iv) == 32
                aes = AES.new(key, MODE_CBC, iv[:16])
                return unpad(aes.decrypt(ciphertext), AES.block_size)
            return bytes(PakCrypto._decrypt_simple1(ciphertext))
        
        @staticmethod
        def encrypt_index(plaintext: bytes, pak_info: TencentPakInfo) -> bytes:
            if pak_info.version > 7:
                key = PakCrypto.rsa_extract(pak_info.packed_key, RSA_MOD_1)
                iv = PakCrypto.rsa_extract(pak_info.packed_iv, RSA_MOD_1)
                assert len(key) == 32 and len(iv) == 32
                aes = AES.new(key, MODE_CBC, iv[:16])
                return aes.encrypt(pad(plaintext, AES.block_size))
            return bytes(PakCrypto._encrypt_simple1(plaintext))
        
        @staticmethod
        def _is_simple1_method(m: int) -> bool:
            return m == EM_SIMPLE1
        
        @staticmethod
        def _is_simple2_method(m: int) -> bool:
            return m == EM_SIMPLE2
        
        @staticmethod
        def _is_sm4_method(m: int) -> bool:
            return m == EM_SM4_2 or m == EM_SM4_4 or (m & EM_SM4_NEW_MASK) != 0
        
        @staticmethod
        def _is_unknown_17_method(m: int) -> bool:
            return m == EM_UNKNOWN_17
        
        @staticmethod
        def align_encrypted_content_size(n: int, method: int) -> int:
            if PakCrypto._is_simple2_method(method):
                return Misc.align_up(n, SIMPLE2_BLOCK_SIZE)
            if PakCrypto._is_sm4_method(method):
                return Misc.align_up(n, 16)
            return n
        
        @staticmethod
        def encrypt_block(plaintext: bytes, file: PurePath, method: int) -> bytes:
            if PakCrypto._is_simple1_method(method):
                return PakCrypto._encrypt_simple1(plaintext)
            if PakCrypto._is_simple2_method(method):
                return PakCrypto._encrypt_simple2(pad(plaintext, SIMPLE2_BLOCK_SIZE))
            if PakCrypto._is_sm4_method(method):
                return PakCrypto._encrypt_sm4(plaintext, file, method)
            if PakCrypto._is_unknown_17_method(method):
                return plaintext
            if method == 0:
                return plaintext
            raise AssertionError(f'Unknown encryption method: {method}')
        
        @staticmethod
        def encrypt_block_no_padding(plaintext: bytes, file: PurePath, method: int) -> bytes:
            if PakCrypto._is_simple1_method(method):
                return PakCrypto._encrypt_simple1(plaintext)
            if PakCrypto._is_simple2_method(method):
                assert len(plaintext) % 16 == 0
                return PakCrypto._encrypt_simple2(plaintext)
            if PakCrypto._is_sm4_method(method):
                assert len(plaintext) % 16 == 0
                key = PakCrypto._derive_sm4_key(file, method)
                sm4 = PakCrypto._sm4_context_for_key(key)
                return b''.join(sm4.encrypt(plaintext[i:i + 16]) for i in range(0, len(plaintext), 16))
            if PakCrypto._is_unknown_17_method(method):
                return plaintext
            if method == 0:
                return plaintext
            raise AssertionError(f'Unknown encryption method: {method}')
        
        @staticmethod
        def decrypt_block(ciphertext: bytes, file: PurePath, method: int) -> bytes:
            if PakCrypto._is_simple1_method(method):
                return PakCrypto._decrypt_simple1(ciphertext)
            if PakCrypto._is_simple2_method(method):
                return PakCrypto._decrypt_simple2(ciphertext)
            if PakCrypto._is_sm4_method(method):
                return PakCrypto._decrypt_sm4(ciphertext, file, method)
            if PakCrypto._is_unknown_17_method(method):
                return ciphertext
            if method == 0:
                return ciphertext
            raise AssertionError(f'Unknown encryption method: {method}')
        
        @staticmethod
        @lru_cache(maxsize=33)
        def generate_block_indices(n: int, method: int) -> list:
            if n <= 0: return []
            if not PakCrypto._is_sm4_method(method):
                return list(range(n))
            perm = []
            lcg = PakCrypto._LCG(n)
            while len(perm) != n:
                x = lcg.next() % n
                if x not in perm:
                    perm.append(x)
            inv = [0] * len(perm)
            for i, x in enumerate(perm):
                inv[x] = i
            return inv

    class CompressionFinder:
        ZLIB_LEVELS_TO_TRY = list(range(9, 0, -1))
        ZSTD_LEVELS_TO_TRY = list(range(22, 0, -1)) + list(range(-1, -8, -1))
        
        @staticmethod
        def find_best_level_and_compress(uncompressed_chunk: bytes,
                                         original_compressed_size: int,
                                         dict_data: Optional[bytes],
                                         compression_method: int):
            if compression_method == CM_ZLIB:
                level = 9
            elif compression_method in (CM_ZSTD, CM_ZSTD_DICT):
                level = 22
            else:
                return (None, uncompressed_chunk)
            
            compressed_data = PakCompression.compress_block(
                uncompressed_chunk, dict_data, compression_method, level=level)
            return (level, compressed_data)

    class PakCompression:
        
        @staticmethod
        @lru_cache(maxsize=33)
        def _zstd_decompressor(dict_data: Optional[bytes]) -> ZstdDecompressor:
            dict_obj = ZstdCompressionDict(dict_data, DICT_TYPE_AUTO) if dict_data else None
            return ZstdDecompressor(dict_obj)
        
        @staticmethod
        @lru_cache(maxsize=128)
        def _zstd_compressor(dict_data: Optional[bytes], level: int) -> ZstdCompressor:
            dict_obj = ZstdCompressionDict(dict_data, DICT_TYPE_AUTO) if dict_data else None
            return ZstdCompressor(level=level, dict_data=dict_obj)
        
        @staticmethod
        def decompress_block(block: bytes, dict_data: Optional[bytes], compression_method: int) -> bytes:
            if compression_method == CM_ZLIB:
                return zlib.decompress(block)
            if compression_method == CM_ZSTD or compression_method == CM_ZSTD_DICT:
                if compression_method != CM_ZSTD_DICT:
                    dict_data = None
                return PakCompression._zstd_decompressor(dict_data).decompress(block)
            raise AssertionError(f'Unknown decompression method: {compression_method}')
        
        @staticmethod
        def compress_block(block: bytes, dict_data: Optional[bytes],
                           compression_method: int, level: Optional[int] = None) -> bytes:
            if compression_method == CM_ZLIB:
                use_level = level if level is not None else 9
                return zlib.compress(block, level=use_level)
            if compression_method == CM_ZSTD or compression_method == CM_ZSTD_DICT:
                use_level = level if level is not None else 22
                if compression_method != CM_ZSTD_DICT:
                    dict_data = None
                return PakCompression._zstd_compressor(dict_data, use_level).compress(block)
            raise AssertionError(f'Unknown compression method: {compression_method}')

    SM4_SECRET_2 = '>gahRZFL4r2*TByfx6#X'
    SM4_SECRET_4 = '09ea7a1d9e6528b72b48'

    class TencentPakFile:
        _file_path: PurePath
        _file_content: memoryview
        _is_od: bool
        _mount_point: PurePath
        _is_zstd_with_dict: bool
        _zstd_dict: Optional[bytes]
        _files: list
        _index: dict
        _pak_info: TencentPakInfo
        _raw_mount_point: str
        _index_dirs: list
        
        def __init__(self, file_path: PurePath, is_od: bool = False):
            self._file_path = file_path
            with open(file_path, 'rb') as f:
                self._file_content = memoryview(f.read())
            self._is_od = is_od
            self._mount_point = PurePath()
            self._is_zstd_with_dict = 'zsdic' in str(self._file_path)
            self._zstd_dict = None
            self._files = []
            self._index = {}
            self._pak_info = TencentPakInfo(self._file_content, PakCrypto.zuc_keystream())
            self._verify_stem_hash()
            self._tencent_load_index()
        
        def _verify_stem_hash(self):
            if not self._is_od and self._pak_info.version >= 9:
                expected = zlib.crc32(self._file_path.stem.encode('utf-32le'))
                if self._pak_info.stem_hash != expected:
                    self._fix_stem_hash(expected)
                    self._pak_info.stem_hash = expected
        
        def _fix_stem_hash(self, new_hash: int):
            try:
                footer_size = TencentPakInfo._mem_size(self._pak_info.version)
                footer_start = len(self._file_content) - footer_size
                
                offset = footer_start
                if self._pak_info.version >= 7:
                    offset += 32
                if self._pak_info.version >= 8:
                    offset += 768
                offset += 4
                
                with open(self._file_path, 'r+b') as f:
                    f.seek(offset)
                    f.write(struct.pack('<I', new_hash))
                
                data = bytearray(self._file_content)
                struct.pack_into('<I', data, offset, new_hash)
                self._file_content = memoryview(data)
            except Exception:
                pass
        
        def _tencent_load_index(self):
            index_data = self._file_content[self._pak_info.index_offset:self._pak_info.index_offset + self._pak_info.index_size]
            if self._pak_info.index_encrypted:
                index_data = PakCrypto.decrypt_index(index_data, self._pak_info)
            self._load_index(index_data)
        
        def _load_index(self, index_data: bytes):
            reader = Reader_pak(index_data)
            self._raw_mount_point = reader.string()
            self._mount_point = self._construct_mount_point(self._raw_mount_point)
            num_files_in_pak = reader.u4()
            self._files = [TencentPakEntry(reader, self._pak_info.version) for _ in range(num_files_in_pak)]
            self._index_dirs = []
            
            try:
                num_dirs = reader.u8()
                for _ in range(num_dirs):
                    raw_dir_path = reader.string()
                    num_files = reader.u8()
                    dir_files = []
                    e = {}
                    for _ in range(num_files):
                        raw_file_name = reader.string()
                        file_idx = ~reader.i4()
                        entry = self._files[file_idx]
                        dir_files.append((raw_file_name, file_idx))
                        e[raw_file_name] = entry
                    self._index_dirs.append((raw_dir_path, dir_files))
                    
                    if self._is_zstd_with_dict and PurePath(raw_dir_path).name == 'zstddic':
                        assert len(e) == 1
                        self._construct_zstd_dict(list(e.values())[0])
                    else:
                        self._index[PurePath(raw_dir_path)] = e
            except struct.error:
                pass
        
        @staticmethod
        def _construct_mount_point(mount_point: str) -> PurePath:
            res = PurePath()
            for part in PurePath(mount_point).parts:
                if part != '..':
                    res /= part
            return res
        
        def _peek_content(self, offset: int, size: int, method: int) -> memoryview:
            size = PakCrypto.align_encrypted_content_size(size, method)
            return self._file_content[offset:offset + size]
        
        def _peek_block_content(self, block: PakCompressedBlock, method: int) -> memoryview:
            size = PakCrypto.align_encrypted_content_size(block.end - block.start, method)
            return self._file_content[block.start:block.start + size]
        
        def _construct_zstd_dict(self, dict_entry: TencentPakEntry):
            assert not self._zstd_dict and not dict_entry.encrypted and dict_entry.compression_method == CM_NONE
            reader = Reader_pak(self._peek_content(dict_entry.offset, dict_entry.size, 0))
            dict_size = reader.u8()
            reader.u4()
            assert dict_size == reader.u4()
            dict_data = reader.s(dict_size)
            self._zstd_dict = dict_data
        
        def serialize_index(self) -> bytes:
            writer = PakIndexWriter()
            writer.write_string(self._raw_mount_point)
            writer.write_u4(len(self._files))
            for entry in self._files:
                entry.write(writer, self._pak_info.version)
            writer.write_u8(len(self._index_dirs))
            for raw_dir_path, dir_files in self._index_dirs:
                writer.write_string(raw_dir_path)
                writer.write_u8(len(dir_files))
                for raw_file_name, file_idx in dir_files:
                    writer.write_string(raw_file_name)
                    writer.write_bytes(struct.pack('<i', ~file_idx))
            writer.write_u4(len(self._raw_mount_point.encode('utf-8')) + 1 if self._raw_mount_point else 0)
            return bytes(writer.data)
        
        def serialize_pak_info(self, index_offset: int, index_size: int,
                               index_hash: bytes, keystream: list) -> bytes:
            val_index_encrypted = 1 if self._pak_info.index_encrypted else 0
            enc_index_encrypted = (val_index_encrypted ^ keystream[3]) & 0xFF
            enc_magic = self._pak_info.magic ^ keystream[2]
            val_version = self._pak_info.version
            
            if val_version >= 6:
                key = struct.pack('<5I', *keystream[4:9])
                enc_index_hash = bytes(a ^ b for a, b in zip(index_hash, key))
            else:
                enc_index_hash = b'\x00' * 20
            
            enc_index_size = index_size ^ ((keystream[10] << 32) | keystream[11])
            enc_index_offset = index_offset ^ ((keystream[0] << 32) | keystream[1])
            
            return struct.pack('<BII20sQQ', enc_index_encrypted, enc_magic,
                              val_version, enc_index_hash, enc_index_size, enc_index_offset)
        
        def serialize_tencent_pak_info(self, index_offset: int, index_size: int,
                                        index_hash: bytes, keystream: list) -> bytes:
            data = bytearray()
            
            if self._pak_info.version >= 7:
                key = struct.pack('<8I', *keystream[7:15])
                enc_unk1 = bytes(a ^ b for a, b in zip(self._pak_info.unk1, key))
                data.extend(enc_unk1)
            
            if self._pak_info.version >= 8:
                data.extend(self._pak_info.packed_key)
                data.extend(self._pak_info.packed_iv)
                data.extend(self._pak_info.packed_index_hash)
            
            if self._pak_info.version >= 9:
                enc_stem_hash = (self._pak_info.stem_hash ^ keystream[8]) if hasattr(self._pak_info, 'stem_hash') and self._pak_info.stem_hash is not None else self._pak_info.magic ^ keystream[8]
                data.extend(struct.pack('<I', enc_stem_hash))
                enc_unk2 = self._pak_info.unk2 ^ keystream[9]
                data.extend(struct.pack('<I', enc_unk2))
            
            if self._pak_info.version >= 12:
                data.extend(self._pak_info.content_org_hash)
            
            pak_info_bytes = self.serialize_pak_info(index_offset, index_size, index_hash, keystream)
            data.extend(pak_info_bytes)
            return bytes(data)
        
        def _write_to_disk(self, file_path: Path, entry: TencentPakEntry):
            if PakCrypto._is_unknown_17_method(entry.encryption_method):
                raise Exception('UNKNOWN_17 encryption method')
            
            with open(file_path, 'wb') as f:
                if entry.compression_method == CM_NONE:
                    data = self._peek_content(entry.offset, entry.size, entry.encryption_method)
                    if entry.encrypted:
                        data = PakCrypto.decrypt_block(bytes(data), PurePath(file_path), entry.encryption_method)
                    f.write(data[:entry.size])
                else:
                    dec_data = bytearray()
                    for x in PakCrypto.generate_block_indices(len(entry.compressed_blocks), entry.encryption_method):
                        data = self._peek_block_content(entry.compressed_blocks[x], entry.encryption_method)
                        if entry.encrypted:
                            data = PakCrypto.decrypt_block(bytes(data), PurePath(file_path), entry.encryption_method)
                        if not data:
                            continue
                        data = data[:entry.compressed_blocks[x].end - entry.compressed_blocks[x].start]
                        dec_data.extend(PakCompression.decompress_block(bytes(data), self._zstd_dict, entry.compression_method))
                    f.write(bytes(dec_data)[:entry.uncompressed_size])
        
        def dump_all(self, out_path: Path):
            count = 0
            for dir_path, dir_content in self._index.items():
                for file_name, entry in dir_content.items():
                    if '\x00' in file_name or '\x00' in str(dir_path) or '?' in file_name or '*' in file_name or '..' in str(dir_path):
                        continue
                    target_dir = out_path / dir_path
                    target_dir.mkdir(parents=True, exist_ok=True)
                    target = target_dir / file_name
                    self._write_to_disk(target, entry)
                    count += 1
            
            if count == 0:
                console.print(Panel('[yellow]No files found in this PAK.[/yellow]', title='No Results', style='yellow'))
                return None
            console.print(Panel(f'[green]Extracted {count} file(s) to {out_path}[/green]',
                               title='Unpack Complete', style='green'))
        
        def repack(self, source_dir: Path, target_pak: Path):
            console.print(Panel(f'[bold cyan]INITIALIZING: {target_pak.name}[/bold cyan]',
                               title='Initialization', style='cyan'))
            
            entry_to_path = {}
            for dir_path, dir_content in self._index.items():
                for file_name, entry in dir_content.items():
                    entry_to_path[id(entry)] = (dir_path, file_name)
            
            has_modified_files = False
            for entry in self._files:
                if id(entry) in entry_to_path:
                    dir_path, file_name = entry_to_path[id(entry)]
                    if (source_dir / dir_path / file_name).exists():
                        has_modified_files = True
                        break
            
            if not has_modified_files:
                console.print(Panel('[yellow]NO MODIFIED FILES TO REPACK. PAK REMAINS UNCHANGED.[/yellow]',
                                   title='Repack', style='yellow'))
                return None
            
            temp_fd, temp_path = tempfile.mkstemp(suffix='.pak', dir=target_pak.parent)
            os.close(temp_fd)
            temp_pak = Path(temp_path)
            
            modified_count = 0
            
            with open(target_pak, 'rb') as old_file, open(temp_pak, 'wb') as new_file:
                current_offset = 0
                
                for idx, entry in enumerate(self._files):
                    file_name = 'unknown'
                    dir_path = ''
                    if id(entry) in entry_to_path:
                        dir_path, file_name = entry_to_path[id(entry)]
                    
                    modified_file_path = source_dir / dir_path / file_name
                    
                    if modified_file_path.exists():
                        with open(modified_file_path, 'rb') as f_modified:
                            modified_data = f_modified.read()
                        
                        if len(modified_data) >= 4 and _K is not None:
                            if modified_data[:4] == b'\x1bLua':
                                modified_data = xor_game_crypt(modified_data)
                        
                        block_size = entry.compression_block_size
                        if block_size <= 0:
                            block_size = 65536
                        
                        orig_enc_method = entry.encryption_method
                        orig_comp_method = entry.compression_method
                        if orig_comp_method == 2 and self._zstd_dict is None:
                            orig_comp_method = 1
                            entry.compression_method = 1
                        
                        orig_encrypted = entry.encrypted
                        
                        if orig_comp_method == CM_NONE:
                            chunk = modified_data
                            if orig_encrypted:
                                pad_len = (16 - len(chunk) % 16) % 16
                                if pad_len != 16:
                                    chunk = chunk + b'\x00' * pad_len
                                data_to_write = PakCrypto.encrypt_block_no_padding(chunk, PurePath(file_name), orig_enc_method)
                            else:
                                data_to_write = chunk
                            
                            file_start_offset = current_offset
                            new_file.write(data_to_write)
                            total_written = len(chunk)
                            current_offset += len(data_to_write)
                            
                            entry.offset = file_start_offset
                            entry.uncompressed_size = len(modified_data)
                            entry.size = total_written
                            entry.compressed_blocks = []
                            entry.compression_block_size = 0
                            entry.content_hash = hashlib.sha1(data_to_write).digest()
                            entry.unk2 = hashlib.sha1(modified_data).digest()
                        else:
                            chunks = []
                            uncompressed_offset = 0
                            while uncompressed_offset < len(modified_data):
                                chunk = modified_data[uncompressed_offset:uncompressed_offset + block_size]
                                chunks.append(chunk)
                                uncompressed_offset += block_size
                            
                            n_chunks = len(chunks)
                            if n_chunks == 0:
                                n_chunks = 1
                                chunks = [b'']
                            
                            new_blocks = []
                            file_start_offset = current_offset
                            total_written = 0
                            payload_bytes = bytearray()
                            
                            for chunk_idx, chunk in enumerate(chunks):
                                orig_chunk_size = 0
                                if entry.compressed_blocks and chunk_idx < len(entry.compressed_blocks):
                                    orig_block = entry.compressed_blocks[chunk_idx]
                                    orig_chunk_size = orig_block.end - orig_block.start
                                
                                best_level, compressed_chunk = CompressionFinder.find_best_level_and_compress(
                                    chunk, orig_chunk_size, self._zstd_dict, orig_comp_method)
                                
                                if orig_encrypted:
                                    pad_len = (16 - len(compressed_chunk) % 16) % 16
                                    if pad_len != 16:
                                        compressed_chunk = compressed_chunk + b'\x00' * pad_len
                                    encrypted_chunk = PakCrypto.encrypt_block_no_padding(
                                        compressed_chunk, PurePath(file_name), orig_enc_method)
                                else:
                                    encrypted_chunk = compressed_chunk
                                
                                new_file.write(encrypted_chunk)
                                payload_bytes.extend(encrypted_chunk)
                                
                                block = PakCompressedBlock(Reader_pak(b'\x00' * 16))
                                block.start = current_offset
                                block.end = current_offset + len(compressed_chunk)
                                new_blocks.append(block)
                                
                                current_offset += len(encrypted_chunk)
                                total_written += len(encrypted_chunk)
                            
                            inv = PakCrypto.generate_block_indices(n_chunks, orig_enc_method)
                            reordered_blocks = [None] * n_chunks
                            for i, x in enumerate(inv):
                                reordered_blocks[x] = new_blocks[i]
                            
                            entry.offset = file_start_offset
                            entry.uncompressed_size = len(modified_data)
                            entry.size = total_written
                            entry.compressed_blocks = reordered_blocks
                            entry.compression_block_size = block_size
                            entry.content_hash = hashlib.sha1(payload_bytes).digest()
                            entry.unk2 = hashlib.sha1(modified_data).digest()
                        
                        modified_count += 1
                        console.print(f'[green][OK] REPACKED -> [yellow]{file_name}[/yellow]')
                    else:
                        old_file.seek(entry.offset)
                        
                        if entry.compression_method == CM_NONE:
                            copy_size = PakCrypto.align_encrypted_content_size(entry.size, entry.encryption_method)
                        elif entry.compressed_blocks:
                            last_block = entry.compressed_blocks[-1]
                            copy_size = (last_block.start - entry.offset +
                                        PakCrypto.align_encrypted_content_size(last_block.end - last_block.start, entry.encryption_method))
                        else:
                            copy_size = 0
                        
                        raw_data = old_file.read(copy_size)
                        
                        shift_amount = current_offset - entry.offset
                        entry.offset = current_offset
                        
                        for block in entry.compressed_blocks:
                            block.start += shift_amount
                            block.end += shift_amount
                        
                        new_file.write(raw_data)
                        current_offset += len(raw_data)
                
                index_data = self.serialize_index()
                index_hash = SHA1.new(index_data).digest()
                
                if self._pak_info.version > 7:
                    try:
                        aes_key = PakCrypto.rsa_extract(self._pak_info.packed_key, RSA_MOD_1)
                        aes_iv = PakCrypto.rsa_extract(self._pak_info.packed_iv, RSA_MOD_1)
                        aes_enc = AES.new(aes_key, MODE_CBC, aes_iv[:16])
                        index_data_to_write = aes_enc.encrypt(pad(index_data, AES.block_size))
                        self._pak_info.index_encrypted = True
                    except Exception:
                        index_data_to_write = index_data
                        self._pak_info.index_encrypted = False
                else:
                    index_data_to_write = bytes(PakCrypto._encrypt_simple1(index_data))
                    self._pak_info.index_encrypted = True
                
                new_index_offset = current_offset
                new_file.write(index_data_to_write)
                new_index_size = len(index_data_to_write)
                
                keystream = PakCrypto.zuc_keystream()
                self._pak_info.stem_hash = zlib.crc32(target_pak.stem.encode('utf-32le'))
                self._pak_info.index_hash = index_hash
                footer_data = self.serialize_tencent_pak_info(new_index_offset, new_index_size, index_hash, keystream)
                new_file.write(footer_data)
            
            shutil.move(temp_pak, target_pak)
            console.print(Panel(f'[bold green]Repacked PAK saved to {target_pak}[/bold green]',
                               title='Success', style='green'))

    def display_pak_files() -> List[Path]:
        paks = list(INPUT_FILE.glob('*.pak'))
        if not paks:
            console.print(Panel(f'❌ No PAK files found in {INPUT_FILE} folder', border_style='red'))
            return []
        
        table = Table(title='Select PAK File(s)', box=box.ROUNDED, header_style='bold yellow', show_lines=True)
        table.add_column('No.', style='bold green', width=12, justify='center')
        table.add_column('File Name', style='bold white', width=50)
        table.add_column('Size', style='green', width=12, justify='right')
        
        for i, p in enumerate(paks, 1):
            sz = p.stat().st_size / (1024 * 1024)
            table.add_row(str(i), p.name, f'{sz:.2f} MB')
        
        console.print(table)
        
        while True:
            try:
                choice = Prompt.ask("Select PAK files (comma-separated numbers, 'all' for all, or 0 to cancel)").strip()
                if choice.lower() == 'all':
                    return paks
                if choice == '0':
                    return []
                
                indices = [int(p.strip()) - 1 for p in choice.split(',') if p.strip()]
                selected = [paks[i] for i in indices if 0 <= i < len(paks)]
                if not selected:
                    console.print('[red]Invalid selection. Try again.[/red]')
                    continue
                return selected
            except Exception:
                console.print('[red]Invalid input. Try again.[/red]')

    def repack_pak():
        if not ensure_sm4_secrets():
            console.print('[red]❌ SM4_SECRET_NEW not available. Repack aborted.[/red]')
            input('Press Enter to continue...')
            return None
        
        paks = display_pak_files()
        if not paks:
            input('Press Enter to continue...')
            return None
        
        for pak_path in paks:
            out_pak = REPACKED_PAK_DIR / pak_path.name
            REPACKED_PAK_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy2(pak_path, out_pak)
            console.print(Panel(f'Repacking [bold]{pak_path.name}[/bold] using edited files from [bold]{EDITED_FILES_DIR}[/bold]',
                               title='Repack PAK', style='green'))
            
            try:
                pak = TencentPakFile(PurePath(pak_path))
                
                with tempfile.TemporaryDirectory() as tmpdir:
                    tmp_path = Path(tmpdir)
                    
                    if EDITED_FILES_DIR.exists():
                        edited_files = []
                        for root, _, files in os.walk(EDITED_FILES_DIR):
                            for file in files:
                                edited_files.append(Path(root) / file)
                        
                        for edited_file in edited_files:
                            file_name = edited_file.name
                            local_size = edited_file.stat().st_size
                            rel_path = edited_file.relative_to(EDITED_FILES_DIR).as_posix()
                            
                            exact_path_match = None
                            for dir_path, dir_content in pak._index.items():
                                for index_file_name, entry in dir_content.items():
                                    index_full_path = (dir_path / index_file_name).as_posix()
                                    if index_full_path.lower() == rel_path.lower():
                                        exact_path_match = (index_full_path, entry)
                                        break
                                if exact_path_match:
                                    break
                            
                            if exact_path_match:
                                selected_path, selected_entry = exact_path_match
                            else:
                                matches = []
                                for dir_path, dir_content in pak._index.items():
                                    for index_file_name, entry in dir_content.items():
                                        if index_file_name.lower() == file_name.lower():
                                            index_full_path = (dir_path / index_file_name).as_posix()
                                            matches.append((index_full_path, entry))
                                
                                if not matches:
                                    continue
                                
                                if len(matches) > 1:
                                    matches_sorted = sorted(matches, key=lambda m: abs(m[1].uncompressed_size - local_size))
                                    exact_size_found = False
                                    if (len(matches_sorted) > 0 and
                                        abs(matches_sorted[0][1].uncompressed_size - local_size) == 0 and
                                        (len(matches_sorted) == 1 or
                                         abs(matches_sorted[1][1].uncompressed_size - local_size) > 0)):
                                        selected_path, selected_entry = matches_sorted[0]
                                        exact_size_found = True
                                    else:
                                        exact_size_found = False
                                    
                                    if not exact_size_found:
                                        nearest_matches = matches_sorted[:2]
                                        console.print(Panel(
                                            f'[bold green] SELECT PATH FOR FILE [/bold green]: [bold cyan]{file_name}[/bold cyan]\n'
                                            f'Please select which path:',
                                            title='Path Selector', style='yellow'))
                                        
                                        for i, (path, entry) in enumerate(nearest_matches, 1):
                                            sz = entry.uncompressed_size
                                            console.print(f'  [bold green][{i}][/bold green] {path} (Size: {sz} bytes')
                                        
                                        choices = [str(x) for x in range(1, len(nearest_matches) + 1)]
                                        choice = Prompt.ask(
                                            f'[bold green] SELECT PATH NUMBER FOR [/bold green][bold green]{file_name}[/bold green] in {pak_path.name}',
                                            choices=choices)
                                        selected_path, selected_entry = nearest_matches[int(choice) - 1]
                                else:
                                    selected_path, selected_entry = matches[0]
                            
                            target_full = tmp_path / selected_path
                            target_full.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(edited_file, target_full)
                            console.print(f' [cyan] ✅ DONE-> [/cyan] [green]{file_name}[/green]')
                    
                    pak.repack(tmp_path, out_pak)
                
                console.print(Panel(f'Repacked PAK saved to {out_pak}', title='Success', style='green'))
            except Exception as e:
                console.print(Panel(f'Error: {e}', title='Error', style='red'))
        
        input('Press Enter to continue...')

    def unpack_obb():
        input_dir = ORIGINAL_OBB
        unpacked_dir = UNPACKED_OBB
        
        unpacked_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
            obb_files = [os.path.join(input_dir, f) for f in files if any(f.lower().endswith(ext) for ext in ('.obb', '.zip'))]
        except Exception as e:
            console.print(Panel(f'[red]Error reading {input_dir}: {e}[/red]', title='[red]Error[/red]', border_style='red'))
            return False
        
        if not obb_files:
            console.print(Panel(f'[red]No OBB or ZIP files found in {input_dir}[/red]', title='[red]Error[/red]', border_style='red'))
            return False
        
        success_all = True
        
        for obb_path in obb_files:
            set_permissions(obb_path)
            
            console.print(Panel(f'Unpacking [bold]{os.path.basename(obb_path)}[/bold] to [bold]{unpacked_dir}[/bold]',
                               title='Unpack OBB', style='cyan'))
            
            try:
                with zipfile.ZipFile(obb_path, 'r') as zf:
                    namelist = zf.namelist()
                    total_files = len(namelist)
                    
                    with Progress(SpinnerColumn(), TextColumn('[progress.description]{task.description}'), console=console) as progress:
                        task = progress.add_task(description=f'Extracting {os.path.basename(obb_path)}...', total=total_files)
                        
                        for file_info in zf.infolist():
                            zf.extract(file_info, unpacked_dir)
                            progress.update(task, advance=1, description=f'Extracted: {file_info.filename[:40]}...')
                
                console.print(Panel(f'[green]✅ Successfully extracted {os.path.basename(obb_path)} to {unpacked_dir}[/green]',
                                   title='Success', style='green'))
            except Exception as e:
                console.print(Panel(f'[red]Error extracting {os.path.basename(obb_path)}: {e}[/red]',
                                   title='[red]Error[/red]', border_style='red'))
                success_all = False
        
        pak_path = unpacked_dir / 'ShadowTrackerExtra' / 'Content' / 'Paks'
        if pak_path.exists():
            pak_files = list(pak_path.glob('*.pak'))
            if pak_files:
                console.print(f'[green][OK] Found {len(pak_files)} PAK files at: {pak_path}[/green]')
                for pak_file in pak_files:
                    console.print(f'  - [cyan]{pak_file.name}[/cyan]')
            else:
                console.print(f'[yellow][WARNING] No PAK files found at expected location: {pak_path}[/yellow]')
        else:
            console.print(f'[yellow][WARNING] PAK directory not found at expected location: {pak_path}[/yellow]')
        
        return success_all

    def adjust_size(repacked_obb_path: Path, original_obb_size: int):
        import struct as struct_mod
        
        repacked_obb_size = os.path.getsize(repacked_obb_path)
        
        if repacked_obb_size > original_obb_size:
            raise ValueError(f'Repacked OBB ({repacked_obb_size} bytes) is larger than original OBB ({original_obb_size} bytes).')
        
        if repacked_obb_size == original_obb_size:
            console.print(f'[green][OK] Size already matches: {original_obb_size} bytes.[/green]')
            return None
        
        bytes_to_add = original_obb_size - repacked_obb_size
        
        with open(repacked_obb_path, 'r+b') as f:
            f.seek(0, os.SEEK_END)
            file_len = f.tell()
            seek_len = min(file_len, 1024)
            f.seek(file_len - seek_len, os.SEEK_SET)
            buf = f.read(seek_len)
            
            idx = buf.rfind(b'PK\x05\x06')
            if idx == -1:
                seek_len = min(file_len, 65535)
                f.seek(file_len - seek_len, os.SEEK_SET)
                buf = f.read(seek_len)
                idx = buf.rfind(b'PK\x05\x06')
            
            if idx == -1:
                raise ValueError('Could not find ZIP End of Central Directory (EOCD) signature.')
            
            eocd_pos = file_len - len(buf) + idx
            
            f.seek(eocd_pos, os.SEEK_SET)
            eocd_data = f.read(22)
            sig, disk, disk_cd, disk_entries, total_entries, cd_size, cd_offset, comment_len = struct_mod.unpack('<IHHHHIIH', eocd_data)
            
            new_comment_len = comment_len + bytes_to_add
            if new_comment_len > 65535:
                raise ValueError(f'Required comment padding ({bytes_to_add} bytes) exceeds maximum ZIP comment length (65535). Use dummy file padding first.')
            
            f.seek(eocd_pos + 20, os.SEEK_SET)
            f.write(struct_mod.pack('<H', new_comment_len))
            
            f.seek(0, os.SEEK_END)
            f.write(b'\x00' * bytes_to_add)
        
        console.print(f'[green][OK] Resized to match original size: {original_obb_size} bytes using ZIP comment padding.[/green]')

    def set_permissions(file_path: Path):
        try:
            os.chmod(file_path, 0o755)
        except Exception:
            pass

    def repack_obb():
        input_dir = ORIGINAL_OBB
        repack_obb_dir = REPACKED_OBB
        repack_pak_dir = REPACKED_PAK_DIR
        unpacked_obb_dir = UNPACKED_OBB
        
        try:
            files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
            obb_files = [os.path.join(input_dir, f) for f in files if any(f.lower().endswith(ext) for ext in ('.obb', '.zip'))]
        except Exception as e:
            console.print(Panel(f'[red]Error reading {input_dir}: {e}[/red]', title='[red]Error[/red]', border_style='red'))
            return False
        
        if not obb_files:
            console.print(Panel(f'[red]No OBB/ZIP files found in {input_dir}[/red]', title='[red]Error[/red]', border_style='red'))
            return False
        
        if len(obb_files) == 1:
            original_obb_path = obb_files[0]
        else:
            table = Table(title='Select Original OBB File to Repack', box=box.ROUNDED, header_style='bold yellow', show_lines=True)
            table.add_column('No.', style='bold green', width=12, justify='center')
            table.add_column('File Name', style='bold white', width=50)
            table.add_column('Size', style='green', width=12, justify='right')
            
            for i, p in enumerate(obb_files, 1):
                sz = os.path.getsize(p) / (1024 * 1024)
                table.add_row(str(i), os.path.basename(p), f'{sz:.2f} MB')
            
            console.print(table)
            
            while True:
                try:
                    choice = Prompt.ask('Enter number of OBB file to repack').strip()
                    idx = int(choice) - 1
                    if 0 <= idx < len(obb_files):
                        original_obb_path = obb_files[idx]
                        break
                    console.print('[red]Invalid selection. Try again.[/red]')
                except ValueError:
                    console.print('[red]Invalid input. Try again.[/red]')
        
        original_size = os.path.getsize(original_obb_path)
        obb_filename = os.path.basename(original_obb_path)
        
        pak_files = list(repack_pak_dir.glob('*.pak'))
        if not pak_files:
            console.print(Panel(f'[red]No PAK files found in {repack_pak_dir}[/red]', title='[red]Error[/red]', border_style='red'))
            return False
        
        table = Table(title='Select PAK File to include in OBB', box=box.ROUNDED, header_style='bold yellow', show_lines=True)
        table.add_column('No.', style='bold green', width=12, justify='center')
        table.add_column('File Name', style='bold white', width=50)
        table.add_column('Size', style='green', width=12, justify='right')
        
        for i, p in enumerate(pak_files, 1):
            sz = p.stat().st_size / (1024 * 1024)
            table.add_row(str(i), p.name, f'{sz:.2f} MB')
        
        console.print(table)
        
        while True:
            try:
                choice = Prompt.ask("Select PAK files to include (comma-separated numbers, 'all' for all, or 0 to cancel)").strip()
                if choice.lower() == 'all':
                    selected_paks = pak_files
                    break
                if choice == '0':
                    console.print('[yellow][INFO] Operation cancelled.[/yellow]')
                    return False
                
                selected_indices = [int(x.strip()) for x in choice.split(',')]
                selected_paks = [pak_files[i - 1] for i in selected_indices if 1 <= i <= len(pak_files)]
                if not selected_paks:
                    console.print('[red][ERROR] Invalid selection. Please try again.[/red]')
                    continue
                break
            except (ValueError, IndexError):
                console.print('[red][ERROR] Invalid input. Please enter numbers separated by commas.[/red]')
        
        console.print(f'[green][OK] Selected {len(selected_paks)} PAK files for repacking:[/green]')
        for pak_file in selected_paks:
            console.print(f'  - [cyan]{pak_file.name}[/cyan]')
        
        unpacked_obb_dir.mkdir(parents=True, exist_ok=True)
        repack_obb_dir.mkdir(parents=True, exist_ok=True)
        
        console.print(Panel(f'Extracting original OBB to {unpacked_obb_dir}...', title='Extracting', style='cyan'))
        
        try:
            with zipfile.ZipFile(original_obb_path, 'r') as zf:
                total_files = len(zf.namelist())
                
                with Progress(SpinnerColumn(), TextColumn('[progress.description]{task.description}'), console=console) as progress:
                    task = progress.add_task('Extracting original OBB...', total=total_files)
                    
                    for file_info in zf.infolist():
                        zf.extract(file_info, unpacked_obb_dir)
                        progress.update(task, advance=1, description=f'Extracted: {file_info.filename[:40]}...')
        except Exception as e:
            console.print(Panel(f'[red]Failed to extract original OBB: {e}[/red]', title='Error', style='red'))
            return False
        
        obb_copy_path = unpacked_obb_dir / obb_filename
        shutil.copy2(original_obb_path, obb_copy_path)
        console.print(f'[green][OK] Copied original OBB to {obb_copy_path}[/green]')
        
        pak_dest_dir = unpacked_obb_dir / 'ShadowTrackerExtra' / 'Content' / 'Paks'
        pak_dest_dir.mkdir(parents=True, exist_ok=True)
        
        for pak_src in selected_paks:
            pak_dest = pak_dest_dir / pak_src.name
            shutil.copy2(pak_src, pak_dest)
            console.print(f'[green][OK] Placed updated {pak_src.name} in OBB structure.[/green]')
        
        console.print(Panel('Creating updated OBB with new PAK files...', title='Zipping', style='cyan'))
        
        try:
            with zipfile.ZipFile(original_obb_path, 'r') as orig_zf:
                orig_infos = orig_zf.infolist()
            
            with zipfile.ZipFile(obb_copy_path, 'w', zipfile.ZIP_STORED) as zf:
                for info in orig_infos:
                    file_path = unpacked_obb_dir / info.filename
                    if not file_path.exists():
                        console.print(f'[yellow][WARNING] File {info.filename} from original OBB not found in extracted folder. Skipping.[/yellow]')
                        continue
                    
                    new_info = zipfile.ZipInfo(info.filename)
                    new_info.date_time = info.date_time
                    new_info.compress_type = zipfile.ZIP_STORED
                    new_info.external_attr = info.external_attr
                    
                    with open(file_path, 'rb') as f_in:
                        zf.writestr(new_info, f_in.read())
        except Exception as e:
            console.print(Panel(f'[red]Failed to create updated OBB: {e}[/red]', title='Error', style='red'))
            return False
        
        current_size = os.path.getsize(obb_copy_path)
        if original_size - current_size >= 256:
            dummy_data_len = original_size - current_size - 256
            console.print(f'[cyan][*] Padding OBB with dummy file of size {dummy_data_len} bytes...[/cyan]')
            
            with zipfile.ZipFile(obb_copy_path, 'a', zipfile.ZIP_STORED) as zf:
                zf.writestr('padding.bin', b'\x00' * dummy_data_len)
        
        console.print(f'[green][OK] Created updated OBB with {len(selected_paks)} PAK files preserving original file order & metadata.[/green]')
        
        final_obb_path = repack_obb_dir / obb_filename
        if final_obb_path.exists():
            final_obb_path.unlink()
        shutil.move(obb_copy_path, final_obb_path)
        
        actual_size = os.path.getsize(final_obb_path)
        bytes_to_add = original_size - actual_size
        
        try:
            adjust_size(final_obb_path, original_size)
        except ValueError as e:
            console.print(Panel(f'[red]Size adjustment error: {e}[/red]', title='Error', style='red'))
            return False
        
        console.print(Panel(f'[bold green]Successfully saved updated OBB at:\n{final_obb_path}[/bold green]',
                           title='Repack OBB Success', style='green'))
        return True

    # ============================================================
    # 🔥 MAIN MENU - ONLY 3 OPTIONS
    # ============================================================
    # ============================================================
    # 🔥 MAIN MENU - CLEAN SIMPLE COMMANDS & TERMUX RESPONSIVE UI
    # ============================================================
    import sys
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.box import HEAVY, MINIMAL_DOUBLE_HEAD
    from rich.prompt import Prompt

    console = Console()

    while True:
        console.clear()
        # 👇 YAHAN APKE EXISTING BANNER/PROFILE FUNCTIONS RUN HOGENGE
        print_banner_and_header()
        print_user_profile()

        console.print()
        
        # 🟢 Termux responsive table with simple 1, 2, 3, 0 numbering
        table = Table(
            show_header=True, 
            header_style=f"bold black on {get_banner_color()}", 
            box=HEAVY,
            title= f'[bold {get_banner_color()}]✦ ─── [ ANTE REST CORE ENGINE ] ─── ✦[/bold {get_banner_color()}]', 
            title_style=f"bold {get_banner_color()}",
            show_lines=False, 
            border_style=get_banner_color(),
            expand=True,  # 👈 Poori screen width fit karne ke liye
            padding=(0, 1)
        )
        
        if CURRENT_SESSION_COLOR == 'rainbow':
            table.add_column(rainbow_text('CMD'), width=6, justify='center')
            table.add_column(rainbow_text('OPERATION PROTOCOL'), ratio=2)
            table.add_column(rainbow_text('STATUS / ACTION'), ratio=2)
            rainbow_row(table, '1', 'UNZIP OBB', 'EXTRACT ARCHIVE')
            rainbow_row(table, '2', 'REPACK PAK', 'BUILD EDITED FILES')
            rainbow_row(table, '3', 'REZIP OBB', 'COMPRESS & PACKAGE')
            rainbow_row(table, '0', 'EXIT', 'BACK MENU [✖]')
        else:
            table.add_column('CMD', style='bold bright_yellow', width=6, justify='center')
            table.add_column('OPERATION PROTOCOL', style='bold bright_white', ratio=2)
            table.add_column('STATUS / ACTION', style=get_banner_color(), ratio=2)
            table.add_row('1', 'UNZIP OBB', '[bold cyan]EXTRACT ARCHIVE')
            table.add_row('2', 'REPACK PAK', '[bold cyan]BUILD EDITED FILES')
            table.add_row('3', 'REZIP OBB', '[bold cyan]COMPRESS & PACKAGE')
            table.add_row('0', 'EXIT ', '[bold red]BACK MENU [✖][/bold red]')
        
        # 🛡️ Outer Bright Green Neon Panel Design
        outer_panel = Panel(
            table,
            border_style=get_banner_color(),
            box=MINIMAL_DOUBLE_HEAD,
            title='[bold bright_yellow]SELECT MODULE[/bold bright_yellow]',
            title_align='center',
            padding=(1, 2)
        )
        
        console.print(outer_panel)
        console.print()
        
        # 🎯 Simple Prompt line (1/2/3/0)
        choice = Prompt.ask(
            '[bold {get_banner_color()}]⚡ INPUT COMMAND ➔[/bold {get_banner_color()}]', 
            choices=['0', '1', '2', '3']
        )
        
        if choice == '0':
            console.print(Panel('[bold red]🔴 TERMINATING SESSION... GOODBYE![/bold red]', border_style='red', box=HEAVY))
            return
        elif choice == '1':
            unpack_obb()
            input('\n[bold {get_banner_color()}]Press Enter to return to main terminal...[/bold {get_banner_color()}]')
        elif choice == '2':
            repack_pak()
            input('\n[bold {get_banner_color()}]Press Enter to continue...[/bold {get_banner_color()}]')
        elif choice == '3':
            repack_obb()
            input('\n[bold {get_banner_color()}]Press Enter to continue...[/bold {get_banner_color()}]')







    # ============================================================
    # MAIN MENU
    # ============================================================
    # [YOUR EXISTING MENU CODE HERE - SAME AS BEFORE]

@security_guard
def change_big_banner():
    """
    OPTION 14 — COLOR & BANNER CHANGER

    Screenshot-style flow:
      1 SELECT COLOR
      2 CHANGE BANNER
      3 PAK SCANNING
      0 BACK

    The selected name/color is stored in the existing session globals, so
    the existing banner/header code automatically uses the new values.
    """
    global CURRENT_SESSION_BANNER, CURRENT_SESSION_COLOR

    color_options = [
        ("1",  "🌿 DEFAULT (Original Green)", "bright_green"),
        ("2",  "💙 Bright Blue",              "bright_blue"),
        ("3",  "❤️ Bright Red",               "bright_red"),
        ("4",  "💛 Bright Yellow",            "bright_yellow"),
        ("5",  "🩵 Bright Cyan",              "bright_cyan"),
        ("6",  "💜 Bright Magenta",           "bright_magenta"),
        ("7",  "🔵 Cyan",                     "cyan"),
        ("8",  "🌸 Magenta",                  "magenta"),
        ("9",  "🔷 Blue",                     "blue"),
        ("10", "🔴 Red",                      "red"),
        ("11", "🌈 Rainbow",                  "rainbow"),
    ]
    color_map = {n: c for n, _, c in color_options}

    def show_menu():
        b = get_banner_color()
        table = Table(
            show_header=True,
            box=box.HEAVY,
            border_style=b,
            expand=True,
        )
        table.add_column("OPT", justify="center", width=5)
        table.add_column("COMMAND", width=28)
        table.add_column("DESCRIPTION")

        table.add_row("1", f"[bold {b}]🎨 SELECT COLOR[/]",
                      "Change Tool Theme Color")
        table.add_row("2", f"[bold {b}]📝 CHANGE BANNER[/]",
                      "Change Banner Name")
        table.add_row("3", f"[bold {b}]📦 PAK SCANNING[/]",
                      "Scan PAK/OBB Files")
        table.add_row("0", "[bold red]BACK[/]",
                      "Return to Main Menu")

        console.print(Panel(
            table,
            title=f"[bold {b}]COLOR & BANNER CHANGER[/]",
            border_style=b,
            box=box.HEAVY,
        ))

    while True:
        console.clear()
        print_banner_and_header()
        show_menu()

        b_color = get_banner_color()
        choice = Prompt.ask(
            f"[bold {b_color}]Select option [0/1/2/3][/]",
            choices=["0", "1", "2", "3"],
            default="0",
        )

        if choice == "0":
            return

        # --------------------------------------------------------
        # 1 — SELECT COLOR (exact 10-color screenshot-style page)
        # --------------------------------------------------------
        if choice == "1":
            console.clear()
            print_banner_and_header()
            b = get_banner_color()

            color_table = Table(
                title=f"[bold {b}]🎨 SELECT COLOR THEME (11 COLORS) 🎨[/]",
                show_header=True,
                box=box.HEAVY,
                border_style=b,
                expand=True,
            )
            color_table.add_column("OPT", justify="center", width=6)
            color_table.add_column("COLOR", width=34)
            color_table.add_column("PREVIEW", justify="center", width=18)

            for num, name, color in color_options:
                color_table.add_row(
                    num,
                    f"[bold {color}]{name}[/]",
                    f"[bold {color}]████████████[/]",
                )

            console.print(color_table)

            selected = Prompt.ask(
                f"[bold {b}]Select color option (1-11) "
                f"[1/2/3/4/5/6/7/8/9/10/11][/]",
                choices=[n for n, _, _ in color_options],
                default="1",
            )

            chosen_color = color_map[selected]
            if chosen_color == "rainbow":
                CURRENT_SESSION_COLOR = "rainbow"
                console.print(Text("\n") + rainbow_text("✓ Rainbow Mode Activated!", 0))
            else:
                _stop_rainbow()
                CURRENT_SESSION_COLOR = chosen_color
                console.print(
                    f"\n[bold {CURRENT_SESSION_COLOR}]✓ Theme color changed: "
                    f"{CURRENT_SESSION_COLOR}[/]"
                )
            time.sleep(1.2)
            continue

        # --------------------------------------------------------
        # 2 — CHANGE BANNER
        # --------------------------------------------------------
        if choice == "2":
            console.clear()
            print_banner_and_header()
            b = get_banner_color()

            console.print(Panel(
                f"[bold {b}]📝 CHANGE BANNER NAME[/]\n"
                "[dim]Enter the new banner name.[/]",
                border_style=b,
                box=box.HEAVY,
            ))

            new_name = Prompt.ask(
                f"[bold {b}]Naya Banner Name Type Karo[/]",
                default=CURRENT_SESSION_BANNER,
            ).strip()

            if not new_name:
                console.print("[bold red]❌ Naam empty nahi ho sakta![/]")
                time.sleep(1.5)
                continue

            CURRENT_SESSION_BANNER = " ".join(new_name.split())[:40].upper()

            console.print(
                f"\n[bold {CURRENT_SESSION_COLOR}]✓ Banner Update Ho Gaya:[/]"
            )
            console.print(
                f"[bold {CURRENT_SESSION_COLOR}]Name: "
                f"{CURRENT_SESSION_BANNER}[/]"
            )
            time.sleep(1.5)
            continue

        # --------------------------------------------------------
        # 3 — PAK/OBB SCANNING (read-only)
        # --------------------------------------------------------
        if choice == "3":
            console.clear()
            print_banner_and_header()
            b = get_banner_color()

            roots = [Path.cwd(), Path.home()]
            android_storage = Path("/storage/emulated/0")
            if android_storage.exists():
                roots.append(android_storage)

            found = []
            seen = set()

            for root in roots:
                try:
                    for p in root.rglob("*"):
                        if not p.is_file():
                            continue
                        if p.suffix.lower() not in {".pak", ".obb"}:
                            continue

                        try:
                            resolved = str(p.resolve())
                        except OSError:
                            resolved = str(p)

                        if resolved in seen:
                            continue
                        seen.add(resolved)

                        try:
                            size = p.stat().st_size
                        except OSError:
                            size = 0

                        found.append((p, size))

                        if len(found) >= 200:
                            break
                except (OSError, PermissionError):
                    pass

                if len(found) >= 200:
                    break

            scan = Table(
                title="📦 PAK / OBB SCANNING",
                show_header=True,
                box=box.HEAVY,
                border_style=b,
                expand=True,
            )
            scan.add_column("#", justify="right", width=5)
            scan.add_column("FILE NAME")
            scan.add_column("SIZE", justify="right", width=12)

            def fmt_size(n):
                if n >= 1024**3:
                    return f"{n / 1024**3:.2f} GB"
                if n >= 1024**2:
                    return f"{n / 1024**2:.2f} MB"
                if n >= 1024:
                    return f"{n / 1024:.2f} KB"
                return f"{n} B"

            for i, (path, size) in enumerate(found, 1):
                scan.add_row(str(i), str(path), fmt_size(size))

            if found:
                console.print(scan)
                console.print(
                    f"\n[bold {b}]✓ Found {len(found)} PAK/OBB file(s).[/]"
                )
            else:
                console.print(Panel(
                    "[yellow]No .pak or .obb files found in the scanned "
                    "locations.[/]",
                    border_style=b,
                ))

            Prompt.ask("\nPress Enter to continue", default="")
            continue

def dump_obb_index_to_csv():
    console.clear()
    print_banner_and_header()
    b_color = get_banner_color()
    
    console.print(Panel(f"[bold {b_color}]📊 OBB INDEX CSV DUMPER[/bold {b_color}]\n[dim]Extracting Original OBB Index to CSV format...[/dim]", border_style=b_color))

    base = Path(BASE_DIR_NAME) / "OBB_UNPACKER"
    org_path = base / ORGNAL_DIR
    csv_out_path = base / "CSV_DUMPS"
    os.makedirs(to_long_path(csv_out_path), exist_ok=True)

    pak_files = list_paks_in_folder(org_path)
    if not pak_files:
        console.print(Panel(f"[red]No .pak/.obb files found in {org_path.resolve()}[/red]", title="❗ No PAKs", style="red"))
        Prompt.ask("\nPress Enter to continue", default="")
        return

    console.print(files_available_panel(pak_files, folder_label="Select OBB to Dump CSV"))
    pick = Prompt.ask(f"[bold {b_color}]Select OBB file number[/bold {b_color}]", choices=[str(i) for i in range(1, len(pak_files) + 1)])
    pak_path = pak_files[int(pick) - 1]

    csv_file_name = csv_out_path / f"{pak_path.stem}_index.csv"

    try:
        console.print(f"\n[bold cyan]⏳ Reading Index from {pak_path.name}...[/bold cyan]")
        pak = TencentPakFile(pak_path)
        with open(to_long_path(csv_file_name), 'w', encoding='utf-8') as f:
            f.write("File_Path,Offset,Size,Uncompressed_Size,Encryption_Method\n")
            total_files = 0
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), console=console) as progress:
                task = progress.add_task("[cyan]Writing to CSV...", total=len(pak._index))
                for dir_path, files in pak._index.items():
                    for name, entry in files.items():
                        if entry is not None:
                            full_path = str(dir_path / name).replace("\\", "/")
                            f.write(f"{full_path},{entry.offset},{entry.size},{entry.uncompressed_size},{entry.encryption_method}\n")
                            total_files += 1
                    progress.advance(task)

        console.print("\n")
        console.print(Panel(f"[bold green]✅ SUCCESS! Index Dumped Successfully![/bold green]\n"
                            f"[white]Total Files Logged:[/white] [cyan]{total_files}[/cyan]\n"
                            f"[white]CSV Saved at:[/white] [yellow]{csv_file_name.resolve()}[/yellow]", border_style="green"))

    except Exception as e:
        console.print(Panel(f"[red]Failed to dump CSV: {e}[/red]"))

    Prompt.ask("\nPress Enter to return to menu", default="")

# ==================================================
# 🔥 BLACK TOOL (UE4 String Editor) - Integrated 🔥
# ==================================================
BLACK_TOOL_BASE_DIR_NAME = os.path.join("𝐊𝐀𝐙𝐔𝐊𝐈_𝐓𝐎𝐎𝐋", "CREDIT_TOOL")
BLACK_TOOL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), BLACK_TOOL_BASE_DIR_NAME)
WORK_DIR_BLACK = os.path.join(BLACK_TOOL_DIR, "ORGNAL")
MODIFIED_DIR_BLACK = os.path.join(BLACK_TOOL_DIR, "MODDED FILE")

def black_tool_ensure_work_dir():
    for d in [BLACK_TOOL_DIR, WORK_DIR_BLACK, MODIFIED_DIR_BLACK]:
        if not os.path.exists(d):
            try:
                os.makedirs(d)
                print(f"{to_fancy('INFO')}: Created directory {d}")
            except Exception as e:
                console.print(f"[red]Cannot create directory {d}: {e}[/red]")
                sys.exit()

def black_tool_list_files_in_dir(extensions=('.uasset', '.uexp')):
    try:
        if not os.path.exists(WORK_DIR_BLACK):
            black_tool_ensure_work_dir()
        all_files = os.listdir(WORK_DIR_BLACK)
        target_files = [f for f in all_files if f.lower().endswith(extensions)]
        target_files.sort()
        return target_files
    except Exception as e:
        console.print(f"[red]Error reading directory: {e}[/red]")
        return []

class UE4StringTool:
    def __init__(self):
        self.MIN_STRING_LEN = 2
        self.MAX_STRING_LEN = 8000

    def read_int(self, f):
        data = f.read(4)
        if len(data) < 4: return None
        return struct.unpack('<i', data)[0]

    def is_garbage_text(self, text):
        if not text or len(text.strip()) == 0: return True
        allowed_control = {'\n', '\r', '\t'}
        for char in text:
            code = ord(char)
            if code == 0: return True
            if code < 32 and char not in allowed_control: return True
            if char == '\ufffd': return True
        return False

    def is_valid_string_start(self, f, current_pos):
        f.seek(current_pos)
        length = self.read_int(f)
        if length is None: return False
        if length == 0: return False
        if not (self.MIN_STRING_LEN <= abs(length) <= self.MAX_STRING_LEN): return False
        try:
            if length < 0:
                read_len = -length * 2
                data = f.read(read_len)
                if len(data) != read_len: return False
                if data[-2:] != b'\x00\x00': return False
                text = data[:-2].decode('utf-16le')
            else:
                read_len = length
                data = f.read(read_len)
                if len(data) != read_len: return False
                if data[-1:] != b'\x00': return False
                text = data[:-1].decode('utf-8')
            if self.is_garbage_text(text): return False
            return True
        except:
            return False

    def extract_file(self, file_name):
        file_path = os.path.join(WORK_DIR_BLACK, file_name)
        if not os.path.exists(file_path):
            return False, f"File not found: {file_name}"
        json_path = file_path + ".json"
        console.print(f"\n[bold yellow]{to_fancy('Create JSON')}: {file_name}[/bold yellow]")
        try:
            with open(file_path, 'rb') as f:
                f.seek(0, 2)
                file_size = f.tell()
                f.seek(0)
                entries = []
                cursor = 0
                with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), console=console) as progress:
                    task = progress.add_task("[cyan]Extracting strings...", total=file_size)
                    while cursor < file_size - 4:
                        progress.update(task, completed=cursor)
                        if self.is_valid_string_start(f, cursor):
                            f.seek(cursor)
                            length = self.read_int(f)
                            is_utf16 = length < 0
                            abs_len = abs(length)
                            if is_utf16:
                                raw_data = f.read(abs_len * 2)
                                text = raw_data[:-2].decode('utf-16le')
                                total_size = 4 + (abs_len * 2)
                            else:
                                raw_data = f.read(abs_len)
                                text = raw_data[:-1].decode('utf-8')
                                total_size = 4 + abs_len
                            entries.append({
                                "offset": cursor,
                                "original_len_int": length,
                                "text": text
                            })
                            cursor += total_size
                        else:
                            cursor += 1
                if not entries:
                    return False, "No valid text strings found."
                with open(json_path, 'w', encoding='utf-8') as jf:
                    json.dump(entries, jf, indent=4, ensure_ascii=False)
            return True, f"Exported {len(entries)} strings -> {os.path.basename(json_path)}"
        except Exception as e:
            return False, str(e)

    def repack_file(self, file_name):
        original_file_path = os.path.join(WORK_DIR_BLACK, file_name)
        json_path = original_file_path + ".json"
        
        if not os.path.exists(original_file_path):
            return False, f"Missing original file: {file_name}"
        if not os.path.exists(json_path):
            return False, f"Missing file: {file_name}.json"

        modified_file_path = os.path.join(MODIFIED_DIR_BLACK, file_name)
        console.print(f"[bold yellow]{to_fancy('Repacking')}: {file_name}...[/bold yellow]")

        try:
            with open(json_path, 'r', encoding='utf-8') as jf:
                entries = json.load(jf)
            entries.sort(key=lambda x: x['offset'])

            with open(original_file_path, 'rb') as f_orig, open(modified_file_path, 'wb') as f_out:
                cursor_orig = 0
                count_modified = 0
                for i, entry in enumerate(entries):
                    gap_size = entry['offset'] - cursor_orig
                    if gap_size > 0:
                        f_out.write(f_orig.read(gap_size))
                    elif gap_size < 0:
                        f_orig.seek(entry['offset'])

                    new_text = entry['text']
                    old_len_int = entry['original_len_int']
                    is_utf16 = old_len_int < 0
                    if is_utf16: max_byte_size = abs(old_len_int) * 2
                    else: max_byte_size = abs(old_len_int)

                    f_orig.seek(entry['offset'] + 4)
                    old_raw_display = f_orig.read(max_byte_size)
                    try:
                        if is_utf16: old_text_display = old_raw_display[:-2].decode('utf-16le')
                        else: old_text_display = old_raw_display[:-1].decode('utf-8')
                    except: old_text_display = "<Decode error>"
                    
                    if new_text != old_text_display:
                        count_modified += 1

                    if is_utf16: new_bytes = new_text.encode('utf-16le') + b'\x00\x00'
                    else: new_bytes = new_text.encode('utf-8') + b'\x00'
                    current_byte_size = len(new_bytes)

                    if current_byte_size > max_byte_size:
                        console.print(f"\n[bold red]❌ CRITICAL ERROR AT LINE {i+1} (Offset: {entry['offset']})[/bold red]")
                        console.print(f"[bold red]   [!] New string is longer than original string ({current_byte_size} > {max_byte_size} bytes)[/bold red]")
                        f_out.close(); f_orig.close()
                        if os.path.exists(modified_file_path): os.remove(modified_file_path)
                        return False, "New string length exceeds original string length."

                    f_out.write(struct.pack('<i', old_len_int))
                    f_out.write(new_bytes)

                    pad_len = max_byte_size - current_byte_size
                    if pad_len > 0:
                        f_out.write(b'\x00' * pad_len)

                    f_orig.seek(entry['offset'])
                    len_check = self.read_int(f_orig)
                    skip_len = 4 + (abs(len_check) * 2 if len_check < 0 else abs(len_check))
                    f_orig.seek(entry['offset'] + skip_len)
                    cursor_orig = f_orig.tell()

                f_out.write(f_orig.read())

            return True, f"Updated {count_modified} lines -> {os.path.basename(modified_file_path)} (in MODDED FILE folder)"
        except Exception as e:
            return False, str(e)

def black_tool_do_unpack_fancy(tool):
    console.clear()
    print_banner_and_header()
    print_user_profile()
    b_color = get_banner_color()
    console.print(Panel(f"[bold {b_color}]{to_fancy('MASTER UNPACK (ALL FILES)')}[/bold {b_color}]\n"
                        f"[dim]Extracting all UEXP/UASSET files to JSON at once...[/dim]", border_style=b_color))
    
    files = black_tool_list_files_in_dir(('.uasset', '.uexp'))
    if not files:
        console.print(Panel(f"[red]{to_fancy('No files found to unpack!')}[/red]", border_style="red"))
        Prompt.ask(f"\n[bold white]{to_fancy('Press Enter to continue...')}[/bold white]", default="")
        return

    unpacked_count = 0
    console.print(f"\n[bold cyan]⏳ Auto-Unpacking all files...[/bold cyan]")
    for fname in files:
        success, msg = tool.extract_file(fname)
        if success:
            console.print(f"[bold green]✔ {to_fancy('SUCCESS')}:[/bold green] {to_fancy(fname)}")
            unpacked_count += 1
        else:
            console.print(f"[bold red]❌ {to_fancy('FAILED')}:[/bold red] {to_fancy(fname)}\n   [dim]{msg}[/dim]")

    console.print("\n")
    if unpacked_count > 0:
        console.print(Panel(f"[bold green]✅ {to_fancy('ALL DONE')}! {unpacked_count} {to_fancy('files unpacked successfully.')}[/bold green]\n[white]JSON files created in ORGNAL folder.[/white]", border_style="green"))
    else:
        console.print(Panel(f"[yellow]⚠️ {to_fancy('No files were unpacked.')}[/yellow]", border_style="yellow"))
    Prompt.ask("\n[bold white]Press Enter to continue...[/bold white]", default="")

def black_tool_do_repack_fancy(tool):
    console.clear()
    print_banner_and_header()
    print_user_profile()
    b_color = get_banner_color()
    console.print(Panel(f"[bold {b_color}]{to_fancy('MASTER REPACK (ALL FILES)')}[/bold {b_color}]\n"
                        f"[dim]Converting all JSON back to UEXP at once...[/dim]", border_style=b_color))
    
    files = black_tool_list_files_in_dir(('.uasset', '.uexp'))
    if not files:
        console.print(Panel(f"[red]{to_fancy('No files found to repack!')}[/red]", border_style="red"))
        Prompt.ask(f"\n[bold white]{to_fancy('Press Enter to continue...')}[/bold white]", default="")
        return

    repacked_count = 0
    repacked_files_list = [] 
    
    console.print(f"\n[bold cyan]⏳ Auto-Repacking all files...[/bold cyan]")
    for fname in files:
        json_path = os.path.join(WORK_DIR_BLACK, fname + ".json")
        if os.path.exists(json_path):
            success, msg = tool.repack_file(fname)
            if success:
                console.print(f"[bold green]✔ {to_fancy('SUCCESS')}:[/bold green] {to_fancy(fname)}")
                repacked_count += 1
                repacked_files_list.append(fname)
            else:
                console.print(f"[bold red]❌ {to_fancy('FAILED')}:[/bold red] {to_fancy(fname)}\n   [dim]{msg}[/dim]")
        else:
            console.print(f"[dim yellow]⚠️ Skipped (No JSON found): {to_fancy(fname)}[/dim yellow]")

    console.print("\n")
    if repacked_count > 0:
        console.print(Panel(f"[bold green]✅ {to_fancy('ALL DONE')}! {repacked_count} {to_fancy('files repacked successfully.')}[/bold green]\n[white]Files are in MODDED FILE folder.[/white]", border_style="green"))
        
        copy_choice = Prompt.ask(f"\n[bold yellow]❓ KYA AAP INHE 'Modified_files' AUR 'MOD_REPACK' MEIN OPEN COPY KARNA CHAHTE HAI?[/bold yellow] (y/n)", default="y")
        
        if copy_choice.lower() == 'y':
            target_modified = Path(BASE_DIR_NAME) / "OBB_UNPACKER" / "Modified_files"
            target_enc_open = ANLAISH_DIR / "MOD_REPACK"
            
            os.makedirs(to_long_path(target_modified), exist_ok=True)
            os.makedirs(to_long_path(target_enc_open), exist_ok=True)
            
            copied_mod = 0
            copied_enc = 0
            
            for fname in repacked_files_list:
                src = os.path.join(MODIFIED_DIR_BLACK, fname)
                if os.path.exists(src):
                    shutil.copy2(src, os.path.join(target_modified, fname))
                    copied_mod += 1
                    shutil.copy2(src, os.path.join(target_enc_open, fname))
                    copied_enc += 1
            
            if copied_mod > 0:
                console.print(f"\n[bold {get_banner_color()}]🚀 BOOM! {copied_mod} files copied to 'Modified_files'![/bold {get_banner_color()}]")
            if copied_enc > 0:
                console.print(f"[bold cyan]💎 {copied_enc} Credit files copied OPEN in 'MOD_REPACK'![/bold cyan]")
            if copied_mod == 0 and copied_enc == 0:
                console.print(f"[bold red]❌ Error: File copy nahi ho payi.[/bold red]")
    else:
        console.print(Panel(f"[yellow]⚠️ {to_fancy('No files were repacked.')}[/yellow]", border_style="yellow"))
        
    Prompt.ask("\n[bold white]Press Enter to continue...[/bold white]", default="")

TARGET_GROUPS = {
    "1. MATCH START & THEME": ["Match starts in <MatchStartInfo>{0}</>", "Match starts in", "Your match starts in", "Bonus Challenge match starts", "LEAN (BGMI 2026 Theme Song)"],
    "2. CHICKEN DINNER": ["WINNER WINNER CHICKEN DINNER!", "WINNER WINNER CHICKEN DINNER", "Winner Winner Chicken Dinner", "Winner winner chicken dinner"],