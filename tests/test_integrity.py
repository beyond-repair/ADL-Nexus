from pathlib import Path
from layer5_security.integrity import file_hash, tree_hash, verify_anchor

def test_file_hash_deterministic(tmp_path: Path):
    f = tmp_path / "a.txt"
    f.write_text("hello nexus")
    h1 = file_hash(f)
    h2 = file_hash(f)
    assert h1 == h2
    assert len(h1) == 64

def test_tree_hash_stable(tmp_path: Path):
    (tmp_path / "x.py").write_text("print(1)")
    (tmp_path / "y.md").write_text("# y")
    h1 = tree_hash(tmp_path, patterns=[".py", ".md"])
    h2 = tree_hash(tmp_path, patterns=[".py", ".md"])
    assert h1 == h2

def test_verify_anchor(tmp_path: Path):
    f = tmp_path / "b.txt"
    f.write_text("anchor-me")
    digest = file_hash(f)
    r = verify_anchor(f, digest)
    assert r["ok"] is True
    r2 = verify_anchor(f, "0" * 64)
    assert r2["ok"] is False
