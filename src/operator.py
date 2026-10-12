# Operator that copies the active armature's bone names to the clipboard

import bpy

from . import messages, names


def set_clipboard(context: bpy.types.Context, text: str) -> None:
    """
    Put text on the system clipboard.

    Kept as its own function because background Blender cannot read the
    clipboard back; tests replace it to see the text.

    Parameters
    ----------
    context : bpy.types.Context
        Current Blender context.
    text : str
        Text to copy.
    """
    context.window_manager.clipboard = text


def _text(template: str, **fields) -> str:
    """
    Fill a message template from :mod:`messages`, in the interface language
    when Blender translates reports.

    Parameters
    ----------
    template : str
        One of the templates in :mod:`messages`.
    **fields
        Values for its named fields.

    Returns
    -------
    str
        The message.
    """
    return bpy.app.translations.pgettext_rpt(template).format(**fields)


class OBJECT_OT_copy_bone_names(bpy.types.Operator):
    """Copy the names of all bones of the active armature to the clipboard, one per line, parents before children"""
    bl_idname = "object.copy_bone_names"
    bl_label = "Copy Bone Names"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'ARMATURE'

    def execute(self, context):
        obj = context.active_object
        # Bones added in Edit mode reach armature.bones only after this
        if obj.mode == 'EDIT':
            obj.update_from_editmode()
        bones = obj.data.bones
        if len(bones) == 0:
            self.report({'WARNING'}, _text(messages.NO_BONES, name=obj.name))
            return {'CANCELLED'}
        set_clipboard(context, names.bone_names_text(bones))
        self.report({'INFO'}, _text(messages.COPIED, count=len(bones), name=obj.name))
        return {'FINISHED'}


def menu_func(self, context):
    """Add the command at the bottom of the Object, Armature and Pose menus."""
    self.layout.separator()
    self.layout.operator(OBJECT_OT_copy_bone_names.bl_idname)
