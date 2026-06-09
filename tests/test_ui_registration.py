"""Service-layer tests for user registration functionality.

Tests the UserRegistrationWindow business logic including:
- Form field validation
- User registration workflow
- Error handling and user feedback
- Role selection and assignment
"""

import unittest
from unittest.mock import MagicMock, patch

from src.services.auth_service import AuthService, AuthenticationError
from src.validators.form_validator import ValidationError


class TestUserRegistrationLogic(unittest.TestCase):
    """Test user registration logic and validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_queries = MagicMock()
        self.auth_service = AuthService(self.mock_queries)

    def test_registration_with_valid_credentials(self):
        """Test successful user registration with valid credentials."""
        self.mock_queries.get_user_by_username.return_value = None
        self.mock_queries.create_user.return_value = 1

        user = self.auth_service.register_user(
            "newuser", "ValidPass123!", "admin"
        )

        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.role, "admin")

    def test_registration_with_duplicate_username(self):
        """Test registration fails with duplicate username."""
        mock_user = MagicMock()
        self.mock_queries.get_user_by_username.return_value = mock_user

        with self.assertRaises(AuthenticationError):
            self.auth_service.register_user(
                "existinguser", "ValidPass123!", "admin"
            )

    def test_registration_with_empty_username(self):
        """Test registration fails with empty username."""
        with self.assertRaises(ValidationError):
            self.auth_service.register_user("", "ValidPass123!", "admin")

    def test_registration_with_empty_password(self):
        """Test registration fails with empty password."""
        self.mock_queries.get_user_by_username.return_value = None

        with self.assertRaises(ValidationError):
            self.auth_service.register_user("newuser", "", "admin")

    def test_registration_with_short_password(self):
        """Test registration fails with password shorter than 6 characters."""
        self.mock_queries.get_user_by_username.return_value = None

        with self.assertRaises(ValidationError):
            self.auth_service.register_user("newuser", "short", "admin")

    def test_registration_with_teacher_role(self):
        """Test successful registration with teacher role."""
        self.mock_queries.get_user_by_username.return_value = None
        self.mock_queries.create_user.return_value = 2

        user = self.auth_service.register_user(
            "teacheruser", "TeacherPass123!", "teacher"
        )

        self.assertEqual(user.role, "teacher")
        self.mock_queries.create_user.assert_called_once_with(
            username="teacheruser",
            password_hash=user.password_hash,
            role="teacher",
        )

    def test_registration_with_staff_role(self):
        """Test successful registration with staff role."""
        self.mock_queries.get_user_by_username.return_value = None
        self.mock_queries.create_user.return_value = 3

        user = self.auth_service.register_user(
            "staffuser", "StaffPass123!", "staff"
        )

        self.assertEqual(user.role, "staff")

    def test_registration_default_role_is_staff(self):
        """Test registration defaults to staff role when not specified."""
        self.mock_queries.get_user_by_username.return_value = None
        self.mock_queries.create_user.return_value = 4

        user = self.auth_service.register_user(
            "defaultuser", "DefaultPass123!"
        )

        self.assertEqual(user.role, "staff")

    def test_password_hash_is_stored_not_plaintext(self):
        """Test that password hash is stored, not plaintext password."""
        self.mock_queries.get_user_by_username.return_value = None
        self.mock_queries.create_user.return_value = 5

        user = self.auth_service.register_user(
            "testuser", "TestPass123!", "admin"
        )

        # Verify password is hashed
        self.assertNotEqual(user.password_hash, "TestPass123!")
        self.assertEqual(len(user.password_hash), 64)  # SHA256 hex length

    def test_can_login_after_registration(self):
        """Test user can login after registration."""
        # Setup: Register user
        self.mock_queries.get_user_by_username.return_value = None
        self.mock_queries.create_user.return_value = 6

        registered_user = self.auth_service.register_user(
            "loginuser", "LoginPass123!", "admin"
        )

        # Setup: Mock login
        self.mock_queries.get_user_by_username.return_value = registered_user

        with patch.object(
            AuthService, "verify_password", return_value=True
        ):
            logged_in_user = self.auth_service.login(
                "loginuser", "LoginPass123!"
            )

            self.assertEqual(logged_in_user.username, "loginuser")
            self.assertTrue(self.auth_service.is_logged_in())

    def test_username_case_sensitivity(self):
        """Test that usernames are case-sensitive."""
        # First user
        self.mock_queries.get_user_by_username.return_value = None
        self.mock_queries.create_user.return_value = 7

        self.auth_service.register_user("TestUser", "Pass123!", "admin")

        # Second registration with different case should succeed (assuming DB allows it)
        self.mock_queries.get_user_by_username.return_value = None
        self.mock_queries.create_user.return_value = 8

        user2 = self.auth_service.register_user(
            "testuser", "Pass123!", "admin"
        )
        self.assertEqual(user2.username, "testuser")

    def test_registration_creates_unique_user_ids(self):
        """Test that each registration creates unique user IDs."""
        self.mock_queries.get_user_by_username.return_value = None

        # Register first user
        self.mock_queries.create_user.return_value = 10
        user1 = self.auth_service.register_user(
            "user1", "Pass123!", "admin"
        )

        # Register second user
        self.mock_queries.create_user.return_value = 11
        user2 = self.auth_service.register_user(
            "user2", "Pass123!", "admin"
        )

        self.assertNotEqual(user1.user_id, user2.user_id)

    def test_registration_error_message_for_duplicate_username(self):
        """Test error message is clear for duplicate username."""
        mock_user = MagicMock()
        self.mock_queries.get_user_by_username.return_value = mock_user

        with self.assertRaises(AuthenticationError) as context:
            self.auth_service.register_user(
                "duplicate", "Pass123!", "admin"
            )

        self.assertIn("already exists", str(context.exception).lower())

    def test_registration_validates_password_strength(self):
        """Test that password strength is validated during registration."""
        self.mock_queries.get_user_by_username.return_value = None

        # Password must be at least 6 characters
        with self.assertRaises(ValidationError):
            self.auth_service.register_user("user", "weak", "admin")

    def test_registration_success_sets_created_at(self):
        """Test that registration sets created_at timestamp."""
        self.mock_queries.get_user_by_username.return_value = None
        self.mock_queries.create_user.return_value = 12

        user = self.auth_service.register_user(
            "timeuser", "TimePass123!", "admin"
        )

        self.assertIsNotNone(user.created_at)

    def test_multiple_registrations_with_different_roles(self):
        """Test registering multiple users with different roles."""
        self.mock_queries.get_user_by_username.return_value = None

        users_to_register = [
            ("admin_user", "AdminPass123!", "admin"),
            ("teacher_user", "TeachPass123!", "teacher"),
            ("staff_user", "StaffPass123!", "staff"),
        ]

        registered_users = []

        for i, (username, password, role) in enumerate(users_to_register):
            self.mock_queries.create_user.return_value = 20 + i
            user = self.auth_service.register_user(username, password, role)
            registered_users.append(user)

        self.assertEqual(registered_users[0].role, "admin")
        self.assertEqual(registered_users[1].role, "teacher")
        self.assertEqual(registered_users[2].role, "staff")


if __name__ == "__main__":
    unittest.main()
