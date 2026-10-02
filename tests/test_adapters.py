from adapters.sunder.bridge import SunderAdapter
from adapters.cleanroom.bridge import CleanRoomAdapter

_FAKE_UPSTREAM = ("snap", "sunder", "spike", "anchor")


def test_sunder_adapter_distinguishes_unavailable_from_live():
    a = SunderAdapter()
    out = a.run_goal("test goal")
    assert out["adapter"] == "sunder"
    assert "claim" in out
    assert "live path reserved" not in repr(out)
    scan = out["scan"]
    assert scan["mode"] != "live" or scan.get("executed") is True
    if a.status.mode == "unavailable":
        assert a.status.available is False
        assert "unavailable" in a.status.message
        assert scan["mode"] == "unavailable"
        assert scan["executed"] is False
    elif a.status.mode == "detected":
        assert a.status.available is False
        assert scan["mode"] == "detected"
        assert scan["executed"] is False
        assert scan.get("note") == "detected-not-executed"
    elif a.status.mode == "live":
        assert scan["executed"] is True
        assert scan["mode"] == "live"
    else:
        raise AssertionError(f"unexpected sunder mode {a.status.mode}")
    caps = a.capabilities()
    for name in _FAKE_UPSTREAM:
        assert name not in caps
    assert "scan" in caps and "run_goal" in caps


def test_cleanroom_missing_engine_is_unavailable_not_engine_result():
    a = CleanRoomAdapter()
    info = a.info()
    assert info["adapter"] == "cleanroom"
    if a.status.mode == "unavailable":
        assert a.status.available is False
        assert "unavailable" in a.status.message
        put = a.put("k", "v")
        assert put["engine"] is False
        assert put["source"] == "local-stub"
        got = a.get("k")
        assert got["source"] == "local-stub"
        assert got["engine"] is False
        assert got["value"] == "v"
        assert "external engine" in info["claim"] or "stub" in info["claim"]
    elif a.status.mode == "live":
        assert a.status.available is True
        got = a.get("missing-key-not-local")
        assert got["source"] == "engine"
        assert got["engine"] is True
    else:
        raise AssertionError(f"unexpected clean-room mode {a.status.mode}")
