# Builds the clipboard text from bones; plain Python, no bpy needed

from typing import Iterable


def bone_names_text(bones: Iterable) -> str:
    """
    Join bone names into the text that goes to the clipboard.

    Parameters
    ----------
    bones : iterable
        Objects with a ``name`` attribute, such as ``armature.bones``, in the
        order the names should appear.

    Returns
    -------
    str
        One name per line, in the given order, with no line break after the
        last name; an empty string when there are no bones.
    """
    return "\n".join(bone.name for bone in bones)
