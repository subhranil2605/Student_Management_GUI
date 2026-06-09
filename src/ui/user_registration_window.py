"""User registration window for creating new user accounts."""

import tkinter as tk
from tkinter import ttk

from src.config.settings import USER_ROLES
from src.config.ui_config import COLORS, FONTS, PADDING
from src.services.auth_service import AuthService, AuthenticationError
from src.ui.base import BaseWindow
from src.ui.components import FormEntry, FormCombobox
from src.validators.form_validator import ValidationError


class UserRegistrationWindow(BaseWindow):
    """
    User registration window for creating new user accounts.

    Provides interface for users to register with username, password, and role.
    """

    def __init__(self, parent: tk.Tk, auth_service: AuthService):
        """
        Initialize user registration window.

        Args:
            parent: Parent window (root Tk instance)
            auth_service: Authentication service instance
        """
        super().__init__(parent, "User Registration", 450, 550)
        self.auth_service = auth_service
        self.registration_successful = False

        self.setup_ui()
        self.center_window()

    def setup_ui(self) -> None:
        """Set up user registration window UI."""
        # Main frame
        main_frame = ttk.Frame(self, padding=PADDING["lg"])
        main_frame.pack(fill="both", expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Create New User Account",
            font=FONTS["title"],
            foreground=COLORS["primary"],
        )
        title_label.pack(pady=PADDING["lg"])

        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Register a new user account",
            font=FONTS["subheading"],
            foreground=COLORS["gray"],
        )
        subtitle_label.pack(pady=PADDING["sm"])

        # Form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill="x", padx=PADDING["lg"], pady=PADDING["lg"])

        # Username field
        self.username_entry = FormEntry(
            form_frame, "Username", width=30, required=True
        )
        self.username_entry.pack(fill="x", pady=PADDING["md"])

        # Password field
        self.password_entry = FormEntry(
            form_frame, "Password", width=30, show="*", required=True
        )
        self.password_entry.pack(fill="x", pady=PADDING["md"])

        # Confirm Password field
        self.confirm_password_entry = FormEntry(
            form_frame, "Confirm Password", width=30, show="*", required=True
        )
        self.confirm_password_entry.pack(fill="x", pady=PADDING["md"])

        # Role selection
        role_values = list(USER_ROLES.values())
        self.role_combobox = FormCombobox(
            form_frame, "Role", values=role_values, required=True
        )
        self.role_combobox.pack(fill="x", pady=PADDING["md"])

        # Button frame
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x", pady=PADDING["lg"])

        # Register button
        self.register_btn = ttk.Button(
            button_frame, text="Register", command=self.on_register, width=20
        )
        self.register_btn.pack(side="left", padx=PADDING["sm"])

        # Cancel button
        self.cancel_btn = ttk.Button(
            button_frame, text="Cancel", command=self.on_cancel, width=20
        )
        self.cancel_btn.pack(side="left", padx=PADDING["sm"])

    def on_register(self) -> None:
        """Handle register button click."""
        # Get input values
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        role = self.role_combobox.get()

        # Clear previous errors
        self.username_entry.clear_error()
        self.password_entry.clear_error()
        self.confirm_password_entry.clear_error()
        self.role_combobox.clear_error()

        # Validate username
        if not username:
            self.username_entry.set_error("Username is required")
            self.username_entry.entry.focus()
            return

        # Validate password
        if not password:
            self.password_entry.set_error("Password is required")
            self.password_entry.entry.focus()
            return

        # Validate confirm password
        if not confirm_password:
            self.confirm_password_entry.set_error("Please confirm your password")
            self.confirm_password_entry.entry.focus()
            return

        # Check password strength (minimum 6 characters)
        if len(password) < 6:
            self.password_entry.set_error("Password must be at least 6 characters")
            self.password_entry.entry.focus()
            return

        # Check passwords match
        if password != confirm_password:
            self.confirm_password_entry.set_error("Passwords do not match")
            self.confirm_password_entry.entry.focus()
            return

        # Validate role selection
        if not role or role == "Select":
            self.role_combobox.set_error("Please select a role")
            return

        # Attempt registration
        try:
            user = self.auth_service.register_user(username, password, role)
            self.registration_successful = True
            self.show_success(
                "Registration Successful", f"User '{user.username}' created successfully!"
            )
            self.parent.event_generate("<<RegistrationSuccess>>")
            self.close_window()
        except AuthenticationError as e:
            self.show_error("Registration Failed", str(e))
            self.username_entry.clear()
            self.username_entry.entry.focus()
        except ValidationError as e:
            self.show_error("Validation Error", str(e))
        except Exception as e:
            self.show_error("Error", f"Registration failed: {str(e)}")

    def on_cancel(self) -> None:
        """Handle cancel button click."""
        self.close_window()
