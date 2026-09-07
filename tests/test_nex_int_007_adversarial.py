"""NEX-INT-007 adversarial tests A–F + boundary checks."""
from __future__ import annotations
import sys, tempfile, threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapters.workforce.contract import WorkRequest, WorkResult, WorkStatus
from adapters.workforce.adapter import InProcessWorkforceAdapter
from persistence import DurableExecutionStore, ExecutionState
from governed_workforce import GovernedWorkforce


def _gw(tmp: str):
    adapter = InProcessWorkforceAdapter()
    store = DurableExecutionStore(Path(tmp) / "exec.jsonl")
    return GovernedWorkforce(adapter, store=store), adapter


def test_A_duplicate_callback_after_completed():
    with tempfile.TemporaryDirectory() as tmp:
        gw, adapter = _gw(tmp)
        req = WorkRequest("adv-a", "dup callback")
        r1 = gw.submit(req)
        assert r1.status is WorkStatus.COMPLETED
        gw.complete_callback(WorkResult("adv-a", WorkStatus.COMPLETED, output={"hacked": True}))
        rec = gw.store.get("adv-a")
        assert rec.state is ExecutionState.COMPLETED
        assert rec.result != {"hacked": True}


def test_B_late_callback_after_recovery():
    with tempfile.TemporaryDirectory() as tmp:
        gw, adapter = _gw(tmp)
        store = gw.store
        store.begin("adv-b", "g1", "s1")
        store.mark_running("adv-b")
        recovered = gw.recover()
        assert any(r.request_id == "adv-b" and r.state is ExecutionState.INDETERMINATE for r in recovered)
        gw.complete_callback(WorkResult("adv-b", WorkStatus.COMPLETED, output={"late": True}))
        rec = store.get("adv-b")
        assert rec.state is ExecutionState.INDETERMINATE
        assert rec.result != {"late": True}


def test_C_callback_recovery_race():
    with tempfile.TemporaryDirectory() as tmp:
        gw, adapter = _gw(tmp)
        store = gw.store
        store.begin("adv-c", "g1", "s1")
        store.mark_running("adv-c")

        def do_callback():
            gw.complete_callback(WorkResult("adv-c", WorkStatus.COMPLETED, output={"from": "cb"}))
        def do_recover():
            gw.recover()

        t1 = threading.Thread(target=do_callback)
        t2 = threading.Thread(target=do_recover)
        t1.start(); t2.start()
        t1.join(); t2.join()
        rec = store.get("adv-c")
        assert rec.state in {
            ExecutionState.COMPLETED, ExecutionState.INDETERMINATE, ExecutionState.FAILED
        }
        assert rec.state is not ExecutionState.RUNNING


def test_D_concurrent_duplicate_request_id():
    with tempfile.TemporaryDirectory() as tmp:
        gw, adapter = _gw(tmp)
        req = WorkRequest("adv-d", "concurrent")
        def submit():
            gw.submit(req)
        threads = [threading.Thread(target=submit) for _ in range(8)]
        for t in threads: t.start()
        for t in threads: t.join()
        assert adapter.invocation_count("adv-d") == 1
        assert gw.store.get("adv-d") is not None


def test_E_submit_after_terminal_observation_only():
    with tempfile.TemporaryDirectory() as tmp:
        gw, adapter = _gw(tmp)
        req = WorkRequest("adv-e", "once")
        r1 = gw.submit(req)
        assert r1.status is WorkStatus.COMPLETED
        count_after_first = adapter.invocation_count("adv-e")
        r2 = gw.submit(req)
        assert r2.status is WorkStatus.COMPLETED
        assert adapter.invocation_count("adv-e") == count_after_first


def test_F_submit_after_indeterminate_no_redrive():
    with tempfile.TemporaryDirectory() as tmp:
        gw, adapter = _gw(tmp)
        store = gw.store
        store.begin("adv-f", "g1", "s1")
        store.mark_running("adv-f")
        gw.recover()
        assert store.get("adv-f").state is ExecutionState.INDETERMINATE
        before = adapter.invocation_count("adv-f")
        r = gw.submit(WorkRequest("adv-f", "retry?"))
        assert adapter.invocation_count("adv-f") == before
        assert r.status is WorkStatus.FAILED


def test_boundary_no_agent_task_imports():
    import ast
    for rel in ["governed_workforce.py", "adapters/workforce/adapter.py", "persistence/store.py"]:
        tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = []
                if isinstance(node, ast.Import):
                    names = [a.name for a in node.names]
                else:
                    names = [node.module or ""] + [a.name for a in node.names]
                blob = " ".join(names)
                assert "Agent" not in blob and "Orchestrator" not in blob
                assert "digital_double.core" not in blob
