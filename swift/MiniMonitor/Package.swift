// swift-tools-version:5.9
// MiniMonitor: watch the Homylon engine think, in Terminal. Uses HomylonKit from GitHub.
//
//   swift run MiniMonitor              (the engine runs on this computer)
//   swift run MiniMonitor 192.168.1.10 (the engine runs on another computer)

import PackageDescription

let package = Package(
    name: "MiniMonitor",
    platforms: [.macOS("11.7")],
    dependencies: [
        .package(url: "https://github.com/Homylon/homylon-kit-swift", from: "1.0.2"),
    ],
    targets: [
        .executableTarget(name: "MiniMonitor",
                          dependencies: [.product(name: "HomylonKit", package: "homylon-kit-swift")]),
    ]
)
