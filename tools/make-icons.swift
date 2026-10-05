// Draws the input-menu icons: filled badges with knocked-out letters, like Apple's own (A, Ca).
// Keyboard layouts can't use Apple's text labels (TISIconLabels works only for input methods), so this
// square image is used everywhere. It is a template (TISIconIsTemplate): dark on a light menu bar or menu,
// white on a dark one or when highlighted. Filled, so it stays visible on the switcher's blue selection,
// where templates are drawn dark.
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
  let ctx = NSGraphicsContext(bitmapImageRep: rep)!
  NSGraphicsContext.current = ctx
  // Metrics of macOS 27's own badges (A, Ca): 16 pt tall, 3.5 pt corners, 8 pt cap height (SF 11 pt semibold).
  let s = CGFloat(pixels) / 16  // design on a 16-pt grid
  let badge = NSRect(x: 0, y: 0, width: 16 * s, height: 16 * s)
  NSColor.black.set()
  NSBezierPath(roundedRect: badge, xRadius: 3.5 * s, yRadius: 3.5 * s).fill()
  var font = NSFont.systemFont(ofSize: 11 * s, weight: .semibold)
  if (text as NSString).size(withAttributes: [.font: font]).width > 13 * s {  // keep a margin inside the badge
    font = NSFont.systemFont(ofSize: 11 * s, weight: .semibold, width: .condensed)
  }
  let size = (text as NSString).size(withAttributes: [.font: font])
  let capCenter = font.capHeight / 2 - font.descender  // centre the capitals, not the line box
  let origin = NSPoint(x: badge.midX - size.width / 2, y: badge.midY - capCenter)
  ctx.compositingOperation = .destinationOut  // knock the letters out of the badge
  (text as NSString).draw(at: origin, withAttributes: [.font: font, .foregroundColor: NSColor.black])
  ctx.flushGraphics()
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
