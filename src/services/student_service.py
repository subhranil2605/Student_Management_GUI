"""Student management service."""

from datetime import date
from typing import List, Optional

from src.database.models import Student
from src.database.queries import DatabaseQueries
from src.validators.form_validator import FormValidator, ValidationError
from src.validators.business_rules import BusinessRuleValidator


class StudentServiceError(Exception):
    """Custom exception for student service errors."""

    pass


class StudentService:
    """Service for managing student information and operations."""

    def __init__(
        self, queries: DatabaseQueries, business_validator: BusinessRuleValidator
    ):
        """
        Initialize student service.

        Args:
            queries: Database queries instance
            business_validator: Business rule validator instance
        """
        self.queries = queries
        self.business_validator = business_validator

    def register_student(
        self,
        student_id: str,
        fullname: str,
        sex: str,
        category: str,
        dob: date,
        registration_number: str,
        session: str,
        course: str,
        **kwargs
    ) -> Student:
        """
        Register a new student.

        Args:
            student_id: Unique student ID
            fullname: Full name
            sex: Gender
            category: Student category
            dob: Date of birth
            registration_number: Registration number
            session: Academic session
            course: Course/Program
            **kwargs: Additional student information

        Returns:
            Created Student object

        Raises:
            ValidationError: If input is invalid
            StudentServiceError: If registration fails
        """
        try:
            # Validate basic fields
            student_id = self.business_validator.validate_student_id_unique(
                student_id
            )
            fullname = FormValidator.validate_name(fullname)
            sex = FormValidator.validate_dropdown_selection(sex, "Gender")
            category = FormValidator.validate_dropdown_selection(
                category, "Category"
            )
            dob = self.business_validator.validate_student_age_range(dob)
            registration_number = FormValidator.validate_required_field(
                registration_number, "Registration Number"
            )
            session = FormValidator.validate_dropdown_selection(
                session, "Session"
            )
            course = FormValidator.validate_dropdown_selection(
                course, "Course"
            )

            # Create student in database
            student = self.queries.create_student(
                student_id=student_id,
                fullname=fullname,
                sex=sex,
                category=category,
                dob=dob,
                registration_number=registration_number,
                session=session,
                course=course,
                **kwargs
            )

            return student
        except ValidationError:
            raise
        except Exception as e:
            raise StudentServiceError(f"Student registration failed: {str(e)}")

    def get_student(self, student_id: str) -> Optional[Student]:
        """
        Get student by ID.

        Args:
            student_id: Student ID to retrieve

        Returns:
            Student object or None if not found

        Raises:
            StudentServiceError: If retrieval fails
        """
        try:
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )
            return self.queries.get_student_by_id(student_id)
        except ValidationError as e:
            raise StudentServiceError(str(e))
        except Exception as e:
            raise StudentServiceError(f"Failed to retrieve student: {str(e)}")

    def update_student(self, student_id: str, **kwargs) -> Student:
        """
        Update student information.

        Args:
            student_id: Student ID to update
            **kwargs: Fields to update

        Returns:
            Updated Student object

        Raises:
            ValidationError: If input is invalid
            StudentServiceError: If update fails
        """
        try:
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )

            # Validate provided fields
            if "fullname" in kwargs and kwargs["fullname"]:
                kwargs["fullname"] = FormValidator.validate_name(
                    kwargs["fullname"]
                )

            if "email" in kwargs and kwargs["email"]:
                kwargs["email"] = FormValidator.validate_email(
                    kwargs["email"]
                )

            if "phone" in kwargs and kwargs["phone"]:
                kwargs["phone"] = FormValidator.validate_phone(
                    kwargs["phone"]
                )

            if "dob" in kwargs and kwargs["dob"]:
                kwargs["dob"] = self.business_validator.validate_student_age_range(
                    kwargs["dob"]
                )

            # Update in database
            student = self.queries.update_student(student_id, **kwargs)
            return student
        except ValidationError:
            raise
        except Exception as e:
            raise StudentServiceError(f"Failed to update student: {str(e)}")

    def delete_student(self, student_id: str) -> bool:
        """
        Delete a student record.

        Args:
            student_id: Student ID to delete

        Returns:
            True if deleted successfully

        Raises:
            ValidationError: If input is invalid
            StudentServiceError: If deletion fails
        """
        try:
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )

            # Verify student exists
            student = self.get_student(student_id)
            if not student:
                raise StudentServiceError(f"Student {student_id} not found")

            # Delete from database
            self.queries.delete_student(student_id)
            return True
        except ValidationError as e:
            raise StudentServiceError(str(e))
        except StudentServiceError:
            raise
        except Exception as e:
            raise StudentServiceError(f"Failed to delete student: {str(e)}")

    def search_students(self, query: str) -> List[Student]:
        """
        Search students by name, ID, or registration number.

        Args:
            query: Search query

        Returns:
            List of matching Student objects

        Raises:
            StudentServiceError: If search fails
        """
        try:
            query = FormValidator.validate_required_field(
                query, "Search query"
            )
            return self.queries.search_students(query)
        except ValidationError as e:
            raise StudentServiceError(str(e))
        except Exception as e:
            raise StudentServiceError(f"Search failed: {str(e)}")

    def get_all_students(self) -> List[Student]:
        """
        Get all registered students.

        Returns:
            List of all Student objects

        Raises:
            StudentServiceError: If retrieval fails
        """
        try:
            return self.queries.get_all_students()
        except Exception as e:
            raise StudentServiceError(f"Failed to retrieve students: {str(e)}")

    def filter_students(
        self,
        category: Optional[str] = None,
        session: Optional[str] = None,
        course: Optional[str] = None,
    ) -> List[Student]:
        """
        Filter students by category, session, or course.

        Args:
            category: Student category to filter
            session: Academic session to filter
            course: Course to filter

        Returns:
            List of filtered Student objects

        Raises:
            StudentServiceError: If filtering fails
        """
        try:
            filters = {}

            if category and category != "Select":
                filters["category"] = category

            if session and session != "Select":
                filters["session"] = session

            if course and course != "Select":
                filters["course"] = course

            if not filters:
                return self.get_all_students()

            return self.queries.filter_students(**filters)
        except Exception as e:
            raise StudentServiceError(f"Filtering failed: {str(e)}")

    def add_student_photo(
        self, student_id: str, photo_path: str
    ) -> bool:
        """
        Add or update student photo.

        Args:
            student_id: Student ID
            photo_path: Path to photo file

        Returns:
            True if photo added successfully

        Raises:
            ValidationError: If input is invalid
            StudentServiceError: If operation fails
        """
        try:
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )
            photo_path = FormValidator.validate_required_field(
                photo_path, "Photo path"
            )

            self.queries.add_student_photo(student_id, photo_path)
            return True
        except ValidationError as e:
            raise StudentServiceError(str(e))
        except Exception as e:
            raise StudentServiceError(f"Failed to add photo: {str(e)}")

    def get_student_photo(self, student_id: str) -> Optional[bytes]:
        """
        Get student photo.

        Args:
            student_id: Student ID

        Returns:
            Photo data or None if not found

        Raises:
            StudentServiceError: If retrieval fails
        """
        try:
            student_id = FormValidator.validate_required_field(
                student_id, "Student ID"
            )
            return self.queries.get_student_photo(student_id)
        except ValidationError as e:
            raise StudentServiceError(str(e))
        except Exception as e:
            raise StudentServiceError(f"Failed to retrieve photo: {str(e)}")

    def get_student_count(self) -> int:
        """
        Get total number of registered students.

        Returns:
            Count of students

        Raises:
            StudentServiceError: If count fails
        """
        try:
            students = self.get_all_students()
            return len(students)
        except Exception as e:
            raise StudentServiceError(f"Failed to get student count: {str(e)}")

    def get_students_by_session(self, session: str) -> List[Student]:
        """
        Get all students in a specific session.

        Args:
            session: Academic session

        Returns:
            List of students in session

        Raises:
            StudentServiceError: If retrieval fails
        """
        try:
            session = FormValidator.validate_required_field(session, "Session")
            return self.queries.filter_students(session=session)
        except ValidationError as e:
            raise StudentServiceError(str(e))
        except Exception as e:
            raise StudentServiceError(f"Failed to retrieve students: {str(e)}")
