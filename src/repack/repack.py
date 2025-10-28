import os
import sys
from pathlib import Path
from typing import Optional
from loguru import logger
from optionsconfig import init_options, Options
from utils import run_process

class Repacker:
    """
    Handles extraction and repacking of Unreal Engine .pak files using UnrealPak.exe.
    """
    def __init__(self, options: Optional[Options] = None, repack_output_file: Optional[str] = None) -> None:
        if options is None:
            options = init_options()
        if repack_output_file is None:
            raise ValueError("repack_output_file is required for Repacker")
        self.options = options
        self.repack_output_file = repack_output_file
        self.ue_install_dir = options.ue_install_dir
        self.steam_game_download_dir = options.steam_game_download_dir
        self.crypto_json = Path(__file__).parent / "Crypto.json"
        self.pak_extract_dir = Path(__file__).parent / "PakExtract"
        self.unrealpak_exe = Path(self.ue_install_dir) / "Engine" / "Binaries" / "Win64" / "UnrealPak.exe"
        self.paks_dir = Path(self.steam_game_download_dir) / "DungeonCrawler" / "Content" / "Paks"
        self._validate_setup()

    def _validate_setup(self) -> None:
        if not Path(self.unrealpak_exe).exists():
            raise FileNotFoundError(f"UnrealPak.exe not found at {self.unrealpak_exe}")
        if not Path(self.crypto_json).exists():
            raise FileNotFoundError(f"Crypto.json not found at {self.crypto_json}")
        if not Path(self.paks_dir).exists():
            raise FileNotFoundError(f"PAK files directory not found: {self.paks_dir}")
        logger.info(f"Validated UnrealPak.exe, Crypto.json, and PAKs directory.")

    def extract_paks(self):
        logger.info(f"Extracting all .pak files from {self.paks_dir} to {self.pak_extract_dir}")
        for pak_file in Path(self.paks_dir).rglob("*.pak"):
            cmd = [
                str(self.unrealpak_exe),
                f"-cryptokeys=\"{self.crypto_json}\"",
                f"\"{pak_file}\"",
                f"-Extract", f"\"{self.pak_extract_dir}\"",
                "-extracttomountpoint"
            ]
            logger.info(f"Extracting {pak_file}")
            logger.debug(f"Command: {' '.join(f'\"{c}\"' if ' ' in c else c for c in cmd)}")
            run_process(options=cmd, name="UnrealPak Extract", timeout=1800)
        logger.success("Extraction of all .pak files completed.")

    def repack(self):
        logger.info(f"Repacking {self.repack_output_file} from {self.pak_extract_dir}")
        cmd = [
            str(self.unrealpak_exe),
            f"-cryptokeys=\"{self.crypto_json}\"",
            f"\"{self.repack_output_file}\"",
            f"-Create=\"{self.pak_extract_dir}\"",
            "-compress",
            "-compressionformat=Oodle"
        ]
        logger.debug(f"Command: {' '.join(f'\"{c}\"' if ' ' in c else c for c in cmd)}")
        run_process(options=cmd, name="UnrealPak Repack", timeout=1800)
        logger.success("Repacking completed.")

    def cleanup(self):
        logger.info(f"Cleaning up {self.pak_extract_dir}")
        if self.pak_extract_dir.exists():
            for root, dirs, files in os.walk(self.pak_extract_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.pak_extract_dir)
        logger.success("Cleanup completed.")

    def run(self):
        self.extract_paks()
        self.repack()
        self.cleanup()


def main(options: Optional[Options] = None, repack_output_file: Optional[str] = None):
    if options is None:
        raise ValueError("Options must be provided")
    if repack_output_file is None:
        raise ValueError("repack_output_file must be provided")
    try:
        repacker = Repacker(options, repack_output_file)
        repacker.run()
        logger.success("Repack process completed successfully!")
        return True
    except Exception as e:
        logger.error(f"Repack failed: {e}")
        raise
