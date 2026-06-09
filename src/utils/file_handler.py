"""File upload and handling utilities."""

import os
import shutil
from pathlib import Path
from typing import Optional


class FileHandlerError(Exception):
    """Custom exception for file handling errors."""

    pass


class FileHandler:
    """Handle file operations like upload, validation, and storage."""

    # Allowed file extensions
    ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    ALLOWED_DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt"}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

    @staticmethod
    def validate_file_exists(file_path: str) -> bool:
        """
        Check if file exists at given path.

        Args:
            file_path: Path to file

        Returns:
            True if file exists, False otherwise

        Raises:
            FileHandlerError: If path is invalid
        """
        if not file_path:
            raise FileHandlerError("File path cannot be empty")

        return os.path.exists(file_path)

    @staticmethod
    def validate_file_extension(
        file_path: str, allowed_extensions: Optional[set] = None
    ) -> bool:
        """
        Validate file extension.

        Args:
            file_path: Path to file
            allowed_extensions: Set of allowed extensions (e.g., {'.jpg', '.png'})
                               If None, allows common extensions

        Returns:
            True if extension is allowed, False otherwise

        Raises:
            FileHandlerError: If file path is invalid
        """
        if not file_path:
            raise FileHandlerError("File path cannot be empty")

        file_ext = Path(file_path).suffix.lower()
        if not file_ext:
            raise FileHandlerError("File has no extension")

        if allowed_extensions is None:
            allowed_extensions = FileHandler.ALLOWED_IMAGE_EXTENSIONS | FileHandler.ALLOWED_DOCUMENT_EXTENSIONS

        return file_ext in allowed_extensions

    @staticmethod
    def validate_file_size(file_path: str, max_size: int = MAX_FILE_SIZE) -> bool:
        """
        Validate file size.

        Args:
            file_path: Path to file
            max_size: Maximum allowed file size in bytes (default: 5MB)

        Returns:
            True if file size is within limit, False otherwise

        Raises:
            FileHandlerError: If file doesn't exist
        """
        if not FileHandler.validate_file_exists(file_path):
            raise FileHandlerError(f"File not found: {file_path}")

        file_size = os.path.getsize(file_path)
        return file_size <= max_size

    @staticmethod
    def copy_file(source: str, destination: str, overwrite: bool = False) -> None:
        """
        Copy file from source to destination.

        Args:
            source: Source file path
            destination: Destination file path
            overwrite: Whether to overwrite existing file

        Raises:
            FileHandlerError: If source doesn't exist or destination exists
        """
        if not FileHandler.validate_file_exists(source):
            raise FileHandlerError(f"Source file not found: {source}")

        if os.path.exists(destination) and not overwrite:
            raise FileHandlerError(
                f"Destination file already exists: {destination}. Use overwrite=True to replace."
            )

        # Create destination directory if needed
        dest_dir = os.path.dirname(destination)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)

        shutil.copy2(source, destination)

    @staticmethod
    def move_file(source: str, destination: str, overwrite: bool = False) -> None:
        """
        Move file from source to destination.

        Args:
            source: Source file path
            destination: Destination file path
            overwrite: Whether to overwrite existing file

        Raises:
            FileHandlerError: If source doesn't exist or destination exists
        """
        if not FileHandler.validate_file_exists(source):
            raise FileHandlerError(f"Source file not found: {source}")

        if os.path.exists(destination) and not overwrite:
            raise FileHandlerError(
                f"Destination file already exists: {destination}. Use overwrite=True to replace."
            )

        # Create destination directory if needed
        dest_dir = os.path.dirname(destination)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)

        shutil.move(source, destination)

    @staticmethod
    def delete_file(file_path: str) -> None:
        """
        Delete file at given path.

        Args:
            file_path: Path to file

        Raises:
            FileHandlerError: If file doesn't exist
        """
        if not FileHandler.validate_file_exists(file_path):
            raise FileHandlerError(f"File not found: {file_path}")

        os.remove(file_path)

    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Get file size in bytes.

        Args:
            file_path: Path to file

        Returns:
            File size in bytes

        Raises:
            FileHandlerError: If file doesn't exist
        """
        if not FileHandler.validate_file_exists(file_path):
            raise FileHandlerError(f"File not found: {file_path}")

        return os.path.getsize(file_path)

    @staticmethod
    def get_file_name(file_path: str) -> str:
        """
        Get file name from path.

        Args:
            file_path: Path to file

        Returns:
            File name
        """
        return os.path.basename(file_path)

    @staticmethod
    def ensure_directory(directory_path: str) -> None:
        """
        Ensure directory exists, create if needed.

        Args:
            directory_path: Path to directory
        """
        if directory_path:
            os.makedirs(directory_path, exist_ok=True)
