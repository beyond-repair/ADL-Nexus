# ADL Nexus — Interactive Clients

Two surfaces for talking to the Digital Workforce:

| Client | Path | Target |
|--------|------|--------|
| **Nexus Party** (primary) | `godot_nexus_party/` | Godot 4 → **Android APK** + desktop |
| **Pixel Chat Web** (prototype) | `web_pixel_chat/` | Browser / PWA-style local demo |

## Design

- **ChatGPT-like conversation** with the party
- **Final Fantasy–inspired pixel party strip** (portraits + status)
- Agents are **interactive** and can **address each other**
- Backed by Nexus roles (Engineer, Researcher, Writer, Analyst, Tester, Operator, Manager)

## APK build (Godot 4.3+)

1. Install [Godot 4.3+](https://godotengine.org/download)
2. Open `client/godot_nexus_party/project.godot`
3. **Editor → Manage Export Templates** → download templates for your Godot version
4. Install Android SDK / JDK; configure **Editor Settings → Export → Android**
5. **Project → Export → Android** → use preset `Android` in `export_presets.cfg`
6. Export APK or AAB

See `godot_nexus_party/EXPORT_ANDROID.md`.

## Claim status

- UI + multi-agent dialogue bus: **implemented in project sources**
- Live bridge to Python `core.nexus`: **stub / local scripted agents** in v0.3 client
- Production signed Play Store release: **not claimed**
