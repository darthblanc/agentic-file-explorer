import unittest
import os
import shutil
import tempfile
from file import File


class TestFileModel(unittest.TestCase):
    def setUp(self):
        self._orig_data_dir = os.environ.get("DATA_DIR")
        self.tmp_dir = tempfile.mkdtemp()
        os.environ["DATA_DIR"] = self.tmp_dir

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        if self._orig_data_dir is None:
            os.environ.pop("DATA_DIR", None)
        else:
            os.environ["DATA_DIR"] = self._orig_data_dir

    def test_new_file_and_getters(self):
        content = "hello world"
        rel_path = "path/to/file.txt"
        full_path = os.path.join(self.tmp_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as fd:
            fd.write(content)

        f = File.new_file(rel_path, "text/plain")
        self.assertTrue(f.id.startswith("file:"))
        self.assertEqual(f.name, "file.txt")
        self.assertEqual(f.path, rel_path)
        self.assertEqual(f.get_content(), content)
        self.assertEqual(str(f), f.id)
        self.assertEqual(f.size, len(content.encode("utf-8")))


if __name__ == '__main__':
    unittest.main()
