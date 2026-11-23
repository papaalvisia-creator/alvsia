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

def test_source_inventory_is_fused():
    r=smart_engine.source_inventory()
    assert "IkramTool_V130_4.7.zip" in r["sources"]
    assert "TOOL.zip" in r["sources"]
    assert "RegulerResault_ALVSIA_tool_no_on_vip_engine.zip" in r["sources"]

def test_t24_backend_loaded():
    r=smart_engine.run(__file__,"self_test")
    assert r["checks"]["alvsia_t24_engine"] is True
    assert r["checks"]["alvsia_engine"] is True
