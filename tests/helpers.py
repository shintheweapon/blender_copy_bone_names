# Shared helpers that build small Blender scenes for tests

from typing import Dict, Iterable, Optional, Tuple

import bpy

BoneSpec = Tuple[str, Optional[str]]


def new_scene() -> None:
    """Empty the current file so each test starts from a clean scene."""
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_armature(bones: Iterable[BoneSpec], name: str = 'Armature') -> bpy.types.Object:
    """
    Create an active armature object from bone names and parents.

    Parameters
    ----------
    bones : iterable of tuple
        ``(name, parent_name)`` per bone, parents first. Each bone is one unit
        long and starts where the previous one ends.
    name : str
        Name for the armature object and data.

    Returns
    -------
    bpy.types.Object
        The armature object, linked to the scene, active and in Object mode.
    """
    data = bpy.data.armatures.new(name)
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones: Dict[str, bpy.types.EditBone] = {}
    for index, (bone_name, parent_name) in enumerate(bones):
        eb = data.edit_bones.new(bone_name)
        eb.head = (0.0, 0.0, float(index))
        eb.tail = (0.0, 0.0, float(index + 1))
        if parent_name is not None:
            eb.parent = edit_bones[parent_name]
        edit_bones[bone_name] = eb
    bpy.ops.object.mode_set(mode='OBJECT')
    return obj
