import concurrent.futures
from pathlib import Path
from typing import List, Callable, Optional
from dataclasses import dataclass
import logging
import fnmatch

logging.basicConfig(level=logging.INFO)

@dataclass
class Result:
    path: Path
    success: bool
    data: Optional[str] = None
    error: Optional[str] = None

class BatchProcessor:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def process_directory(self, path: Path, pattern: str = "*") -> List[Result]:
        """Process all files in a directory matching the given pattern.

        Args:
            path (Path): The directory path to process.
            pattern (str): The pattern to match files against.

        Returns:
            List[Result]: A list of results for each processed file.
        """
        if not path.is_dir():
            logging.error(f"The path {path} is not a directory.")
            return []

        files = [file for file in path.iterdir() if fnmatch.fnmatch(file.name, pattern)]
        return self.process_files(files)

    def process_files(self, paths: List[Path], callback: Optional[Callable] = None) -> List[Result]:
        """Process a list of files concurrently.

        Args:
            paths (List[Path]): List of file paths to process.
            callback (Callable, optional): A callback function to process each file.

        Returns:
            List[Result]: A list of results for each processed file.
        """
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_path = {executor.submit(self._process_file, path, callback): path for path in paths}

            for future in concurrent.futures.as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logging.error(f"Error processing {path}: {e}")
                    results.append(Result(path=path, success=False, error=str(e)))

        return results

    def _process_file(self, path: Path, callback: Optional[Callable]) -> Result:
        """Process a single file and return a Result.

        Args:
            path (Path): The file path to process.
            callback (Optional[Callable]): A callback function to process the file.

        Returns:
            Result: The result of processing the file.
        """
        try:
            if callback:
                data = callback(path)
            else:
                data = self._default_processing(path)

            return Result(path=path, success=True, data=data)
        except Exception as e:
            return Result(path=path, success=False, error=str(e))

    def _default_processing(self, path: Path) -> str:
        """Default file processing logic.

        Args:
            path (Path): The file path to process.

        Returns:
            str: A placeholder string indicating successful processing.
        """
        # Simulate processing logic
        return f"Processed {path.name}"
