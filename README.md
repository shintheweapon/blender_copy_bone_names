# Copy Bone Names

A Blender add-on that copies the names of all bones of the active armature to the clipboard, one name per line.
It does the same as this line in Blender's Python Console, as a menu command:

```python
bpy.context.window_manager.clipboard = "\n".join(b.name for b in C.object.data.bones)
```

Requires Blender 4.5 or later.

## Install

1. Download `copy_bone_names-1.0.0.zip` from this repository's Releases page, or build it (see [Build](#build)).
2. In Blender: **Edit > Preferences > Get Extensions**, open the menu at the top right, choose **Install from Disk**
   and pick the zip.

## Use

1. Select an armature, so that it is the active object.
2. Run **Copy Bone Names** from the menu of the current mode:
   - Object mode: **Object > Copy Bone Names**;
   - Edit mode: **Armature > Copy Bone Names**;
   - Pose mode: **Pose > Copy Bone Names**;
   - in any of these modes, **F3** and type "Copy Bone Names".
3. Paste anywhere, for example into a text editor or a spreadsheet.

What gets copied:
- every bone of the armature, one name per line, with no line break after the last name;
- in the order of the armature's bone list, where each bone comes after its parent;
- in Edit mode, bones added since entering Edit mode as well.

The status bar reports how many names were copied. When the armature has no bones, the command gives a warning
and leaves the clipboard unchanged.

The extension declares the **clipboard** permission, because copying to the clipboard is all it does.

## Simplified Chinese

With Blender's interface language set to Simplified Chinese (简体中文), the command is **复制骨骼名称** and its tooltip
and reports are in Chinese too. The words follow Blender's own translation: 骨架 (armature), 骨骼 (bone), 剪贴板
(clipboard).

## Develop

The add-on's files are in `src/`:
- `names.py`: joins the bone names (plain Python);
- `operator.py`: the command, its menu entry and the clipboard write;
- `messages.py`: the report texts;
- `i18n_zh_hans.py`: the Simplified Chinese table;
- `__init__.py`: registration.

### Test

```
blender.exe -b -P tests\run_tests.py
```

The runner sets the interface language to English for the run, because the tests check English texts. The tests
replace the clipboard write, because background Blender cannot read the clipboard back.

### Build

```
.\build.ps1
```

It runs Blender's extension build on `src` and writes `dist\copy_bone_names-<version>.zip`, then checks the zip's
layout. It needs the path to your blender.exe: pass it with `.\build.ps1 -Blender "<path to blender.exe>"`, or put it
on the first line of `build.local.txt` next to `build.ps1` (git-ignored, so the path stays on your machine).

## License

GPL-3.0-or-later; see [LICENSE](LICENSE).
