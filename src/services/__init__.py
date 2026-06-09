"""Services module for business logic."""

from src.services.auth_service import AuthService, AuthenticationError
from src.services.marks_service import MarksService, MarksServiceError
from src.services.student_service import StudentService, StudentServiceError

__all__ = [
    "AuthService",
    "AuthenticationError",
    "StudentService",
    "StudentServiceError",
    "MarksService",
    "MarksServiceError",
]
