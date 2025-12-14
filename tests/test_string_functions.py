import unittest
from string_functions import strip_base_directory


class TestStringFunctions(unittest.TestCase):
    def test_strip_base_matching(self):
        self.assertEqual(strip_base_directory("data/hello/world.txt"), "./hello/world.txt")

    def test_strip_base_nonmatching(self):
        # path that doesn't start with 'data' should be unchanged
        self.assertEqual(strip_base_directory("/tmp/data/file.txt"), "/tmp/data/file.txt")


if __name__ == '__main__':
    unittest.main()
