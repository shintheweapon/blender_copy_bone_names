# Changelog

## 1.0.0

### Added
- **Copy Bone Names** command: copies the names of all bones of the active armature to the clipboard, one name per
  line, parents before children, and reports how many names it copied.
- The command is at the bottom of the Object menu (Object mode), the Armature menu (Edit mode) and the Pose menu
  (Pose mode), and in F3 search.
- In Edit mode, bones added since entering Edit mode are included.
- An armature with no bones gives a warning and leaves the clipboard unchanged.
- Simplified Chinese interface (zh_HANS), using Blender's own words for armature, bone and clipboard.
