"""Image processing and handling utilities."""

from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image

from src.utils.file_handler import FileHandler, FileHandlerError


class ImageHandlerError(Exception):
    """Custom exception for image handling errors."""

    pass


class ImageHandler:
    """Handle image processing, resizing, and format conversion."""

    # Supported image formats
    SUPPORTED_FORMATS = {"JPEG", "PNG", "GIF", "BMP", "TIFF"}
    MAX_WIDTH = 1200
    MAX_HEIGHT = 1200
    THUMBNAIL_SIZE = (150, 150)

    @staticmethod
    def load_image(file_path: str) -> Image.Image:
        """
        Load image from file.

        Args:
            file_path: Path to image file

        Returns:
            PIL Image object

        Raises:
            ImageHandlerError: If file is not a valid image
        """
        try:
            if not FileHandler.validate_file_exists(file_path):
                raise ImageHandlerError(f"Image file not found: {file_path}")

            if not FileHandler.validate_file_extension(
                file_path, FileHandler.ALLOWED_IMAGE_EXTENSIONS
            ):
                raise ImageHandlerError(f"Unsupported image format: {file_path}")

            image = Image.open(file_path)
            image.load()  # Verify image is valid
            return image
        except ImageHandlerError:
            raise
        except Exception as e:
            raise ImageHandlerError(f"Failed to load image: {str(e)}")

    @staticmethod
    def resize_image(
        image: Image.Image,
        max_width: int = MAX_WIDTH,
        max_height: int = MAX_HEIGHT,
        maintain_aspect: bool = True,
    ) -> Image.Image:
        """
        Resize image to fit within dimensions.

        Args:
            image: PIL Image object
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels
            maintain_aspect: Whether to maintain aspect ratio

        Returns:
            Resized PIL Image object
        """
        if not isinstance(image, Image.Image):
            raise ImageHandlerError("Input must be a PIL Image object")

        if maintain_aspect:
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        else:
            image = image.resize((max_width, max_height), Image.Resampling.LANCZOS)

        return image

    @staticmethod
    def create_thumbnail(
        image: Image.Image, size: Tuple[int, int] = THUMBNAIL_SIZE
    ) -> Image.Image:
        """
        Create thumbnail from image.

        Args:
            image: PIL Image object
            size: Thumbnail size as (width, height) tuple

        Returns:
            Thumbnail PIL Image object
        """
        if not isinstance(image, Image.Image):
            raise ImageHandlerError("Input must be a PIL Image object")

        thumbnail = image.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        return thumbnail

    @staticmethod
    def convert_format(image: Image.Image, format: str = "PNG") -> Image.Image:
        """
        Convert image to different format.

        Args:
            image: PIL Image object
            format: Target format (PNG, JPEG, etc.)

        Returns:
            Converted PIL Image object

        Raises:
            ImageHandlerError: If format is not supported
        """
        if not isinstance(image, Image.Image):
            raise ImageHandlerError("Input must be a PIL Image object")

        if format.upper() not in ImageHandler.SUPPORTED_FORMATS:
            raise ImageHandlerError(f"Unsupported image format: {format}")

        if format.upper() in {"JPEG"} and image.mode in {"RGBA", "LA", "P"}:
            rgb_image = Image.new("RGB", image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
            return rgb_image

        return image.convert("RGB") if format.upper() == "JPEG" else image

    @staticmethod
    def save_image(
        image: Image.Image, file_path: str, format: Optional[str] = None, quality: int = 95
    ) -> None:
        """
        Save image to file.

        Args:
            image: PIL Image object
            file_path: Destination file path
            format: Image format (auto-detected from extension if None)
            quality: JPEG quality (0-100)

        Raises:
            ImageHandlerError: If save fails
        """
        try:
            if not isinstance(image, Image.Image):
                raise ImageHandlerError("Input must be a PIL Image object")

            if format is None:
                ext = Path(file_path).suffix.upper().lstrip(".")
                format = "JPEG" if ext == "JPG" else ext

            # Create directory if needed
            FileHandler.ensure_directory(str(Path(file_path).parent))

            if format.upper() in {"JPEG", "JPG"}:
                image = ImageHandler.convert_format(image, "JPEG")
                image.save(file_path, format="JPEG", quality=quality, optimize=True)
            else:
                image.save(file_path, format=format.upper(), optimize=True)
        except Exception as e:
            raise ImageHandlerError(f"Failed to save image: {str(e)}")

    @staticmethod
    def get_image_dimensions(file_path: str) -> Tuple[int, int]:
        """
        Get image dimensions without loading entire image.

        Args:
            file_path: Path to image file

        Returns:
            Tuple of (width, height) in pixels

        Raises:
            ImageHandlerError: If file is not a valid image
        """
        try:
            image = ImageHandler.load_image(file_path)
            return image.size
        except ImageHandlerError:
            raise
        except Exception as e:
            raise ImageHandlerError(f"Failed to get image dimensions: {str(e)}")

    @staticmethod
    def image_to_bytes(image: Image.Image, format: str = "PNG") -> bytes:
        """
        Convert image to bytes for storage or transmission.

        Args:
            image: PIL Image object
            format: Image format

        Returns:
            Image data as bytes

        Raises:
            ImageHandlerError: If conversion fails
        """
        try:
            if not isinstance(image, Image.Image):
                raise ImageHandlerError("Input must be a PIL Image object")

            buffer = BytesIO()
            image.save(buffer, format=format.upper())
            return buffer.getvalue()
        except Exception as e:
            raise ImageHandlerError(f"Failed to convert image to bytes: {str(e)}")

    @staticmethod
    def bytes_to_image(image_bytes: bytes) -> Image.Image:
        """
        Convert image bytes to PIL Image object.

        Args:
            image_bytes: Image data as bytes

        Returns:
            PIL Image object

        Raises:
            ImageHandlerError: If conversion fails
        """
        try:
            if not image_bytes:
                raise ImageHandlerError("Image bytes cannot be empty")

            buffer = BytesIO(image_bytes)
            image = Image.open(buffer)
            image.load()  # Verify image is valid
            return image
        except Exception as e:
            raise ImageHandlerError(f"Failed to convert bytes to image: {str(e)}")

    @staticmethod
    def crop_image(
        image: Image.Image, left: int, top: int, right: int, bottom: int
    ) -> Image.Image:
        """
        Crop image to specified box.

        Args:
            image: PIL Image object
            left: Left coordinate
            top: Top coordinate
            right: Right coordinate
            bottom: Bottom coordinate

        Returns:
            Cropped PIL Image object
        """
        if not isinstance(image, Image.Image):
            raise ImageHandlerError("Input must be a PIL Image object")

        return image.crop((left, top, right, bottom))
