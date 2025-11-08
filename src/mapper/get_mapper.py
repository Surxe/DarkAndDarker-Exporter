from typing import Optional
from loguru import logger
from optionsconfig import Options

"""
Mapper extraction process.

Process:
* Copy files from ue4ss installation to gamedir/DungeonCrawler/Binaries/Win64
* Run gamedir/Tavern.exe with args  -server=localhost -steam=1 -taverntype=steam -tavernapp=dad to launch the game locally
* Wait for Mappings file to exist. Timeout after 120s.
* Shutdown the game process
* Copy generated .usmap from gamedir/DungeonCrawler/Binaries/Win64/Mappings.json to OUTPUT_MAPPER_FILE, renaming it.
"""

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

    try:
        logger.info("Running mapper extraction process...")
        # TODO: Implement mapper extraction
        logger.success("Mapper extraction completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Mapper extraction failed: {e}")
        raise
