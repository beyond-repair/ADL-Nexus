# ADL Nexus Party — Playtest / RC note

**Client:** `client/godot_nexus_party` (primary interactive party-chat)  
**Branch:** `fix/nexus-party-playtest-pass`  
**Status:** **IN PROGRESS** — headless import + Main load + automated smoke verified; **desktop hand play** still required for COMPLETE — PLAYTEST VERIFIED.

## Identity (preserve)

- Local-first **scripted** multi-agent chat (no live Python bridge claimed)
- FF-style party strip + @mention / party debate / manager-route
- Claim-capped; offline agents

## Fixes in this pass

1. **@mention parsing** — exact `@id`, `@id rest`, and `@id, rest` (comma no longer left in the prompt)
2. **PartyBar.setup** — immediate `remove_child` + `free` (no deferred `queue_free` stack on re-setup); `class_name PartyBar`
3. **Main status + input lock** — status updates on ready / thinking / agent spoke; Send disabled while the bus runs a turn
4. **AgentBus.reply_delay** — default 0.35s; smoke sets `0.0` for speed
5. **`.gitignore`** — ignore `**/.godot/` and local Android/export build dirs
6. **Smoke** — `scripts/smoke_party.gd` covers mention, debate speakers, route (engineer/researcher), PartyBar slots

## Verification performed (automated / headless)

| Check | Result |
|-------|--------|
| Godot **4.7.2** `--import` | PASS |
| Main scene `--quit-after 3` headless | PASS (no script errors) |
| `smoke_party.gd` mention / debate / route / PartyBar | **PASS** (`SMOKE_PARTY PASS`, exit 0) |
| `web_pixel_chat` static HTTP serve (index/app/agents/styles) | PASS (prototype parity; not primary) |

Godot binary used: `/home/box/godot/Godot_v4.7.2-stable_linux.x86_64`

### Re-run smoke

```bash
cd client/godot_nexus_party
godot --headless --path . --script res://scripts/smoke_party.gd
```

## Hand playtest checklist (parent / desktop)

Required for **COMPLETE — PLAYTEST VERIFIED**:

1. Open project in Godot 4.3+ (4.7.2 OK) → Run Main
2. See party strip with 7 agents (Cid, Vivi, Garnet, Quina, Steiner, Freya, Zidane)
3. Send `@engineer fix tests` → Cid replies + portrait pulses; status updates
4. Send `party debate SPARC residual` → full debate chain + system line
5. Send a plain message (e.g. `refactor the apk`) → Zidane routes then specialist; optional Steiner challenge
6. Confirm input does not double-send while party is thinking
7. Optional: open `client/web_pixel_chat` via `python -m http.server` and note parity (prototype only)

## Remaining open

- Desktop/windowed **hand play** of the primary loop (this environment has no interactive desktop)
- Optional web_pixel_chat parity polish (mention comma edge — not blocking Godot RC)
- Android export APK not exercised this pass (templates/SDK not required for party chat RC)
- **BLACKSITE** remains blocked waiting on human hand clear — out of scope this run

## Not done / not claimed

- Live Python Nexus bridge
- Network multiplayer
- Feature bloat beyond scripted party loops
