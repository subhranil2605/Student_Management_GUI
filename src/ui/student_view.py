"""Student details view window."""

import tkinter as tk
from tkinter import ttk

from src.config.ui_config import COLORS, FONTS, PADDING
from src.services.student_service import StudentService
from src.ui.base import BaseWindow
from src.ui.components import FormEntry


class StudentDetailsWindow(BaseWindow):
    """
    Student details view window.

    Displays all student information in a read-only or editable format.
    """

    def __init__(
        self,
        parent: tk.Tk,
        student_service: StudentService,
        student_id: str,
        editable: bool = False,
    ):
        """
        Initialize student details window.

        Args:
            parent: Parent window
            student_service: Student service instance
            student_id: ID of student to display
            editable: Whether student can edit fields
        """
        super().__init__(parent, "Student Details", 900, 700)
        self.student_service = student_service
        self.student_id = student_id
        self.editable = editable
        self.student = None

        self.setup_ui()
        self.load_student()

    def setup_ui(self) -> None:
        """Set up student details UI."""
        # Main frame with notebook
        main_frame = ttk.Frame(self, padding=PADDING["md"])
        main_frame.pack(fill="both", expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Student Information",
            font=FONTS["title"],
            foreground=COLORS["primary"],
        )
        title_label.pack(pady=PADDING["md"])

        # Notebook for organizing information
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=PADDING["md"])

        # Personal information tab
        self.personal_frame = ttk.Frame(self.notebook, padding=PADDING["lg"])
        self.notebook.add(self.personal_frame, text="Personal Info")

        # Contact information tab
        self.contact_frame = ttk.Frame(self.notebook, padding=PADDING["lg"])
        self.notebook.add(self.contact_frame, text="Contact Info")

        # Academic information tab
        self.academic_frame = ttk.Frame(self.notebook, padding=PADDING["lg"])
        self.notebook.add(self.academic_frame, text="Academic Info")

        # Create form fields
        self.create_personal_fields()
        self.create_contact_fields()
        self.create_academic_fields()

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=PADDING["md"])

        if self.editable:
            save_btn = ttk.Button(
                button_frame, text="Save", command=self.on_save
            )
            save_btn.pack(side="left", padx=PADDING["sm"])

        close_btn = ttk.Button(
            button_frame, text="Close", command=self.close_window
        )
        close_btn.pack(side="left", padx=PADDING["sm"])

    def create_personal_fields(self) -> None:
        """Create personal information fields."""
        # Student ID
        self.student_id_entry = FormEntry(
            self.personal_frame, "Student ID", required=True
        )
        self.student_id_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.student_id_entry.entry.configure(state="readonly")

        # Name
        self.name_entry = FormEntry(
            self.personal_frame, "Full Name", required=True
        )
        self.name_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.name_entry.entry.configure(state="readonly")

        # Sex
        self.sex_entry = FormEntry(self.personal_frame, "Sex")
        self.sex_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.sex_entry.entry.configure(state="readonly")

        # Category
        self.category_entry = FormEntry(self.personal_frame, "Category")
        self.category_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.category_entry.entry.configure(state="readonly")

        # Religion
        self.religion_entry = FormEntry(self.personal_frame, "Religion")
        self.religion_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.religion_entry.entry.configure(state="readonly")

        # Nationality
        self.nationality_entry = FormEntry(self.personal_frame, "Nationality")
        self.nationality_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.nationality_entry.entry.configure(state="readonly")

    def create_contact_fields(self) -> None:
        """Create contact information fields."""
        # Phone
        self.phone_entry = FormEntry(self.contact_frame, "Phone Number")
        self.phone_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.phone_entry.entry.configure(state="readonly")

        # Email
        self.email_entry = FormEntry(self.contact_frame, "Email Address")
        self.email_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.email_entry.entry.configure(state="readonly")

        # Guardian Name
        self.guardian_name_entry = FormEntry(
            self.contact_frame, "Guardian Name"
        )
        self.guardian_name_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.guardian_name_entry.entry.configure(state="readonly")

        # Guardian Phone
        self.guardian_phone_entry = FormEntry(
            self.contact_frame, "Guardian Phone"
        )
        self.guardian_phone_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.guardian_phone_entry.entry.configure(state="readonly")

        # Guardian Email
        self.guardian_email_entry = FormEntry(
            self.contact_frame, "Guardian Email"
        )
        self.guardian_email_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.guardian_email_entry.entry.configure(state="readonly")

        # Address
        self.address_entry = FormEntry(self.contact_frame, "Address", width=50)
        self.address_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.address_entry.entry.configure(state="readonly")

        # City
        self.city_entry = FormEntry(self.contact_frame, "City")
        self.city_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.city_entry.entry.configure(state="readonly")

    def create_academic_fields(self) -> None:
        """Create academic information fields."""
        # Registration Number
        self.reg_no_entry = FormEntry(
            self.academic_frame, "Registration Number"
        )
        self.reg_no_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.reg_no_entry.entry.configure(state="readonly")

        # Session
        self.session_entry = FormEntry(self.academic_frame, "Session")
        self.session_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.session_entry.entry.configure(state="readonly")

        # Course
        self.course_entry = FormEntry(self.academic_frame, "Course")
        self.course_entry.pack(fill="x", pady=PADDING["sm"])
        if not self.editable:
            self.course_entry.entry.configure(state="readonly")

    def load_student(self) -> None:
        """Load student data from service."""
        try:
            self.student = self.student_service.get_student(self.student_id)

            # Populate fields
            self.student_id_entry.set(self.student.student_id)
            self.name_entry.set(self.student.name)
            self.sex_entry.set(self.student.sex)
            self.category_entry.set(self.student.category)
            self.religion_entry.set(self.student.religion)
            self.nationality_entry.set(self.student.nationality)

            self.phone_entry.set(self.student.phone)
            self.email_entry.set(self.student.email)
            self.guardian_name_entry.set(self.student.guardian_name)
            self.guardian_phone_entry.set(self.student.guardian_phone)
            self.guardian_email_entry.set(self.student.guardian_email)
            self.address_entry.set(self.student.address)
            self.city_entry.set(self.student.city)

            self.reg_no_entry.set(self.student.registration_number)
            self.session_entry.set(self.student.session)
            self.course_entry.set(self.student.course)
        except Exception as e:
            self.show_error("Error", f"Failed to load student: {str(e)}")

    def on_save(self) -> None:
        """Save changes to student."""
        try:
            # Collect updated data
            data = {
                "student_id": self.student_id_entry.get(),
                "name": self.name_entry.get(),
                "sex": self.sex_entry.get(),
                "category": self.category_entry.get(),
                "religion": self.religion_entry.get(),
                "nationality": self.nationality_entry.get(),
                "phone": self.phone_entry.get(),
                "email": self.email_entry.get(),
                "guardian_name": self.guardian_name_entry.get(),
                "guardian_phone": self.guardian_phone_entry.get(),
                "guardian_email": self.guardian_email_entry.get(),
                "address": self.address_entry.get(),
                "city": self.city_entry.get(),
                "registration_number": self.reg_no_entry.get(),
                "session": self.session_entry.get(),
                "course": self.course_entry.get(),
            }

            # Update through service
            self.student_service.update_student(self.student_id, data)
            self.show_success("Success", "Student information updated")
            self.close_window()
        except Exception as e:
            self.show_error("Error", f"Failed to save: {str(e)}")
