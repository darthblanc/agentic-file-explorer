import os
import shutil
import unittest
import tempfile

from file import File
from file_dictionary import FileDictionary, file_dict


class TestFileDictionary(unittest.TestCase):
    def setUp(self):
        # ensure a clean singleton for tests
        file_dict.files = {}

    def test_add_and_contains_and_get(self):
        f = File.new_file("a.txt", "content")
        fd = FileDictionary()
        fd.add(f)
        self.assertIn(f.id, fd)
        got = fd.get(f.id)
        self.assertEqual(got.get_content(), "content")

    def test_set_and_str_and_remove(self):
        f1 = File.new_file("a.txt", "one")
        f2 = File.new_file("b.txt", "two")
        fd = FileDictionary()
        fd.set([f1, f2])
        s = str(fd)
        self.assertIn("file:a.txt", s)
        self.assertIn("file:b.txt", s)
        fd.remove(f1.id)
        self.assertNotIn(f1.id, fd.files)

    def test_get_raises_on_missing(self):
        fd = FileDictionary()
        with self.assertRaises(ValueError):
            fd.get("nonexistent")


if __name__ == '__main__':
    unittest.main()
