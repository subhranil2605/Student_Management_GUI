"""Form field validation logic."""

import re
from datetime import date, datetime
from typing import Optional, Tuple

from src.config.settings import VALIDATION_RULES


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


class FormValidator:
    """Form field validators for user input."""

    @staticmethod
    def validate_name(
        name: str, min_length: int = 2, max_length: int = 100
    ) -> str:
        """
        Validate student/person name.

        Args:
            name: Name to validate
            min_length: Minimum allowed length
            max_length: Maximum allowed length

        Returns:
            Validated and cleaned name

        Raises:
            ValidationError: If validation fails
        """
        if not name or not name.strip():
            raise ValidationError("Name cannot be empty")

        cleaned_name = str(name).strip().title()

        if len(cleaned_name) < min_length:
            raise ValidationError(
                f"Name must be at least {min_length} characters"
            )

        if len(cleaned_name) > max_length:
            raise ValidationError(
                f"Name cannot exceed {max_length} characters"
            )

        # Check if name contains only letters and spaces
        pattern = VALIDATION_RULES["name"]["pattern"]
        if not re.match(pattern, cleaned_name):
            raise ValidationError("Name can only contain letters and spaces")

        return cleaned_name

    @staticmethod
    def validate_email(email: str) -> str:
        """
        Validate email address format.

        Args:
            email: Email to validate

        Returns:
            Validated email (lowercased)

        Raises:
            ValidationError: If validation fails
        """
        if not email or not email.strip():
            raise ValidationError("Email cannot be empty")

        cleaned_email = str(email).strip().lower()
        pattern = VALIDATION_RULES["email"]["pattern"]

        if not re.match(pattern, cleaned_email):
            raise ValidationError("Invalid email format")

        return cleaned_email

    @staticmethod
    def validate_phone(phone: str) -> str:
        """
        Validate phone number format.

        Args:
            phone: Phone number to validate

        Returns:
            Validated phone number

        Raises:
            ValidationError: If validation fails
        """
        if not phone or not phone.strip():
            raise ValidationError("Phone number cannot be empty")

        cleaned_phone = str(phone).strip()
        pattern = VALIDATION_RULES["phone"]["pattern"]
        min_length = VALIDATION_RULES["phone"]["min_length"]

        if len(cleaned_phone) < min_length:
            raise ValidationError(
                f"Phone number must be {min_length} digits"
            )

        if not re.match(pattern, cleaned_phone):
            raise ValidationError(
                "Phone number must contain only digits"
            )

        return cleaned_phone

    @staticmethod
    def validate_aadhaar(aadhaar: str) -> str:
        """
        Validate Aadhaar number format.

        Args:
            aadhaar: Aadhaar number to validate

        Returns:
            Validated Aadhaar number

        Raises:
            ValidationError: If validation fails
        """
        if not aadhaar or not aadhaar.strip():
            raise ValidationError("Aadhaar cannot be empty")

        cleaned_aadhaar = str(aadhaar).strip()
        pattern = VALIDATION_RULES["aadhaar"]["pattern"]

        if not re.match(pattern, cleaned_aadhaar):
            raise ValidationError("Aadhaar must be 12 digits")

        return cleaned_aadhaar

    @staticmethod
    def validate_date(date_str: str, date_format: str = "%Y-%m-%d") -> date:
        """
        Validate date format.

        Args:
            date_str: Date string to validate
            date_format: Expected date format

        Returns:
            Parsed date object

        Raises:
            ValidationError: If validation fails
        """
        if not date_str or not date_str.strip():
            raise ValidationError("Date cannot be empty")

        try:
            parsed_date = datetime.strptime(str(date_str).strip(), date_format)
            return parsed_date.date()
        except ValueError:
            raise ValidationError(f"Invalid date format. Use {date_format}")

    @staticmethod
    def validate_dob(dob: date, min_age: int = 15, max_age: int = 60) -> date:
        """
        Validate date of birth and age range.

        Args:
            dob: Date of birth
            min_age: Minimum allowed age
            max_age: Maximum allowed age

        Returns:
            Validated date of birth

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(dob, date):
            raise ValidationError("Invalid date of birth")

        today = date.today()
        age = today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )

        if age < min_age:
            raise ValidationError(
                f"Student age must be at least {min_age} years"
            )

        if age > max_age:
            raise ValidationError(
                f"Student age cannot exceed {max_age} years"
            )

        if dob >= today:
            raise ValidationError("Date of birth cannot be in the future")

        return dob

    @staticmethod
    def validate_percentage(percentage: str) -> float:
        """
        Validate percentage value (0-100).

        Args:
            percentage: Percentage string to validate

        Returns:
            Validated percentage as float

        Raises:
            ValidationError: If validation fails
        """
        if not percentage or not percentage.strip():
            raise ValidationError("Percentage cannot be empty")

        try:
            value = float(str(percentage).strip())

            if value < 0 or value > 100:
                raise ValidationError(
                    "Percentage must be between 0 and 100"
                )

            return value
        except ValueError:
            raise ValidationError("Percentage must be a valid number")

    @staticmethod
    def validate_marks(marks: str) -> float:
        """
        Validate marks (0-100).

        Args:
            marks: Marks string to validate

        Returns:
            Validated marks as float

        Raises:
            ValidationError: If validation fails
        """
        if not marks or not marks.strip():
            raise ValidationError("Marks cannot be empty")

        try:
            value = float(str(marks).strip())

            if value < 0 or value > 100:
                raise ValidationError("Marks must be between 0 and 100")

            return value
        except ValueError:
            raise ValidationError("Marks must be a valid number")

    @staticmethod
    def validate_gpa(gpa: str) -> float:
        """
        Validate GPA value (0-4.0).

        Args:
            gpa: GPA string to validate

        Returns:
            Validated GPA as float

        Raises:
            ValidationError: If validation fails
        """
        if not gpa or not gpa.strip():
            raise ValidationError("GPA cannot be empty")

        try:
            value = float(str(gpa).strip())

            if value < 0 or value > 4.0:
                raise ValidationError("GPA must be between 0 and 4.0")

            return value
        except ValueError:
            raise ValidationError("GPA must be a valid number")

    @staticmethod
    def validate_cgpa(cgpa: str) -> float:
        """
        Validate CGPA value (0-4.0).

        Args:
            cgpa: CGPA string to validate

        Returns:
            Validated CGPA as float

        Raises:
            ValidationError: If validation fails
        """
        if not cgpa or not cgpa.strip():
            raise ValidationError("CGPA cannot be empty")

        try:
            value = float(str(cgpa).strip())

            if value < 0 or value > 4.0:
                raise ValidationError("CGPA must be between 0 and 4.0")

            return value
        except ValueError:
            raise ValidationError("CGPA must be a valid number")

    @staticmethod
    def validate_password(password: str, min_length: int = 6) -> str:
        """
        Validate password strength.

        Args:
            password: Password to validate
            min_length: Minimum password length

        Returns:
            Validated password

        Raises:
            ValidationError: If validation fails
        """
        if not password:
            raise ValidationError("Password cannot be empty")

        if len(password) < min_length:
            raise ValidationError(
                f"Password must be at least {min_length} characters"
            )

        return password

    @staticmethod
    def validate_required_field(value: str, field_name: str) -> str:
        """
        Validate that a field is not empty.

        Args:
            value: Field value to validate
            field_name: Name of the field for error message

        Returns:
            Cleaned value

        Raises:
            ValidationError: If field is empty
        """
        if not value or not str(value).strip():
            raise ValidationError(f"{field_name} is required")

        return str(value).strip()

    @staticmethod
    def validate_dropdown_selection(
        value: str, field_name: str
    ) -> str:
        """
        Validate that dropdown selection is not "Select".

        Args:
            value: Selected value
            field_name: Name of the field

        Returns:
            Validated value

        Raises:
            ValidationError: If "Select" is chosen
        """
        if value == "Select" or not value:
            raise ValidationError(f"Please select a valid {field_name}")

        return value

    @staticmethod
    def validate_text_area(
        text: str, min_length: int = 5, max_length: int = 500
    ) -> str:
        """
        Validate text area content.

        Args:
            text: Text to validate
            min_length: Minimum text length
            max_length: Maximum text length

        Returns:
            Cleaned text

        Raises:
            ValidationError: If validation fails
        """
        if not text or not text.strip():
            raise ValidationError("Text area cannot be empty")

        cleaned_text = str(text).strip()

        if len(cleaned_text) < min_length:
            raise ValidationError(
                f"Text must be at least {min_length} characters"
            )

        if len(cleaned_text) > max_length:
            raise ValidationError(
                f"Text cannot exceed {max_length} characters"
            )

        return cleaned_text
