"""Database query operations for CRUD and search."""

from typing import Optional

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


class QueryError(Exception):
    """Custom exception for database query errors."""

    pass


class DatabaseQueries:
    """Database query operations."""

    def __init__(self, db_manager: DatabaseManager):
        """Initialize database queries.

        Args:
            db_manager: DatabaseManager instance.
        """
        self.db = db_manager

    # ==================== USER OPERATIONS ====================

    def create_user(
        self, username: str, password_hash: str, role: str = "staff"
    ) -> int:
        """Create a new user.

        Args:
            username: Username.
            password_hash: Hashed password.
            role: User role (admin, teacher, staff).

        Returns:
            User ID.

        Raises:
            QueryError: If user creation fails.
        """
        try:
            query = (
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)"
            )
            user_id = self.db.execute(query, (username, password_hash, role))
            return user_id
        except Exception as e:
            raise QueryError(f"Failed to create user: {str(e)}") from e

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username.

        Args:
            username: Username to search.

        Returns:
            User object or None if not found.
        """
        query = "SELECT id, username, password_hash, role, created_at FROM users WHERE username = ?"
        results = self.db.execute(query, (username,))
        if results:
            row = results[0]
            return User(
                user_id=row[0],
                username=row[1],
                password_hash=row[2],
                role=row[3],
                created_at=row[4],
            )
        return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID.

        Args:
            user_id: User ID.

        Returns:
            User object or None if not found.
        """
        query = "SELECT id, username, password_hash, role, created_at FROM users WHERE id = ?"
        results = self.db.execute(query, (user_id,))
        if results:
            row = results[0]
            return User(
                user_id=row[0],
                username=row[1],
                password_hash=row[2],
                role=row[3],
                created_at=row[4],
            )
        return None

    # ==================== STUDENT OPERATIONS ====================

    def create_student(self, student: Student) -> int:
        """Create a new student.

        Args:
            student: Student object.

        Returns:
            Student ID.

        Raises:
            QueryError: If student creation fails.
        """
        try:
            query = """
                INSERT INTO students (
                    fullname, sex, category, religion, nationality, handicapped,
                    percentage_handicap, dob, father_name, father_occupation,
                    mother_name, mother_occupation, guardian_name, guardian_relation,
                    session, reg_no, student_id, course, contact, email,
                    guardian_contact, guardian_email, aadhaar, permanent_address,
                    permanent_pincode, present_address, present_pincode, city,
                    district, state, country, last_institution,
                    last_institution_address, hobby
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                          ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                student.basic_info.fullname,
                student.basic_info.sex,
                student.basic_info.category,
                student.basic_info.religion,
                student.basic_info.nationality,
                student.basic_info.handicapped,
                student.basic_info.percentage_handicap,
                student.basic_info.dob,
                student.basic_info.father_name,
                student.basic_info.father_occupation,
                student.basic_info.mother_name,
                student.basic_info.mother_occupation,
                student.basic_info.guardian_name,
                student.basic_info.guardian_relation,
                student.academic_info.session,
                student.academic_info.reg_no,
                student.academic_info.student_id,
                student.academic_info.course,
                student.contact_info.contact,
                student.contact_info.email,
                student.contact_info.guardian_contact,
                student.contact_info.guardian_email,
                student.address_info.aadhaar,
                student.address_info.permanent_address,
                student.address_info.permanent_pincode,
                student.address_info.present_address,
                student.address_info.present_pincode,
                student.address_info.city,
                student.address_info.district,
                student.address_info.state,
                student.address_info.country,
                student.education_info.last_institution,
                student.education_info.last_institution_address,
                student.education_info.hobby,
            )
            student_id = self.db.execute(query, params)

            # Insert photo if provided
            if student.photo:
                self.add_student_photo(student_id, student.photo)

            # Insert exam marks if provided
            for mark in student.exam_marks:
                self.add_student_marks(student_id, mark)

            return student_id
        except Exception as e:
            raise QueryError(f"Failed to create student: {str(e)}") from e

    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        """Get student by ID.

        Args:
            student_id: Student ID.

        Returns:
            Student object or None if not found.
        """
        query = "SELECT * FROM students WHERE id = ?"
        results = self.db.execute(query, (student_id,))
        if not results:
            return None

        row = dict(results[0])
        student = self._dict_to_student(row, student_id)
        return student

    def get_student_by_email(self, email: str) -> Optional[Student]:
        """Get student by email.

        Args:
            email: Student email.

        Returns:
            Student object or None if not found.
        """
        query = "SELECT * FROM students WHERE email = ?"
        results = self.db.execute(query, (email,))
        if not results:
            return None

        row = dict(results[0])
        student_id = row["id"]
        student = self._dict_to_student(row, student_id)
        return student

    def get_student_by_student_id(self, student_id_str: str) -> Optional[Student]:
        """Get student by student ID string.

        Args:
            student_id_str: Student ID string.

        Returns:
            Student object or None if not found.
        """
        query = "SELECT * FROM students WHERE student_id = ?"
        results = self.db.execute(query, (student_id_str,))
        if not results:
            return None

        row = dict(results[0])
        student_id = row["id"]
        student = self._dict_to_student(row, student_id)
        return student

    def get_all_students(self, session: Optional[str] = None) -> list[Student]:
        """Get all students or students in a session.

        Args:
            session: Optional session filter.

        Returns:
            List of Student objects.
        """
        if session:
            query = "SELECT * FROM students WHERE session = ? ORDER BY fullname"
            results = self.db.execute(query, (session,))
        else:
            query = "SELECT * FROM students ORDER BY fullname"
            results = self.db.execute(query, ())

        students = []
        for row in results or []:
            row_dict = dict(row)
            student_id = row_dict["id"]
            student = self._dict_to_student(row_dict, student_id)
            students.append(student)
        return students

    def search_students(self, search_term: str) -> list[Student]:
        """Search students by name, email, or student ID.

        Args:
            search_term: Search term.

        Returns:
            List of matching Student objects.
        """
        query = """
            SELECT * FROM students WHERE
            fullname LIKE ? OR email LIKE ? OR student_id LIKE ?
            ORDER BY fullname
        """
        search = f"%{search_term}%"
        results = self.db.execute(query, (search, search, search))

        students = []
        for row in results or []:
            row_dict = dict(row)
            student_id = row_dict["id"]
            student = self._dict_to_student(row_dict, student_id)
            students.append(student)
        return students

    def update_student(self, student: Student) -> bool:
        """Update student information.

        Args:
            student: Updated Student object.

        Returns:
            True if successful.

        Raises:
            QueryError: If update fails.
        """
        try:
            query = """
                UPDATE students SET
                fullname = ?, sex = ?, category = ?, religion = ?,
                nationality = ?, handicapped = ?, percentage_handicap = ?,
                dob = ?, father_name = ?, father_occupation = ?,
                mother_name = ?, mother_occupation = ?, guardian_name = ?,
                guardian_relation = ?, session = ?, reg_no = ?, student_id = ?,
                course = ?, contact = ?, email = ?, guardian_contact = ?,
                guardian_email = ?, aadhaar = ?, permanent_address = ?,
                permanent_pincode = ?, present_address = ?, present_pincode = ?,
                city = ?, district = ?, state = ?, country = ?,
                last_institution = ?, last_institution_address = ?, hobby = ?,
                updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            params = (
                student.basic_info.fullname,
                student.basic_info.sex,
                student.basic_info.category,
                student.basic_info.religion,
                student.basic_info.nationality,
                student.basic_info.handicapped,
                student.basic_info.percentage_handicap,
                student.basic_info.dob,
                student.basic_info.father_name,
                student.basic_info.father_occupation,
                student.basic_info.mother_name,
                student.basic_info.mother_occupation,
                student.basic_info.guardian_name,
                student.basic_info.guardian_relation,
                student.academic_info.session,
                student.academic_info.reg_no,
                student.academic_info.student_id,
                student.academic_info.course,
                student.contact_info.contact,
                student.contact_info.email,
                student.contact_info.guardian_contact,
                student.contact_info.guardian_email,
                student.address_info.aadhaar,
                student.address_info.permanent_address,
                student.address_info.permanent_pincode,
                student.address_info.present_address,
                student.address_info.present_pincode,
                student.address_info.city,
                student.address_info.district,
                student.address_info.state,
                student.address_info.country,
                student.education_info.last_institution,
                student.education_info.last_institution_address,
                student.education_info.hobby,
                student.student_id,
            )
            self.db.execute(query, params)

            # Update photo if provided
            if student.photo:
                self.update_student_photo(student.student_id, student.photo)

            return True
        except Exception as e:
            raise QueryError(f"Failed to update student: {str(e)}") from e

    def delete_student(self, student_id: int) -> bool:
        """Delete a student.

        Args:
            student_id: Student ID.

        Returns:
            True if successful.
        """
        query = "DELETE FROM students WHERE id = ?"
        self.db.execute(query, (student_id,))
        return True

    def student_exists(self, email: str = None, student_id: str = None) -> bool:
        """Check if student exists by email or student ID.

        Args:
            email: Student email.
            student_id: Student ID string.

        Returns:
            True if student exists.
        """
        if email:
            query = "SELECT id FROM students WHERE email = ?"
            results = self.db.execute(query, (email,))
        elif student_id:
            query = "SELECT id FROM students WHERE student_id = ?"
            results = self.db.execute(query, (student_id,))
        else:
            return False

        return len(results) > 0 if results else False

    # ==================== STUDENT PHOTO OPERATIONS ====================

    def add_student_photo(self, student_id: int, photo_data: bytes) -> None:
        """Add or update student photo.

        Args:
            student_id: Student ID.
            photo_data: Binary photo data.
        """
        # Check if photo exists
        query = "SELECT id FROM student_photos WHERE student_id = ?"
        results = self.db.execute(query, (student_id,))

        if results:
            # Update existing
            update_query = "UPDATE student_photos SET photo = ? WHERE student_id = ?"
            self.db.execute(update_query, (photo_data, student_id))
        else:
            # Insert new
            insert_query = "INSERT INTO student_photos (student_id, photo) VALUES (?, ?)"
            self.db.execute(insert_query, (student_id, photo_data))

    def get_student_photo(self, student_id: int) -> Optional[bytes]:
        """Get student photo.

        Args:
            student_id: Student ID.

        Returns:
            Photo binary data or None.
        """
        query = "SELECT photo FROM student_photos WHERE student_id = ?"
        results = self.db.execute(query, (student_id,))
        if results:
            return results[0][0]
        return None

    def update_student_photo(self, student_id: int, photo_data: bytes) -> None:
        """Update student photo.

        Args:
            student_id: Student ID.
            photo_data: Binary photo data.
        """
        self.add_student_photo(student_id, photo_data)

    def add_email_photo(self, email: str, photo_data: bytes) -> None:
        """Add photo associated with email (for auth workflow).

        Args:
            email: Email address.
            photo_data: Binary photo data.
        """
        query = "INSERT OR REPLACE INTO email_photos (email, photo) VALUES (?, ?)"
        self.db.execute(query, (email, photo_data))

    def get_email_photo(self, email: str) -> Optional[bytes]:
        """Get photo by email.

        Args:
            email: Email address.

        Returns:
            Photo binary data or None.
        """
        query = "SELECT photo FROM email_photos WHERE email = ?"
        results = self.db.execute(query, (email,))
        if results:
            return results[0][0]
        return None

    # ==================== MARKS OPERATIONS ====================

    def add_student_marks(self, student_id: int, marks: ExamMarks) -> None:
        """Add exam marks for student.

        Args:
            student_id: Student ID.
            marks: ExamMarks object.
        """
        query = """
            INSERT INTO student_marks
            (student_id, exam_number, exam_name, board, total_marks, cgpa, percentage, pass_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            student_id,
            marks.exam_number,
            marks.exam_name,
            marks.board,
            marks.total_marks,
            marks.cgpa,
            marks.percentage,
            marks.pass_year,
        )
        self.db.execute(query, params)

    def get_student_marks(self, student_id: int) -> list[ExamMarks]:
        """Get all marks for a student.

        Args:
            student_id: Student ID.

        Returns:
            List of ExamMarks objects.
        """
        query = "SELECT * FROM student_marks WHERE student_id = ? ORDER BY exam_number"
        results = self.db.execute(query, (student_id,))

        marks = []
        for row in results or []:
            row_dict = dict(row)
            exam_mark = ExamMarks(
                exam_number=row_dict["exam_number"],
                exam_name=row_dict["exam_name"] or "",
                board=row_dict["board"] or "",
                total_marks=row_dict["total_marks"] or "",
                cgpa=row_dict["cgpa"] or "",
                percentage=row_dict["percentage"] or "",
                pass_year=row_dict["pass_year"] or "",
            )
            marks.append(exam_mark)
        return marks

    def update_student_marks(self, student_id: int, exam_number: int, marks: ExamMarks) -> None:
        """Update exam marks for student.

        Args:
            student_id: Student ID.
            exam_number: Exam number.
            marks: Updated ExamMarks object.
        """
        query = """
            UPDATE student_marks
            SET exam_name = ?, board = ?, total_marks = ?, cgpa = ?, percentage = ?, pass_year = ?
            WHERE student_id = ? AND exam_number = ?
        """
        params = (
            marks.exam_name,
            marks.board,
            marks.total_marks,
            marks.cgpa,
            marks.percentage,
            marks.pass_year,
            student_id,
            exam_number,
        )
        self.db.execute(query, params)

    # ==================== HELPER METHODS ====================

    def _dict_to_student(self, row_dict: dict, student_id: int) -> Student:
        """Convert database row to Student object.

        Args:
            row_dict: Database row as dictionary.
            student_id: Student database ID.

        Returns:
            Student object.
        """
        basic_info = StudentBasicInfo(
            fullname=row_dict.get("fullname", ""),
            sex=row_dict.get("sex", ""),
            category=row_dict.get("category", ""),
            religion=row_dict.get("religion", ""),
            nationality=row_dict.get("nationality", ""),
            handicapped=row_dict.get("handicapped", ""),
            percentage_handicap=row_dict.get("percentage_handicap", ""),
            dob=row_dict.get("dob", ""),
            father_name=row_dict.get("father_name", ""),
            father_occupation=row_dict.get("father_occupation", ""),
            mother_name=row_dict.get("mother_name", ""),
            mother_occupation=row_dict.get("mother_occupation", ""),
            guardian_name=row_dict.get("guardian_name", ""),
            guardian_relation=row_dict.get("guardian_relation", ""),
        )

        academic_info = StudentAcademicInfo(
            session=row_dict.get("session", ""),
            reg_no=row_dict.get("reg_no", ""),
            student_id=row_dict.get("student_id", ""),
            course=row_dict.get("course", ""),
        )

        contact_info = StudentContactInfo(
            contact=row_dict.get("contact", ""),
            email=row_dict.get("email", ""),
            guardian_contact=row_dict.get("guardian_contact", ""),
            guardian_email=row_dict.get("guardian_email", ""),
        )

        address_info = StudentAddressInfo(
            aadhaar=row_dict.get("aadhaar", ""),
            permanent_address=row_dict.get("permanent_address", ""),
            permanent_pincode=row_dict.get("permanent_pincode", ""),
            present_address=row_dict.get("present_address", ""),
            present_pincode=row_dict.get("present_pincode", ""),
            city=row_dict.get("city", ""),
            district=row_dict.get("district", ""),
            state=row_dict.get("state", ""),
            country=row_dict.get("country", ""),
        )

        education_info = StudentEducationInfo(
            last_institution=row_dict.get("last_institution", ""),
            last_institution_address=row_dict.get("last_institution_address", ""),
            hobby=row_dict.get("hobby", ""),
        )

        # Get exam marks
        exam_marks = self.get_student_marks(student_id)

        # Get photo
        photo = self.get_student_photo(student_id)

        return Student(
            student_id=student_id,
            basic_info=basic_info,
            academic_info=academic_info,
            contact_info=contact_info,
            address_info=address_info,
            education_info=education_info,
            exam_marks=exam_marks,
            photo=photo,
        )
