Tool which installs dependencies (ALCOM, .NET, VPM, Unity Hub, Unity, ...) and prepares a VRChat Avatar project for you with latest recommended packages:
- VRChat SDK Base
- VRChat SDK Avatars
- [VRCFury](https://vrcfury.com/getting-started) - general-purpose tool (connect stuff, manage Gestures, add Toggles, SPS, ...)
- lilToon shader - shader which is depended on by many assets
- Poiyomi Toon Shader - shader which is depended on by many assets
- [Modular Avatar](https://modular-avatar.nadena.dev/docs/tutorials/clothing) - attach clothing to avatar
- GoGo Loco - complex avatar positioning in-game without needing full body tracking
- [AAO: Avatar Optimizer](https://vpm.anatawa12.com/avatar-optimizer/en/docs/tutorial/basic-usage/) - avatar optimizer
- [d4rkAvatarOptimizer](https://github.com/d4rkc0d3r/d4rkAvatarOptimizer/blob/main/README.md#how-to-use) - avatar optimizer
- [Avatar Compressor](https://lac.limitex.dev/en/docs/components/texture-compressor/) - avatar texture compressor
- Gesture Manager - check results of hand gestures in editor (Quality of Life)


# Usage

[Download](https://github.com/GeeTwentyFive/VRChatAvatarCreationSimplified/releases/latest) -> Run as admin/root -> Open project in ALCOM


# Basics

1) Find an avatar base on https://boothplorer.com/avatars (more items = better)
(NOTE: **each avatar/asset has their own usage instructions on their pages on booth.pm** (click on red “View on BOOTH” button on the right in avatar’s Boothplorer page))
2) Drag and drop into project scene
3) Add a 'VRC Avatar Descriptor' component to it
4) ^ set 'View Position' to between avatar's eyes
5) 'VRChat SDK > Show Control Panel' (top-middle of window) -> build and upload

(^ https://creators.vrchat.com/avatars/creating-your-first-avatar)


# Extra info

- Avatar optimization: https://vrwiki.info/wiki/Avatar_Optimization_Tutorial

- Finding lewd assets (like naked body texture and pp): Go to your avatar’s page on https://boothplorer.com/ -> click on “+” icon -> set “R18/Adult” to “Show Only R18/Adult”

- Position avatar without having full body tracking: Drag & drop GoGo Loco prefab onto avatar

- Preview results of hand gestures in editor: Add `Gesture Manager` to scene then use it

- Eye/face tracking support: https://docs.vrcft.io/docs/intro/getting-started

- Synchronize Lovense toys with VRChat: https://osc.toys/getting-started


# Building

(at least Python 3.14 is required)

1) Get **dependencies:** `beautifulsoup4`

2) `pyinstaller -F VAC_Simplified.py --uac-admin`


# Contributors

- [mitowo](https://github.com/mitowo)
