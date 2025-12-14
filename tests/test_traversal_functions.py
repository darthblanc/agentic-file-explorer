import os
import shutil
import unittest
import json
import importlib
from pathlib import Path

# Ensure DATA_DIR is set before modules that read it at import-time
os.environ["DATA_DIR"] = "test"
DATA_DIR = os.environ["DATA_DIR"]

# Reload setup_directory and traversal_functions so they pick up the TEST DATA_DIR
import importlib
import setup_directory
importlib.reload(setup_directory)
import traversal_functions
importlib.reload(traversal_functions)
from traversal_functions import breadth_first_search, depth_first_search


class TestTraversalFunctions(unittest.TestCase):
    def setUp(self):
        # create a small directory tree
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(os.path.join(DATA_DIR, "a"), exist_ok=True)
        os.makedirs(os.path.join(DATA_DIR, "a", "sub"), exist_ok=True)
        # files
        open(os.path.join(DATA_DIR, "root.txt"), "w").close()
        open(os.path.join(DATA_DIR, "a", "foo.txt"), "w").close()
        open(os.path.join(DATA_DIR, "a", "sub", "target.txt"), "w").close()

    def tearDown(self):
        if os.path.exists(DATA_DIR):
            shutil.rmtree(DATA_DIR)

    def test_bfs_lists_matches_non_targeted(self):
        res = breadth_first_search("")
        # expect at least root entries
        self.assertIn("root.txt", json.dumps(res))

    def test_bfs_targeted_find_file(self):
        res = breadth_first_search("", target="target.txt")
        # when targeted should include match for target
        found = any("target.txt" in x for x in res.get("match", []))
        self.assertTrue(found)

    def test_dfs_targeted_find_file(self):
        res = depth_first_search("", target="target.txt")
        found = any("target.txt" in x for x in res.get("match", []))
        self.assertTrue(found)


if __name__ == '__main__':
    unittest.main()
