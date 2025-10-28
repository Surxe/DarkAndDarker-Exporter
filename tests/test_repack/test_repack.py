import unittest
from src.repack.repack import Repacker

class DummyOptions:
    def __init__(self, ue_install_dir, steam_game_download_dir, output_data_dir):
        self.ue_install_dir = ue_install_dir
        self.steam_game_download_dir = steam_game_download_dir
        self.output_data_dir = output_data_dir

DUMMY_UE_INSTALL_DIR = "C:/Dummy/UE_Install"
DUMMY_STEAM_GAME_DOWNLOAD_DIR = "C:/Dummy/SteamGame"
DUMMY_OUTPUT_DATA_DIR = "C:/Dummy/Output"
DUMMY_REPACK_OUTPUT_FILE = "C:/Dummy/Output/repacked.pak"

class TestRepacker(unittest.TestCase):
    def setUp(self):
        self.options = DummyOptions(DUMMY_UE_INSTALL_DIR, DUMMY_STEAM_GAME_DOWNLOAD_DIR, DUMMY_OUTPUT_DATA_DIR)
        self.repack_output_file = DUMMY_REPACK_OUTPUT_FILE

    def test_repacker_init_file_not_found(self):
        # Should raise FileNotFoundError for dummy paths
        with self.assertRaises(FileNotFoundError):
            Repacker(self.options, self.repack_output_file)

    def test_repacker_missing_output_file(self):
        # Should raise ValueError if repack_output_file is None
        with self.assertRaises(ValueError):
            Repacker(self.options, None)

    def test_repacker_missing_options(self):
        # Should raise ValueError if options is None
        with self.assertRaises(ValueError):
            Repacker(None, self.repack_output_file)

if __name__ == "__main__":
    unittest.main()
