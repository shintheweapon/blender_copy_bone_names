# Tests for names.bone_names_text; plain Python

import unittest
from types import SimpleNamespace

from src import names


def bones(*bone_names):
    """Stand-ins for Blender bones: objects with a ``name``."""
    return [SimpleNamespace(name=n) for n in bone_names]


class BoneNamesTextTests(unittest.TestCase):

    def test_one_name_per_line_in_order(self):
        self.assertEqual(names.bone_names_text(bones('Root', 'Spine', 'Head')),
                         "Root\nSpine\nHead")

    def test_no_line_break_after_the_last_name(self):
        self.assertFalse(names.bone_names_text(bones('Root')).endswith("\n"))

    def test_no_bones_gives_an_empty_string(self):
        self.assertEqual(names.bone_names_text([]), "")

    def test_names_are_kept_exactly(self):
        text = names.bone_names_text(bones('L_Foot_Target2', '骨骼 01', 'a.b'))
        self.assertEqual(text.split("\n"), ['L_Foot_Target2', '骨骼 01', 'a.b'])


if __name__ == '__main__':
    unittest.main()
