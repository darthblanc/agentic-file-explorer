import os
import shutil
import tempfile
import unittest

from file import File
from file_dictionary import FileDictionary


class TestAgentFileContext(unittest.TestCase):
    """Tests what file references look like in the agent's context window."""

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

    def _write_file(self, rel_path: str, content: str):
        full_path = os.path.join(self.tmp_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as fd:
            fd.write(content)

    def test_single_file_reference(self):
        self._write_file("notes.txt", "hello")
        fd = FileDictionary()
        fd.add(File.new_file("notes.txt", "text/plain"))

        context = str(fd)
        self.assertEqual(context, "file:notes.txt")

    def test_multiple_file_references_no_content_leaked(self):
        self._write_file("a.txt", "secret content A")
        self._write_file("b.txt", "secret content B")
        fd = FileDictionary()
        fd.set([File.new_file("a.txt"), File.new_file("b.txt")])

        context = str(fd)
        self.assertIn("file:a.txt", context)
        self.assertIn("file:b.txt", context)
        self.assertNotIn("secret content A", context)
        self.assertNotIn("secret content B", context)

    def test_get_content_reads_from_disk(self):
        self._write_file("doc.txt", "initial content")
        fd = FileDictionary()
        fd.add(File.new_file("doc.txt", "text/plain"))

        # Simulate agent reading the file after content changes on disk
        full_path = os.path.join(self.tmp_dir, "doc.txt")
        with open(full_path, "w") as f:
            f.write("updated content")

        self.assertEqual(fd.get("file:doc.txt").get_content(), "updated content")


if __name__ == "__main__":
    unittest.main()
