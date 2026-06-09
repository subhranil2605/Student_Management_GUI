"""Student registration window."""

import tkinter as tk
from tkinter import messagebox, ttk

from src.config.settings import (
    COURSES,
    GENDERS,
    HANDICAP_OPTIONS,
    NATIONALITIES,
    RELIGIONS,
    SESSIONS,
    STUDENT_CATEGORIES,
)
from src.config.ui_config import COLORS, FONTS, PADDING
from src.services.auth_service import AuthService
from src.services.student_service import StudentService
from src.ui.base import BaseWindow
from src.ui.components import FormCombobox, FormEntry, FormTextArea
from src.validators.form_validator import ValidationError


class RegistrationWindow(BaseWindow):
    """
    Student registration window.

    Multi-step form for registering new students with validation.
    """

    def __init__(
        self,
        parent: tk.Tk,
        student_service: StudentService,
        auth_service: AuthService,
    ):
        """
        Initialize registration window.

        Args:
            parent: Parent window
            student_service: Student service instance
            auth_service: Auth service instance
        """
        super().__init__(parent, "Student Registration", 900, 700)
        self.student_service = student_service
        self.auth_service = auth_service

        # Form data
        self.form_data = {}

        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up registration window UI."""
        # Main frame with notebook for tabs
        main_frame = ttk.Frame(self, padding=PADDING["md"])
        main_frame.pack(fill="both", expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Student Registration Form",
            font=FONTS["title"],
            foreground=COLORS["primary"],
        )
        title_label.pack(pady=PADDING["md"])

        # Notebook for multi-page form
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=PADDING["md"], pady=PADDING["md"])

        # Page 1: Personal Information
        self.page1_frame = self.create_page1()
        self.notebook.add(self.page1_frame, text="Personal Info")

        # Page 2: Contact Information
        self.page2_frame = self.create_page2()
        self.notebook.add(self.page2_frame, text="Contact Info")

        # Page 3: Academic Information
        self.page3_frame = self.create_page3()
        self.notebook.add(self.page3_frame, text="Academic Info")

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=PADDING["md"])

        submit_btn = ttk.Button(button_frame, text="Submit", command=self.on_submit)
        submit_btn.pack(side="left", padx=PADDING["sm"])

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.close_window)
        cancel_btn.pack(side="left", padx=PADDING["sm"])

    def create_page1(self) -> ttk.Frame:
        """Create page 1 (personal information)."""
        frame = ttk.Frame(self.notebook, padding=PADDING["lg"])

        # Name
        self.name_entry = FormEntry(frame, "Full Name", required=True)
        self.name_entry.pack(fill="x", pady=PADDING["sm"])

        # Sex
        self.sex_combo = FormCombobox(
            frame, "Sex", GENDERS, required=True
        )
        self.sex_combo.pack(fill="x", pady=PADDING["sm"])

        # Category
        self.category_combo = FormCombobox(
            frame, "Category", STUDENT_CATEGORIES, required=True
        )
        self.category_combo.pack(fill="x", pady=PADDING["sm"])

        # Religion
        self.religion_combo = FormCombobox(
            frame, "Religion", ["Select"] + RELIGIONS, required=True
        )
        self.religion_combo.pack(fill="x", pady=PADDING["sm"])

        # Nationality
        self.nationality_combo = FormCombobox(
            frame, "Nationality", ["Select"] + NATIONALITIES, required=True
        )
        self.nationality_combo.pack(fill="x", pady=PADDING["sm"])

        # Disability
        self.disability_combo = FormCombobox(
            frame, "Disability", ["Select"] + HANDICAP_OPTIONS, required=False
        )
        self.disability_combo.pack(fill="x", pady=PADDING["sm"])

        # Disability percentage
        self.disability_pct_entry = FormEntry(
            frame, "Disability %", width=30, required=False
        )
        self.disability_pct_entry.pack(fill="x", pady=PADDING["sm"])

        return frame

    def create_page2(self) -> ttk.Frame:
        """Create page 2 (contact information)."""
        frame = ttk.Frame(self.notebook, padding=PADDING["lg"])

        # Phone
        self.phone_entry = FormEntry(frame, "Phone Number", required=True)
        self.phone_entry.pack(fill="x", pady=PADDING["sm"])

        # Email
        self.email_entry = FormEntry(frame, "Email Address", required=True)
        self.email_entry.pack(fill="x", pady=PADDING["sm"])

        # Guardian name
        self.guardian_name_entry = FormEntry(
            frame, "Guardian Name", required=True
        )
        self.guardian_name_entry.pack(fill="x", pady=PADDING["sm"])

        # Guardian contact
        self.guardian_phone_entry = FormEntry(
            frame, "Guardian Phone", required=True
        )
        self.guardian_phone_entry.pack(fill="x", pady=PADDING["sm"])

        # Guardian email
        self.guardian_email_entry = FormEntry(
            frame, "Guardian Email", required=True
        )
        self.guardian_email_entry.pack(fill="x", pady=PADDING["sm"])

        # Address
        self.address_area = FormTextArea(
            frame, "Address", width=40, height=4, required=True
        )
        self.address_area.pack(fill="x", pady=PADDING["sm"])

        # City
        self.city_entry = FormEntry(frame, "City", required=True)
        self.city_entry.pack(fill="x", pady=PADDING["sm"])

        # Pincode
        self.pincode_entry = FormEntry(frame, "Pincode", required=True)
        self.pincode_entry.pack(fill="x", pady=PADDING["sm"])

        return frame

    def create_page3(self) -> ttk.Frame:
        """Create page 3 (academic information)."""
        frame = ttk.Frame(self.notebook, padding=PADDING["lg"])

        # Student ID
        self.student_id_entry = FormEntry(frame, "Student ID", required=True)
        self.student_id_entry.pack(fill="x", pady=PADDING["sm"])

        # Registration Number
        self.reg_no_entry = FormEntry(
            frame, "Registration Number", required=True
        )
        self.reg_no_entry.pack(fill="x", pady=PADDING["sm"])

        # Session
        self.session_combo = FormCombobox(
            frame, "Session", ["Select"] + SESSIONS, required=True
        )
        self.session_combo.pack(fill="x", pady=PADDING["sm"])

        # Course
        self.course_combo = FormCombobox(
            frame, "Course", ["Select"] + COURSES, required=True
        )
        self.course_combo.pack(fill="x", pady=PADDING["sm"])

        return frame

    def get_form_data(self) -> dict:
        """
        Collect all form data.

        Returns:
            Dictionary of form data

        Raises:
            ValidationError: If validation fails
        """
        data = {
            # Page 1
            "name": self.name_entry.get(),
            "sex": self.sex_combo.get(),
            "category": self.category_combo.get(),
            "religion": self.religion_combo.get(),
            "nationality": self.nationality_combo.get(),
            "disability": self.disability_combo.get(),
            "disability_percentage": self.disability_pct_entry.get(),
            # Page 2
            "phone": self.phone_entry.get(),
            "email": self.email_entry.get(),
            "guardian_name": self.guardian_name_entry.get(),
            "guardian_phone": self.guardian_phone_entry.get(),
            "guardian_email": self.guardian_email_entry.get(),
            "address": self.address_area.get(),
            "city": self.city_entry.get(),
            "pincode": self.pincode_entry.get(),
            # Page 3
            "student_id": self.student_id_entry.get(),
            "registration_number": self.reg_no_entry.get(),
            "session": self.session_combo.get(),
            "course": self.course_combo.get(),
        }
        return data

    def on_submit(self) -> None:
        """Handle form submission."""
        try:
            # Get and validate form data
            data = self.get_form_data()

            # Register student through service
            student = self.student_service.register_student(data)

            self.show_success(
                "Success", f"Student {student.name} registered successfully!"
            )
            self.close_window()
        except ValidationError as e:
            self.show_error("Validation Error", str(e))
        except Exception as e:
            self.show_error("Registration Error", f"An error occurred: {str(e)}")
