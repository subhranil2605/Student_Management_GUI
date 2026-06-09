"""Business rule validation logic."""

from datetime import date
from typing import TYPE_CHECKING

from src.validators.form_validator import ValidationError

if TYPE_CHECKING:
    from src.database.queries import DatabaseQueries


class BusinessRuleValidator:
    """Business rule validators for application logic."""

    def __init__(self, queries: "DatabaseQueries"):
        """
        Initialize business rule validator.

        Args:
            queries: Database queries instance for checking business rules
        """
        self.queries = queries

    def validate_student_id_unique(
        self, student_id: str, exclude_id: int = None
    ) -> str:
        """
        Validate that student ID is unique.

        Args:
            student_id: Student ID to check
            exclude_id: Student ID to exclude (for updates)

        Returns:
            Validated student ID

        Raises:
            ValidationError: If student ID already exists
        """
        if not student_id or not student_id.strip():
            raise ValidationError("Student ID cannot be empty")

        # Check if student ID exists
        existing = self.queries.get_student_by_id(student_id)
        if existing and (exclude_id is None or existing.student_id != exclude_id):
            raise ValidationError(
                f"Student ID {student_id} already exists"
            )

        return str(student_id).strip()

    def validate_student_age_range(
        self, dob: date, min_age: int = 15, max_age: int = 60
    ) -> date:
        """
        Validate student age is within acceptable range.

        Args:
            dob: Date of birth
            min_age: Minimum age
            max_age: Maximum age

        Returns:
            Validated date of birth

        Raises:
            ValidationError: If age is outside range
        """
        from datetime import date as date_class

        if not isinstance(dob, date_class):
            raise ValidationError("Invalid date of birth")

        today = date_class.today()
        age = today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )

        if age < min_age:
            raise ValidationError(
                f"Student must be at least {min_age} years old"
            )

        if age > max_age:
            raise ValidationError(
                f"Student cannot be older than {max_age} years"
            )

        return dob

    def validate_marks_range(self, marks: float) -> float:
        """
        Validate marks are within valid range.

        Args:
            marks: Marks value to validate

        Returns:
            Validated marks

        Raises:
            ValidationError: If marks are outside valid range
        """
        if not isinstance(marks, (int, float)):
            raise ValidationError("Marks must be a number")

        if marks < 0 or marks > 100:
            raise ValidationError("Marks must be between 0 and 100")

        return float(marks)

    def validate_cgpa_calculation(
        self, total_marks: float, total_subjects: int
    ) -> float:
        """
        Validate and calculate CGPA.

        Args:
            total_marks: Total marks obtained
            total_subjects: Number of subjects

        Returns:
            Calculated CGPA (0-4.0)

        Raises:
            ValidationError: If calculation is invalid
        """
        if total_subjects <= 0:
            raise ValidationError("Number of subjects must be greater than 0")

        if total_marks < 0:
            raise ValidationError("Total marks cannot be negative")

        if total_marks > total_subjects * 100:
            raise ValidationError(
                "Total marks exceed maximum possible value"
            )

        # Convert to CGPA (0-100 to 0-4.0)
        percentage = (total_marks / (total_subjects * 100)) * 100
        cgpa = (percentage / 100) * 4.0

        return min(cgpa, 4.0)

    def validate_gpa_from_percentage(self, percentage: float) -> float:
        """
        Convert percentage to GPA (0-4.0).

        Args:
            percentage: Percentage value (0-100)

        Returns:
            Converted GPA

        Raises:
            ValidationError: If percentage is invalid
        """
        if percentage < 0 or percentage > 100:
            raise ValidationError("Percentage must be between 0 and 100")

        # Standard conversion: percentage / 25
        gpa = percentage / 25.0
        return min(gpa, 4.0)

    def validate_disability_percentage(
        self, has_disability: str, disability_percentage: str
    ) -> float:
        """
        Validate disability percentage if disability is marked.

        Args:
            has_disability: "yes" or "no"
            disability_percentage: Disability percentage

        Returns:
            Validated disability percentage

        Raises:
            ValidationError: If validation fails
        """
        if has_disability.lower() == "yes":
            if not disability_percentage or not disability_percentage.strip():
                raise ValidationError(
                    "Disability percentage is required when disability is marked"
                )

            try:
                percentage = float(disability_percentage)
                if percentage < 0 or percentage > 100:
                    raise ValidationError(
                        "Disability percentage must be between 0 and 100"
                    )
                return percentage
            except ValueError:
                raise ValidationError(
                    "Disability percentage must be a valid number"
                )

        return 0.0

    def validate_nationality_country(
        self, nationality: str, country: str
    ) -> str:
        """
        Validate country based on nationality.

        Args:
            nationality: Selected nationality
            country: Selected country

        Returns:
            Validated country

        Raises:
            ValidationError: If validation fails
        """
        if nationality == "Indian":
            if country.lower() != "india":
                raise ValidationError(
                    "Country must be India for Indian nationality"
                )
        elif nationality == "Others":
            if not country or country.lower() == "india":
                raise ValidationError(
                    "Please enter a valid country for non-Indian nationality"
                )

        return country

    def validate_address_fields(
        self, same_address: str, present_address: str = None
    ) -> str:
        """
        Validate address fields based on same_address flag.

        Args:
            same_address: "yes" or "no"
            present_address: Present address (required if same_address is "no")

        Returns:
            Validated present address

        Raises:
            ValidationError: If validation fails
        """
        if same_address.lower() == "no":
            if not present_address or not present_address.strip():
                raise ValidationError("Present address is required")

            if len(present_address.strip()) < 10:
                raise ValidationError(
                    "Present address must be at least 10 characters"
                )

            return present_address.strip()

        return ""

    def validate_duplicate_registration(
        self, student_id: str, registration_number: str
    ) -> bool:
        """
        Check if student is already registered.

        Args:
            student_id: Student ID to check
            registration_number: Registration number to check

        Returns:
            True if student exists, False otherwise
        """
        try:
            existing = self.queries.student_exists(student_id)
            return existing
        except Exception:
            return False

    def validate_marks_prerequisites(
        self, subject: str, marks: float
    ) -> float:
        """
        Validate marks entry prerequisites.

        Args:
            subject: Subject name
            marks: Marks obtained

        Returns:
            Validated marks

        Raises:
            ValidationError: If validation fails
        """
        if not subject or not subject.strip():
            raise ValidationError("Subject name is required")

        if marks < 0 or marks > 100:
            raise ValidationError("Marks must be between 0 and 100")

        return marks
