#!/usr/bin/env python3
"""ADL Nexus Core. User-facing version is core.version (pyproject 0.3.2)."""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Path bootstrap only. Not a governance dispatcher. ensure_paths appends
# sibling roots; it does not put them at sys.path[0]. Clean-room discovery
# does not import core.clean_room_vsa.
try:
    from scripts.bootstrap_path import ensure_paths
    ensure_paths(verbose=False)
except ImportError:
    pass

from core.version import __version__
from core.kernel import get_kernel
from layer0_governance.registry import list_subsystems, get_audit_log
from layer2_agent_runtime.runtime import AgentRuntime
from layer3_workforce.roles import list_roles, get_role
from layer7_research.registry import list_experiments


def build_coding_agent() -> AgentRuntime:
    """Same runtime the kernel pathway uses. No second tool implementation."""
    return AgentRuntime("coding-agent")


def main():
    parser = argparse.ArgumentParser(description=f"ADL Nexus Core v{__version__}")
    parser.add_argument("command",
                        choices=["status", "register", "run", "audit", "memory", "registry",
                                 "roles", "research", "adapters", "metrics", "integrity",
                                 "packages", "call", "layers"],
                        help="Core command")
    parser.add_argument("--goal", default="analyze repository", help="Goal for the coding agent")
    parser.add_argument("--path", default=".", help="Path for repository analysis / integrity")
    parser.add_argument("--pathway", default="", help="Pathway name for `call` (e.g. development)")
    parser.add_argument("--action", default="info", help="Action name for `call`")
    parser.add_argument("--arg", action="append", default=[], help="Positional arg for `call` (repeatable)")
    parser.add_argument("--kw", action="append", default=[], help="key=value for `call` (repeatable)")
    parser.add_argument(
        "--seed", action="store_true",
        help="With research: seed the CFT lab baseline (not product bootstrap)",
    )
    args = parser.parse_args()

    # Bootstrap exception: NexusKernel.bootstrap() registers subsystems.
    # Mutating commands (run, integrity) go through NexusKernel.call only.
    k = get_kernel()

    if args.command == "status":
        print(k.status())

    elif args.command == "register":
        print(list_subsystems())

    elif args.command == "run":
        executed = k.call("runtime", "execute", args.goal, {"path": args.path})
        if not executed.ok:
            print("DENIED —", executed.reason)
            return 1
        if not getattr(executed.result, "success", False):
            print("DENIED —", getattr(executed.result, "message", executed.result))
            return 1
        print("Result:", executed.result)
        sunder_out = k.call("sunder", "run_goal", args.goal, {"path": args.path})
        if not sunder_out.ok:
            print("DENIED — sunder:", sunder_out.reason)
            return 1
        print("Sunder path:", sunder_out.result)
        mem_out = k.call(
            "memory", "put", "last_run",
            {"goal": args.goal, "success": True},
        )
        if not mem_out.ok:
            print("DENIED — memory:", mem_out.reason)
            return 1
        cr_out = k.call("cleanroom", "put", "last_goal", args.goal)
        if not cr_out.ok:
            print("DENIED — cleanroom:", cr_out.reason)
            return 1

    elif args.command == "audit":
        print("=== Governance Audit (last 15) ===")
        for entry in get_audit_log()[-15:]:
            print(entry)
        print("\n=== Security Log ===")
        for entry in k.security.get_log():
            print(entry)
        print("\n=== Policy Snapshot ===")
        print(k.security.policy_snapshot())

    elif args.command == "memory":
        print("Local MemoryStore keys:", k.memory.keys())
        for key in k.memory.keys():
            print(f"  {key}: {k.memory.get(key)}")
        print("\nClean-room adapter:", k.cleanroom.info())

    elif args.command == "registry":
        for name, entry in list_subsystems().items():
            print(f"{name}: layer={entry['layer']} claim={entry['claim_level']} caps={entry['capabilities']}")

    elif args.command == "roles":
        for r in list_roles():
            role = get_role(r)
            print(f"{role.name}: {role.capabilities} (claim {role.claim_level})")

    elif args.command == "research":
        if args.seed:
            seeded = k.call("research", "seed")
            if not seeded.ok:
                print("DENIED —", seeded.reason)
                return 1
        for exp in list_experiments():
            print(f"\n[{exp['status']}] {exp['id']} — {exp['title']} (claim {exp['claim_level']})")
            print(f"  Hypothesis: {exp['hypothesis']}")
            print(f"  Source: {exp['source_repo']}")
            for ev in exp.get("evidence", []):
                print(f"    · ({ev['kind']}) {ev['content'][:110]} [source: {ev['source']}]")

    elif args.command == "adapters":
        print("Sunder:", k.sunder.status)
        print("  capabilities:", k.sunder.capabilities())
        print("Clean-room:", k.cleanroom.status)
        print("  info:", k.cleanroom.info())

    elif args.command == "metrics":
        print(k.metrics())

    elif args.command == "packages":
        from core.pathways import probe_packages, list_pathways
        print("Pathways:", ", ".join(list_pathways()))
        rows = probe_packages()
        ok = 0
        for row in rows:
            mark = "OK" if row["import_ok"] else "FAIL"
            if row["import_ok"]:
                ok += 1
            extra = "" if row["import_ok"] else f"  {row['error']}"
            print(f"  [{mark}] L{row['layer']} {row['pathway']:12} {row['module']}{extra}")
        print(f"{ok}/{len(rows)} packages importable")
        return 0 if ok == len(rows) else 1

    elif args.command == "layers":
        from core.pathways import list_pathways, describe
        for name in list_pathways():
            d = describe(name)
            print(f"L{d['layer']} {name:12} -> {d['module']}  actions={d['actions']}")

    elif args.command == "call":
        if not args.pathway:
            print("usage: nexus call --pathway development --action analyze --kw path=.")
            return 2
        kwargs = {}
        for item in args.kw:
            if "=" not in item:
                print("bad --kw, expected key=value:", item)
                return 2
            key, _, value = item.partition("=")
            kwargs[key] = value
        result = k.call(args.pathway, args.action, *args.arg, **kwargs)
        print({"ok": result.ok, "allowed": result.allowed, "pathway": result.pathway,
               "action": result.action, "reason": result.reason, "result": result.result})
        return 0 if result.ok else 1

    elif args.command == "integrity":
        target = Path(args.path)
        if target.is_file():
            hashed = k.call("integrity", "file_hash", str(target))
            kind = "file"
        else:
            hashed = k.call(
                "integrity", "tree_hash", str(target),
                [".py", ".md", ".yaml", ".yml", ".toml"],
            )
            kind = "tree"
        if not hashed.ok:
            print("DENIED:", hashed.reason)
            return 1
        print({"type": kind, "path": str(target), "sha256": hashed.result})
        stored = k.call(
            "memory", "put", "last_integrity",
            {"path": str(target), "sha256": hashed.result},
        )
        if not stored.ok:
            print("DENIED — memory:", stored.reason)
            return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
