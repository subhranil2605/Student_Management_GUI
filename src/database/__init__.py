"""Database module for data access layer."""

from src.database.db_manager import DatabaseManager
from src.database.models import (
    ExamMarks,
    Student,
    StudentAcademicInfo,
    StudentAddressInfo,
    StudentBasicInfo,
    StudentContactInfo,
    StudentEducationInfo,
    User,
)
from src.database.queries import DatabaseQueries, QueryError

__all__ = [
    "DatabaseManager",
    "DatabaseQueries",
    "QueryError",
    "User",
    "Student",
    "StudentBasicInfo",
    "StudentAcademicInfo",
    "StudentContactInfo",
    "StudentAddressInfo",
    "StudentEducationInfo",
    "ExamMarks",
]
