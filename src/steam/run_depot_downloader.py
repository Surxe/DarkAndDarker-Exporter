import os
import shutil
from pathlib import Path
from loguru import logger
from utils import run_process
from typing import Optional

APP_ID = '2016590'  # war robots: frontier's app_id
DEPOT_ID = '2016591'  # the big depot


class DepotDownloader:
    def __init__(self, wrf_dir: str, steam_username: str, steam_password: str, force: bool) -> None:
        self.depot_downloader_cmd_path = 'src/steam/DepotDownloader/DepotDownloader.exe'
        if not os.path.exists(self.depot_downloader_cmd_path):
            raise Exception('Is DepotDownloader installed? Run dependency_manager.py')
        if not steam_username or not steam_password:
            raise Exception('Steam username and password are required')

        self.app_id = APP_ID
        self.depot_id = DEPOT_ID

        self.steam_username = steam_username
        self.steam_password = steam_password
        self.wrf_dir = wrf_dir
        self.manifest_path = os.path.join(self.wrf_dir, 'manifest.txt')
        self.force = force

    def run(self, manifest_id: Optional[str | None]) -> None:
        # no input manifest id downloads the latest version
        if manifest_id is None:
            manifest_id = self._get_latest_manifest_id()
            logger.debug(f"DepotDownloader retrieved latest manifest id of: {manifest_id}")

        # Check if the manifest is already downloaded
        downloaded_manifest_id = self._read_downloaded_manifest_id()
        if downloaded_manifest_id == manifest_id and not self.force:
            logger.info(f'Already downloaded manifest {manifest_id}')
            return True

        self._download(manifest_id)
        self._write_downloaded_manifest_id(manifest_id)
        self._remove_steam_api_dll()

        return True

    def _download(self, manifest_id: str) -> None:
        logger.debug(f'Downloading game with manifest id {manifest_id}')

        subprocess_options = [
            os.path.join(self.depot_downloader_cmd_path),
            '-app', self.app_id,
            '-depot', self.depot_id,
            '-manifest', manifest_id,
            '-username', self.steam_username,
            '-password', self.steam_password,
            '-remember-password',
            '-dir', self.wrf_dir,
        ]
        run_process(subprocess_options, name='download-game-files')

        #TODO, verify files are downloaded

    def _read_downloaded_manifest_id(self) -> Optional[str]:
        if not os.path.exists(self.manifest_path):
            return None

        with open(self.manifest_path, 'r') as f:
            manifest_id = f.read().strip()
        return manifest_id

    def _get_latest_manifest_id(self) -> Optional[str]:
        # create temporary folder to store manifest file
        temp_dir = os.path.join(self.wrf_dir, 'temp')

        subprocess_options = [
            os.path.join(self.depot_downloader_cmd_path),
            '-app',
            self.app_id,
            '-depot',
            self.depot_id,
            '-username',
            self.steam_username,
            '-password',
            self.steam_password,
            '-remember-password',
            '-dir',
            temp_dir,
            '-manifest-only',
            '-validate',
        ]
        run_process(subprocess_options, name='get-latest-manifest-id')

        manifest_id = None
        for filename in os.listdir(temp_dir):
            if filename.startswith('manifest'):
                # manifest formatted as manifest_<depot_id>_<manifest_id>.txt
                manifest_id = filename.replace('manifest_', '').replace('.txt', '').split('_')[-1]

        shutil.rmtree(temp_dir)
        return manifest_id

    def _write_downloaded_manifest_id(self, manifest_id: str) -> None:
        logger.debug('Writing manifest id', manifest_id, 'to', self.manifest_path)
        with open(self.manifest_path, 'w') as f:
            f.write(manifest_id)

    def _remove_steam_api_dll(self) -> None:
        try:
            steam_api_dll_path = Path(self.wrf_dir) / "Engine" / "Binaries" / "ThirdParty" / "Steamworks" / "Steamv153" / "Win64" / "steam_api64.dll"
            if steam_api_dll_path.exists():
                steam_api_dll_path.unlink()
                logger.debug(f'Removed {steam_api_dll_path}')
            else:
                logger.debug(f'steam_api64.dll not found at {steam_api_dll_path}, skipping removal')
                logger.debug('Is the dll named differently for you? If so, we should probably add the file name as an option.')
        except (FileNotFoundError, OSError) as e:
            logger.debug(f'Could not remove steam_api64.dll: {e}')