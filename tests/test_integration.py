"""Integration tests for complete workflows.

Tests complete application workflows including:
- User authentication and session management
- Student registration with full validation
- Student information management
- Marks entry and CGPA calculation
"""

import sqlite3
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from src.config.settings import USER_ROLES, STUDENT_CATEGORIES
from src.database.db_manager import DatabaseManager
from src.database.models import ExamMarks, Student, User
from src.database.queries import DatabaseQueries
from src.services.auth_service import AuthService
from src.services.marks_service import MarksService
from src.services.student_service import StudentService
from src.validators.business_rules import BusinessRuleValidator
from src.validators.form_validator import FormValidator, ValidationError


@pytest.fixture
def temp_db() -> Generator[str, None, None]:
    """Create temporary database for testing."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as f:
        db_path = f.name

    yield db_path

    Path(db_path).unlink(missing_ok=True)


@pytest.fixture
def db_manager(temp_db: str) -> DatabaseManager:
    """Initialize database manager with test database."""
    manager = DatabaseManager(temp_db)
    return manager


@pytest.fixture
def queries(db_manager: DatabaseManager) -> DatabaseQueries:
    """Get queries instance."""
    return DatabaseQueries(db_manager)


@pytest.fixture
def auth_service(queries: DatabaseQueries) -> AuthService:
    """Create auth service."""
    return AuthService(queries)


@pytest.fixture
def student_service(
    queries: DatabaseQueries, auth_service: AuthService
) -> StudentService:
    """Create student service."""
    return StudentService(queries, auth_service)


@pytest.fixture
def marks_service(
    queries: DatabaseQueries, student_service: StudentService
) -> MarksService:
    """Create marks service."""
    return MarksService(queries, student_service)


@pytest.fixture
def form_validator() -> FormValidator:
    """Create form validator."""
    return FormValidator()


@pytest.fixture
def business_validator(queries: DatabaseQueries) -> BusinessRuleValidator:
    """Create business rule validator."""
    return BusinessRuleValidator(queries)


class TestAuthenticationWorkflow:
    """Test complete authentication workflow."""

    def test_user_registration_and_login(
        self, auth_service: AuthService, queries: DatabaseQueries
    ) -> None:
        """Test user registration followed by login."""
        username = "testuser"
        password = "SecurePass123!"

        auth_service.register_user(username, password, USER_ROLES["admin"])

        result = auth_service.login(username, password)
        assert result is True
        assert auth_service.is_logged_in()

        current_user = auth_service.get_current_user()
        assert current_user is not None
        assert current_user.username == username

    def test_login_with_invalid_password(self, auth_service: AuthService) -> None:
        """Test login with incorrect password."""
        username = "testuser"
        password = "SecurePass123!"

        auth_service.register_user(username, password, USER_ROLES["admin"])

        result = auth_service.login(username, "WrongPassword")
        assert result is False
        assert not auth_service.is_logged_in()

    def test_session_management(
        self, auth_service: AuthService, queries: DatabaseQueries
    ) -> None:
        """Test session creation and termination."""
        username = "testuser"
        password = "SecurePass123!"

        auth_service.register_user(username, password, USER_ROLES["teacher"])
        assert auth_service.login(username, password)
        assert auth_service.is_logged_in()

        auth_service.logout()
        assert not auth_service.is_logged_in()

    def test_role_based_access_control(self, auth_service: AuthService) -> None:
        """Test role-based access control."""
        admin_user = "admin"
        teacher_user = "teacher"
        password = "SecurePass123!"

        auth_service.register_user(admin_user, password, USER_ROLES["admin"])
        auth_service.register_user(teacher_user, password, USER_ROLES["teacher"])

        auth_service.login(admin_user, password)
        assert auth_service.is_admin()
        assert not auth_service.is_teacher()

        auth_service.logout()

        auth_service.login(teacher_user, password)
        assert not auth_service.is_admin()
        assert auth_service.is_teacher()


class TestStudentRegistrationWorkflow:
    """Test complete student registration workflow."""

    def test_full_student_registration(
        self,
        student_service: StudentService,
        form_validator: FormValidator,
        business_validator: BusinessRuleValidator,
        queries: DatabaseQueries,
    ) -> None:
        """Test complete student registration with validation."""
        student_id = "STU001"
        name = "John Doe"
        email = "john@example.com"
        phone = "9876543210"
        dob = "2005-01-15"
        sex = "M"
        category = STUDENT_CATEGORIES[0]
        nationality = "Indian"
        address = "123 Main St"
        city = "Mumbai"
        state = "Maharashtra"
        country = "India"

        form_validator.validate_name(name)
        form_validator.validate_email(email)
        form_validator.validate_phone(phone)
        form_validator.validate_date(dob)

        student_data = {
            "student_id": student_id,
            "name": name,
            "email": email,
            "phone": phone,
            "dob": dob,
            "sex": sex,
            "category": category,
            "nationality": nationality,
            "address": address,
            "city": city,
            "state": state,
            "country": country,
        }

        student_service.register_student(student_data)

        retrieved_student = queries.get_student_by_id(student_id)
        assert retrieved_student is not None
        assert retrieved_student.name == name
        assert retrieved_student.email == email

    def test_duplicate_student_registration(
        self, student_service: StudentService, form_validator: FormValidator
    ) -> None:
        """Test that duplicate student ID is rejected."""
        student_id = "STU001"
        student_data = {
            "student_id": student_id,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "dob": "2005-01-15",
            "sex": "M",
            "category": STUDENT_CATEGORIES[0],
            "nationality": "Indian",
            "address": "123 Main St",
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
        }

        student_service.register_student(student_data)

        with pytest.raises(Exception):
            student_service.register_student(student_data)

    def test_student_information_update(
        self, student_service: StudentService, queries: DatabaseQueries
    ) -> None:
        """Test updating student information."""
        student_id = "STU001"
        original_data = {
            "student_id": student_id,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "dob": "2005-01-15",
            "sex": "M",
            "category": STUDENT_CATEGORIES[0],
            "nationality": "Indian",
            "address": "123 Main St",
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
        }

        student_service.register_student(original_data)

        updated_data = original_data.copy()
        updated_data["email"] = "newemail@example.com"
        updated_data["phone"] = "9999999999"

        student_service.update_student(student_id, updated_data)

        retrieved = queries.get_student_by_id(student_id)
        assert retrieved is not None
        assert retrieved.email == "newemail@example.com"
        assert retrieved.phone == "9999999999"

    def test_student_search_and_filter(
        self, student_service: StudentService
    ) -> None:
        """Test searching and filtering students."""
        students_data = [
            {
                "student_id": f"STU00{i}",
                "name": f"Student {i}",
                "email": f"student{i}@example.com",
                "phone": f"987654321{i}",
                "dob": "2005-01-15",
                "sex": "M",
                "category": STUDENT_CATEGORIES[0],
                "nationality": "Indian",
                "address": f"{i} Main St",
                "city": "Mumbai",
                "state": "Maharashtra",
                "country": "India",
            }
            for i in range(1, 4)
        ]

        for data in students_data:
            student_service.register_student(data)

        results = student_service.search_students("Student 2")
        assert len(results) > 0
        assert any(s.name == "Student 2" for s in results)


class TestMarksManagementWorkflow:
    """Test complete marks management workflow."""

    def test_marks_entry_and_retrieval(
        self,
        student_service: StudentService,
        marks_service: MarksService,
        queries: DatabaseQueries,
    ) -> None:
        """Test entering and retrieving marks."""
        student_id = "STU001"
        student_data = {
            "student_id": student_id,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "dob": "2005-01-15",
            "sex": "M",
            "category": STUDENT_CATEGORIES[0],
            "nationality": "Indian",
            "address": "123 Main St",
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
        }

        student_service.register_student(student_data)

        marks_data = {
            "student_id": student_id,
            "subject": "Mathematics",
            "marks": 85,
            "semester": "Sem-I",
            "exam_type": "Final",
        }

        marks_service.add_marks(marks_data)

        marks = marks_service.get_marks(student_id)
        assert len(marks) > 0
        assert marks[0]["subject"] == "Mathematics"
        assert marks[0]["marks"] == 85

    def test_cgpa_calculation(
        self,
        student_service: StudentService,
        marks_service: MarksService,
    ) -> None:
        """Test CGPA calculation with multiple marks."""
        student_id = "STU001"
        student_data = {
            "student_id": student_id,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "dob": "2005-01-15",
            "sex": "M",
            "category": STUDENT_CATEGORIES[0],
            "nationality": "Indian",
            "address": "123 Main St",
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
        }

        student_service.register_student(student_data)

        subjects = [
            {"subject": "Mathematics", "marks": 90},
            {"subject": "English", "marks": 85},
            {"subject": "Science", "marks": 88},
        ]

        for subject_marks in subjects:
            marks_data = {
                "student_id": student_id,
                "subject": subject_marks["subject"],
                "marks": subject_marks["marks"],
                "semester": "Sem-I",
                "exam_type": "Final",
            }
            marks_service.add_marks(marks_data)

        cgpa = marks_service.calculate_cgpa(student_id)
        assert cgpa is not None
        assert 0 <= cgpa <= 10

    def test_grade_assignment(
        self,
        student_service: StudentService,
        marks_service: MarksService,
    ) -> None:
        """Test grade assignment based on percentage."""
        student_id = "STU001"
        student_data = {
            "student_id": student_id,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "dob": "2005-01-15",
            "sex": "M",
            "category": STUDENT_CATEGORIES[0],
            "nationality": "Indian",
            "address": "123 Main St",
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
        }

        student_service.register_student(student_data)

        test_cases = [
            (90, "A+"),
            (85, "A"),
            (75, "B"),
            (65, "C"),
            (55, "D"),
        ]

        for marks, expected_grade in test_cases:
            grade = marks_service.assign_grade_by_percentage(marks)
            assert grade == expected_grade


class TestValidationIntegration:
    """Test validation integration across workflows."""

    def test_validation_error_handling(self, form_validator: FormValidator) -> None:
        """Test validation error handling."""
        invalid_inputs = [
            ("", "validate_name"),
            ("a" * 101, "validate_name"),
            ("invalid-email", "validate_email"),
            ("12345", "validate_phone"),
            ("invalid-date", "validate_date"),
        ]

        for invalid_input, validator_method in invalid_inputs:
            with pytest.raises(ValidationError):
                getattr(form_validator, validator_method)(invalid_input)

    def test_business_rule_validation(
        self, business_validator: BusinessRuleValidator, queries: DatabaseQueries
    ) -> None:
        """Test business rule validation."""
        user_data = ("testuser", "hash", USER_ROLES["admin"], "2026-01-01")
        queries.create_user(*user_data)

        with pytest.raises(Exception):
            business_validator.validate_student_id_unique("STU001", queries)
            queries.create_student("STU001", "Test", "test@example.com")
            business_validator.validate_student_id_unique("STU001", queries)


class TestDataPersistence:
    """Test data persistence across operations."""

    def test_data_consistency_across_services(
        self,
        student_service: StudentService,
        marks_service: MarksService,
        queries: DatabaseQueries,
    ) -> None:
        """Test data consistency when using multiple services."""
        student_id = "STU001"
        student_data = {
            "student_id": student_id,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "dob": "2005-01-15",
            "sex": "M",
            "category": STUDENT_CATEGORIES[0],
            "nationality": "Indian",
            "address": "123 Main St",
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
        }

        student_service.register_student(student_data)

        marks_service.add_marks(
            {
                "student_id": student_id,
                "subject": "Math",
                "marks": 85,
                "semester": "Sem-I",
                "exam_type": "Final",
            }
        )

        retrieved_student = queries.get_student_by_id(student_id)
        assert retrieved_student is not None
        assert retrieved_student.name == "John Doe"

        marks = queries.get_student_marks(student_id)
        assert len(marks) > 0

    def test_transaction_rollback_on_error(
        self, student_service: StudentService, queries: DatabaseQueries
    ) -> None:
        """Test transaction rollback on error."""
        student_id = "STU001"
        student_data = {
            "student_id": student_id,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "dob": "2005-01-15",
            "sex": "M",
            "category": STUDENT_CATEGORIES[0],
            "nationality": "Indian",
            "address": "123 Main St",
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
        }

        student_service.register_student(student_data)

        try:
            student_service.register_student(student_data)
        except Exception:
            pass

        retrieved = queries.get_student_by_id(student_id)
        assert retrieved is not None


class TestErrorHandlingAndRecovery:
    """Test error handling and recovery mechanisms."""

    def test_graceful_database_error_handling(
        self, student_service: StudentService
    ) -> None:
        """Test graceful handling of database errors."""
        invalid_data = {
            "student_id": None,
            "name": "",
            "email": "invalid",
            "phone": "123",
            "dob": "2005-01-15",
            "sex": "M",
            "category": STUDENT_CATEGORIES[0],
            "nationality": "Indian",
            "address": "123 Main St",
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
        }

        with pytest.raises(Exception):
            student_service.register_student(invalid_data)

    def test_form_validation_with_recovery(
        self, form_validator: FormValidator
    ) -> None:
        """Test form validation with recovery."""
        test_cases = [
            ("John Doe", "validate_name", "John Doe"),
            ("john@example.com", "validate_email", "john@example.com"),
            ("9876543210", "validate_phone", "9876543210"),
            ("85", "validate_marks", 85.0),
        ]

        for valid_input, validator_method, expected in test_cases:
            result = getattr(form_validator, validator_method)(valid_input)
            assert result == expected
