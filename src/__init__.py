# Copy Bone Names: copies the active armature's bone names to the clipboard

import bpy

from . import i18n_zh_hans, operator

# Menus that get the command: Object (Object mode), Armature (Edit mode), Pose (Pose mode)
MENUS = ('VIEW3D_MT_object', 'VIEW3D_MT_edit_armature', 'VIEW3D_MT_pose')


def register():
    """Register the translations, the operator and its menu entries."""
    bpy.app.translations.register(__name__, {'zh_HANS': i18n_zh_hans.table()})
    bpy.utils.register_class(operator.OBJECT_OT_copy_bone_names)
    for menu in MENUS:
        getattr(bpy.types, menu).append(operator.menu_func)


def unregister():
    """Unregister everything added by :func:`register`."""
    for menu in MENUS:
        getattr(bpy.types, menu).remove(operator.menu_func)
    bpy.utils.unregister_class(operator.OBJECT_OT_copy_bone_names)
    bpy.app.translations.unregister(__name__)
