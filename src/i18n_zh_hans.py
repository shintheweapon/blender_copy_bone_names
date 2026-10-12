# Simplified Chinese (zh_HANS) translations of the add-on's texts; plain Python.
# Keys are (context, English text) as bpy.app.translations expects; the
# English texts must match the code exactly (tests check this). The words
# follow Blender's own zh_HANS translation: 骨架, 骨骼, 复制, 剪贴板.

from typing import Dict, Tuple

from . import messages

# Contexts used by Blender: '*' for most texts, 'Operator' for operator labels
DEFAULT = '*'
OPERATOR = 'Operator'

LABEL = "Copy Bone Names"

_TEXTS = {
    LABEL: "复制骨骼名称",
    ("Copy the names of all bones of the active armature to the clipboard, "
     "one per line, parents before children"):
        "把当前骨架所有骨骼的名称复制到剪贴板，每行一个，父级在前",
    messages.COPIED: "已复制 {name} 的 {count} 个骨骼名称",
    messages.NO_BONES: "{name} 没有骨骼",
}


def table() -> Dict[Tuple[str, str], str]:
    """
    Build the translation table to register with Blender.

    Returns
    -------
    dict
        ``{(context, English): Chinese}``. Every text is under the default
        context; the command label is also under the operator context, where
        Blender looks it up for menus and F3 search.
    """
    entries = {(DEFAULT, english): chinese for english, chinese in _TEXTS.items()}
    entries[(OPERATOR, LABEL)] = _TEXTS[LABEL]
    return entries
