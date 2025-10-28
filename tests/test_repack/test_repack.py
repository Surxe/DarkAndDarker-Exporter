import unittest
from src.repack.repack import Repacker
from pathlib import Path

class DummyOptions:
    def __init__(self, ue_install_dir, steam_game_download_dir, output_data_dir, repack_output_file):
        self.ue_install_dir = ue_install_dir
        self.steam_game_download_dir = steam_game_download_dir
        self.output_data_dir = output_data_dir
        self.repack_output_file = repack_output_file

DUMMY_UE_INSTALL_DIR = "C:/Dummy/UE_Install"
DUMMY_STEAM_GAME_DOWNLOAD_DIR = "C:/Dummy/SteamGame"
DUMMY_OUTPUT_DATA_DIR = "C:/Dummy/Output"
DUMMY_REPACK_OUTPUT_FILE = "C:/Dummy/Output/repacked.pak"

class TestRepacker(unittest.TestCase):
    def test_cleanup_removes_pak_extract_dir(self):
        import tempfile
        import shutil
        # Create a temporary PakExtract directory with files and subdirs
        with tempfile.TemporaryDirectory() as temp_dir:
            pak_extract_dir = Path(temp_dir) / "PakExtract"
            pak_extract_dir.mkdir()
            # Add a file
            test_file = pak_extract_dir / "test.txt"
            test_file.write_text("dummy")
            # Add a subdirectory
            subdir = pak_extract_dir / "subdir"
            subdir.mkdir()
            subfile = subdir / "subfile.txt"
            subfile.write_text("dummy")

            # Patch Repacker to use our temp PakExtract dir
            opts = DummyOptions(DUMMY_UE_INSTALL_DIR, DUMMY_STEAM_GAME_DOWNLOAD_DIR, DUMMY_OUTPUT_DATA_DIR, DUMMY_REPACK_OUTPUT_FILE)
            repacker = Repacker.__new__(Repacker)
            repacker.options = opts
            repacker.pak_extract_dir = pak_extract_dir
            # Run cleanup
            repacker.cleanup()
            # PakExtract dir should be removed
            self.assertFalse(pak_extract_dir.exists())
    def setUp(self):
        self.options = DummyOptions(DUMMY_UE_INSTALL_DIR, DUMMY_STEAM_GAME_DOWNLOAD_DIR, DUMMY_OUTPUT_DATA_DIR, DUMMY_REPACK_OUTPUT_FILE)

    def test_repacker_init_file_not_found(self):
        # Should raise FileNotFoundError for dummy paths
        with self.assertRaises(FileNotFoundError):
            Repacker(self.options)

    def test_repacker_missing_options(self):
        # Should raise AttributeError if options is None
        with self.assertRaises(AttributeError):
            Repacker(None)

if __name__ == "__main__":
    unittest.main()
