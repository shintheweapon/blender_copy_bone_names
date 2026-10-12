# End-to-end tests: register the add-on and run the command in each mode

import unittest
from unittest import mock

import bpy

import helpers
import src
from src import operator

SKELETON = [('Root', None), ('Spine', 'Root'), ('Head', 'Spine'), ('Arm', 'Spine')]


class CopyBoneNamesTests(unittest.TestCase):

    def setUp(self):
        helpers.new_scene()
        src.register()
        self.copied = []
        patcher = mock.patch.object(operator, 'set_clipboard',
                                    lambda context, text: self.copied.append(text))
        patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        if bpy.context.object is not None and bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        src.unregister()

    def test_object_mode_copies_all_names_parents_first(self):
        arm = helpers.make_armature(SKELETON)
        self.assertEqual(bpy.ops.object.copy_bone_names(), {'FINISHED'})
        self.assertEqual(self.copied, ["Root\nSpine\nHead\nArm"])
        self.assertEqual(self.copied[0], "\n".join(b.name for b in arm.data.bones))

    def test_edit_mode_includes_a_bone_added_in_edit_mode(self):
        arm = helpers.make_armature(SKELETON)
        bpy.ops.object.mode_set(mode='EDIT')
        added = arm.data.edit_bones.new('Added')
        added.head = (0.0, 1.0, 0.0)
        added.tail = (0.0, 2.0, 0.0)
        added.parent = arm.data.edit_bones['Root']
        self.assertEqual(bpy.ops.object.copy_bone_names(), {'FINISHED'})
        self.assertIn('Added', self.copied[0].split("\n"))
        self.assertEqual(arm.mode, 'EDIT')

    def test_pose_mode(self):
        helpers.make_armature(SKELETON)
        bpy.ops.object.mode_set(mode='POSE')
        self.assertEqual(bpy.ops.object.copy_bone_names(), {'FINISHED'})
        self.assertEqual(self.copied, ["Root\nSpine\nHead\nArm"])

    def test_armature_without_bones_leaves_the_clipboard_alone(self):
        helpers.make_armature([])
        self.assertEqual(bpy.ops.object.copy_bone_names(), {'CANCELLED'})
        self.assertEqual(self.copied, [])

    def test_not_available_for_a_mesh(self):
        mesh = bpy.data.objects.new('Mesh', bpy.data.meshes.new('Mesh'))
        bpy.context.scene.collection.objects.link(mesh)
        bpy.context.view_layer.objects.active = mesh
        self.assertFalse(bpy.ops.object.copy_bone_names.poll())

    def test_not_available_without_an_active_object(self):
        bpy.context.view_layer.objects.active = None
        self.assertFalse(bpy.ops.object.copy_bone_names.poll())

    def test_command_is_in_the_three_menus(self):
        for menu in src.MENUS:
            draw_funcs = getattr(bpy.types, menu)._dyn_ui_initialize()
            self.assertIn(operator.menu_func, draw_funcs, menu)

    def test_unregister_removes_the_command(self):
        src.unregister()
        try:
            self.assertFalse(hasattr(bpy.types, 'OBJECT_OT_copy_bone_names'))
            for menu in src.MENUS:
                self.assertNotIn(operator.menu_func,
                                 getattr(bpy.types, menu)._dyn_ui_initialize(), menu)
        finally:
            src.register()


if __name__ == '__main__':
    unittest.main()
