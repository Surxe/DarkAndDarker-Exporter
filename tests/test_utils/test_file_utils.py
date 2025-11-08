import unittest
import os
import tempfile
from src.utils import ensure_parent_dir

class TestFileUtils(unittest.TestCase):
    def test_ensure_parent_dir_creates_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a deep path that doesn't exist
            deep_path = os.path.join(temp_dir, "level1", "level2", "file.txt")
            
            # Ensure parent directory is created
            ensure_parent_dir(deep_path)
            
            # Check that the parent directory exists
            parent_dir = os.path.dirname(deep_path)
            self.assertTrue(os.path.exists(parent_dir))
            self.assertTrue(os.path.isdir(parent_dir))

    def test_ensure_parent_dir_existing_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a path in an existing directory
            file_path = os.path.join(temp_dir, "file.txt")
            
            # This should not raise an error
            ensure_parent_dir(file_path)
            
            # Directory should still exist
            self.assertTrue(os.path.exists(temp_dir))
            self.assertTrue(os.path.isdir(temp_dir))

if __name__ == '__main__':
    unittest.main()