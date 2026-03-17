import logging
import os
from pathlib import Path
from typing import Optional
import win32com.client

class AdobeAcrobatClient:
    """
    A client interface for interacting with Adobe Acrobat using the Windows COM interface.

    Attributes:
        config_path (Optional[Path]): Path to the configuration file.
        acrobat_app (Optional): The COM object for Adobe Acrobat application.
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initializes the AdobeAcrobatClient.

        Args:
            config_path (Optional[Path]): The path to the configuration file.
        """
        self.config_path = config_path
        self.acrobat_app = None
        self.setup_logging()

    def setup_logging(self) -> None:
        """Sets up the logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("adobe_acrobat_client.log"),
                logging.StreamHandler()
            ]
        )
        logging.info("Logging is set up.")

    def connect(self) -> bool:
        """
        Connects to the Adobe Acrobat application.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        try:
            self.acrobat_app = win32com.client.Dispatch("AcroExch.App")
            self.acrobat_app.Show()
            logging.info("Connected to Adobe Acrobat.")
            return True
        except Exception as e:
            logging.error(f"Failed to connect to Adobe Acrobat: {e}")
            return False

    def disconnect(self) -> None:
        """Disconnects from the Adobe Acrobat application."""
        if self.acrobat_app:
            self.acrobat_app.Exit()
            self.acrobat_app = None
            logging.info("Disconnected from Adobe Acrobat.")
        else:
            logging.warning("No active connection to disconnect.")

    def get_version(self) -> str:
        """
        Retrieves the version of the Adobe Acrobat application.

        Returns:
            str: The version of Adobe Acrobat.

        Raises:
            RuntimeError: If the application is not connected.
        """
        if not self.acrobat_app:
            raise RuntimeError("Adobe Acrobat is not connected.")
        
        try:
            version = self.acrobat_app.GetVersion()
            logging.info(f"Adobe Acrobat version: {version}")
            return version
        except Exception as e:
            logging.error(f"Failed to get version: {e}")
            raise RuntimeError("Could not retrieve version information.")

    def is_installed(self) -> bool:
        """
        Checks if Adobe Acrobat is installed on the system.

        Returns:
            bool: True if Adobe Acrobat is installed, False otherwise.
        """
        installed = os.path.exists(r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe") or \
                    os.path.exists(r"C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe")
        logging.info(f"Adobe Acrobat installed: {installed}")
        return installed
