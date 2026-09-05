# Adapters

Claim-capped bridges between ADL Nexus and upstream subsystems.

Design rules:
1. Never hard-require the upstream package at import time of Core.
2. Detect availability at runtime.
3. Fall back to local stubs with explicit status.
4. Keep claim level honest in manifests.

Current adapters:
- `sunder` → Layer 2 Agent Runtime
- `cleanroom` → Layer 1 Memory Kernel
