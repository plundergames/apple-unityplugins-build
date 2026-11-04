# Apple Unity plug-ins build

Builds `Apple.Core` and `Apple.GameKit` from [apple/unityplugins](https://github.com/apple/unityplugins) as `.tgz` packages on a macOS runner, because Apple publishes no prebuilt packages and building needs Xcode. Contains no game code and no keys. `patch_apple_sources.py` makes two small changes to Apple's sources before building; its comments explain them.

Run: **Actions > Build Apple Unity plug-ins > Run workflow**, enter the Apple release tag, download the `apple-unity-plugins` artifact. Only needed when updating the plug-ins.
