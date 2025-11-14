# DarkAndDarker-Exporter

A comprehensive data extraction pipeline for Dark and Darker that downloads game files, creates a mapping file, and exports game assets & textures to JSON/PNG.


## Overview

DarkAndDarker-Exporter orchestrates a complete 4-step process the extract and convert Dark and Darker game data:

1. **Dependency Manager** - Downloads/updates all required dependencies
2. **Steam Download/Update** - Downloads/updates game files via DepotDownloader
3. **Repack** - Repacks to avoid duplicate paks with differing data
4. **Get Mapper** - Creates mapper file via UE4SS
5. **BatchExport** - Extracts game assets as JSON or PNG via CUE4P-BatchExport

Assets are exported "as is", meaning it does not perform any alterations on the source data and therefore will not break when developers make changes to the file structure.

## Table of Contents

- [DarkAndDarker-Exporter](#darkanddarker-exporter)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Process Details](#process-details)
    - [1. Dependency Manager](#1-dependency-manager)
    - [2. Steam Download/Update](#2-steam-downloadupdate)
    - [3. Repack](#3-repack)
    - [4. Get Mapper File](#4-get-mapper-file)
    - [5. BatchExport](#5-batchexport)
  - [Prerequisites](#prerequisites)
    - [Windows Operating System](#windows-operating-system)
    - [Unreal Engine 5.3](#unreal-engine-53)
    - [Steam account](#steam-account)
  - [Installation](#installation)
  - [Options](#options)
    - [Command Line Argument Usage](#command-line-argument-usage)
    - [Parameters](#parameters)
      - [Logging](#logging)
      - [Dependencies](#dependencies)
      - [Steam Download](#steam-download)
      - [Repacking](#repacking)
      - [Mapper](#mapper)
      - [Batch Export](#batch-export)
    - [Miscellaneous Option Behavior](#miscellaneous-option-behavior)
    - [Common Issues](#common-issues)
    - [Safety Concerns](#safety-concerns)
      - [Is it a bannable offense?](#is-it-a-bannable-offense)
      - [Why is it safe to run?](#why-is-it-safe-to-run)
  - [Contributing](#contributing)
    - [Future Ideas](#future-ideas)
  - [Disclaimer](#disclaimer)

## Process Details

### 1. Dependency Manager
- Runs `dependency_manager.py` to download latest release of all dependencies if outdated/missing
- Downloads [CUE4P-BatchExport](https://github.com/Surxe/CUE4P-BatchExport), [DepotDownloader](https://github.com/SteamRE/DepotDownloader), and [UE4SS](https://github.com/UE4SS-RE/RE-UE4SS) tools from their respective GitHub releases
- Automatically checks versions and updates only when the version changes

### 2. Steam Download/Update  
- Runs `run_depot_downloader` to download/update the latest Dark and Darker game version from Steam
  - It is not recommended to pass your existing DaD installation
- Download is saved at `STEAM_GAME_DOWNLOAD_DIR`
- Supports downloading specific manifest versions or latest version
- Uses Steam credentials for authentication
  - It is recommended to create a separate steam account
  - You may find it easiest to disable SteamGuard 2FA, but this is only recommended in combination with using a separate steam account
- Manifest id (if downloaded latest via `MANIFEST_ID`=`(blank)`) is saved to `STEAM_GAME_DOWNLOAD_DIR`/manifest.txt
- Steam API DLL is removed from the installation at `Engine\Binaries\ThirdParty\Steamworks\Steamv153\Win64\steam_api64.dll` so that it does not interact with a steam installation

### 3. Repack
- Uses UnrealPak.exe from local Unreal Engine 5.3 installation
- Extracts all .pak files from game directory using Crypto.json keys
- Extracts to a temporary "PakExtract" directory with -extracttomountpoint flag
- Repacks all content into a single .pak file with Oodle compression
- Output is saved to `REPACK_OUTPUT_FILE`
- Cleans up the temporary extraction directory after repacking

### 4. Get Mapper File
- Copies UE4SS files to game's DungeonCrawler/Binaries/Win64 directory
- Sets up UE4SS AutoUSMAP mod in the Mods directory
- Launches game with required arguments and `server=localhost` so that it does connect to DaD servers
- Waits for UE4SS to hook into the process and generate mapping file
- Monitors file generation with 120-second timeout
- Checks file write access every 3 seconds with 30-second timeout
- Copies generated .usmap file to `OUTPUT_MAPPER_FILE`
- Cleans up temporary files after extraction

### 5. BatchExport
- Uses the mapper file and steam download
- Exports all `.pak`, `.utoc`, and `.locres` source files to `.json` and/or `.png`
- Saves them in `OUTPUT_DATA_DIR`
- Converts game assets to human-readable JSON format
- Extracts texture assets to PNG format

## Prerequisites
DepotDownloader, BatchExport, and UE4SS are all downloaded via `dependendency_manager`.

### Windows Operating System
A Windows Operating System is required specifically for launching Dark and Darker for retrieving the `.usmap` file. For obtaining the mappings headless with linux through wine, see [ynot01/headless-darker](https://github.com/ynot01/headless-darker). For running without Windows, you can get the mapping from another source, then use `SHOULD_GET_MAPPER="False"` and provide the mappings path for the batch export step.

### Unreal Engine 5.3
[Unreal Engine 5.3](https://www.unrealengine.com/en-US/download) however, needs to be installed before hand. 

Specifically UE5.3 should be installed, not the latest version. This is the version DaD runs on. 

Include the following in your installation which should total roughly 40gb at the time of writing:
* Core Components
* Starter Components
* Templates and Feature Packs
* Engine Source
* NOT Editor symbols for debugging
* NOT Android
* NOT IOS
* NOT Linux
* NOT TVOS

### Steam account
A steam account with Dark and Darker added to its library. The Legendary status is not necessary, so it can be added for free if you otherwise play on Blacksmith/Epic Games.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Surxe/DarkAndDarker-Exporter.git
cd DarkAndDarker-Exporter
```

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

1. Copy and configure the environment file:
```bash
cp .env.example .env
# Edit .env with your specific paths and Steam credentials
```

1. Run the exporter:
```bash
python src/run.py --help
```


## Options

### Command Line Argument Usage

For each option, the command line argument may be used at runtime instead of providing it in the `.env`.

```bash
python src/run.py                       # Run all steps with default/env values
python src/run.py --log-level INFO      # Run all steps with default/env values, except with LOG_LEVEL INFO
```

### Parameters

Copy `.env.example` to `.env` and configure the following parameters, unless they will be provided as arguments at runtime:

<!-- BEGIN_GENERATED_OPTIONS -->
#### Logging

- **LOG_LEVEL** - Logging level. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL.
  - Default: `"DEBUG"`
  - Command line: `--log-level`


#### Dependencies

- **SHOULD_DOWNLOAD_DEPENDENCIES** - Whether to download dependencies.
  - Default: `"false"`
  - Command line: `--should-download-dependencies`

* **FORCE_DOWNLOAD_DEPENDENCIES** - Re-download dependencies even if they are already present.
  - Default: `"false"`
  - Command line: `--force-download-dependencies`
  - Depends on: `SHOULD_DOWNLOAD_DEPENDENCIES`


#### Steam Download

- **SHOULD_DOWNLOAD_STEAM_GAME** - Whether to download Steam game files.
  - Default: `"false"`
  - Command line: `--should-download-steam-game`

* **FORCE_STEAM_DOWNLOAD** - Re-download/update Steam game files even if they are already present.
  - Default: `"false"`
  - Command line: `--force-steam-download`
  - Depends on: `SHOULD_DOWNLOAD_STEAM_GAME`

* **MANIFEST_ID** - Steam manifest ID to download. If blank, the latest manifest ID will be used.
  - Default: `""` (empty)
  - Command line: `--manifest-id`
  - Depends on: `SHOULD_DOWNLOAD_STEAM_GAME`
  - See [SteamDB](https://steamdb.info/app/1491000/depot/1491005/manifests/) for available values

* **STEAM_USERNAME** - Steam username for authentication.
  - Default: None - required when SHOULD_DOWNLOAD_STEAM_GAME is True
  - Command line: `--steam-username`
  - Depends on: `SHOULD_DOWNLOAD_STEAM_GAME`

* **STEAM_PASSWORD** - Steam password for authentication.
  - Default: None - required when SHOULD_DOWNLOAD_STEAM_GAME is True
  - Command line: `--steam-password`
  - Depends on: `SHOULD_DOWNLOAD_STEAM_GAME`

* **STEAM_GAME_DOWNLOAD_DIR** - Path to the local Steam game installation directory.
  - Default: None - required when SHOULD_DOWNLOAD_STEAM_GAME or SHOULD_REPACK is True
  - Command line: `--steam-game-download-dir`
  - Depends on: `SHOULD_DOWNLOAD_STEAM_GAME`, `SHOULD_REPACK`
  - Game should not be played from this directory if you have ran get_mapper. It will put dll files that will be flagged if not played local-only.


#### Repacking

- **SHOULD_REPACK** - Whether to repack the game files into a single archive.
  - Default: `"false"`
  - Command line: `--should-repack`

* **FORCE_REPACK** - Force repacking even if the output file already exists.
  - Default: `"false"`
  - Command line: `--force-repack`
  - Depends on: `SHOULD_REPACK`

* **UE_INSTALL_DIR** - Path to the Unreal Engine 5.3 installation directory.
  - Default: None - required when SHOULD_REPACK is True
  - Command line: `--ue-install-dir`
  - Depends on: `SHOULD_REPACK`

* **REPACK_OUTPUT_FILE** - File path to save the repacked game archive to. Should end in .pak
  - Default: None - required when SHOULD_REPACK or SHOULD_BATCH_EXPORT is True
  - Command line: `--repack-output-file`
  - Depends on: `SHOULD_REPACK`, `SHOULD_BATCH_EXPORT`


#### Mapper

- **SHOULD_GET_MAPPER** - Whether to run the mapper extraction process.
  - Default: `"false"`
  - Command line: `--should-get-mapper`

* **FORCE_GET_MAPPER** - Re-run the mapper extraction even if mapper file exists.
  - Default: `"false"`
  - Command line: `--force-get-mapper`
  - Depends on: `SHOULD_GET_MAPPER`

* **OUTPUT_MAPPER_FILE** - File path the mapping file (.usmap) will be saved to. Should end in .usmap
  - Default: None - required when SHOULD_GET_MAPPER or SHOULD_BATCH_EXPORT is True
  - Command line: `--output-mapper-file`
  - Depends on: `SHOULD_GET_MAPPER`, `SHOULD_BATCH_EXPORT`


#### Batch Export

- **SHOULD_BATCH_EXPORT** - Whether to run the BatchExport tool to export assets.
  - Default: `"false"`
  - Command line: `--should-batch-export`

* **FORCE_EXPORT** - Re-run the BatchExport even if output directory is not empty.
  - Default: `"false"`
  - Command line: `--force-export`
  - Depends on: `SHOULD_BATCH_EXPORT`

* **OUTPUT_DATA_DIR** - Path to save the exported assets to.
  - Default: None - required when SHOULD_BATCH_EXPORT is True
  - Command line: `--output-data-dir`
  - Depends on: `SHOULD_BATCH_EXPORT`


<!-- END_GENERATED_OPTIONS -->

### Miscellaneous Option Behavior

* An option's value is determined by the following priority, in descending order
  * Argument
  * Option
  * Default
* If all options prefixed with `SHOULD_` are defaulted to `False`, they are instead all defaulted to `True` for ease of use
* Options are only required if their section's root `SHOULD_` option is `True`


### Common Issues

1. **Steam Authentication Fails**
   - Verify your Steam username and password are correct
   - Check that Steam Guard is not blocking the login
   - Ensure DepotDownloader has the latest version

2. **Path Not Found Errors**
   - Verify all directory paths exist and are accessible
   - Use forward slashes (/) in paths for compatibility
   - Ensure parent directories exist for output paths

### Safety Concerns
#### Is it a bannable offense?
If used for malicious purposes, yes

#### Why is it safe to run?
* Dark and Darker is launched with `server=localhost` so it does not connect to their servers
* Steam API DLL is removed, so launching DaD does not connect to Steamworks
* An alternate steam account is still recommended, particularly for logging in to the account to download the game without needing to satisfy SteamGuard notifications
* If recommendations are not met or usage of this tool is modified, these safety nets may cease to apply

## Contributing

* After making changes to `options_schema.py`, rerun `build/docs.py` to rebuild the `.env.example` and `README.md`
* *Try* to follow standards set by `STANDARDS.md`

### Future Ideas
* Linux or wine support (DaD struggles to launch headless with wine)
* Unreal Engine 5.3 installation added to `dependency_manager`
  * Is an Epic Games Launcher install also required?
  * Is an EGL account required?
  * Does rerunning the install to the same dir perform a repair that doesn't take as long as a clean install?


## Disclaimer

This tool is for educational and research purposes. Ensure you comply with the terms of service of Dark and Darker and Steam when using this software.