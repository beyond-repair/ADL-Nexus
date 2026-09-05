#!/usr/bin/env python3
"""ADL Nexus Core v0.1 — local-first entrypoint."""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

# Ensure package root is importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from layer0_governance.registry import register_subsystem, evaluate_request, list_subsystems, get_audit_log
from layer1_memory.store import MemoryStore
from layer2_agent_runtime.runtime import AgentRuntime

def build_coding_agent() -> AgentRuntime:
    agent = AgentRuntime("coding-agent")

    def list_files(goal: str, context: dict):
        path = Path(context.get("path", "."))
        return [str(p) for p in path.rglob("*") if p.is_file()][:50]

    def summarize(goal: str, context: dict):
        files = list_files(goal, context)
        return {"file_count": len(files), "sample": files[:10]}

    def echo(goal: str, context: dict):
        return {"goal": goal, "context_keys": list(context.keys())}

    agent.register_tool("list_files", list_files)
    agent.register_tool("summarize", summarize)
    agent.register_tool("echo", echo)
    return agent

def main():
    parser = argparse.ArgumentParser(description="ADL Nexus Core v0.1")
    parser.add_argument("command", choices=["status", "register", "run", "audit", "memory"], help="Core command")
    parser.add_argument("--goal", default="analyze repository", help="Goal for the coding agent")
    parser.add_argument("--path", default=".", help="Path for repository analysis")
    args = parser.parse_args()

    # Bootstrap governance
    register_subsystem("nexus-core", layer=0, claim_level=2, capabilities=["status", "run", "audit", "memory"])
    register_subsystem("coding-agent", layer=2, claim_level=2, capabilities=["list_files", "summarize", "echo"])

    mem = MemoryStore()
    agent = build_coding_agent()

    if args.command == "status":
        decision = evaluate_request("nexus-core", "status")
        print("Governance:", decision)
        print("Registered subsystems:", list(list_subsystems().keys()))
        print("Memory keys:", mem.keys())

    elif args.command == "register":
        print("Subsystems:", list_subsystems())

    elif args.command == "run":
        decision = evaluate_request("coding-agent", "list_files")
        if not decision.allowed:
            print("DENIED:", decision.reason)
            return 1
        result = agent.execute(args.goal, {"path": args.path})
        print("Result:", result)
        mem.put("last_run", {"goal": args.goal, "success": result.success})

    elif args.command == "audit":
        for entry in get_audit_log()[-10:]:
            print(entry)

    elif args.command == "memory":
        print("Keys:", mem.keys())
        for k in mem.keys():
            print(f"  {k}: {mem.get(k)}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
