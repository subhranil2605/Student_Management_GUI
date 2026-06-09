"""Admin panel for student management."""

import tkinter as tk
from tkinter import messagebox, ttk

from src.config.ui_config import COLORS, FONTS, PADDING
from src.services.student_service import StudentService
from src.ui.base import BaseWindow
from src.ui.components import FormEntry, TableFrame


class AdminPanel(BaseWindow):
    """
    Admin panel for managing students.

    Displays student list with search, filter, and CRUD operations.
    """

    def __init__(self, parent: tk.Tk, student_service: StudentService):
        """
        Initialize admin panel.

        Args:
            parent: Parent window
            student_service: Student service instance
        """
        super().__init__(parent, "Student Management - Admin Panel", 1000, 700)
        self.student_service = student_service

        self.setup_ui()
        self.load_students()

    def setup_ui(self) -> None:
        """Set up admin panel UI."""
        # Main frame
        main_frame = ttk.Frame(self, padding=PADDING["md"])
        main_frame.pack(fill="both", expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Student Management",
            font=FONTS["title"],
            foreground=COLORS["primary"],
        )
        title_label.pack(pady=PADDING["md"])

        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill="x", pady=PADDING["md"])

        # Search field
        self.search_entry = FormEntry(control_frame, "Search by Name/ID", width=30)
        self.search_entry.pack(side="left", padx=PADDING["sm"])

        # Search button
        search_btn = ttk.Button(
            control_frame, text="Search", command=self.on_search
        )
        search_btn.pack(side="left", padx=PADDING["sm"])

        # Refresh button
        refresh_btn = ttk.Button(
            control_frame, text="Refresh", command=self.load_students
        )
        refresh_btn.pack(side="left", padx=PADDING["sm"])

        # Table frame
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=PADDING["md"])

        columns = ["ID", "Name", "Email", "Phone", "Session", "Course"]
        self.table = TableFrame(table_frame, columns, [50, 150, 200, 120, 100, 100])
        self.table.pack(fill="both", expand=True)

        # Action frame
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x", pady=PADDING["md"])

        # View button
        view_btn = ttk.Button(
            action_frame, text="View Details", command=self.on_view
        )
        view_btn.pack(side="left", padx=PADDING["sm"])

        # Edit button
        edit_btn = ttk.Button(
            action_frame, text="Edit", command=self.on_edit
        )
        edit_btn.pack(side="left", padx=PADDING["sm"])

        # Delete button
        delete_btn = ttk.Button(
            action_frame, text="Delete", command=self.on_delete
        )
        delete_btn.pack(side="left", padx=PADDING["sm"])

        # Add button
        add_btn = ttk.Button(
            action_frame, text="Add New Student", command=self.on_add
        )
        add_btn.pack(side="left", padx=PADDING["sm"])

    def load_students(self) -> None:
        """Load and display all students."""
        try:
            self.table.clear()
            students = self.student_service.get_all_students()

            for student in students:
                values = [
                    student.student_id,
                    student.name,
                    student.email,
                    student.phone,
                    student.session,
                    student.course,
                ]
                self.table.insert_row(values)
        except Exception as e:
            self.show_error("Error", f"Failed to load students: {str(e)}")

    def on_search(self) -> None:
        """Handle search button click."""
        search_term = self.search_entry.get()

        if not search_term:
            self.load_students()
            return

        try:
            self.table.clear()
            students = self.student_service.search_students(search_term)

            for student in students:
                values = [
                    student.student_id,
                    student.name,
                    student.email,
                    student.phone,
                    student.session,
                    student.course,
                ]
                self.table.insert_row(values)
        except Exception as e:
            self.show_error("Search Error", f"Search failed: {str(e)}")

    def on_view(self) -> None:
        """View selected student details."""
        item_id = self.table.get_selected()

        if not item_id:
            self.show_error("Error", "Please select a student")
            return

        values = self.table.get_row_values(item_id)
        student_id = values[0]

        try:
            student = self.student_service.get_student(student_id)
            self.show_student_details(student)
        except Exception as e:
            self.show_error("Error", f"Failed to load student: {str(e)}")

    def show_student_details(self, student) -> None:
        """
        Show student details in a dialog.

        Args:
            student: Student object
        """
        details = f"""
Student ID: {student.student_id}
Name: {student.name}
Email: {student.email}
Phone: {student.phone}
Session: {student.session}
Course: {student.course}
Category: {student.category}
Nationality: {student.nationality}
Address: {student.address}
City: {student.city}
"""
        messagebox.showinfo("Student Details", details, parent=self)

    def on_edit(self) -> None:
        """Edit selected student."""
        item_id = self.table.get_selected()

        if not item_id:
            self.show_error("Error", "Please select a student")
            return

        self.show_error("Info", "Edit functionality coming soon")

    def on_delete(self) -> None:
        """Delete selected student."""
        item_id = self.table.get_selected()

        if not item_id:
            self.show_error("Error", "Please select a student")
            return

        values = self.table.get_row_values(item_id)
        student_id = values[0]
        student_name = values[1]

        if self.ask_confirmation(
            "Delete Student", f"Delete student {student_name}? This cannot be undone."
        ):
            try:
                self.student_service.delete_student(student_id)
                self.show_success("Success", f"Student {student_name} deleted")
                self.load_students()
            except Exception as e:
                self.show_error("Delete Error", f"Failed to delete: {str(e)}")

    def on_add(self) -> None:
        """Add new student."""
        self.show_error("Info", "Add new student functionality coming soon")
