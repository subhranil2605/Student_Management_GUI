"""Unit tests for service layer."""

import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from src.services.auth_service import AuthService, AuthenticationError
from src.services.student_service import StudentService, StudentServiceError
from src.services.marks_service import MarksService, MarksServiceError
from src.validators.business_rules import BusinessRuleValidator
from src.validators.form_validator import ValidationError


class TestAuthService(unittest.TestCase):
    """Test authentication service."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_queries = MagicMock()
        self.auth_service = AuthService(self.mock_queries)

    def test_hash_password_valid(self):
        """Test password hashing."""
        password = "test_password_123"
        hashed = AuthService.hash_password(password)
        self.assertNotEqual(hashed, password)
        self.assertEqual(len(hashed), 64)

    def test_hash_password_too_short(self):
        """Test short password raises error."""
        with self.assertRaises(ValidationError):
            AuthService.hash_password("short")

    def test_verify_password_valid(self):
        """Test password verification."""
        password = "test_password_123"
        hashed = AuthService.hash_password(password)
        self.assertTrue(AuthService.verify_password(password, hashed))

    def test_verify_password_invalid(self):
        """Test wrong password fails verification."""
        password = "test_password_123"
        hashed = AuthService.hash_password(password)
        self.assertFalse(AuthService.verify_password("wrong_password", hashed))

    def test_register_user_valid(self):
        """Test user registration."""
        self.mock_queries.get_user_by_username.return_value = None
        self.mock_queries.create_user.return_value = 1

        user = self.auth_service.register_user(
            "testuser", "password123", role="admin"
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.role, "admin")

    def test_register_user_duplicate(self):
        """Test duplicate username registration fails."""
        mock_user = MagicMock()
        self.mock_queries.get_user_by_username.return_value = mock_user

        with self.assertRaises(AuthenticationError):
            self.auth_service.register_user("testuser", "password123")

    def test_login_valid(self):
        """Test valid login."""
        mock_user = MagicMock()
        mock_user.username = "testuser"
        mock_user.role = "admin"
        mock_user.user_id = 1
        mock_user.created_at = "2024-01-01"

        self.mock_queries.get_user_by_username.return_value = mock_user

        # Mock verify_password to return True
        with patch.object(
            AuthService, "verify_password", return_value=True
        ):
            user = self.auth_service.login("testuser", "password123")

        self.assertEqual(user.username, "testuser")
        self.assertTrue(self.auth_service.is_logged_in())

    def test_login_invalid_username(self):
        """Test login with invalid username."""
        self.mock_queries.get_user_by_username.return_value = None

        with self.assertRaises(AuthenticationError):
            self.auth_service.login("wronguser", "password123")

    def test_login_invalid_password(self):
        """Test login with invalid password."""
        mock_user = MagicMock()
        self.mock_queries.get_user_by_username.return_value = mock_user

        with patch.object(
            AuthService, "verify_password", return_value=False
        ):
            with self.assertRaises(AuthenticationError):
                self.auth_service.login("testuser", "wrongpassword")

    def test_logout(self):
        """Test logout."""
        self.auth_service.current_user = MagicMock()
        self.auth_service.logout()
        self.assertFalse(self.auth_service.is_logged_in())

    def test_is_admin(self):
        """Test admin role check."""
        mock_user = MagicMock()
        mock_user.is_admin.return_value = True
        self.auth_service.current_user = mock_user

        self.assertTrue(self.auth_service.is_admin())

    def test_is_teacher(self):
        """Test teacher role check."""
        mock_user = MagicMock()
        mock_user.is_teacher.return_value = True
        self.auth_service.current_user = mock_user

        self.assertTrue(self.auth_service.is_teacher())

    def test_change_password_valid(self):
        """Test changing password."""
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_user.password_hash = AuthService.hash_password("oldpassword123")
        self.auth_service.current_user = mock_user

        with patch.object(
            AuthService, "verify_password", return_value=True
        ):
            result = self.auth_service.change_password(
                "oldpassword123", "newpassword123"
            )

        self.assertTrue(result)


class TestStudentService(unittest.TestCase):
    """Test student service."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_queries = MagicMock()
        self.mock_business_validator = MagicMock(spec=BusinessRuleValidator)
        self.student_service = StudentService(
            self.mock_queries, self.mock_business_validator
        )

    def test_register_student_valid(self):
        """Test student registration."""
        test_dob = date(2000, 1, 15)

        self.mock_business_validator.validate_student_id_unique.return_value = (
            "STU001"
        )
        self.mock_business_validator.validate_student_age_range.return_value = (
            test_dob
        )
        self.mock_queries.create_student.return_value = MagicMock()

        student = self.student_service.register_student(
            student_id="STU001",
            fullname="John Doe",
            sex="Male",
            category="General",
            dob=test_dob,
            registration_number="REG001",
            session="2022-2026",
            course="B.Tech",
        )

        self.assertIsNotNone(student)

    def test_get_student_valid(self):
        """Test getting student."""
        mock_student = MagicMock()
        self.mock_queries.get_student_by_id.return_value = mock_student

        student = self.student_service.get_student("STU001")

        self.assertEqual(student, mock_student)

    def test_get_student_not_found(self):
        """Test getting non-existent student."""
        self.mock_queries.get_student_by_id.return_value = None

        student = self.student_service.get_student("STU999")

        self.assertIsNone(student)

    def test_search_students_valid(self):
        """Test student search."""
        mock_students = [MagicMock(), MagicMock()]
        self.mock_queries.search_students.return_value = mock_students

        results = self.student_service.search_students("John")

        self.assertEqual(len(results), 2)

    def test_get_all_students(self):
        """Test getting all students."""
        mock_students = [MagicMock(), MagicMock(), MagicMock()]
        self.mock_queries.get_all_students.return_value = mock_students

        students = self.student_service.get_all_students()

        self.assertEqual(len(students), 3)

    def test_filter_students(self):
        """Test filtering students."""
        mock_students = [MagicMock()]
        self.mock_queries.filter_students.return_value = mock_students

        students = self.student_service.filter_students(
            category="General", session="2022-2026"
        )

        self.assertEqual(len(students), 1)

    def test_delete_student_valid(self):
        """Test deleting student."""
        mock_student = MagicMock()
        self.mock_queries.get_student_by_id.return_value = mock_student

        result = self.student_service.delete_student("STU001")

        self.assertTrue(result)


class TestMarksService(unittest.TestCase):
    """Test marks service."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_queries = MagicMock()
        self.mock_business_validator = MagicMock(spec=BusinessRuleValidator)
        self.marks_service = MarksService(
            self.mock_queries, self.mock_business_validator
        )

    def test_add_marks_valid(self):
        """Test adding marks."""
        self.mock_business_validator.validate_marks_range.side_effect = [
            85.0, 100.0
        ]
        self.mock_queries.add_marks.return_value = MagicMock()

        marks = self.marks_service.add_marks(
            student_id="STU001",
            subject="Mathematics",
            marks_obtained=85,
            total_marks=100,
        )

        self.assertIsNotNone(marks)

    def test_calculate_cgpa_valid(self):
        """Test CGPA calculation."""
        mock_marks = [
            MagicMock(percentage=85),
            MagicMock(percentage=90),
            MagicMock(percentage=80),
        ]
        self.mock_queries.get_student_marks.return_value = mock_marks

        cgpa = self.marks_service.calculate_cgpa("STU001")

        self.assertGreater(cgpa, 0)
        self.assertLessEqual(cgpa, 4.0)

    def test_calculate_cgpa_no_marks(self):
        """Test CGPA calculation with no marks."""
        self.mock_queries.get_student_marks.return_value = []

        cgpa = self.marks_service.calculate_cgpa("STU001")

        self.assertEqual(cgpa, 0.0)

    def test_get_average_marks_valid(self):
        """Test getting average marks."""
        mock_marks = [
            MagicMock(percentage=85),
            MagicMock(percentage=90),
        ]
        self.mock_queries.get_student_marks.return_value = mock_marks

        average = self.marks_service.get_average_marks("STU001")

        self.assertEqual(average, 87.5)

    def test_get_best_subject(self):
        """Test getting best subject."""
        mock_marks = [
            MagicMock(subject="Math", marks_obtained=85),
            MagicMock(subject="English", marks_obtained=95),
        ]
        self.mock_queries.get_student_marks.return_value = mock_marks

        best = self.marks_service.get_best_subject("STU001")

        self.assertEqual(best, "English")

    def test_get_worst_subject(self):
        """Test getting worst subject."""
        mock_marks = [
            MagicMock(subject="Math", marks_obtained=85),
            MagicMock(subject="English", marks_obtained=60),
        ]
        self.mock_queries.get_student_marks.return_value = mock_marks

        worst = self.marks_service.get_worst_subject("STU001")

        self.assertEqual(worst, "English")

    def test_assign_grade_a(self):
        """Test grade assignment for A."""
        grade = self.marks_service.assign_grade_by_percentage(95)
        self.assertEqual(grade, "A")

    def test_assign_grade_b(self):
        """Test grade assignment for B."""
        grade = self.marks_service.assign_grade_by_percentage(85)
        self.assertEqual(grade, "B")

    def test_assign_grade_c(self):
        """Test grade assignment for C."""
        grade = self.marks_service.assign_grade_by_percentage(75)
        self.assertEqual(grade, "C")

    def test_assign_grade_d(self):
        """Test grade assignment for D."""
        grade = self.marks_service.assign_grade_by_percentage(65)
        self.assertEqual(grade, "D")

    def test_assign_grade_f(self):
        """Test grade assignment for F."""
        grade = self.marks_service.assign_grade_by_percentage(50)
        self.assertEqual(grade, "F")


if __name__ == "__main__":
    unittest.main()
