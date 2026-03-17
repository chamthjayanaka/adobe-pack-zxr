from pathlib import Path
from typing import Optional
import subprocess
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for common installation paths
INSTALLATION_PATHS = [
    Path("C:/Program Files/Adobe/Adobe Acrobat DC/Acrobat.exe"),
    Path("C:/Program Files (x86)/Adobe/Adobe Acrobat DC/Acrobat.exe"),
    Path("C:/Program Files/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe"),
    Path("C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe"),
]

def find_installation() -> Optional[Path]:
    """Find the installation path of Adobe Acrobat.

    Returns:
        Optional[Path]: The path to the Acrobat executable if found, otherwise None.
    """
    for path in INSTALLATION_PATHS:
        if path.exists():
            logging.info(f"Found installation at: {path}")
            return path
    logging.warning("Adobe Acrobat installation not found.")
    return None

def get_version() -> Optional[str]:
    """Get the version of Adobe Acrobat if installed.

    Returns:
        Optional[str]: The version number if found, otherwise None.
    """
    executable_path = get_executable_path()
    if executable_path:
        try:
            result = subprocess.run([str(executable_path), '--version'], capture_output=True, text=True)
            version = result.stdout.strip()
            logging.info(f"Adobe Acrobat version: {version}")
            return version
        except Exception as e:
            logging.error(f"Error retrieving version: {e}")
    return None

def is_installed() -> bool:
    """Check if Adobe Acrobat is installed.

    Returns:
        bool: True if installed, False otherwise.
    """
    installed = find_installation() is not None
    logging.info(f"Adobe Acrobat installed: {installed}")
    return installed

def get_executable_path() -> Optional[Path]:
    """Get the executable path of Adobe Acrobat.

    Returns:
        Optional[Path]: The path to the Acrobat executable if found, otherwise None.
    """
    path = find_installation()
    if path:
        return path
    return None
