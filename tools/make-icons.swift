// Draws the input-menu icons: bare letters, like the labels macOS shows for its own layouts (РУ, A).
// Keyboard layouts can't use Apple's text labels (TISIconLabels works only for input methods), so this
// square image is used everywhere. It is a template (TISIconIsTemplate), so like the native labels it is
// dark on a light menu bar or menu and turns white on a dark one or when highlighted.
// Usage: swift tools/make-icons.swift   → src/icons/*.icns (commit them; build.py copies them)
import AppKit

let labels: [(file: String, text: String)] = [
  ("sakha-windows", "СА"),
  ("sakha-russian", "СР"),
  ("sakha-latin", "SA"),
  ("sakha-novgorodov", "NV"),
]

func render(_ text: String, pixels: Int) -> Data {
  let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: pixels, pixelsHigh: pixels, bitsPerSample: 8,
                             samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB,
                             bytesPerRow: 0, bitsPerPixel: 0)!
  NSGraphicsContext.saveGraphicsState()
  NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
  // Native label metrics (measured on macOS 27): SF semibold, 8 pt cap height ≈ 11 pt type.
  let s = CGFloat(pixels) / 16  // design on a 16-pt grid
  var font = NSFont.systemFont(ofSize: 11 * s, weight: .semibold)
  var size = (text as NSString).size(withAttributes: [.font: font])
  if size.width > 16 * s {  // too wide for the square icon: condensed, same height
    font = NSFont.systemFont(ofSize: 11 * s, weight: .semibold, width: .condensed)
    size = (text as NSString).size(withAttributes: [.font: font])
  }
  let capCenter = font.capHeight / 2 - font.descender  // centre the capitals, not the line box
  let origin = NSPoint(x: 8 * s - size.width / 2, y: 8 * s - capCenter)
  (text as NSString).draw(at: origin, withAttributes: [.font: font, .foregroundColor: NSColor.black])
  NSGraphicsContext.restoreGraphicsState()
  return rep.representation(using: .png, properties: [:])!
}

let root = URL(fileURLWithPath: #filePath).deletingLastPathComponent().deletingLastPathComponent()
let icons = root.appendingPathComponent("src/icons")
try FileManager.default.createDirectory(at: icons, withIntermediateDirectories: true)
for label in labels {
  let set = FileManager.default.temporaryDirectory.appendingPathComponent("\(label.file).iconset")
  try? FileManager.default.removeItem(at: set)
  try FileManager.default.createDirectory(at: set, withIntermediateDirectories: true)
  for points in [16, 32, 128, 256, 512] {
    try render(label.text, pixels: points).write(to: set.appendingPathComponent("icon_\(points)x\(points).png"))
    try render(label.text, pixels: points * 2).write(to: set.appendingPathComponent("icon_\(points)x\(points)@2x.png"))
  }
  let iconutil = Process()
  iconutil.executableURL = URL(fileURLWithPath: "/usr/bin/iconutil")
  iconutil.arguments = ["-c", "icns", set.path, "-o", icons.appendingPathComponent("\(label.file).icns").path]
  try iconutil.run()
  iconutil.waitUntilExit()
  print("src/icons/\(label.file).icns")
}
