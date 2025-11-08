# DarkAndDarker-Exporter

A comprehensive data extraction pipeline for Dark and Darker that downloads game files, creates a mapping file, and exports game assets to JSON format.


## Overview

DarkAndDarker-Exporter orchestrates a complete 4-step process the extract and convert Dark and Darker game data:

1. **Dependency Manager** - Downloads/updates all required dependencies
2. **Steam Download/Update** - Downloads/updates game files via DepotDownloader
3. **DLL Injection for Mapper** - Creates mapper file via game injection TODO
4. **BatchExport** - Converts game assets to JSON format


## Process Details

### 1. Dependency Manager
- Runs `dependency_manager.py` to download latest release of all dependencies if outdated/missing
- Downloads BatchExport and DepotDownloader tools from their respective GitHub releases
- Automatically checks versions and updates only when necessary

### 2. Steam Download/Update  
- Runs `run_depot_downloader` to download/update the latest War Robots Frontiers game version from Steam
- Download is saved at `STEAM_GAME_DOWNLOAD_DIR`
- Supports downloading specific manifest versions or latest version
- Uses Steam credentials for authentication
- Manifest id (if downloaded latest via `MANIFEST_ID`=`(blank)`) is saved to `STEAM_GAME_DOWNLOAD_DIR`/manifest.txt

### 3. DLL Injection for Mapper File
- todo

### 4. BatchExport
- Uses the mapper file and steam download
- Exports all `.pak`, `.utoc`, and `.locres` source files to `.json`
- Saves them in `OUTPUT_DATA_DIR`
- Converts game assets to human-readable JSON format


## Installation

1. Clone the repository:
```bash
git clone https://github.com/Surxe/WRFrontiers-Exporter.git
cd WRFrontiers-Exporter
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Copy and configure the environment file:
```bash
cp .env.example .env
# Edit .env with your specific paths and Steam credentials
```

4. Run the exporter:
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


#### Batch Export

* **OUTPUT_MAPPER_FILE** - File path the mapping file (.usmap) will be saved to. Should end in .usmap
  - Default: None - required when SHOULD_GET_MAPPER or SHOULD_BATCH_EXPORT is True
  - Command line: `--output-mapper-file`
  - Depends on: `SHOULD_GET_MAPPER`, `SHOULD_BATCH_EXPORT`

* **UE4SS_INSTALL_DIR** - Path to the UE4SS installation directory.
  - Default: None - required when SHOULD_GET_MAPPER is True
  - Command line: `--ue4ss-install-dir`
  - Depends on: `SHOULD_GET_MAPPER`

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

1. **DLL Injection Fails**
   - placeholder

2. **Steam Authentication Fails**
   - Verify your Steam username and password are correct
   - Check that Steam Guard is not blocking the login
   - Ensure DepotDownloader has the latest version

3. **Path Not Found Errors**
   - Verify all directory paths exist and are accessible
   - Use forward slashes (/) in paths for compatibility
   - Ensure parent directories exist for output paths


## Contributing

* After making changes to `options_schema.py`, rerun `build/docs.py` to rebuild the `.env.example` and `README.md`
* Follow standards set by `STANDARDS.md`


## Disclaimer

This tool is for educational and research purposes. Ensure you comply with the terms of service of Dark and Darker and Steam when using this software.