# ADL Nexus Party — Playtest / RC note

**Client:** `client/godot_nexus_party` (primary interactive party-chat)  
**Branch:** `fix/nexus-party-playtest-pass`  
**Status:** **COMPLETE — PLAYTEST VERIFIED** (desktop hand play 2026-10-09 ~12:34–12:40 AM ET)

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

## Hand playtest (2026-10-09 ~12:34–12:40 AM ET) — PASS

**Method:** Godot 4.7.2 windowed on `DISPLAY=:1`, driven with real XTEST mouse/keyboard. Overall: **hand play PASS**.

| # | Check | Result |
|---|-------|--------|
| 1 | 7 party slots: Cid, Vivi, Garnet, Quina, Steiner, Freya, Zidane | **PASS** |
| 2 | `@engineer fix tests` → Cid reply + status updates | **PASS** (portrait pulse not visually confirmed in captures — brief/unverified, non-blocking) |
| 3 | `party debate SPARC residual` → full chain Zidane→Vivi→Quina→Steiner→Cid→Garnet→Zidane | **PASS** |
| 4 | `refactor the apk` → Zidane route → Cid → Steiner challenge | **PASS** |
| 5 | Input lock: DOUBLESEND_TEST/LOCKTEST while thinking never posted; no double-send | **PASS** |
| 6 | No script errors/crashes; ALSA dummy audio only (benign) | **PASS** |

## Remaining open

- Optional: portrait pulse visibility polish (pulse brief/unverified in captures — non-blocking)
- Android export APK not exercised this pass (templates/SDK not required for party chat RC)
- **BLACKSITE** remains blocked waiting on human hand clear — out of scope this run
- Optional web_pixel_chat parity polish (mention comma edge — not blocking Godot RC)

## Not done / not claimed

- Live Python Nexus bridge
- Network multiplayer
- Feature bloat beyond scripted party loops
