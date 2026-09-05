from adapters.sunder.bridge import SunderAdapter
from adapters.cleanroom.bridge import CleanRoomAdapter

def test_sunder_adapter_stub_mode():
    a = SunderAdapter()
    assert a.status.mode in ("live", "stub")
    out = a.run_goal("test goal")
    assert out["adapter"] == "sunder"
    assert "claim" in out

def test_cleanroom_adapter_stub_mode():
    a = CleanRoomAdapter()
    assert a.status.mode in ("live", "stub")
    a.put("k", "v")
    assert a.get("k") == "v"
    info = a.info()
    assert info["adapter"] == "cleanroom"
