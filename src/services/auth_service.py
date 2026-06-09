"""Authentication service for user management."""

import hashlib
from datetime import datetime, timedelta
from typing import Optional

from src.database.models import User
from src.database.queries import DatabaseQueries
from src.validators.form_validator import FormValidator, ValidationError


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""

    pass


class AuthService:
    """Service for handling user authentication and sessions."""

    def __init__(self, queries: DatabaseQueries):
        """
        Initialize authentication service.

        Args:
            queries: Database queries instance
        """
        self.queries = queries
        self.current_user: Optional[User] = None
        self.session_timeout = timedelta(hours=8)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using SHA256.

        Args:
            password: Plain text password

        Returns:
            Hashed password

        Raises:
            ValidationError: If password is invalid
        """
        FormValidator.validate_password(password, min_length=6)
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            password: Plain text password to verify
            password_hash: Stored password hash

        Returns:
            True if password matches, False otherwise
        """
        return hashlib.sha256(password.encode()).hexdigest() == password_hash

    def register_user(
        self, username: str, password: str, role: str = "staff"
    ) -> User:
        """
        Register a new user.

        Args:
            username: Username to register
            password: Plain text password
            role: User role (admin, teacher, staff)

        Returns:
            Created User object

        Raises:
            ValidationError: If input is invalid
            AuthenticationError: If registration fails
        """
        try:
            # Validate inputs
            username = FormValidator.validate_required_field(
                username, "Username"
            )
            password = FormValidator.validate_password(password)

            # Check if username already exists
            existing_user = self.queries.get_user_by_username(username)
            if existing_user:
                raise AuthenticationError(
                    f"Username '{username}' already exists"
                )

            # Hash password
            password_hash = self.hash_password(password)

            # Create user in database
            user_id = self.queries.create_user(
                username=username, password_hash=password_hash, role=role
            )

            # Return user object
            return User(
                user_id=user_id,
                username=username,
                password_hash=password_hash,
                role=role,
                created_at=datetime.now().isoformat(),
            )
        except ValidationError:
            raise
        except Exception as e:
            raise AuthenticationError(f"Registration failed: {str(e)}")

    def login(self, username: str, password: str) -> User:
        """
        Authenticate user with username and password.

        Args:
            username: Username
            password: Plain text password

        Returns:
            Authenticated User object

        Raises:
            ValidationError: If inputs are invalid
            AuthenticationError: If authentication fails
        """
        try:
            # Validate inputs
            username = FormValidator.validate_required_field(
                username, "Username"
            )
            password = FormValidator.validate_required_field(
                password, "Password"
            )

            # Get user from database
            user = self.queries.get_user_by_username(username)
            if not user:
                raise AuthenticationError("Invalid username or password")

            # Verify password
            if not self.verify_password(password, user.password_hash):
                raise AuthenticationError("Invalid username or password")

            # Set current user
            self.current_user = user

            return user
        except ValidationError:
            raise
        except AuthenticationError:
            raise
        except Exception as e:
            raise AuthenticationError(f"Login failed: {str(e)}")

    def logout(self) -> None:
        """Logout current user."""
        self.current_user = None

    def is_logged_in(self) -> bool:
        """Check if a user is currently logged in."""
        return self.current_user is not None

    def get_current_user(self) -> Optional[User]:
        """Get currently logged in user."""
        return self.current_user

    def is_admin(self) -> bool:
        """Check if current user is admin."""
        if not self.current_user:
            return False
        return self.current_user.is_admin()

    def is_teacher(self) -> bool:
        """Check if current user is teacher."""
        if not self.current_user:
            return False
        return self.current_user.is_teacher()

    def is_staff(self) -> bool:
        """Check if current user is staff."""
        if not self.current_user:
            return False
        return self.current_user.is_staff()

    def change_password(
        self, old_password: str, new_password: str
    ) -> bool:
        """
        Change password for current user.

        Args:
            old_password: Current password
            new_password: New password

        Returns:
            True if password changed successfully

        Raises:
            ValidationError: If inputs are invalid
            AuthenticationError: If change fails
        """
        if not self.current_user:
            raise AuthenticationError("No user logged in")

        try:
            # Validate new password
            new_password = FormValidator.validate_password(new_password)

            # Verify old password
            if not self.verify_password(
                old_password, self.current_user.password_hash
            ):
                raise AuthenticationError("Current password is incorrect")

            # Hash new password
            new_password_hash = self.hash_password(new_password)

            # Update in database
            query = "UPDATE users SET password_hash = ? WHERE id = ?"
            self.queries.db.execute(
                query, (new_password_hash, self.current_user.user_id)
            )

            # Update current user object
            self.current_user.password_hash = new_password_hash

            return True
        except ValidationError:
            raise
        except AuthenticationError:
            raise
        except Exception as e:
            raise AuthenticationError(f"Password change failed: {str(e)}")

    def verify_admin_access(self) -> bool:
        """
        Verify that current user has admin access.

        Returns:
            True if user is admin

        Raises:
            AuthenticationError: If user is not admin
        """
        if not self.current_user:
            raise AuthenticationError("No user logged in")

        if not self.current_user.is_admin():
            raise AuthenticationError("Admin access required")

        return True

    def verify_teacher_access(self) -> bool:
        """
        Verify that current user has teacher access.

        Returns:
            True if user is admin or teacher

        Raises:
            AuthenticationError: If user is not admin or teacher
        """
        if not self.current_user:
            raise AuthenticationError("No user logged in")

        if not (self.current_user.is_admin() or self.current_user.is_teacher()):
            raise AuthenticationError("Teacher access required")

        return True
