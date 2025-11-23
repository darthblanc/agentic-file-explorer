import os
os.environ["DATA_DIR"] = "test"
DATA_DIR = os.environ["DATA_DIR"]

import shutil
import unittest
from txt_tools import read_txt, write_to_txt, append_to_txt, append_to_txt, clear

class TestFileTools(unittest.TestCase):
    def setUp(self):
        """Create a temporary data directory before each test."""
        self.data_dir = DATA_DIR
        os.makedirs(self.data_dir, exist_ok=True)
        self.test_file = os.path.join(self.data_dir, "test.txt")
        self.sub_dir = os.path.join(self.data_dir, "subdir")
        os.makedirs(self.sub_dir, exist_ok=True)

    def tearDown(self):
        """Remove the data directory after each test."""
        if os.path.exists(self.data_dir):
            shutil.rmtree(self.data_dir)

    def test_w_and_r(self):
        """Test writing and reading from a file using LangChain tools."""
        write_to_txt.invoke({"path": "test.txt", "content": "Hello World"})
        result = read_txt.invoke({"path": "test.txt"})
        self.assertEqual(result, "Hello World")

    def test_a(self):
        """Test appending to a file using LangChain tools."""
        write_to_txt.invoke({"path": "test.txt", "content": "Line 1"})
        append_to_txt.invoke({"path": "test.txt", "content": "Line 2\n"})
        result = read_txt.invoke({"path": "test.txt"})
        self.assertEqual(result, "Line 1\nLine 2\n")

    def test_c(self):
        """Test clearing a file using LangChain tools."""
        write_to_txt.invoke({"path": "test.txt", "content": "Some content"})
        clear.invoke({"path": "test.txt"})
        result = read_txt.invoke({"path": "test.txt"})
        self.assertEqual(result, "")   

if __name__ == "__main__":
    unittest.main()
