// Dumps an installed macOS keyboard layout to JSON: {layer: {keycode: output}}.
// Usage: swift tools/dump-layout.swift com.apple.keylayout.Russian > src/base/russian.json
import Carbon
import Foundation

let wanted = CommandLine.arguments[1]
let sources = TISCreateInputSourceList(nil, true).takeRetainedValue() as! [TISInputSource]
guard let source = sources.first(where: {
  (Unmanaged<CFString>.fromOpaque(TISGetInputSourceProperty($0, kTISPropertyInputSourceID)).takeUnretainedValue() as String) == wanted
}) else { fatalError("input source \(wanted) not found") }
let data = Unmanaged<CFData>.fromOpaque(TISGetInputSourceProperty(source, kTISPropertyUnicodeKeyLayoutData)).takeUnretainedValue() as Data

// UCKeyTranslate modifier state = (Carbon modifier mask >> 8) & 0xFF
let layers: [(String, UInt32)] = [("base", 0), ("shift", 2), ("caps", 4), ("opt", 8), ("shiftopt", 10), ("capsopt", 12), ("cmd", 1), ("ctrl", 16)]
var result: [String: [String: String]] = [:]
data.withUnsafeBytes { raw in
  let layout = raw.bindMemory(to: UCKeyboardLayout.self).baseAddress!
  for (name, mods) in layers {
    var map: [String: String] = [:]
    for code in UInt16(0)..<128 {
      var dead: UInt32 = 0, length = 0
      var buffer = [UniChar](repeating: 0, count: 8)
      let status = UCKeyTranslate(layout, code, UInt16(kUCKeyActionDown), mods, UInt32(LMGetKbdType()),
                                  OptionBits(kUCKeyTranslateNoDeadKeysBit), &dead, 8, &length, &buffer)
      if status == noErr && length > 0 { map[String(code)] = String(utf16CodeUnits: buffer, count: length) }
    }
    result[name] = map
  }
}
let json = try! JSONSerialization.data(withJSONObject: result, options: [.prettyPrinted, .sortedKeys])
print(String(data: json, encoding: .utf8)!)
