from dotenv import load_dotenv

import os
import subprocess
import os
import shutil
from loguru import logger
from typing import Union, List, Optional, Any
load_dotenv()

###############################
#             FILE            #
###############################

def clear_dir(dir_path: str) -> None:
    """Clear directory contents but keep the directory itself"""
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)

def normalize_path(path: str) -> str:
    """Normalize a file path to use forward slashes for cross-platform consistency."""
    # Use os.path.normpath to normalize the path properly for the current platform
    # This ensures drive letters and absolute paths are handled correctly
    normalized = os.path.normpath(path)
    # Only convert backslashes to forward slashes for display consistency in tests
    # but preserve the platform-specific absolute path characteristics
    return normalized.replace('\\', '/')


###############################
#           Process           #
###############################

def kill_process_tree(parent_pid) -> None:
    """Kill a parent process and all its children.
    
    Args:
        parent_pid: The process ID of the parent process to kill
    """
    try:
        import psutil  # Import here to avoid making psutil a requirement for other utils
        parent = psutil.Process(parent_pid)
        children = parent.children(recursive=True)
        
        for child in children:
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
            
        parent.kill()
    except (psutil.NoSuchProcess, ImportError) as e:
        logger.warning(f"Error killing process tree: {e}")

def ensure_parent_dir(file_path: str) -> None:
    """Ensure the parent directory of a file exists.
    
    Args:
        file_path: The path to the file whose parent directory should exist
    """
    parent_dir = os.path.dirname(file_path)
    os.makedirs(parent_dir, exist_ok=True)

def run_process(options: Union[List[str], str], name: str = '', timeout: int = 60*60, background: bool = False) -> Optional[subprocess.Popen]: #times out after 1hr
    """Runs a subprocess with the given options and logs its output line by line

    Args:
        options (list[str] | str): The command and arguments to execute
        name (str, optional): An optional name to identify the process in logs. Defaults to ''
        timeout (int, optional): Maximum time to wait for process completion in seconds. Defaults to 3600 (1 hour)
        background (bool, optional): If True, starts the process in background and returns the process object. Defaults to False.
    
    Returns:
        subprocess.Popen: If background=True, returns the process object for later management
        None: If background=False (default), waits for completion and returns None
    """
    import select
    import time
    
    process = None
    try:
        # Handle shell scripts on Windows by explicitly using bash
        if isinstance(options, str) and options.endswith('.sh') and os.name == 'nt':
            options = ['bash', options]
        elif isinstance(options, list) and len(options) > 0 and options[0].endswith('.sh') and os.name == 'nt':
            options = ['bash'] + options

        process = subprocess.Popen(  # noqa: F821
            options, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

        # If background mode, return the process object immediately
        if background:
            logger.info(f'Started background process {name} with PID {process.pid}')
            return process

        start_time = time.time()
        
        # Read output line by line with timeout protection
        with process.stdout:
            while True:
                # Check if process has finished
                if process.poll() is not None:
                    # Process finished, read any remaining output
                    remaining_output = process.stdout.read()
                    if remaining_output:
                        for line in remaining_output.splitlines():
                            logger.debug(f'[process: {name}] {line.strip()}')
                    break
                
                # Check timeout
                if time.time() - start_time > timeout:
                    process.terminate()
                    try:
                        process.wait(timeout=5)  # Give it 5 seconds to terminate gracefully
                    except subprocess.TimeoutExpired:
                        process.kill()  # Force kill if it doesn't terminate
                    raise Exception(f'Process {name} timed out after {timeout} seconds')
                
                # Use select on Unix-like systems for non-blocking read
                if hasattr(select, 'select') and os.name != 'nt':
                    ready, _, _ = select.select([process.stdout], [], [], 0.1)
                    if ready:
                        line = process.stdout.readline()
                        if line:
                            logger.debug(f'[process: {name}] {line.strip()}')
                        elif process.poll() is not None:
                            # Process finished and no more output
                            break
                else:
                    # Windows fallback - read with short timeout simulation
                    try:
                        line = process.stdout.readline()
                        if line:
                            logger.debug(f'[process: {name}] {line.strip()}')
                        elif process.poll() is not None:
                            # Process finished and no more output
                            break
                    except Exception:
                        # If readline fails, check if process is still running
                        if process.poll() is not None:
                            break
                        time.sleep(0.1)  # Brief pause to prevent tight loop

    except Exception as e:
        # Clean up process if it's still running
        if process and process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        raise Exception(f'Failed to run {name} process', e)

    # Wait for process to complete and get exit code
    exit_code = process.wait()
    if exit_code != 0:
        raise Exception(f'Process {name} exited with code {exit_code}')