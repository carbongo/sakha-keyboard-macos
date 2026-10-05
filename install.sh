#!/usr/bin/env bash
# Sakha keyboard layouts for macOS — installer / uninstaller.
#
#   curl -fsSL https://raw.githubusercontent.com/carbongo/sakha-keyboard-macos/main/install.sh | bash
#
# No logout needed: the bundle is registered with the Text Input Sources API right away.
set -euo pipefail

REPO="carbongo/sakha-keyboard-macos"
DEST="$HOME/Library/Keyboard Layouts"
BUNDLE="Sakha.bundle"
OLD_BUNDLES=("Sakha (Yakut).bundle")  # v1 — replaced by v2
DEFAULT_LAYOUT="sakha-windows"  # what -y, a blank answer and non-interactive installs enable

# key | keylayout ID (build.py) | menu name | description
LAYOUTS=(
  "sakha-windows|-19001|Sakha (Windows)|Windows-style: Sakha letters on the number row"
  "sakha-russian|-19002|Sakha (Russian)|Plain Russian, Sakha letters on Opt"
  "sakha-latin|-19003|Sakha (Latin)|Common Turkic Latin alphabet"
  "sakha-novgorodov|-19004|Sakha (Novgorodov)|1920s Novgorodov alphabet"
)

usage() {
  cat <<EOF
Sakha keyboard layouts for macOS

Usage: install.sh [options]

  -y, --yes             Don't ask; enable Sakha (Windows) only
  -l, --layouts LIST    Comma-separated layouts to enable:
                        sakha-windows, sakha-russian, sakha-latin, sakha-novgorodov, all
      --no-enable       Install only; add layouts yourself in System Settings
  -v, --version TAG     Install a specific release (default: latest)
  -u, --uninstall       Remove the layouts
      --gui             Ask with macOS dialogs instead of the terminal
  -h, --help            Show this help

Examples:
  curl -fsSL https://raw.githubusercontent.com/$REPO/main/install.sh | bash
  curl -fsSL https://raw.githubusercontent.com/$REPO/main/install.sh | bash -s -- -l sakha-windows,sakha-latin
EOF
}

# ── output ──────────────────────────────────────────────────────────────
if [[ -t 1 ]]; then B=$'\e[1m' D=$'\e[2m' G=$'\e[32m' Y=$'\e[33m' R=$'\e[31m' C=$'\e[36m' N=$'\e[0m'; else B='' D='' G='' Y='' R='' C='' N=''; fi
say()  { printf '%s\n' "$*"; }
step() { printf '%s==>%s %s%s%s\n' "$C" "$N" "$B" "$*" "$N"; }
ok()   { printf '%s ✓%s %s\n' "$G" "$N" "$*"; }
warn() { printf '%s !%s %s\n' "$Y" "$N" "$*" >&2; }
die()  { printf '%s ✗%s %s\n' "$R" "$N" "$*" >&2; [[ $GUI == 1 ]] && dialog "$*" stop; exit 1; }

dialog() {  # message [icon]
  osascript -e "display dialog \"$1\" with title \"Sakha Keyboard\" buttons {\"OK\"} default button 1 with icon ${2:-note}" >/dev/null 2>&1 || true
}

# Ask yes/no; default yes. Reads the terminal even under `curl | bash`.
confirm() {
  if [[ $YES == 1 ]]; then return 0; fi
  if [[ $GUI == 1 ]]; then
    osascript -e "button returned of (display dialog \"$1\" with title \"Sakha Keyboard\" buttons {\"No\", \"Yes\"} default button 2)" 2>/dev/null | grep -q Yes
    return
  fi
  if [[ -r /dev/tty ]]; then
    local reply; printf '%s?%s %s %s[Y/n]%s ' "$Y" "$N" "$1" "$D" "$N" >/dev/tty; read -r reply </dev/tty || reply=
    [[ ! $reply =~ ^[Nn] ]]
  fi
}

# ── layout selection ────────────────────────────────────────────────────
field() { local IFS='|'; read -r -a f <<<"$1"; printf '%s' "${f[$2]}"; }

choose_layouts() {  # prints selected keys, one per line
  if [[ -n $SELECTED ]]; then
    [[ $SELECTED == all ]] && SELECTED=$(for l in "${LAYOUTS[@]}"; do field "$l" 0; printf ','; done)
    tr ',' '\n' <<<"$SELECTED" | sed '/^$/d'
    return
  fi
  if [[ $YES == 1 || ! -r /dev/tty && $GUI == 0 ]]; then echo "$DEFAULT_LAYOUT"; return; fi
  if [[ $GUI == 1 ]]; then
    local items="" first="" l
    for l in "${LAYOUTS[@]}"; do
      items+="\"$(field "$l" 2) — $(field "$l" 3)\","
      [[ $(field "$l" 0) == "$DEFAULT_LAYOUT" ]] && first="\"$(field "$l" 2) — $(field "$l" 3)\""
    done
    local picked
    picked=$(osascript -e "choose from list {${items%,}} with title \"Sakha Keyboard\" with prompt \"Which layouts should be added to your input menu? (⌘-click to pick several)\" default items {$first} with multiple selections allowed" 2>/dev/null) || true
    [[ -z $picked || $picked == false ]] && return
    for l in "${LAYOUTS[@]}"; do [[ $picked == *"$(field "$l" 2)"* ]] && { field "$l" 0; echo; }; done
    return
  fi
  {
    say ""; say "${B}Which layouts should be added to your input menu?${N}"
    local i=1 l
    for l in "${LAYOUTS[@]}"; do printf '  %s%d%s  %-20s %s%s%s\n' "$B" $i "$N" "$(field "$l" 2)" "$D" "$(field "$l" 3)" "$N"; i=$((i + 1)); done
    printf '%s?%s Numbers separated by spaces, or all %s[1]%s ' "$Y" "$N" "$D" "$N"
  } >/dev/tty
  local reply n; read -r reply </dev/tty || reply=
  [[ -z $reply ]] && reply=1
  [[ $reply == all ]] && reply="1 2 3 4"
  for n in ${reply//,/ }; do
    [[ $n =~ ^[1-4]$ ]] && { field "${LAYOUTS[$((n - 1))]}" 0; echo; }
  done
}

# ── Text Input Sources (JavaScript for Automation, ships with macOS) ────
tis() {  # register <bundle> [id|name ...]  |  remove [id|name ...]
  # TISEnableInputSource silently ignores user-installed layouts (macOS 27), so this edits the
  # AppleEnabledInputSources pref the input menu reads; it picks the change up immediately.
  local js="$TMP/tis.js"
  cat >"$js" <<'EOF'
ObjC.import('Carbon');
function run(argv) {
  const action = argv.shift();
  if (action === 'register') $.TISRegisterInputSource($.NSURL.fileURLWithPath(argv.shift()));
  const wanted = argv.map(a => { const [id, name] = a.split('|'); return { id: Number(id), name: name }; });
  const prefs = $.NSUserDefaults.alloc.initWithSuiteName('com.apple.HIToolbox');
  const key = 'AppleEnabledInputSources';
  const current = ObjC.deepUnwrap(prefs.arrayForKey(key)) || [];
  let next = current.filter(e => !wanted.some(w => e['KeyboardLayout ID'] === w.id));
  if (action === 'register') {
    next = next.concat(wanted.map(w => ({ 'InputSourceKind': 'Keyboard Layout', 'KeyboardLayout ID': w.id, 'KeyboardLayout Name': w.name })));
  }
  prefs.setObjectForKey($(next), key);
  prefs.synchronize;
  // How many of our layouts macOS now reports as enabled
  const live = ObjC.castRefToObject($.TISCreateInputSourceList($(), false));
  let count = 0;
  for (let i = 0; i < live.count; i++) {
    const id = ObjC.castRefToObject($.TISGetInputSourceProperty(live.objectAtIndex(i), $.kTISPropertyInputSourceID)).js;
    if (id.startsWith('com.carbongo.keyboardlayout.sakha.')) count++;
  }
  return count;
}
EOF
  osascript -l JavaScript "$js" "$@" 2>/dev/null
}

# ── commands ────────────────────────────────────────────────────────────
fetch_bundle() {  # prints the path of a Sakha.bundle to install
  local here; here=$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd) || here=""
  if [[ -n $here && -d $here/$BUNDLE && -z $VERSION ]]; then printf '%s' "$here/$BUNDLE"; return; fi
  local url="https://github.com/$REPO/releases/latest/download/Sakha-Keyboard.zip"
  [[ -n $VERSION ]] && url="https://github.com/$REPO/releases/download/$VERSION/Sakha-Keyboard.zip"
  step "Downloading ${VERSION:-the latest release}" >&2
  curl -fsSL "$url" -o "$TMP/sakha.zip" || die "Download failed: $url"
  unzip -q "$TMP/sakha.zip" -d "$TMP"
  local found; found=$(find "$TMP" -name "$BUNDLE" -type d -maxdepth 3 | head -1)
  [[ -n $found ]] || die "The release archive has no $BUNDLE"
  printf '%s' "$found"
}

# System Settings keeps its own copy of layout names and icons, so it shows stale icons (e.g. old flags)
# until a logout. Only that copy is cleared: wiping the main IntlDataCache races with registration.
clear_caches() {
  local cache; cache=$(getconf DARWIN_USER_CACHE_DIR 2>/dev/null) || return 0
  rm -f "$cache"com.apple.Keyboard-Settings.extension/com.apple.IntlDataCache.le* 2>/dev/null || true
  killall -q "System Settings" 2>/dev/null || true  # reopens with fresh data
}

install() {
  local src; src=$(fetch_bundle)
  local version; version=$(defaults read "$src/Contents/Info" CFBundleVersion 2>/dev/null || echo "?")
  step "Installing Sakha keyboard layouts $version"

  for old in "${OLD_BUNDLES[@]}"; do
    if [[ -d $DEST/$old ]] && confirm "Remove the old v1 \"$old\" (replaced by this version)"; then
      rm -rf "${DEST:?}/$old"; ok "Removed $old"
    fi
  done

  mkdir -p "$DEST"
  rm -rf "${DEST:?}/$BUNDLE"
  cp -R "$src" "$DEST/"
  xattr -dr com.apple.quarantine "$DEST/$BUNDLE" 2>/dev/null || true
  touch "$DEST" "$DEST/$BUNDLE"  # newer than macOS's layout cache → it rescans the folder
  ok "Copied to ~/Library/Keyboard Layouts"
  clear_caches

  local keys=() ids=() names=() k l
  if [[ $ENABLE == 1 ]]; then
    while IFS= read -r k; do keys+=("$k"); done < <(choose_layouts)
  fi
  for k in ${keys[@]+"${keys[@]}"}; do
    for l in "${LAYOUTS[@]}"; do
      [[ $(field "$l" 0) == "$k" ]] && { ids+=("$(field "$l" 1)|$(field "$l" 2)"); names+=("$(field "$l" 2)"); }
    done
  done
  [[ ${#keys[@]} -gt 0 && ${#ids[@]} -eq 0 ]] && warn "Unknown layout name(s): ${keys[*]}"

  # Right after a cache reset macOS can drop the first registration, so check and retry.
  local live=0 attempt
  for attempt in 1 2 3 4 5; do
    live=$(tis register "$DEST/$BUNDLE" ${ids[@]+"${ids[@]}"}) || live=0
    [[ $live -ge ${#ids[@]} ]] && break
    sleep "$attempt"
  done
  if [[ $live -lt ${#ids[@]} ]]; then
    warn "macOS hasn't picked the layouts up yet. Log out and back in, or run the installer again."
  else
    ok "Registered with macOS — no logout needed"
  fi
  for l in ${names[@]+"${names[@]}"}; do ok "Added $l to the input menu"; done

  say ""
  say "${B}Done.${N} Switch layouts with ${B}Ctrl+Space${N} or ${B}🌐 Globe${N}, or from the input menu."
  say "Add or remove layouts: System Settings → Keyboard → Text Input → Edit."
  [[ $GUI == 1 ]] && dialog "Sakha keyboard layouts are installed.\n\nSwitch with Ctrl+Space or the Globe key. Add more in System Settings → Keyboard → Text Input → Edit."
  return 0
}

uninstall() {
  step "Removing Sakha keyboard layouts"
  [[ -d $DEST/$BUNDLE ]] || { warn "Not installed."; return 0; }
  confirm "Remove all Sakha layouts" || { say "Cancelled."; return 0; }
  local all=() l
  for l in "${LAYOUTS[@]}"; do all+=("$(field "$l" 1)|$(field "$l" 2)"); done
  tis remove "${all[@]}" >/dev/null || true
  rm -rf "${DEST:?}/$BUNDLE"
  clear_caches
  ok "Removed from the input menu and ~/Library/Keyboard Layouts"
  [[ $GUI == 1 ]] && dialog "Sakha keyboard layouts were removed."
  return 0
}

# ── main ────────────────────────────────────────────────────────────────
YES=0 GUI=0 ENABLE=1 ACTION=install SELECTED="" VERSION=""
while [[ $# -gt 0 ]]; do
  case $1 in
    -y | --yes) YES=1 ;;
    -l | --layouts) SELECTED=${2:?--layouts needs a list}; shift ;;
    --no-enable) ENABLE=0 ;;
    -v | --version) VERSION=${2:?--version needs a tag}; shift ;;
    -u | --uninstall) ACTION=uninstall ;;
    --gui) GUI=1 ;;
    -h | --help) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
  shift
done

[[ $(uname -s) == Darwin ]] || die "These layouts are for macOS."
TMP=$(mktemp -d -t sakha-keyboard)
trap 'rm -rf "$TMP"' EXIT
"$ACTION"
