import unittest
import os
import tempfile
from pathlib import Path
import subprocess
from src.utils import ensure_parent_dir, kill_process_tree, run_process

class TestUtils(unittest.TestCase):
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

    def test_kill_process_tree(self):
        # Start a process that spawns child processes
        if os.name == 'nt':
            parent = subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/c', 'ping', '-t', 'localhost'])
        else:
            parent = subprocess.Popen(['bash', '-c', '(sleep 60 &) && sleep 60'])
        
        try:
            # Give it a moment to start up
            import time
            time.sleep(1)
            
            # Kill the process tree
            kill_process_tree(parent.pid)
            
            # Check that the parent process is dead
            try:
                os.kill(parent.pid, 0)
                self.fail("Parent process should be dead")
            except OSError:
                pass  # Process is dead as expected
            
            # Cleanup any remaining processes just in case
            try:
                parent.kill()
            except:
                pass
            
        finally:
            # Ensure cleanup
            try:
                parent.kill()
            except:
                pass

    def test_kill_process_tree_nonexistent_pid(self):
        # This should not raise an error
        import psutil
        max_pid = 99999
        while max_pid > 0:
            if not psutil.pid_exists(max_pid):
                break
            max_pid -= 1
        
        # This should not raise an error
        kill_process_tree(max_pid)

if __name__ == '__main__':
    unittest.main()