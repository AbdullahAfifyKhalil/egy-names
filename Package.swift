// swift-tools-version: 5.9
import PackageDescription

// Root manifest so `https://github.com/AbdullahAfifyKhalil/egy-names.git`
// resolves with Swift Package Manager. The implementation lives in
// swift/EgyNames/ — keep that nested package for local path checkouts.
let package = Package(
    name: "EgyNames",
    platforms: [
        .iOS(.v13),
        .macOS(.v10_15),
        .tvOS(.v13),
        .watchOS(.v6),
        .visionOS(.v1)
    ],
    products: [
        .library(
            name: "EgyNames",
            targets: ["EgyNames"]
        ),
    ],
    targets: [
        .target(
            name: "EgyNames",
            path: "swift/EgyNames/Sources/EgyNames",
            resources: [
                .process("Resources")
            ]
        ),
        .testTarget(
            name: "EgyNamesTests",
            dependencies: ["EgyNames"],
            path: "swift/EgyNames/Tests/EgyNamesTests"
        ),
    ]
)
