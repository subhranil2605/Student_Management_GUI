"""Marks and academic performance management service."""

from typing import List, Optional

from src.database.models import ExamMarks
from src.database.queries import DatabaseQueries
from src.validators.form_validator import FormValidator, ValidationError
from src.validators.business_rules import BusinessRuleValidator


class MarksServiceError(Exception):
    """Custom exception for marks service errors."""

    pass


class MarksService:
    """Service for managing student marks and academic performance."""

    def __init__(
        self, queries: DatabaseQueries, business_validator: BusinessRuleValidator
    ):
        """
        Initialize marks service.

        Args:
            queries: Database queries instance
            business_validator: Business rule validator instance
        """
        self.queries = queries
        self.business_validator = business_validator

    def add_marks(
        self,
        student_id: str,
        subject: str,
        marks_obtained: float,
        total_marks: float = 100.0,
        grade: Optional[str] = None,
    ) -> ExamMarks:
        """
        Add marks for a student in a subject.

        Args:
            student_id: Student ID
            subject: Subject name
            marks_obtained: Marks obtained
            total_marks: Total marks for subject
            grade: Letter grade (optional)

        Returns:
            Created ExamMarks object

        Raises:
            ValidationError: If input is invalid
            MarksServiceError: If operation fails
        """
        try:
            # Validate inputs
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )
            subject = FormValidator.validate_required_field(
                subject, "Subject"
            )
            marks_obtained = self.business_validator.validate_marks_range(
                float(marks_obtained)
            )
            total_marks = self.business_validator.validate_marks_range(
                float(total_marks)
            )

            if marks_obtained > total_marks:
                raise MarksServiceError(
                    "Marks obtained cannot exceed total marks"
                )

            # Calculate percentage
            percentage = (marks_obtained / total_marks) * 100

            # Add to database
            marks = self.queries.add_marks(
                student_id=student_id,
                subject=subject,
                marks_obtained=marks_obtained,
                total_marks=total_marks,
                percentage=percentage,
                grade=grade,
            )

            return marks
        except ValidationError as e:
            raise MarksServiceError(str(e))
        except MarksServiceError:
            raise
        except Exception as e:
            raise MarksServiceError(f"Failed to add marks: {str(e)}")

    def get_marks(self, student_id: str, subject: Optional[str] = None) -> List[ExamMarks]:
        """
        Get marks for a student.

        Args:
            student_id: Student ID
            subject: Optional subject filter

        Returns:
            List of ExamMarks objects

        Raises:
            ValidationError: If input is invalid
            MarksServiceError: If retrieval fails
        """
        try:
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )

            if subject:
                subject = FormValidator.validate_required_field(
                    subject, "Subject"
                )
                return self.queries.get_marks_by_subject(
                    student_id, subject
                )

            return self.queries.get_student_marks(student_id)
        except ValidationError as e:
            raise MarksServiceError(str(e))
        except Exception as e:
            raise MarksServiceError(f"Failed to retrieve marks: {str(e)}")

    def update_marks(
        self,
        student_id: str,
        subject: str,
        marks_obtained: float,
        grade: Optional[str] = None,
    ) -> ExamMarks:
        """
        Update marks for a student in a subject.

        Args:
            student_id: Student ID
            subject: Subject name
            marks_obtained: New marks
            grade: New grade (optional)

        Returns:
            Updated ExamMarks object

        Raises:
            ValidationError: If input is invalid
            MarksServiceError: If update fails
        """
        try:
            # Validate inputs
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )
            subject = FormValidator.validate_required_field(
                subject, "Subject"
            )
            marks_obtained = self.business_validator.validate_marks_range(
                float(marks_obtained)
            )

            # Get existing marks to get total marks
            existing_marks = self.queries.get_marks_by_subject(
                student_id, subject
            )
            if not existing_marks:
                raise MarksServiceError(
                    f"No marks found for {subject}"
                )

            total_marks = existing_marks[0].total_marks
            percentage = (marks_obtained / total_marks) * 100

            # Update in database
            marks = self.queries.update_marks(
                student_id=student_id,
                subject=subject,
                marks_obtained=marks_obtained,
                percentage=percentage,
                grade=grade,
            )

            return marks
        except ValidationError as e:
            raise MarksServiceError(str(e))
        except MarksServiceError:
            raise
        except Exception as e:
            raise MarksServiceError(f"Failed to update marks: {str(e)}")

    def calculate_cgpa(self, student_id: str) -> float:
        """
        Calculate CGPA (Cumulative Grade Point Average) for a student.

        Args:
            student_id: Student ID

        Returns:
            Calculated CGPA (0-4.0)

        Raises:
            ValidationError: If input is invalid
            MarksServiceError: If calculation fails
        """
        try:
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )

            # Get all marks
            marks_list = self.queries.get_student_marks(student_id)

            if not marks_list:
                return 0.0

            # Calculate average percentage
            total_percentage = sum(m.percentage for m in marks_list)
            average_percentage = total_percentage / len(marks_list)

            # Convert to CGPA (0-4.0 scale)
            cgpa = (average_percentage / 100) * 4.0

            return min(cgpa, 4.0)
        except ValidationError as e:
            raise MarksServiceError(str(e))
        except Exception as e:
            raise MarksServiceError(f"Failed to calculate CGPA: {str(e)}")

    def calculate_gpa(self, student_id: str, semester: Optional[int] = None) -> float:
        """
        Calculate GPA for a student (for a semester if specified).

        Args:
            student_id: Student ID
            semester: Optional semester number

        Returns:
            Calculated GPA (0-4.0)

        Raises:
            ValidationError: If input is invalid
            MarksServiceError: If calculation fails
        """
        try:
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )

            # Get all marks (or semester-specific)
            marks_list = self.queries.get_student_marks(student_id)

            if not marks_list:
                return 0.0

            # Calculate average percentage
            total_percentage = sum(m.percentage for m in marks_list)
            average_percentage = total_percentage / len(marks_list)

            # Convert to GPA (0-4.0 scale)
            gpa = (average_percentage / 100) * 4.0

            return min(gpa, 4.0)
        except ValidationError as e:
            raise MarksServiceError(str(e))
        except Exception as e:
            raise MarksServiceError(f"Failed to calculate GPA: {str(e)}")

    def get_average_marks(self, student_id: str) -> float:
        """
        Get average marks for a student.

        Args:
            student_id: Student ID

        Returns:
            Average percentage

        Raises:
            ValidationError: If input is invalid
            MarksServiceError: If calculation fails
        """
        try:
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )

            marks_list = self.queries.get_student_marks(student_id)

            if not marks_list:
                return 0.0

            average = sum(m.percentage for m in marks_list) / len(marks_list)
            return average
        except ValidationError as e:
            raise MarksServiceError(str(e))
        except Exception as e:
            raise MarksServiceError(f"Failed to calculate average: {str(e)}")

    def get_best_subject(self, student_id: str) -> Optional[str]:
        """
        Get subject with highest marks.

        Args:
            student_id: Student ID

        Returns:
            Subject name or None

        Raises:
            ValidationError: If input is invalid
            MarksServiceError: If retrieval fails
        """
        try:
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )

            marks_list = self.queries.get_student_marks(student_id)

            if not marks_list:
                return None

            best_mark = max(marks_list, key=lambda m: m.marks_obtained)
            return best_mark.subject
        except ValidationError as e:
            raise MarksServiceError(str(e))
        except Exception as e:
            raise MarksServiceError(f"Failed to get best subject: {str(e)}")

    def get_worst_subject(self, student_id: str) -> Optional[str]:
        """
        Get subject with lowest marks.

        Args:
            student_id: Student ID

        Returns:
            Subject name or None

        Raises:
            ValidationError: If input is invalid
            MarksServiceError: If retrieval fails
        """
        try:
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )

            marks_list = self.queries.get_student_marks(student_id)

            if not marks_list:
                return None

            worst_mark = min(marks_list, key=lambda m: m.marks_obtained)
            return worst_mark.subject
        except ValidationError as e:
            raise MarksServiceError(str(e))
        except Exception as e:
            raise MarksServiceError(f"Failed to get worst subject: {str(e)}")

    def delete_marks(self, student_id: str, subject: str) -> bool:
        """
        Delete marks for a student in a subject.

        Args:
            student_id: Student ID
            subject: Subject name

        Returns:
            True if deleted successfully

        Raises:
            ValidationError: If input is invalid
            MarksServiceError: If deletion fails
        """
        try:
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )
            subject = FormValidator.validate_required_field(
                subject, "Subject"
            )

            # Verify marks exist
            marks = self.queries.get_marks_by_subject(student_id, subject)
            if not marks:
                raise MarksServiceError("Marks not found")

            # Delete
            self.queries.delete_marks(student_id, subject)
            return True
        except ValidationError as e:
            raise MarksServiceError(str(e))
        except MarksServiceError:
            raise
        except Exception as e:
            raise MarksServiceError(f"Failed to delete marks: {str(e)}")

    def assign_grade_by_percentage(self, percentage: float) -> str:
        """
        Assign letter grade based on percentage.

        Args:
            percentage: Percentage score

        Returns:
            Letter grade (A, B, C, D, F)
        """
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"
