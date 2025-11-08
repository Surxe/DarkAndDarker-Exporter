import os
import time
import shutil
import psutil
from pathlib import Path
from typing import Optional
from loguru import logger
from optionsconfig import Options
from utils import run_process

"""
Mapper extraction process via UE4SS.

Process:
* Copy files from ue4ss installation (src/mapper/ue4ss/UE4SS_v3.0.1) to gamedir/DungeonCrawler/Binaries/Win64
* Copy src/mapper/ue4ss_mod/AutoUSMAP/ to gamedir/DungeonCrawler/Binaries/Win64/Mods/AutoUSMAP
* Copy src/mapper/ue4ss_mod/mods.txt to gamedir/DungeonCrawler/Binaries/Win64/Mods/mods.txt, overwriting if exists.
* Run gamedir/Tavern.exe with args  -server=localhost -steam=1 -taverntype=steam -tavernapp=dad to launch the game locally. UE4SS hooks into the game process.
* Wait for Mappings file to exist. Timeout after 120s. 
* Shutdown the game process
* Copy generated .usmap from gamedir/DungeonCrawler/Binaries/Win64/Mappings.json to OUTPUT_MAPPER_FILE, renaming it.
"""

def kill_process_tree(parent_pid):
    """Kill a parent process and all its children."""
    try:
        parent = psutil.Process(parent_pid)
        children = parent.children(recursive=True)
        
        for child in children:
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
            
        parent.kill()
    except psutil.NoSuchProcess:
        pass

def ensure_parent_dir(file_path: str) -> None:
    """Ensure the parent directory of a file exists."""
    parent_dir = os.path.dirname(file_path)
    os.makedirs(parent_dir, exist_ok=True)

def setup_ue4ss(steam_game_dir: str) -> None:
    """Setup UE4SS files in the game directory."""
    logger.info("Setting up UE4SS files...")
    
    # Paths
    src_dir = Path(__file__).parent
    bin_dir = Path(steam_game_dir) / "DungeonCrawler" / "Binaries" / "Win64"
    mods_dir = bin_dir / "Mods"
    
    # Create Mods directory
    os.makedirs(mods_dir, exist_ok=True)
    
    # Copy UE4SS installation files
    ue4ss_src = src_dir / "ue4ss" / "UE4SS_v3.0.1"
    if not ue4ss_src.exists():
        raise FileNotFoundError(f"UE4SS installation not found at {ue4ss_src}")
    logger.info(f"Copying UE4SS files from {ue4ss_src} to {bin_dir}")
    shutil.copytree(ue4ss_src, bin_dir, dirs_exist_ok=True)
    
    # Copy mod files
    automap_src = src_dir / "ue4ss_mod" / "AutoUSMAP"
    if not automap_src.exists():
        raise FileNotFoundError(f"AutoUSMAP mod not found at {automap_src}")
    logger.info(f"Copying AutoUSMAP mod to {mods_dir}")
    shutil.copytree(automap_src, mods_dir / "AutoUSMAP", dirs_exist_ok=True)
    
    # Copy mods.txt
    mods_txt_src = src_dir / "ue4ss_mod" / "mods.txt"
    if not mods_txt_src.exists():
        raise FileNotFoundError(f"mods.txt not found at {mods_txt_src}")
    mods_dest = mods_dir / "mods.txt"
    logger.info(f"Copying mods.txt to {mods_dest}")
    shutil.copy2(mods_txt_src, mods_dest)

def main(options: Optional[Options] = None) -> bool:
    """
    Main function to run the mapper extraction process.
    
    Args:
        options (Options): Configuration options
        
    Returns:
        bool: True if successful, False otherwise
    """
    if options is None:
        raise ValueError("Options must be provided")
    
    if not options.output_mapper_file:
        raise ValueError("OUTPUT_MAPPER_FILE must be set")

    try:
        logger.info("Running mapper extraction process...")
        
        # Setup paths
        game_dir = options.steam_game_download_dir
        bin_dir = Path(game_dir) / "DungeonCrawler" / "Binaries" / "Win64"
        mappings_file = bin_dir / "Mappings.usmap"
        
        # Skip if output exists and force is False
        if os.path.exists(options.output_mapper_file) and not options.force_get_mapper:
            logger.info(f"Mapper file already exists at {options.output_mapper_file} and FORCE_GET_MAPPER is False. Skipping mapper extraction.")
            return True
        
        # Ensure parent directory exists
        ensure_parent_dir(options.output_mapper_file)
        
        # Setup UE4SS and mods
        setup_ue4ss(game_dir)
        
        # Run the game with required arguments
        tavern_exe = Path(game_dir) / "Tavern.exe"
        if not tavern_exe.exists():
            raise FileNotFoundError(f"Tavern.exe not found at {tavern_exe}")
        
        logger.info("Starting game process...")
        game_process = run_process(
            options=[
                str(tavern_exe),
                "-server=localhost",
                "-steam=1",
                "-taverntype=steam",
                "-tavernapp=dad"
            ],
            name="DarkAndDarker",
            background=True
        )
        logger.info(f"Waiting for game to launch, UE4SS to hook, and mappings file to be generated at {mappings_file}...")
        
        # Wait for mappings file with timeout
        timeout = 120  # 2 minutes
        start_time = time.time()
        while not mappings_file.exists():
            time_waited = time.time() - start_time
            if time_waited > timeout:
                kill_process_tree(game_process.pid)
                raise TimeoutError(f"Timed out waiting for mappings file after {timeout} seconds")
            time.sleep(5)
            logger.info(f"Waiting for mappings file to be generated. Time waited: {time_waited:.2f} seconds / {timeout} seconds")

        logger.info("Mappings file located. Waiting 5 more seconds to ensure file is fully written...")
        time.sleep(5)
        
        logger.info("Mappings file generated successfully")
        
        # Kill the game process
        logger.info("Shutting down game process...")
        kill_process_tree(game_process.pid)
        
        # Copy the mappings file to output location
        logger.info(f"Copying mappings file to {options.output_mapper_file}")
        shutil.copy2(mappings_file, options.output_mapper_file)

        # Remove the mappings file from the binary directory
        logger.info(f"Removing temporary mappings file at {mappings_file}")
        os.remove(mappings_file)
        
        logger.success("Mapper extraction completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Mapper extraction failed: {e}")
        raise
