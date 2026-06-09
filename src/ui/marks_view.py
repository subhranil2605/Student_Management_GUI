"""Marks management window."""

import tkinter as tk
from tkinter import messagebox, ttk

from src.config.ui_config import COLORS, FONTS, PADDING
from src.services.marks_service import MarksService
from src.services.student_service import StudentService
from src.ui.base import BaseWindow
from src.ui.components import FormCombobox, FormEntry, TableFrame


class MarksWindow(BaseWindow):
    """
    Marks management window.

    Interface for entering, viewing, and managing student marks and CGPA.
    """

    def __init__(
        self,
        parent: tk.Tk,
        marks_service: MarksService,
        student_service: StudentService,
    ):
        """
        Initialize marks window.

        Args:
            parent: Parent window
            marks_service: Marks service instance
            student_service: Student service instance
        """
        super().__init__(parent, "Marks Management", 900, 650)
        self.marks_service = marks_service
        self.student_service = student_service

        self.setup_ui()
        self.load_students()

    def setup_ui(self) -> None:
        """Set up marks window UI."""
        # Main frame
        main_frame = ttk.Frame(self, padding=PADDING["md"])
        main_frame.pack(fill="both", expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Marks Management",
            font=FONTS["title"],
            foreground=COLORS["primary"],
        )
        title_label.pack(pady=PADDING["md"])

        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill="x", pady=PADDING["md"])

        # Student selection
        students = self.student_service.get_all_students()
        student_names = ["Select Student"] + [s.name for s in students]

        self.student_combo = FormCombobox(
            control_frame, "Select Student", student_names, required=True
        )
        self.student_combo.pack(side="left", padx=PADDING["sm"])
        self.student_combo.combobox.bind(
            "<<ComboboxSelected>>", lambda e: self.on_student_selected()
        )

        # Load marks button
        load_btn = ttk.Button(
            control_frame, text="Load Marks", command=self.on_load_marks
        )
        load_btn.pack(side="left", padx=PADDING["sm"])

        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=PADDING["md"], pady=PADDING["md"])

        # Marks entry tab
        self.entry_frame = self.create_entry_tab()
        self.notebook.add(self.entry_frame, text="Enter Marks")

        # Marks view tab
        self.view_frame = self.create_view_tab()
        self.notebook.add(self.view_frame, text="View Marks")

    def create_entry_tab(self) -> ttk.Frame:
        """Create marks entry tab."""
        frame = ttk.Frame(self.notebook, padding=PADDING["lg"])

        # Subject
        self.subject_entry = FormEntry(frame, "Subject Name", required=True)
        self.subject_entry.pack(fill="x", pady=PADDING["sm"])

        # Marks
        self.marks_entry = FormEntry(frame, "Marks (0-100)", required=True)
        self.marks_entry.pack(fill="x", pady=PADDING["sm"])

        # Grade
        self.grade_entry = FormEntry(frame, "Grade", required=False)
        self.grade_entry.pack(fill="x", pady=PADDING["sm"])
        self.grade_entry.entry.configure(state="readonly")

        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=PADDING["lg"])

        save_btn = ttk.Button(
            button_frame, text="Save Marks", command=self.on_save_marks
        )
        save_btn.pack(side="left", padx=PADDING["sm"])

        clear_btn = ttk.Button(
            button_frame, text="Clear", command=self.on_clear_form
        )
        clear_btn.pack(side="left", padx=PADDING["sm"])

        return frame

    def create_view_tab(self) -> ttk.Frame:
        """Create marks view tab."""
        frame = ttk.Frame(self.notebook, padding=PADDING["lg"])

        # Marks table
        columns = ["Subject", "Marks", "Grade", "Date"]
        self.marks_table = TableFrame(
            frame, columns, [200, 100, 100, 150]
        )
        self.marks_table.pack(fill="both", expand=True, pady=PADDING["md"])

        # CGPA frame
        cgpa_frame = ttk.LabelFrame(frame, text="Academic Summary", padding=PADDING["md"])
        cgpa_frame.pack(fill="x", pady=PADDING["md"])

        # Average marks
        avg_frame = ttk.Frame(cgpa_frame)
        avg_frame.pack(fill="x", pady=PADDING["sm"])

        avg_label = ttk.Label(
            avg_frame, text="Average Marks:", font=FONTS["subheading"]
        )
        avg_label.pack(side="left", padx=PADDING["sm"])

        self.avg_value = ttk.Label(
            avg_frame, text="0.0", font=FONTS["heading"], foreground=COLORS["success"]
        )
        self.avg_value.pack(side="left", padx=PADDING["sm"])

        # CGPA
        cgpa_frame_inner = ttk.Frame(cgpa_frame)
        cgpa_frame_inner.pack(fill="x", pady=PADDING["sm"])

        cgpa_label = ttk.Label(
            cgpa_frame_inner, text="CGPA:", font=FONTS["subheading"]
        )
        cgpa_label.pack(side="left", padx=PADDING["sm"])

        self.cgpa_value = ttk.Label(
            cgpa_frame_inner, text="0.0", font=FONTS["heading"], foreground=COLORS["success"]
        )
        self.cgpa_value.pack(side="left", padx=PADDING["sm"])

        # Delete button
        delete_btn = ttk.Button(
            cgpa_frame, text="Delete Selected", command=self.on_delete_mark
        )
        delete_btn.pack(pady=PADDING["sm"])

        return frame

    def load_students(self) -> None:
        """Load student list."""
        try:
            students = self.student_service.get_all_students()
            student_names = ["Select Student"] + [s.name for s in students]
            self.student_combo.combobox.configure(values=student_names)
        except Exception as e:
            self.show_error("Error", f"Failed to load students: {str(e)}")

    def on_student_selected(self) -> None:
        """Handle student selection."""
        self.on_load_marks()

    def on_load_marks(self) -> None:
        """Load marks for selected student."""
        student_name = self.student_combo.get()

        if student_name == "Select Student" or not student_name:
            self.show_error("Error", "Please select a student")
            return

        try:
            # Find student by name
            students = self.student_service.get_all_students()
            student = next((s for s in students if s.name == student_name), None)

            if not student:
                self.show_error("Error", "Student not found")
                return

            # Load marks
            self.marks_table.clear()
            marks_list = self.marks_service.get_marks(student.student_id)

            for mark in marks_list:
                values = [
                    mark.subject,
                    str(mark.marks),
                    mark.grade or "",
                    mark.date_added or "",
                ]
                self.marks_table.insert_row(values)

            # Calculate and display CGPA
            cgpa = self.marks_service.calculate_cgpa(student.student_id)
            avg = sum(m.marks for m in marks_list) / len(marks_list) if marks_list else 0

            self.cgpa_value.configure(text=f"{cgpa:.2f}")
            self.avg_value.configure(text=f"{avg:.2f}")
        except Exception as e:
            self.show_error("Error", f"Failed to load marks: {str(e)}")

    def on_save_marks(self) -> None:
        """Save marks for selected student."""
        student_name = self.student_combo.get()

        if student_name == "Select Student" or not student_name:
            self.show_error("Error", "Please select a student")
            return

        subject = self.subject_entry.get()
        marks_str = self.marks_entry.get()

        if not subject or not marks_str:
            self.show_error("Error", "Subject and Marks are required")
            return

        try:
            marks = float(marks_str)

            # Find student by name
            students = self.student_service.get_all_students()
            student = next((s for s in students if s.name == student_name), None)

            if not student:
                self.show_error("Error", "Student not found")
                return

            # Save marks
            self.marks_service.add_marks(student.student_id, subject, marks)
            self.show_success("Success", "Marks saved successfully")

            # Reload marks
            self.on_load_marks()
            self.on_clear_form()
        except ValueError:
            self.show_error("Error", "Marks must be a number between 0-100")
        except Exception as e:
            self.show_error("Error", f"Failed to save marks: {str(e)}")

    def on_delete_mark(self) -> None:
        """Delete selected mark."""
        item_id = self.marks_table.get_selected()

        if not item_id:
            self.show_error("Error", "Please select a mark to delete")
            return

        if self.ask_confirmation("Delete", "Delete this mark entry?"):
            try:
                # For now, show info message
                self.show_error("Info", "Delete functionality coming soon")
                # values = self.marks_table.get_row_values(item_id)
                # self.marks_service.delete_marks(...)
            except Exception as e:
                self.show_error("Error", f"Failed to delete: {str(e)}")

    def on_clear_form(self) -> None:
        """Clear form fields."""
        self.subject_entry.clear()
        self.marks_entry.clear()
        self.grade_entry.clear()
