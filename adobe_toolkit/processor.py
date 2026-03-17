from pathlib import Path
from typing import Dict, Any, List, Callable
import json
import logging
import PyPDF2

logging.basicConfig(level=logging.INFO)

class AdobeAcrobatProcessor:
    def __init__(self, client: 'AdobeAcrobatClient'):
        """
        Initializes the AdobeAcrobatProcessor with a client instance.

        :param client: An instance of AdobeAcrobatClient
        """
        self.client = client

    def process_file(self, path: Path, progress_callback: Callable[[str], None] = None) -> Dict[str, Any]:
        """
        Processes a PDF file to extract text and metadata.

        :param path: The path to the PDF file
        :param progress_callback: Optional callback to report progress
        :return: A dictionary containing extracted text and metadata
        """
        if not path.is_file():
            logging.error(f"File not found: {path}")
            return {}

        progress_callback and progress_callback(f"Processing file: {path.name}")

        try:
            text = self.extract_text(path)
            metadata = self.extract_metadata(path)
            result = {
                'text': text,
                'metadata': metadata
            }
            logging.info(f"Successfully processed file: {path.name}")
            return result
        except Exception as e:
            logging.error(f"Error processing file {path}: {e}")
            return {}

    def extract_text(self, path: Path) -> str:
        """
        Extracts text from a PDF file.

        :param path: The path to the PDF file
        :return: Extracted text as a string
        """
        try:
            with open(path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
            logging.info(f"Text extracted from {path.name}")
            return text
        except Exception as e:
            logging.error(f"Error extracting text from {path}: {e}")
            return ""

    def extract_metadata(self, path: Path) -> Dict:
        """
        Extracts metadata from a PDF file.

        :param path: The path to the PDF file
        :return: A dictionary containing metadata
        """
        try:
            with open(path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                metadata = reader.metadata
            logging.info(f"Metadata extracted from {path.name}")
            return metadata if metadata else {}
        except Exception as e:
            logging.error(f"Error extracting metadata from {path}: {e}")
            return {}

    def batch_process(self, paths: List[Path], progress_callback: Callable[[str], None] = None) -> List[Dict]:
        """
        Processes multiple PDF files in batch.

        :param paths: A list of paths to the PDF files
        :param progress_callback: Optional callback to report progress
        :return: A list of dictionaries containing extracted text and metadata for each file
        """
        results = []
        for path in paths:
            result = self.process_file(path, progress_callback)
            results.append(result)
            progress_callback and progress_callback(f"Completed processing: {path.name}")
        return results
