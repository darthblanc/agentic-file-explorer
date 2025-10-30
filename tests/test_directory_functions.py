import os
os.environ["DATA_DIR"] = "test"
DATA_DIR = os.environ["DATA_DIR"]

import shutil
import unittest
from directory_functions import create_directory, get_directory

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

    def test_g(self):
        """Test counting files in a directory using LangChain tools."""
        open(os.path.join(self.sub_dir, "a.txt"), "w").close()
        open(os.path.join(self.sub_dir, "b.txt"), "w").close()
        message = get_directory.invoke({"directory": "subdir"})
        self.assertEqual(message, "Listed: 2 items [b.txt, a.txt] from directory (subdir)")

    def test_cd(self):
        """Test creating directories using LangChain tools."""
        message = create_directory.invoke({"directory": "sub_subdir"})
        self.assertEqual(message, f"Created directory: {DATA_DIR}/sub_subdir")    


if __name__ == "__main__":
    unittest.main()
