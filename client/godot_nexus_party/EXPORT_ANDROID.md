# Export ADL Nexus Party to Android APK

## Prerequisites

- Godot **4.3 or 4.4** (same major as export templates)
- JDK 17+
- Android SDK (API 34+ recommended)
- Accept Android licenses; set paths in Godot **Editor Settings → Export → Android**
  - `adb`, `jarsigner` / `apksigner`, debug keystore optional for debug APK

## Steps

1. Open this folder as a Godot project (`project.godot`).
2. **Editor → Manage Export Templates** → Install matching templates.
3. **Project → Export**
4. Add preset **Android** if missing (template provided in `export_presets.cfg`).
5. Package / unique name: `labs.atomicdream.nexusparty`
6. **Export Project** → `NexusParty-debug.apk`

## Permissions (minimal)

- Internet: **disabled by default** (local-first)
- Storage: only if you later enable log export

## Connecting to Python Nexus Core later

Use a local HTTP or stdio bridge from a companion service on the device/emulator.
Current build uses **in-engine scripted agents** so the APK runs offline with zero server.
