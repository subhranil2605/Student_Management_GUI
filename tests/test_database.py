"""Database layer tests."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from src.database.db_manager import DatabaseManager
from src.database.models import (
    ExamMarks,
    Student,
    StudentAcademicInfo,
    StudentAddressInfo,
    StudentBasicInfo,
    StudentContactInfo,
    StudentEducationInfo,
)
from src.database.queries import DatabaseQueries


class TestDatabaseManager(unittest.TestCase):
    """Test DatabaseManager class."""

    def setUp(self):
        """Set up test database."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_path = Path(self.temp_db.name)
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.db_path)

    def tearDown(self):
        """Clean up test database."""
        self.db_manager.close()
        self.db_path.unlink()

    def test_database_initialization(self):
        """Test database initialization creates tables."""
        self.assertTrue(self.db_manager.table_exists("users"))
        self.assertTrue(self.db_manager.table_exists("students"))
        self.assertTrue(self.db_manager.table_exists("student_photos"))
        self.assertTrue(self.db_manager.table_exists("student_marks"))
        self.assertTrue(self.db_manager.table_exists("email_photos"))

    def test_get_connection(self):
        """Test database connection."""
        with self.db_manager.get_connection() as conn:
            self.assertIsNotNone(conn)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)

    def test_execute_query(self):
        """Test execute method."""
        # Insert test data
        query = "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)"
        user_id = self.db_manager.execute(query, ("testuser", "hash123", "admin"))
        self.assertIsNotNone(user_id)

        # Verify insertion
        select_query = "SELECT * FROM users WHERE id = ?"
        results = self.db_manager.execute(select_query, (user_id,))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "testuser")

    def test_execute_many(self):
        """Test execute_many method."""
        params_list = [
            ("user1", "hash1", "admin"),
            ("user2", "hash2", "teacher"),
            ("user3", "hash3", "staff"),
        ]
        query = "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)"
        self.db_manager.execute_many(query, params_list)

        # Verify insertions
        select_query = "SELECT COUNT(*) FROM users"
        results = self.db_manager.execute(select_query, ())
        self.assertEqual(results[0][0], 3)

    def test_table_exists(self):
        """Test table_exists method."""
        self.assertTrue(self.db_manager.table_exists("users"))
        self.assertFalse(self.db_manager.table_exists("nonexistent"))

    def test_delete_all_data(self):
        """Test delete_all_data method."""
        # Insert test data
        self.db_manager.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            ("testuser", "hash123", "admin"),
        )

        # Verify insertion
        results = self.db_manager.execute("SELECT COUNT(*) FROM users", ())
        self.assertEqual(results[0][0], 1)

        # Delete all
        self.db_manager.delete_all_data()

        # Verify deletion
        results = self.db_manager.execute("SELECT COUNT(*) FROM users", ())
        self.assertEqual(results[0][0], 0)


class TestDatabaseQueries(unittest.TestCase):
    """Test DatabaseQueries class."""

    def setUp(self):
        """Set up test database and queries."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_path = Path(self.temp_db.name)
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.db_path)
        self.queries = DatabaseQueries(self.db_manager)

    def tearDown(self):
        """Clean up test database."""
        self.db_manager.close()
        self.db_path.unlink()

    # ==================== USER TESTS ====================

    def test_create_user(self):
        """Test user creation."""
        user_id = self.queries.create_user("testuser", "hash123", "admin")
        self.assertIsNotNone(user_id)

    def test_get_user_by_username(self):
        """Test get user by username."""
        self.queries.create_user("testuser", "hash123", "admin")
        user = self.queries.get_user_by_username("testuser")

        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password_hash, "hash123")
        self.assertEqual(user.role, "admin")

    def test_get_user_by_id(self):
        """Test get user by ID."""
        user_id = self.queries.create_user("testuser", "hash123", "admin")
        user = self.queries.get_user_by_id(user_id)

        self.assertIsNotNone(user)
        self.assertEqual(user.user_id, user_id)
        self.assertEqual(user.username, "testuser")

    def test_get_nonexistent_user(self):
        """Test getting non-existent user."""
        user = self.queries.get_user_by_username("nonexistent")
        self.assertIsNone(user)

    # ==================== STUDENT TESTS ====================

    def _create_test_student(self) -> Student:
        """Create a test student."""
        return Student(
            student_id=0,
            basic_info=StudentBasicInfo(
                fullname="John Doe",
                sex="Male",
                category="General",
                religion="Hindu",
                nationality="Indian",
                handicapped="no",
                percentage_handicap="",
                dob="2000-01-01",
                father_name="Father Name",
                father_occupation="Engineer",
                mother_name="Mother Name",
                mother_occupation="Doctor",
                guardian_name="Guardian Name",
                guardian_relation="Uncle",
            ),
            academic_info=StudentAcademicInfo(
                session="2020-2024",
                reg_no="REG001",
                student_id="STU001",
                course="B.Tech",
            ),
            contact_info=StudentContactInfo(
                contact="9876543210",
                email="john@example.com",
                guardian_contact="9876543211",
                guardian_email="guardian@example.com",
            ),
            address_info=StudentAddressInfo(
                aadhaar="123456789012",
                permanent_address="123 Main St",
                permanent_pincode="123456",
                present_address="456 Oak St",
                present_pincode="654321",
                city="Springfield",
                district="District",
                state="State",
                country="India",
            ),
            education_info=StudentEducationInfo(
                last_institution="High School",
                last_institution_address="789 School St",
                hobby="Reading",
            ),
        )

    def test_create_student(self):
        """Test student creation."""
        student = self._create_test_student()
        student_id = self.queries.create_student(student)

        self.assertIsNotNone(student_id)
        self.assertGreater(student_id, 0)

    def test_get_student_by_id(self):
        """Test get student by ID."""
        student = self._create_test_student()
        student_id = self.queries.create_student(student)

        retrieved = self.queries.get_student_by_id(student_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.get_full_name(), "John Doe")
        self.assertEqual(retrieved.get_email(), "john@example.com")

    def test_get_student_by_email(self):
        """Test get student by email."""
        student = self._create_test_student()
        self.queries.create_student(student)

        retrieved = self.queries.get_student_by_email("john@example.com")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.get_full_name(), "John Doe")

    def test_get_student_by_student_id(self):
        """Test get student by student ID."""
        student = self._create_test_student()
        self.queries.create_student(student)

        retrieved = self.queries.get_student_by_student_id("STU001")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.get_student_id(), "STU001")

    def test_get_all_students(self):
        """Test get all students."""
        student1 = self._create_test_student()
        student1.contact_info.email = "student1@example.com"
        student1.academic_info.student_id = "STU001"
        student1.academic_info.reg_no = "REG001"

        student2 = self._create_test_student()
        student2.basic_info.fullname = "Jane Doe"
        student2.contact_info.email = "student2@example.com"
        student2.academic_info.student_id = "STU002"
        student2.academic_info.reg_no = "REG002"

        self.queries.create_student(student1)
        self.queries.create_student(student2)

        students = self.queries.get_all_students()
        self.assertEqual(len(students), 2)

    def test_search_students(self):
        """Test student search."""
        student = self._create_test_student()
        self.queries.create_student(student)

        # Search by name
        results = self.queries.search_students("John")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get_full_name(), "John Doe")

        # Search by email
        results = self.queries.search_students("john@example")
        self.assertEqual(len(results), 1)

        # Search by student ID
        results = self.queries.search_students("STU001")
        self.assertEqual(len(results), 1)

    def test_update_student(self):
        """Test student update."""
        student = self._create_test_student()
        student_id = self.queries.create_student(student)

        # Update student
        updated_student = self.queries.get_student_by_id(student_id)
        updated_student.basic_info.fullname = "Updated Name"
        self.queries.update_student(updated_student)

        # Verify update
        retrieved = self.queries.get_student_by_id(student_id)
        self.assertEqual(retrieved.get_full_name(), "Updated Name")

    def test_delete_student(self):
        """Test student deletion."""
        student = self._create_test_student()
        student_id = self.queries.create_student(student)

        # Delete
        self.queries.delete_student(student_id)

        # Verify deletion
        retrieved = self.queries.get_student_by_id(student_id)
        self.assertIsNone(retrieved)

    def test_student_exists(self):
        """Test student_exists method."""
        student = self._create_test_student()
        self.queries.create_student(student)

        # Check by email
        self.assertTrue(self.queries.student_exists(email="john@example.com"))
        self.assertFalse(self.queries.student_exists(email="nonexistent@example.com"))

        # Check by student ID
        self.assertTrue(self.queries.student_exists(student_id="STU001"))
        self.assertFalse(self.queries.student_exists(student_id="NONEXISTENT"))

    # ==================== PHOTO TESTS ====================

    def test_add_student_photo(self):
        """Test adding student photo."""
        student = self._create_test_student()
        student_id = self.queries.create_student(student)

        photo_data = b"fake_photo_data"
        self.queries.add_student_photo(student_id, photo_data)

        retrieved_photo = self.queries.get_student_photo(student_id)
        self.assertEqual(retrieved_photo, photo_data)

    def test_update_student_photo(self):
        """Test updating student photo."""
        student = self._create_test_student()
        student_id = self.queries.create_student(student)

        # Add initial photo
        self.queries.add_student_photo(student_id, b"photo1")
        self.assertEqual(self.queries.get_student_photo(student_id), b"photo1")

        # Update photo
        self.queries.update_student_photo(student_id, b"photo2")
        self.assertEqual(self.queries.get_student_photo(student_id), b"photo2")

    def test_email_photo(self):
        """Test email photo operations."""
        self.queries.add_email_photo("test@example.com", b"email_photo")

        retrieved = self.queries.get_email_photo("test@example.com")
        self.assertEqual(retrieved, b"email_photo")

    # ==================== MARKS TESTS ====================

    def test_add_student_marks(self):
        """Test adding student marks."""
        student = self._create_test_student()
        student_id = self.queries.create_student(student)

        marks = ExamMarks(
            exam_number=1,
            exam_name="12th Grade",
            board="State Board",
            total_marks="500",
            cgpa="8.5",
            percentage="85",
            pass_year="2020",
        )
        self.queries.add_student_marks(student_id, marks)

        retrieved_marks = self.queries.get_student_marks(student_id)
        self.assertEqual(len(retrieved_marks), 1)
        self.assertEqual(retrieved_marks[0].exam_name, "12th Grade")
        self.assertEqual(retrieved_marks[0].cgpa, "8.5")

    def test_get_student_marks(self):
        """Test getting all student marks."""
        student = self._create_test_student()
        student_id = self.queries.create_student(student)

        # Add multiple marks
        for i in range(1, 5):
            marks = ExamMarks(
                exam_number=i,
                exam_name=f"Exam {i}",
                board="Board",
                total_marks="100",
                cgpa=str(7.0 + i),
                percentage=str(70 + i),
                pass_year="2020",
            )
            self.queries.add_student_marks(student_id, marks)

        retrieved_marks = self.queries.get_student_marks(student_id)
        self.assertEqual(len(retrieved_marks), 4)

    def test_update_student_marks(self):
        """Test updating student marks."""
        student = self._create_test_student()
        student_id = self.queries.create_student(student)

        # Add marks
        marks = ExamMarks(
            exam_number=1,
            exam_name="Original",
            board="Board",
            total_marks="100",
            cgpa="7.5",
            percentage="75",
            pass_year="2020",
        )
        self.queries.add_student_marks(student_id, marks)

        # Update marks
        updated_marks = ExamMarks(
            exam_number=1,
            exam_name="Updated",
            board="Board",
            total_marks="100",
            cgpa="8.5",
            percentage="85",
            pass_year="2020",
        )
        self.queries.update_student_marks(student_id, 1, updated_marks)

        # Verify update
        retrieved_marks = self.queries.get_student_marks(student_id)
        self.assertEqual(retrieved_marks[0].exam_name, "Updated")
        self.assertEqual(retrieved_marks[0].cgpa, "8.5")


class TestDatabaseIntegration(unittest.TestCase):
    """Integration tests for database operations."""

    def setUp(self):
        """Set up test database."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_path = Path(self.temp_db.name)
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.db_path)
        self.queries = DatabaseQueries(self.db_manager)

    def tearDown(self):
        """Clean up test database."""
        self.db_manager.close()
        self.db_path.unlink()

    def test_complete_workflow(self):
        """Test complete student workflow."""
        # Create student
        student = Student(
            student_id=0,
            basic_info=StudentBasicInfo(
                fullname="Integration Test",
                sex="Male",
                category="General",
                religion="Hindu",
                nationality="Indian",
                handicapped="no",
                percentage_handicap="",
                dob="2000-01-01",
                father_name="Father",
                father_occupation="Engineer",
                mother_name="Mother",
                mother_occupation="Doctor",
                guardian_name="Guardian",
                guardian_relation="Uncle",
            ),
            academic_info=StudentAcademicInfo(
                session="2020-2024",
                reg_no="REG999",
                student_id="STU999",
                course="B.Tech",
            ),
            contact_info=StudentContactInfo(
                contact="9876543210",
                email="integration@example.com",
                guardian_contact="9876543211",
                guardian_email="guardian@example.com",
            ),
            address_info=StudentAddressInfo(
                aadhaar="123456789012",
                permanent_address="123 Main St",
                permanent_pincode="123456",
                present_address="456 Oak St",
                present_pincode="654321",
                city="Springfield",
                district="District",
                state="State",
                country="India",
            ),
            education_info=StudentEducationInfo(
                last_institution="High School",
                last_institution_address="789 School St",
                hobby="Reading",
            ),
        )

        # Create student
        student_id = self.queries.create_student(student)
        self.assertIsNotNone(student_id)

        # Add photo
        self.queries.add_student_photo(student_id, b"test_photo")

        # Add marks
        for i in range(1, 5):
            marks = ExamMarks(
                exam_number=i,
                exam_name=f"Exam {i}",
                board="Board",
                total_marks="100",
                cgpa="8.0",
                percentage="80",
                pass_year="2020",
            )
            self.queries.add_student_marks(student_id, marks)

        # Retrieve complete student
        retrieved = self.queries.get_student_by_id(student_id)
        self.assertEqual(retrieved.get_full_name(), "Integration Test")
        self.assertIsNotNone(retrieved.photo)
        self.assertEqual(len(retrieved.exam_marks), 4)

        # Search students
        results = self.queries.search_students("Integration")
        self.assertEqual(len(results), 1)

        # Delete student
        self.queries.delete_student(student_id)
        self.assertIsNone(self.queries.get_student_by_id(student_id))


if __name__ == "__main__":
    unittest.main()
