# Tests for the Simplified Chinese table and its registration

import string
import unittest

import bpy

import helpers
import src
from src import i18n_zh_hans, messages, operator


def fields(text):
    """The named fields of a format string, sorted."""
    return sorted(name for _, name, _, _ in string.Formatter().parse(text) if name)


class TableTests(unittest.TestCase):

    def setUp(self):
        self.table = i18n_zh_hans.table()

    def test_every_interface_text_has_an_entry(self):
        command = operator.OBJECT_OT_copy_bone_names
        texts = [command.bl_label, command.__doc__] + list(messages.templates().values())
        missing = [t for t in texts if (i18n_zh_hans.DEFAULT, t) not in self.table]
        self.assertEqual(missing, [])

    def test_label_in_the_operator_context_too(self):
        self.assertEqual(self.table[(i18n_zh_hans.OPERATOR, "Copy Bone Names")], "复制骨骼名称")

    def test_translations_keep_the_same_fields(self):
        for (_, english), chinese in self.table.items():
            self.assertEqual(fields(english), fields(chinese), english)

    def test_no_entry_is_empty_or_untranslated(self):
        for (_, english), chinese in self.table.items():
            self.assertTrue(chinese.strip(), english)
            self.assertNotEqual(chinese, english)


class ChineseInterfaceTests(unittest.TestCase):

    def setUp(self):
        helpers.new_scene()
        src.register()
        view = bpy.context.preferences.view
        self.saved = (view.language, view.use_translate_interface,
                      view.use_translate_tooltips, view.use_translate_reports)
        view.language = 'zh_HANS'
        view.use_translate_interface = True
        view.use_translate_tooltips = True
        view.use_translate_reports = True

    def tearDown(self):
        view = bpy.context.preferences.view
        (view.language, view.use_translate_interface,
         view.use_translate_tooltips, view.use_translate_reports) = self.saved
        src.unregister()

    def test_label_tooltip_and_reports_in_chinese(self):
        tr = bpy.app.translations
        self.assertEqual(tr.pgettext_iface("Copy Bone Names", "Operator"), "复制骨骼名称")
        self.assertEqual(tr.pgettext_tip(operator.OBJECT_OT_copy_bone_names.__doc__),
                         "把当前骨架所有骨骼的名称复制到剪贴板，每行一个，父级在前")
        self.assertEqual(tr.pgettext_rpt(messages.COPIED).format(count=3, name="Armature"),
                         "已复制 Armature 的 3 个骨骼名称")
        self.assertEqual(tr.pgettext_rpt(messages.NO_BONES).format(name="Armature"),
                         "Armature 没有骨骼")

    def test_english_again_after_unregister(self):
        src.unregister()
        try:
            self.assertEqual(bpy.app.translations.pgettext_iface("Copy Bone Names", "Operator"),
                             "Copy Bone Names")
        finally:
            src.register()


if __name__ == '__main__':
    unittest.main()
