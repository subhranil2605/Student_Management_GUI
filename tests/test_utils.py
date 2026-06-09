"""Unit tests for utility functions and helpers."""

import os
import tempfile
from datetime import date, datetime
from pathlib import Path

import pytest
from PIL import Image

from src.utils.file_handler import FileHandler, FileHandlerError
from src.utils.image_handler import ImageHandler, ImageHandlerError
from src.utils.helpers import (
    assign_grade,
    calculate_cgpa,
    capitalize_name,
    format_currency,
    format_date,
    format_decimal,
    format_phone,
    get_age,
    get_grade_description,
    get_initials,
    gpa_to_percentage,
    parse_currency,
    parse_date,
    percentage_to_gpa,
    safe_divide,
    truncate_string,
)


# ============================================================================
# FileHandler Tests
# ============================================================================


class TestFileHandler:
    """Test FileHandler utility class."""

    def test_validate_file_exists_success(self):
        """Test file existence validation with existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            assert FileHandler.validate_file_exists(tmp_path) is True
        finally:
            os.unlink(tmp_path)

    def test_validate_file_exists_failure(self):
        """Test file existence validation with non-existent file."""
        assert FileHandler.validate_file_exists("/nonexistent/path/file.txt") is False

    def test_validate_file_exists_empty_path(self):
        """Test file existence validation with empty path."""
        with pytest.raises(FileHandlerError):
            FileHandler.validate_file_exists("")

    def test_validate_file_extension_allowed(self):
        """Test file extension validation with allowed extension."""
        assert (
            FileHandler.validate_file_extension(
                "test.jpg", {".jpg", ".png"}
            )
            is True
        )

    def test_validate_file_extension_disallowed(self):
        """Test file extension validation with disallowed extension."""
        assert (
            FileHandler.validate_file_extension(
                "test.exe", {".jpg", ".png"}
            )
            is False
        )

    def test_validate_file_extension_no_extension(self):
        """Test file extension validation with no extension."""
        with pytest.raises(FileHandlerError):
            FileHandler.validate_file_extension("testfile", {".jpg", ".png"})

    def test_validate_file_extension_case_insensitive(self):
        """Test file extension validation is case-insensitive."""
        assert (
            FileHandler.validate_file_extension(
                "test.JPG", {".jpg", ".png"}
            )
            is True
        )

    def test_validate_file_size_valid(self):
        """Test file size validation with valid size."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test content")
            tmp_path = tmp.name

        try:
            assert FileHandler.validate_file_size(tmp_path, max_size=1000) is True
        finally:
            os.unlink(tmp_path)

    def test_validate_file_size_too_large(self):
        """Test file size validation with oversized file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"x" * 1000)
            tmp_path = tmp.name

        try:
            assert FileHandler.validate_file_size(tmp_path, max_size=100) is False
        finally:
            os.unlink(tmp_path)

    def test_validate_file_size_nonexistent(self):
        """Test file size validation with non-existent file."""
        with pytest.raises(FileHandlerError):
            FileHandler.validate_file_size("/nonexistent/file.txt")

    def test_copy_file_success(self):
        """Test successful file copy."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, "source.txt")
            dest = os.path.join(tmpdir, "dest.txt")

            with open(source, "w") as f:
                f.write("test content")

            FileHandler.copy_file(source, dest)
            assert os.path.exists(dest)
            with open(dest, "r") as f:
                assert f.read() == "test content"

    def test_copy_file_nonexistent_source(self):
        """Test copy with non-existent source."""
        with pytest.raises(FileHandlerError):
            FileHandler.copy_file("/nonexistent/source.txt", "/dest/dest.txt")

    def test_copy_file_existing_destination_no_overwrite(self):
        """Test copy with existing destination and no overwrite."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, "source.txt")
            dest = os.path.join(tmpdir, "dest.txt")

            with open(source, "w") as f:
                f.write("source")
            with open(dest, "w") as f:
                f.write("existing")

            with pytest.raises(FileHandlerError):
                FileHandler.copy_file(source, dest, overwrite=False)

    def test_copy_file_with_overwrite(self):
        """Test copy with overwrite enabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, "source.txt")
            dest = os.path.join(tmpdir, "dest.txt")

            with open(source, "w") as f:
                f.write("new content")
            with open(dest, "w") as f:
                f.write("old content")

            FileHandler.copy_file(source, dest, overwrite=True)
            with open(dest, "r") as f:
                assert f.read() == "new content"

    def test_move_file_success(self):
        """Test successful file move."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, "source.txt")
            dest = os.path.join(tmpdir, "dest.txt")

            with open(source, "w") as f:
                f.write("test content")

            FileHandler.move_file(source, dest)
            assert not os.path.exists(source)
            assert os.path.exists(dest)

    def test_delete_file_success(self):
        """Test successful file deletion."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        assert os.path.exists(tmp_path)
        FileHandler.delete_file(tmp_path)
        assert not os.path.exists(tmp_path)

    def test_delete_file_nonexistent(self):
        """Test delete with non-existent file."""
        with pytest.raises(FileHandlerError):
            FileHandler.delete_file("/nonexistent/file.txt")

    def test_get_file_size(self):
        """Test getting file size."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test")
            tmp_path = tmp.name

        try:
            assert FileHandler.get_file_size(tmp_path) == 4
        finally:
            os.unlink(tmp_path)

    def test_get_file_name(self):
        """Test extracting file name from path."""
        assert FileHandler.get_file_name("/path/to/file.txt") == "file.txt"
        assert FileHandler.get_file_name("file.txt") == "file.txt"

    def test_ensure_directory_creates_directory(self):
        """Test directory creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = os.path.join(tmpdir, "new", "nested", "dir")
            FileHandler.ensure_directory(new_dir)
            assert os.path.exists(new_dir)


# ============================================================================
# ImageHandler Tests
# ============================================================================


class TestImageHandler:
    """Test ImageHandler utility class."""

    @pytest.fixture
    def sample_image(self):
        """Create a sample image for testing."""
        img = Image.new("RGB", (200, 200), color="red")
        return img

    @pytest.fixture
    def sample_image_file(self, sample_image):
        """Create a temporary image file."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            sample_image.save(tmp.name)
            tmp_path = tmp.name

        yield tmp_path
        os.unlink(tmp_path)

    def test_load_image_success(self, sample_image_file):
        """Test loading image from file."""
        image = ImageHandler.load_image(sample_image_file)
        assert isinstance(image, Image.Image)
        assert image.size == (200, 200)

    def test_load_image_nonexistent(self):
        """Test loading non-existent image."""
        with pytest.raises(ImageHandlerError):
            ImageHandler.load_image("/nonexistent/image.png")

    def test_load_image_invalid_format(self):
        """Test loading invalid image format."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"not an image")
            tmp_path = tmp.name

        try:
            with pytest.raises(ImageHandlerError):
                ImageHandler.load_image(tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_resize_image_maintain_aspect(self, sample_image):
        """Test image resizing with aspect ratio maintenance."""
        resized = ImageHandler.resize_image(
            sample_image, max_width=100, max_height=100, maintain_aspect=True
        )
        assert resized.size[0] <= 100
        assert resized.size[1] <= 100

    def test_resize_image_no_aspect(self, sample_image):
        """Test image resizing without aspect ratio."""
        resized = ImageHandler.resize_image(
            sample_image, max_width=100, max_height=150, maintain_aspect=False
        )
        assert resized.size == (100, 150)

    def test_create_thumbnail(self, sample_image):
        """Test thumbnail creation."""
        thumbnail = ImageHandler.create_thumbnail(
            sample_image, size=(50, 50)
        )
        assert thumbnail.size[0] <= 50
        assert thumbnail.size[1] <= 50

    def test_convert_format_png_to_rgb(self, sample_image):
        """Test format conversion."""
        converted = ImageHandler.convert_format(sample_image, "JPEG")
        assert converted.mode == "RGB"

    def test_convert_format_unsupported(self, sample_image):
        """Test conversion to unsupported format."""
        with pytest.raises(ImageHandlerError):
            ImageHandler.convert_format(sample_image, "INVALID")

    def test_save_image_success(self, sample_image):
        """Test saving image to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.png")
            ImageHandler.save_image(sample_image, path)
            assert os.path.exists(path)

    def test_get_image_dimensions(self, sample_image_file):
        """Test getting image dimensions."""
        dims = ImageHandler.get_image_dimensions(sample_image_file)
        assert dims == (200, 200)

    def test_image_to_bytes(self, sample_image):
        """Test converting image to bytes."""
        image_bytes = ImageHandler.image_to_bytes(sample_image, format="PNG")
        assert isinstance(image_bytes, bytes)
        assert len(image_bytes) > 0

    def test_bytes_to_image(self, sample_image):
        """Test converting bytes to image."""
        image_bytes = ImageHandler.image_to_bytes(sample_image, format="PNG")
        image = ImageHandler.bytes_to_image(image_bytes)
        assert isinstance(image, Image.Image)

    def test_bytes_to_image_empty(self):
        """Test converting empty bytes to image."""
        with pytest.raises(ImageHandlerError):
            ImageHandler.bytes_to_image(b"")

    def test_crop_image(self, sample_image):
        """Test image cropping."""
        cropped = ImageHandler.crop_image(sample_image, 10, 10, 100, 100)
        assert cropped.size == (90, 90)


# ============================================================================
# Helper Functions Tests
# ============================================================================


class TestHelpers:
    """Test helper utility functions."""

    def test_format_date_default_format(self):
        """Test date formatting with default format."""
        test_date = date(2026, 6, 10)
        assert format_date(test_date) == "10/06/2026"

    def test_format_date_custom_format(self):
        """Test date formatting with custom format."""
        test_date = date(2026, 6, 10)
        assert format_date(test_date, "%Y-%m-%d") == "2026-06-10"

    def test_parse_date_default_format(self):
        """Test date parsing with default format."""
        parsed = parse_date("10/06/2026")
        assert parsed == date(2026, 6, 10)

    def test_parse_date_custom_format(self):
        """Test date parsing with custom format."""
        parsed = parse_date("2026-06-10", "%Y-%m-%d")
        assert parsed == date(2026, 6, 10)

    def test_parse_date_invalid_format(self):
        """Test date parsing with invalid format."""
        with pytest.raises(ValueError):
            parse_date("invalid-date")

    def test_get_age(self):
        """Test age calculation."""
        birth_date = date(2000, 6, 10)
        age = get_age(birth_date)
        assert age >= 26  # At least 26 years old as of 2026

    def test_format_currency_default_symbol(self):
        """Test currency formatting with default symbol."""
        assert format_currency(1000.50) == "₹1,000.50"

    def test_format_currency_custom_symbol(self):
        """Test currency formatting with custom symbol."""
        assert format_currency(1000.50, "$") == "$1,000.50"

    def test_parse_currency_default_symbol(self):
        """Test currency parsing with default symbol."""
        assert parse_currency("₹1,000.50") == 1000.50

    def test_parse_currency_custom_symbol(self):
        """Test currency parsing with custom symbol."""
        assert parse_currency("$1,000.50", "$") == 1000.50

    def test_parse_currency_invalid(self):
        """Test currency parsing with invalid input."""
        with pytest.raises(ValueError):
            parse_currency("invalid")

    def test_calculate_cgpa_simple(self):
        """Test CGPA calculation without weights."""
        cgpa = calculate_cgpa([3.5, 3.8, 3.2])
        assert 3.4 <= cgpa <= 3.6

    def test_calculate_cgpa_weighted(self):
        """Test CGPA calculation with weights."""
        cgpa = calculate_cgpa([4.0, 3.0], [3, 3])
        assert cgpa == 3.5

    def test_calculate_cgpa_empty_list(self):
        """Test CGPA calculation with empty list."""
        with pytest.raises(ValueError):
            calculate_cgpa([])

    def test_calculate_cgpa_mismatched_lengths(self):
        """Test CGPA calculation with mismatched list lengths."""
        with pytest.raises(ValueError):
            calculate_cgpa([3.5, 3.8], [3])

    def test_percentage_to_gpa(self):
        """Test percentage to GPA conversion."""
        assert percentage_to_gpa(100) == 4.0
        assert percentage_to_gpa(75) == 3.0
        assert percentage_to_gpa(50) == 2.0

    def test_percentage_to_gpa_invalid(self):
        """Test percentage to GPA with invalid input."""
        with pytest.raises(ValueError):
            percentage_to_gpa(150)

    def test_gpa_to_percentage(self):
        """Test GPA to percentage conversion."""
        assert gpa_to_percentage(4.0) == 100.0
        assert gpa_to_percentage(3.0) == 75.0
        assert gpa_to_percentage(2.0) == 50.0

    def test_gpa_to_percentage_invalid(self):
        """Test GPA to percentage with invalid input."""
        with pytest.raises(ValueError):
            gpa_to_percentage(5.0)

    def test_assign_grade_a(self):
        """Test grade assignment for A."""
        assert assign_grade(95) == "A"
        assert assign_grade(90) == "A"

    def test_assign_grade_b(self):
        """Test grade assignment for B."""
        assert assign_grade(85) == "B"
        assert assign_grade(80) == "B"

    def test_assign_grade_c(self):
        """Test grade assignment for C."""
        assert assign_grade(75) == "C"
        assert assign_grade(70) == "C"

    def test_assign_grade_d(self):
        """Test grade assignment for D."""
        assert assign_grade(65) == "D"
        assert assign_grade(60) == "D"

    def test_assign_grade_e(self):
        """Test grade assignment for E."""
        assert assign_grade(55) == "E"
        assert assign_grade(50) == "E"

    def test_assign_grade_f(self):
        """Test grade assignment for F."""
        assert assign_grade(45) == "F"
        assert assign_grade(0) == "F"

    def test_get_grade_description_valid(self):
        """Test getting grade description."""
        assert get_grade_description("A") == "Excellent"
        assert get_grade_description("F") == "Fail"

    def test_get_grade_description_invalid(self):
        """Test getting grade description with invalid grade."""
        with pytest.raises(ValueError):
            get_grade_description("Z")

    def test_truncate_string_no_truncation_needed(self):
        """Test truncation with string shorter than max length."""
        assert truncate_string("short", 10) == "short"

    def test_truncate_string_truncation_needed(self):
        """Test truncation with string longer than max length."""
        result = truncate_string("this is a long string", 10)
        assert len(result) == 10
        assert result.endswith("...")

    def test_capitalize_name_simple(self):
        """Test name capitalization."""
        assert capitalize_name("john") == "John"
        assert capitalize_name("JANE") == "Jane"

    def test_capitalize_name_hyphenated(self):
        """Test hyphenated name capitalization."""
        assert capitalize_name("mary-jane") == "Mary-Jane"

    def test_format_phone_valid(self):
        """Test phone number formatting."""
        assert format_phone("9876543210") == "987-654-3210"

    def test_format_phone_invalid_length(self):
        """Test phone formatting with invalid length."""
        with pytest.raises(ValueError):
            format_phone("12345")

    def test_get_initials_simple(self):
        """Test getting initials from name."""
        assert get_initials("John Doe") == "JD"
        assert get_initials("Mary Jane Smith") == "MJS"

    def test_get_initials_empty(self):
        """Test getting initials from empty string."""
        assert get_initials("") == ""

    def test_safe_divide_normal(self):
        """Test safe division with valid inputs."""
        assert safe_divide(10, 2) == 5.0

    def test_safe_divide_by_zero(self):
        """Test safe division by zero."""
        assert safe_divide(10, 0) == 0.0
        assert safe_divide(10, 0, default=1.0) == 1.0

    def test_format_decimal_default_places(self):
        """Test decimal formatting with default places."""
        assert format_decimal(3.14159) == "3.14"

    def test_format_decimal_custom_places(self):
        """Test decimal formatting with custom places."""
        assert format_decimal(3.14159, 3) == "3.142"
