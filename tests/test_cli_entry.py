import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(*args):
    return subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True, timeout=60)


def test_python_m_core_defaults_to_status():
    r = _run("-m", "core")
    assert r.returncode == 0, r.stderr
    assert "'version': '0.3.2'" in r.stdout


def test_research_without_seed_says_how_to_seed():
    r = _run("run.py", "research")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip(), "research printed nothing"
