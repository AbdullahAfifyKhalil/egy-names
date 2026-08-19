// swift-tools-version: 5.9
import PackageDescription

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
            resources: [
                .process("Resources")
            ]
        ),
        .testTarget(
            name: "EgyNamesTests",
            dependencies: ["EgyNames"]
        ),
    ]
)
