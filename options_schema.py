from typing import Literal
from pathlib import Path

"""
# Patterns
* **should_** - Main action flags (e.g., `should_download_steam_game`)
* **force_** - Override/refresh flags (e.g., `force_download_dependencies`)
"""

OPTIONS_SCHEMA = {
    "LOG_LEVEL": {
        "env": "LOG_LEVEL",
        "arg": "--log-level",
        "type": Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        "default": "DEBUG",
        "section": "Logging",
        "help": "Logging level. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL."
    },
    "SHOULD_DOWNLOAD_DEPENDENCIES": {
        "env": "SHOULD_DOWNLOAD_DEPENDENCIES",
        "arg": "--should-download-dependencies",
        "type": bool,
        "default": False,
        "help": "Whether to download dependencies.",
        "section": "Dependencies",
    },
    "FORCE_DOWNLOAD_DEPENDENCIES": {
        "env": "FORCE_DOWNLOAD_DEPENDENCIES",
        "arg": "--force-download-dependencies",
        "type": bool,
        "default": False,
        "section": "Dependencies",
        "help": "Re-download dependencies even if they are already present.",
        "depends_on": ["SHOULD_DOWNLOAD_DEPENDENCIES"]
    },
    "SHOULD_DOWNLOAD_STEAM_GAME": {
        "env": "SHOULD_DOWNLOAD_STEAM_GAME",
        "arg": "--should-download-steam-game",
        "type": bool,
        "default": False,
        "help": "Whether to download Steam game files.",
        "section": "Steam Download",
    },
    "FORCE_STEAM_DOWNLOAD": {
        "env": "FORCE_STEAM_DOWNLOAD",
        "arg": "--force-steam-download",
        "type": bool,
        "default": False,
        "help": "Re-download/update Steam game files even if they are already present.",
        "section": "Steam Download",
        "depends_on": ["SHOULD_DOWNLOAD_STEAM_GAME"]
    },
    "MANIFEST_ID": {
        "env": "MANIFEST_ID",
        "arg": "--manifest-id",
        "type": str,
        "default": "",
        "help": "Steam manifest ID to download. If blank, the latest manifest ID will be used.",
        "links": {"SteamDB": "https://steamdb.info/app/1491000/depot/1491005/manifests/"},
        "section": "Steam Download",
        "depends_on": ["SHOULD_DOWNLOAD_STEAM_GAME"]
    },
    "STEAM_USERNAME": {
        "env": "STEAM_USERNAME",
        "arg": "--steam-username",
        "type": str,
        "default": None,
        "help": "Steam username for authentication.",
        "section": "Steam Download",
        "depends_on": ["SHOULD_DOWNLOAD_STEAM_GAME"]
    },
    "STEAM_PASSWORD": {
        "env": "STEAM_PASSWORD",
        "arg": "--steam-password",
        "type": str,
        "default": None,
        "sensitive": True,
        "help": "Steam password for authentication.",
        "section": "Steam Download",
        "depends_on": ["SHOULD_DOWNLOAD_STEAM_GAME"]
    },
    "STEAM_GAME_DOWNLOAD_DIR": {
        "env": "STEAM_GAME_DOWNLOAD_DIR",
        "arg": "--steam-game-download-dir",
        "type": Path,
        "default": None,
        "help": "Path to the local Steam game installation directory.",
        "help_extended": "Game should not be played from this directory if you have ran get_mapper. It will put dll files that will be flagged if not played local-only.",
        "section": "Steam Download",
        "depends_on": ["SHOULD_DOWNLOAD_STEAM_GAME", "SHOULD_REPACK"]
    },
    "SHOULD_REPACK": {
        "env": "SHOULD_REPACK",
        "arg": "--should-repack",
        "type": bool,
        "default": False,
        "help": "Whether to repack the game files into a single archive.",
        "section": "Repacking",
    },
    "FORCE_REPACK": {
        "env": "FORCE_REPACK",
        "arg": "--force-repack",
        "type": bool,
        "default": False,
        "help": "Force repacking even if the output file already exists.",
        "section": "Repacking",
        "depends_on": ["SHOULD_REPACK"]
    },
    "UE_INSTALL_DIR": {
        "env": "UE_INSTALL_DIR",
        "arg": "--ue-install-dir",
        "type": Path,
        "default": None,
        #"example": "C:\Program Files\Epic Games\UE_5.3",
        "help": "Path to the Unreal Engine 5.3 installation directory.",
        "section": "Repacking",
        "depends_on": ["SHOULD_REPACK"]
    },
    "REPACK_OUTPUT_FILE": {
        "env": "REPACK_OUTPUT_FILE",
        "arg": "--repack-output-file",
        "type": Path,
        "default": None,
        "help": "File path to save the repacked game archive to. Should end in .pak",
        "section": "Repacking",
        "depends_on": ["SHOULD_REPACK", "SHOULD_BATCH_EXPORT"]
    },
    "SHOULD_GET_MAPPER": {
        "env": "SHOULD_GET_MAPPER",
        "arg": "--should-get-mapper",
        "type": bool,
        "default": False,
        "help": "Whether to run the mapper extraction process.",
        "section": "Mapper",
    },
    "FORCE_GET_MAPPER": {
        "env": "FORCE_GET_MAPPER",
        "arg": "--force-get-mapper",
        "type": bool,
        "default": False,
        "help": "Re-run the mapper extraction even if mapper file exists.",
        "section": "Mapper",
        "depends_on": ["SHOULD_GET_MAPPER"]
    },
    "OUTPUT_MAPPER_FILE": {
        "env": "OUTPUT_MAPPER_FILE",
        "arg": "--output-mapper-file",
        "type": Path,
        "default": None,
        "help": "File path the mapping file (.usmap) will be saved to. Should end in .usmap",
        "section": "Batch Export",
        "depends_on": ["SHOULD_GET_MAPPER", "SHOULD_BATCH_EXPORT"]
    },
    "UE4SS_INSTALL_DIR": {
        "env": "UE4SS_INSTALL_DIR",
        "arg": "--ue4ss-install-dir",
        "type": Path,
        "default": None,
        "help": "Path to the UE4SS installation directory.",
        "section": "Batch Export",
        "depends_on": ["SHOULD_GET_MAPPER"]
    },
    "SHOULD_BATCH_EXPORT": {
        "env": "SHOULD_BATCH_EXPORT",
        "arg": "--should-batch-export",
        "type": bool,
        "default": False,
        "help": "Whether to run the BatchExport tool to export assets.",
        "section": "Batch Export",
    },
    "FORCE_EXPORT": {
        "env": "FORCE_EXPORT",
        "arg": "--force-export",
        "type": bool,
        "default": False,
        "help": "Re-run the BatchExport even if output directory is not empty.",
        "section": "Batch Export",
        "depends_on": ["SHOULD_BATCH_EXPORT"]
    },
    "OUTPUT_DATA_DIR": {
        "env": "OUTPUT_DATA_DIR",
        "arg": "--output-data-dir",
        "type": Path,
        "default": None,
        "help": "Path to save the exported assets to.",
        "section": "Batch Export",
        "depends_on": ["SHOULD_BATCH_EXPORT"]
    },
}