from pathlib import Path
import sys, tempfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app" / "src" / "main" / "python"))
import smart_engine

def test_detect_and_analyze():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"sample.lua"
        p.write_bytes(b"-- ALVSIA\nreturn 1\n")
        r=smart_engine.analyze(p)
        assert r["type"]=="LUA"
        assert r["sha256"] and r["size"]>0

def test_lua_protect_roundtrip_container():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"sample.lua"; p.write_bytes(b"return 123\n")
        r=smart_engine.lua_protect(p,Path(td)/"out")
        q=Path(r["output"])
        assert q.is_file()
        assert q.read_bytes().startswith(b"ALVSLUA2")
        assert r["output_sha256"]==smart_engine.sha256(q)
