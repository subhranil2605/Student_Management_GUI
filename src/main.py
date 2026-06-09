"""Main application entry point."""

import tkinter as tk
from tkinter import messagebox

from src.config.ui_config import WINDOW_DIMENSIONS
from src.database.db_manager import DatabaseManager
from src.database.queries import DatabaseQueries
from src.services.auth_service import AuthService
from src.services.marks_service import MarksService
from src.services.student_service import StudentService
from src.validators.business_rules import BusinessRuleValidator
from src.ui.admin_panel import AdminPanel
from src.ui.login_window import LoginWindow
from src.ui.marks_view import MarksWindow
from src.ui.registration_window import RegistrationWindow
from src.ui.themes import setup_ttk_theme


class Application:
    """
    Main application class.

    Orchestrates application lifecycle, window management, and services.
    """

    def __init__(self):
        """Initialize application."""
        self.root = tk.Tk()
        self.root.title("Student Management System")

        # Get window dimensions
        dims = WINDOW_DIMENSIONS.get("root", {"width": 800, "height": 600})
        self.root.geometry(f"{dims['width']}x{dims['height']}")

        # Set up theme
        setup_ttk_theme()

        # Initialize database (DatabaseManager initializes on construction)
        self.db_manager = DatabaseManager()

        # Initialize queries
        self.queries = DatabaseQueries(self.db_manager)

        # Initialize validators
        self.business_validator = BusinessRuleValidator(self.queries)

        # Initialize services
        self.auth_service = AuthService(self.queries)
        self.student_service = StudentService(
            self.queries, self.auth_service
        )
        self.marks_service = MarksService(self.queries, self.business_validator)

        # Bind events
        self.setup_event_bindings()

        # Show login window initially
        self.show_login()

    def setup_event_bindings(self) -> None:
        """Set up event bindings."""
        self.root.bind("<<LoginSuccess>>", self.on_login_success)

    def on_login_success(self, event=None) -> None:
        """
        Handle successful login.

        Shows main admin panel after login.
        """
        self.show_admin_panel()

    def show_login(self) -> None:
        """Show login window."""
        LoginWindow(self.root, self.auth_service)

    def show_admin_panel(self) -> None:
        """Show admin panel."""
        AdminPanel(self.root, self.student_service)

    def show_registration(self) -> None:
        """Show registration window."""
        RegistrationWindow(self.root, self.student_service, self.auth_service)

    def show_marks(self) -> None:
        """Show marks window."""
        MarksWindow(self.root, self.marks_service, self.student_service)

    def run(self) -> None:
        """Run the application."""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror(
                "Application Error",
                f"An error occurred: {str(e)}",
            )
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Clean up resources before exit."""
        try:
            if self.db_manager:
                self.db_manager.close()
        except Exception as e:
            print(f"Error during cleanup: {e}")


def main():
    """Entry point for the application."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
