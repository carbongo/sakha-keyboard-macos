# Installer

`install.sh` does three jobs: the curl one-liner, the release zip's `.command` files (`--gui` uses osascript dialogs), and local dev installs.

| Step | How |
|---|---|
| Find bundle | `Sakha.bundle` next to the script (clone or zip); otherwise download `releases/latest/download/Sakha-Keyboard.zip` (or `-v TAG`) |
| Install | copy to `~/Library/Keyboard Layouts`, strip quarantine |
| No logout | `TISRegisterInputSource(bundleURL)` through JXA (`osascript -l JavaScript`), only if macOS doesn't list our layouts yet: re-registering duplicates them. |
| Enable | Writes `{InputSourceKind, KeyboardLayout ID, KeyboardLayout Name}` into `com.apple.HIToolbox` `AppleEnabledInputSources`, which takes effect at once. `TISEnableInputSource` returns noErr but does nothing for user layouts on macOS 27. |
| ID type | `KeyboardLayout ID` must be `<integer>` (`NSNumber numberWithInt`); a JS number saves as `<real>`, macOS stops matching it and lists the layout again on every install. Prefs treat int == real, so repairing old reals needs `removeObjectForKey` first. |
| Caches | `touch` the layouts folder so macOS rescans it. Clear only System Settings' copy (`…/C/com.apple.Keyboard-Settings.extension/com.apple.IntlDataCache.le*`), which otherwise shows stale icons. **Never delete the main `…/C/com.apple.IntlDataCache.le*`**: it gets rebuilt without user layouts until the next login. |
| Verify | `tis register` returns how many Sakha layouts are live; it retries up to 5×, then asks for a logout |
| Uninstall | Remove those pref entries by layout ID, delete the bundle |

- Prompts read `/dev/tty`, so they work under `curl | bash`. Default (`-y`, blank answer, no tty): `DEFAULT_LAYOUT` = Sakha (Windows) only.
- Must stay bash 3.2-compatible (`/bin/bash` on macOS).
