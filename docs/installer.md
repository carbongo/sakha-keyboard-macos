# Installer

`install.sh` does three jobs: the curl one-liner, the release zip's `.command` files (`--gui` uses osascript dialogs), and local dev installs.

| Step | How |
|---|---|
| Find bundle | `Sakha.bundle` next to the script (clone or zip); otherwise download `releases/latest/download/Sakha-Keyboard.zip` (or `-v TAG`) |
| Install | copy to `~/Library/Keyboard Layouts`, strip quarantine |
| Enable (macOS 27+) | Write `{InputSourceKind, KeyboardLayout ID, KeyboardLayout Name}` into `com.apple.inputsources` `AppleEnabledThirdPartyInputSources` and strip our IDs from HIToolbox `AppleEnabledInputSources`: macOS enables a layout once per list it is in. No register call. The input menu reads the lists only at login (no pref write, `TISEnableInputSource`, notification or agent restart refreshes it), so the installer asks for a logout. |
| Enable (≤ 26) | `TISRegisterInputSource(bundleURL)` through JXA (`osascript -l JavaScript`), only if macOS doesn't list our layouts yet (re-registering duplicates them), then the same entry into HIToolbox `AppleEnabledInputSources`, which takes effect at once. |
| ID type | `KeyboardLayout ID` must be `<integer>` (`NSNumber numberWithInt`); a JS number saves as `<real>`. Prefs treat int == real, so repairing old reals needs `removeObjectForKey` first. |
| Caches | `touch` the layouts folder so macOS rescans it. Clear only System Settings' copy (`…/C/com.apple.Keyboard-Settings.extension/com.apple.IntlDataCache.le*`), which otherwise shows stale icons. **Never delete the main `…/C/com.apple.IntlDataCache.le*`**: it gets rebuilt without user layouts until the next login. |
| Verify | `tis register` returns how many Sakha layouts macOS reports enabled; it retries up to 5×, then asks for a logout |
| Uninstall | Remove our layout IDs from the enabled lists, delete the bundle |

- Prompts read `/dev/tty`, so they work under `curl | bash`. Default (`-y`, blank answer, no tty): `DEFAULT_LAYOUT` = Sakha (Windows) only.
- Must stay bash 3.2-compatible (`/bin/bash` on macOS).
- With no Sakha-language layout left in HIToolbox, macOS 27 enables Apple's own Sakha (`Yakut`) at login.
