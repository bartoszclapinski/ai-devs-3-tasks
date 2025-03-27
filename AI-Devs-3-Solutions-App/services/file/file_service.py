import os
from types import SimpleNamespace
from typing import Optional, List
import json

class FileService:
    """
    Core file operations service.
    Handles basic file operations like reading, writing, checking existence, etc.
    """
    
    def __init__(self):
        self.root_dir = self._get_root_dir()
        self.storage_dir = os.path.join(self.root_dir, "files_storage")

    def _get_root_dir(self) -> str:
        """Get the root directory of the project."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go down to AI-Devs-3-Solutions-App directory
        return os.path.dirname((os.path.dirname(current_dir)))

    def read_file(self, file_path: str) -> SimpleNamespace:
        """
        Read content from a file.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            SimpleNamespace with:
                - success: bool indicating success/failure
                - content: str with file content if successful
                - error: str with error message if failed
        """
        try:
            if not os.path.exists(file_path):
                return SimpleNamespace(
                    success=False, 
                    error="File does not exist"
                )
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            return SimpleNamespace(success=True, content=content)
            
        except Exception as e:
            return SimpleNamespace(success=False, error=str(e))

    def write_file(self, file_path: str, content: str, mode: str = 'w') -> SimpleNamespace:
        """
        Write content to a file.
        
        Args:
            file_path: Path to the file to write
            content: Content to write
            mode: Write mode ('w' for overwrite, 'a' for append)
            
        Returns:
            SimpleNamespace with success status and optional error message
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)
                
            return SimpleNamespace(success=True)
            
        except Exception as e:
            return SimpleNamespace(success=False, error=str(e))

    def append_to_file(self, file_path: str, content: str) -> SimpleNamespace:
        """
        Append content to a file.
        
        Args:
            file_path: Path to the file to append to
            content: Content to append
            
        Returns:
            SimpleNamespace with success status and optional error message
        """
        return self.write_file(file_path, content, mode='a')

    def ensure_directory(self, directory_path: str) -> SimpleNamespace:
        """
        Ensure a directory exists, create if it doesn't.
        
        Args:
            directory_path: Path to the directory
            
        Returns:
            SimpleNamespace with success status and optional error message
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
            return SimpleNamespace(success=True)
        except Exception as e:
            return SimpleNamespace(success=False, error=str(e))

    def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            bool indicating if file exists
        """
        return os.path.exists(file_path)

    def list_files(self, directory: str, pattern: Optional[str] = None) -> List[str]:
        """
        List files in a directory, optionally filtered by pattern.
        
        Args:
            directory: Directory to list files from
            pattern: Optional pattern to filter files (e.g., "*.txt")
            
        Returns:
            List of file names
        """
        try:
            files = os.listdir(directory)
            if pattern:
                import fnmatch
                files = fnmatch.filter(files, pattern)
            return files
        except Exception:
            return []

    def delete_file(self, file_path: str) -> SimpleNamespace:
        """
        Delete a file.
        
        Args:
            file_path: Path to the file to delete
            
        Returns:
            SimpleNamespace with success status and optional error message
        """
        try:
            if self.file_exists(file_path):
                os.remove(file_path)
            return SimpleNamespace(success=True)
        except Exception as e:
            return SimpleNamespace(success=False, error=str(e))

    def get_storage_path(self, *paths: str) -> str:
        """
        Get full path in storage directory.
        
        Args:
            *paths: Path components to join with storage directory
            
        Returns:
            Full path in storage directory
        """
        return os.path.join(self.storage_dir, *paths) 