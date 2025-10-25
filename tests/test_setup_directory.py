import os
os.environ["DATA_DIR"] = "test"
DATA_DIR = os.environ["DATA_DIR"]

import shutil
import unittest
from setup_directory import construct_file_path, construct_directory_path

class TestDirectoryFunctions(unittest.TestCase):
    def setUp(self):
        """Clean up any previous test directories before each test."""
        if os.path.exists(DATA_DIR):
            shutil.rmtree(DATA_DIR)

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(DATA_DIR):
            shutil.rmtree(DATA_DIR)

    def test_f_creates_data_directory(self):
        """Test that f creates the 'data' directory."""
        construct_file_path("testfile.txt")
        self.assertTrue(os.path.isdir(DATA_DIR))

    def test_g_creates_subdirectory(self):
        """Test that g creates 'data/{directory name}' directory."""
        construct_directory_path("subdir")
        self.assertTrue(os.path.isdir(os.path.join(DATA_DIR, "subdir")))

if __name__ == "__main__":
    unittest.main()
