#!/usr/bin/env python3
"""ADL Nexus Core v0.2 — Architecture Complete entrypoint."""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from layer0_governance.registry import register_subsystem, evaluate_request, list_subsystems, get_audit_log
from layer1_memory.store import MemoryStore
from layer2_agent_runtime.runtime import AgentRuntime
from layer5_security.gate import SecurityGate
from layer3_workforce.roles import list_roles, get_role
from layer7_research.registry import seed_cft_baseline, list_experiments, register_experiment

def build_coding_agent() -> AgentRuntime:
    agent = AgentRuntime("coding-agent")

    def list_files(goal: str, context: dict):
        path = Path(context.get("path", "."))
        return [str(p.relative_to(path)) for p in path.rglob("*") if p.is_file()][:80]

    def summarize(goal: str, context: dict):
        files = list_files(goal, context)
        by_ext: dict[str, int] = {}
        for f in files:
            ext = Path(f).suffix or "[none]"
            by_ext[ext] = by_ext.get(ext, 0) + 1
        return {"file_count": len(files), "by_extension": by_ext, "sample": files[:12]}

    def echo(goal: str, context: dict):
        return {"goal": goal, "context_keys": list(context.keys())}

    agent.register_tool("list_files", list_files)
    agent.register_tool("summarize", summarize)
    agent.register_tool("echo", echo)
    return agent

def bootstrap():
    register_subsystem("nexus-core", layer=0, claim_level=2, capabilities=["status", "run", "audit", "memory", "registry", "roles", "research"])
    register_subsystem("coding-agent", layer=2, claim_level=2, capabilities=["list_files", "summarize", "echo"])
    register_subsystem("security-gate", layer=5, claim_level=2, capabilities=["evaluate"])
    register_subsystem("research-fabric", layer=7, claim_level=2, capabilities=["register", "list"])
    seed_cft_baseline()

def main():
    parser = argparse.ArgumentParser(description="ADL Nexus Core v0.2 — Architecture Complete")
    parser.add_argument("command", choices=["status", "register", "run", "audit", "memory", "registry", "roles", "research"], help="Core command")
    parser.add_argument("--goal", default="analyze repository", help="Goal for the coding agent")
    parser.add_argument("--path", default=".", help="Path for repository analysis")
    args = parser.parse_args()

    bootstrap()
    mem = MemoryStore()
    agent = build_coding_agent()
    security = SecurityGate(min_trust=0.5)

    if args.command == "status":
        d = evaluate_request("nexus-core", "status")
        s = security.evaluate("nexus-core", "status")
        print("Governance:", d)
        print("Security:", s)
        print("Subsystems:", list(list_subsystems().keys()))
        print("Workforce roles:", list_roles())
        print("Memory keys:", mem.keys())
        print("Research experiments:", len(list_experiments()))

    elif args.command == "register":
        print(list_subsystems())

    elif args.command == "run":
        g = evaluate_request("coding-agent", "list_files")
        s = security.evaluate("coding-agent", "list_files")
        if not g.allowed or not s.allowed:
            print("DENIED — Governance:", g.reason, "| Security:", s.reason)
            return 1
        result = agent.execute(args.goal, {"path": args.path})
        print("Result:", result)
        mem.put("last_run", {"goal": args.goal, "success": result.success, "security_audit": s.audit_id})

    elif args.command == "audit":
        print("=== Governance Audit (last 15) ===")
        for entry in get_audit_log()[-15:]:
            print(entry)
        print("\n=== Security Log ===")
        for entry in security.get_log():
            print(entry)

    elif args.command == "memory":
        print("Keys:", mem.keys())
        for k in mem.keys():
            print(f"  {k}: {mem.get(k)}")

    elif args.command == "registry":
        for name, entry in list_subsystems().items():
            print(f"{name}: layer={entry['layer']} claim={entry['claim_level']} caps={entry['capabilities']}")

    elif args.command == "roles":
        for r in list_roles():
            role = get_role(r)
            print(f"{role.name}: {role.capabilities} (claim {role.claim_level})")

    elif args.command == "research":
        for exp in list_experiments():
            print(f"[{exp['status']}] {exp['id']} — {exp['title']} (claim {exp['claim_level']})")
            print(f"    Hypothesis: {exp['hypothesis']}")
            print(f"    Source: {exp['source_repo']}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
