from pathlib import Path
import json
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Metadata:
    title: str
    author: str
    created: str
    modified: str
    subject: str = ""
    keywords: str = ""

class AdobeAcrobatMetadataReader:
    """Handles reading and writing metadata for PDF files."""

    @staticmethod
    def read(path: Path) -> Metadata:
        """Reads metadata from a JSON file at the given path.

        Args:
            path (Path): The path to the JSON file containing metadata.

        Returns:
            Metadata: An instance of the Metadata dataclass with parsed data.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            json.JSONDecodeError: If the file content is not valid JSON.
            KeyError: If required metadata fields are missing.
        """
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, 'r', encoding='utf-8') as file:
            try:
                data: Dict[str, Any] = json.load(file)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f"Error decoding JSON from {path}: {e}")

            try:
                return Metadata(
                    title=data['title'],
                    author=data['author'],
                    created=data['created'],
                    modified=data['modified'],
                    subject=data.get('subject', ""),
                    keywords=data.get('keywords', "")
                )
            except KeyError as e:
                raise KeyError(f"Missing required metadata field: {e}")

    @staticmethod
    def write(path: Path, metadata: Metadata) -> bool:
        """Writes metadata to a JSON file at the given path.

        Args:
            path (Path): The path to the JSON file where metadata will be written.
            metadata (Metadata): An instance of the Metadata dataclass to write.

        Returns:
            bool: True if the write operation was successful, False otherwise.

        Raises:
            IOError: If an I/O error occurs during writing.
        """
        try:
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(metadata.__dict__, file, ensure_ascii=False, indent=4)
            return True
        except IOError as e:
            raise IOError(f"Error writing to {path}: {e}") from e
