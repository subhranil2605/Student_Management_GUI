"""Data models for the application."""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class User:
    """User model representing an authenticated user."""

    user_id: int
    username: str
    password_hash: str
    role: str
    created_at: str
    session: str = ""

    def is_admin(self) -> bool:
        """Check if user is an admin."""
        return self.role == "admin"

    def is_teacher(self) -> bool:
        """Check if user is a teacher."""
        return self.role == "teacher"

    def is_staff(self) -> bool:
        """Check if user is staff."""
        return self.role == "staff"


@dataclass
class StudentBasicInfo:
    """Student basic information."""

    fullname: str
    sex: str
    category: str
    religion: str
    nationality: str
    handicapped: str
    percentage_handicap: str
    dob: str
    father_name: str
    father_occupation: str
    mother_name: str
    mother_occupation: str
    guardian_name: str
    guardian_relation: str


@dataclass
class StudentAcademicInfo:
    """Student academic information."""

    session: str
    reg_no: str
    student_id: str
    course: str


@dataclass
class StudentContactInfo:
    """Student contact information."""

    contact: str
    email: str
    guardian_contact: str
    guardian_email: str


@dataclass
class StudentAddressInfo:
    """Student address information."""

    aadhaar: str
    permanent_address: str
    permanent_pincode: str
    present_address: str
    present_pincode: str
    city: str
    district: str
    state: str
    country: str


@dataclass
class StudentEducationInfo:
    """Student education history."""

    last_institution: str
    last_institution_address: str
    hobby: str


@dataclass
class ExamMarks:
    """Marks for a single exam."""

    exam_number: int
    exam_name: str
    board: str
    total_marks: str
    cgpa: str
    percentage: str
    pass_year: str


@dataclass
class Student:
    """Complete student model."""

    student_id: int
    basic_info: StudentBasicInfo
    academic_info: StudentAcademicInfo
    contact_info: StudentContactInfo
    address_info: StudentAddressInfo
    education_info: StudentEducationInfo
    exam_marks: list[ExamMarks] = field(default_factory=list)
    photo: Optional[bytes] = None

    def get_email(self) -> str:
        """Get student email."""
        return self.contact_info.email

    def get_full_name(self) -> str:
        """Get student full name."""
        return self.basic_info.fullname

    def get_student_id(self) -> str:
        """Get student ID."""
        return self.academic_info.student_id

    def to_dict(self) -> dict:
        """Convert student to dictionary."""
        return {
            "id": self.student_id,
            "fullname": self.basic_info.fullname,
            "sex": self.basic_info.sex,
            "category": self.basic_info.category,
            "religion": self.basic_info.religion,
            "nationality": self.basic_info.nationality,
            "handicapped": self.basic_info.handicapped,
            "percentage_handicap": self.basic_info.percentage_handicap,
            "dob": self.basic_info.dob,
            "father_name": self.basic_info.father_name,
            "father_occupation": self.basic_info.father_occupation,
            "mother_name": self.basic_info.mother_name,
            "mother_occupation": self.basic_info.mother_occupation,
            "guardian_name": self.basic_info.guardian_name,
            "guardian_relation": self.basic_info.guardian_relation,
            "session": self.academic_info.session,
            "reg_no": self.academic_info.reg_no,
            "student_id": self.academic_info.student_id,
            "course": self.academic_info.course,
            "contact": self.contact_info.contact,
            "email": self.contact_info.email,
            "guardian_contact": self.contact_info.guardian_contact,
            "guardian_email": self.contact_info.guardian_email,
            "aadhaar": self.address_info.aadhaar,
            "permanent_address": self.address_info.permanent_address,
            "permanent_pincode": self.address_info.permanent_pincode,
            "present_address": self.address_info.present_address,
            "present_pincode": self.address_info.present_pincode,
            "city": self.address_info.city,
            "district": self.address_info.district,
            "state": self.address_info.state,
            "country": self.address_info.country,
            "last_institution": self.education_info.last_institution,
            "last_institution_address": self.education_info.last_institution_address,
            "hobby": self.education_info.hobby,
        }
