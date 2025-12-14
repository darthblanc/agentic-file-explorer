import unittest
import os
from file import File


class TestFileModel(unittest.TestCase):
    def test_new_file_and_getters(self):
        f = File.new_file("path/to/file.txt", "hello world", "text/plain")
        self.assertTrue(f.id.startswith("file:"))
        self.assertEqual(f.name, "file.txt")
        self.assertEqual(f.path, "path/to/file.txt")
        self.assertEqual(f.get_content(), "hello world")
        self.assertEqual(str(f), f.id)
        # size should match utf-8 encoding length
        self.assertEqual(f.size, len("hello world".encode("utf-8")))


if __name__ == '__main__':
    unittest.main()
