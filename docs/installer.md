# Installer

`install.sh` does three jobs: the curl one-liner, the release zip's `.command` files (`--gui` uses osascript dialogs), and local dev installs.

| Step | How |
|---|---|
| Find bundle | `Sakha.bundle` next to the script (clone or zip); otherwise download `releases/latest/download/Sakha-Keyboard.zip` (or `-v TAG`) |
| Install | copy to `~/Library/Keyboard Layouts`, strip quarantine |
| No logout | `TISRegisterInputSource(bundleURL)` through JXA (`osascript -l JavaScript`). Needs nothing beyond stock macOS. |
| Enable | Writes `{InputSourceKind, KeyboardLayout ID, KeyboardLayout Name}` into `com.apple.HIToolbox` `AppleEnabledInputSources`, which takes effect at once. `TISEnableInputSource` returns noErr but does nothing for user layouts on macOS 27. |
| Uninstall | Remove those pref entries by layout ID, delete the bundle |

- Prompts read `/dev/tty`, so they work under `curl | bash`. With no tty, every layout is enabled.
- Must stay bash 3.2-compatible (`/bin/bash` on macOS).
