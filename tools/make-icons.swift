// Draws Apple-style text badges for the input menu (like Apple's "A" / "РУ") as template .icns.
// Usage: swift tools/make-icons.swift   → src/icons/*.icns (commit them; build.py copies them)
import AppKit

let badges: [(file: String, text: String, filled: Bool)] = [
  ("sakha-windows", "СА", true),
  ("sakha-russian", "СА", false),
  ("sakha-latin", "SA", true),
  ("sakha-novgorodov", "SA", false),
]

func render(_ text: String, filled: Bool, pixels: Int) -> Data {
  let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: pixels, pixelsHigh: pixels, bitsPerSample: 8,
                             samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB,
                             bytesPerRow: 0, bitsPerPixel: 0)!
  NSGraphicsContext.saveGraphicsState()
  let ctx = NSGraphicsContext(bitmapImageRep: rep)!
  NSGraphicsContext.current = ctx
  let s = CGFloat(pixels) / 16  // design on a 16-pt grid
  let line = 1.2 * s
  let badge = NSRect(x: 0.6 * s, y: 2.6 * s, width: 14.8 * s, height: 10.8 * s)
  let path = NSBezierPath(roundedRect: badge.insetBy(dx: line / 2, dy: line / 2), xRadius: 2.8 * s, yRadius: 2.8 * s)
  NSColor.black.set()
  if filled { path.fill() } else { path.lineWidth = line; path.stroke() }

  let font = NSFont.systemFont(ofSize: 7.6 * s, weight: .semibold)
  let attrs: [NSAttributedString.Key: Any] = [.font: font, .foregroundColor: NSColor.black, .kern: 0.15 * s]
  let size = (text as NSString).size(withAttributes: attrs)
  let origin = NSPoint(x: badge.midX - size.width / 2, y: badge.midY - size.height / 2 + 0.1 * s)
  if filled { ctx.compositingOperation = .destinationOut }  // knock the letters out of the filled badge
  (text as NSString).draw(at: origin, withAttributes: attrs)
  ctx.flushGraphics()
  NSGraphicsContext.restoreGraphicsState()
  return rep.representation(using: .png, properties: [:])!
}

let root = URL(fileURLWithPath: #filePath).deletingLastPathComponent().deletingLastPathComponent()
let icons = root.appendingPathComponent("src/icons")
try FileManager.default.createDirectory(at: icons, withIntermediateDirectories: true)
for badge in badges {
  let set = FileManager.default.temporaryDirectory.appendingPathComponent("\(badge.file).iconset")
  try? FileManager.default.removeItem(at: set)
  try FileManager.default.createDirectory(at: set, withIntermediateDirectories: true)
  for points in [16, 32, 128, 256, 512] {
    try render(badge.text, filled: badge.filled, pixels: points).write(to: set.appendingPathComponent("icon_\(points)x\(points).png"))
    try render(badge.text, filled: badge.filled, pixels: points * 2).write(to: set.appendingPathComponent("icon_\(points)x\(points)@2x.png"))
  }
  let iconutil = Process()
  iconutil.executableURL = URL(fileURLWithPath: "/usr/bin/iconutil")
  iconutil.arguments = ["-c", "icns", set.path, "-o", icons.appendingPathComponent("\(badge.file).icns").path]
  try iconutil.run()
  iconutil.waitUntilExit()
  print("src/icons/\(badge.file).icns")
}
