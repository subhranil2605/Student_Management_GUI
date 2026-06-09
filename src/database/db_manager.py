"""Database management and connection handling."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from src.config.settings import DATABASE_PATH, DATABASE_TIMEOUT


class DatabaseManager:
    """Manages database connections and initialization."""

    def __init__(self, db_path: Path = DATABASE_PATH):
        """Initialize database manager.

        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self.timeout = DATABASE_TIMEOUT
        self._initialize_database()

    def _initialize_database(self) -> None:
        """Initialize database with required tables."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'staff',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # Students table (main table)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fullname TEXT NOT NULL,
                    sex TEXT,
                    category TEXT,
                    religion TEXT,
                    nationality TEXT,
                    handicapped TEXT,
                    percentage_handicap TEXT,
                    dob TEXT,
                    father_name TEXT,
                    father_occupation TEXT,
                    mother_name TEXT,
                    mother_occupation TEXT,
                    guardian_name TEXT,
                    guardian_relation TEXT,
                    session TEXT,
                    reg_no TEXT UNIQUE,
                    student_id TEXT UNIQUE,
                    course TEXT,
                    contact TEXT,
                    email TEXT UNIQUE,
                    guardian_contact TEXT,
                    guardian_email TEXT,
                    aadhaar TEXT,
                    permanent_address TEXT,
                    permanent_pincode TEXT,
                    present_address TEXT,
                    present_pincode TEXT,
                    city TEXT,
                    district TEXT,
                    state TEXT,
                    country TEXT,
                    last_institution TEXT,
                    last_institution_address TEXT,
                    hobby TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # Photos table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS student_photos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL UNIQUE,
                    photo BLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
                )
                """
            )

            # Marks table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS student_marks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    exam_number INTEGER NOT NULL,
                    exam_name TEXT,
                    board TEXT,
                    total_marks TEXT,
                    cgpa TEXT,
                    percentage TEXT,
                    pass_year TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                    UNIQUE(student_id, exam_number)
                )
                """
            )

            # Email authentication table (for photo storage)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS email_photos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    photo BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conn.commit()

    @contextmanager
    def get_connection(self):
        """Get database connection context manager.

        Yields:
            sqlite3.Connection: Database connection.
        """
        conn = sqlite3.connect(str(self.db_path), timeout=self.timeout)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = ()) -> Optional[list]:
        """Execute a query and return results.

        Args:
            query: SQL query to execute.
            params: Query parameters.

        Returns:
            List of results or None for non-SELECT queries.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.lastrowid if query.strip().upper().startswith("INSERT") else None

    def execute_many(self, query: str, params_list: list[tuple]) -> None:
        """Execute multiple queries with different parameters.

        Args:
            query: SQL query to execute.
            params_list: List of parameter tuples.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()

    def get_last_insert_id(self) -> int:
        """Get last inserted row ID.

        Returns:
            Last insert ID.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT last_insert_rowid()")
            return cursor.fetchone()[0]

    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists.

        Args:
            table_name: Name of the table.

        Returns:
            True if table exists, False otherwise.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,),
            )
            return cursor.fetchone() is not None

    def delete_all_data(self) -> None:
        """Delete all data from database (for testing).

        WARNING: This will delete all data!
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM student_marks")
            cursor.execute("DELETE FROM student_photos")
            cursor.execute("DELETE FROM email_photos")
            cursor.execute("DELETE FROM students")
            cursor.execute("DELETE FROM users")
            conn.commit()

    def close(self) -> None:
        """Close database connection."""
        # SQLite auto-closes via context manager, this is for explicit cleanup
        pass
