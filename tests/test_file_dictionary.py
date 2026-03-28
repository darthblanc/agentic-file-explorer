import os
import shutil
import unittest
import tempfile

from file import File
from file_dictionary import FileDictionary, file_dict


class TestFileDictionary(unittest.TestCase):
    def setUp(self):
        self._orig_data_dir = os.environ.get("DATA_DIR")
        self.tmp_dir = tempfile.mkdtemp()
        os.environ["DATA_DIR"] = self.tmp_dir
        file_dict.files = {}

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        if self._orig_data_dir is None:
            os.environ.pop("DATA_DIR", None)
        else:
            os.environ["DATA_DIR"] = self._orig_data_dir

    def _write_file(self, rel_path: str, content: str):
        full_path = os.path.join(self.tmp_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as fd:
            fd.write(content)

    def test_add_and_contains_and_get(self):
        self._write_file("a.txt", "content")
        f = File.new_file("a.txt")
        fd = FileDictionary()
        fd.add(f)
        self.assertIn(f.id, fd)
        got = fd.get(f.id)
        self.assertEqual(got.get_content(), "content")

    def test_set_and_str_and_remove(self):
        self._write_file("a.txt", "one")
        self._write_file("b.txt", "two")
        f1 = File.new_file("a.txt")
        f2 = File.new_file("b.txt")
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
