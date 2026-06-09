"""Login window for user authentication."""

import tkinter as tk
from tkinter import messagebox, ttk

from src.config.ui_config import COLORS, FONTS, PADDING
from src.services.auth_service import AuthService, AuthenticationError
from src.ui.base import BaseWindow
from src.ui.components import FormEntry


class LoginWindow(BaseWindow):
    """
    Login window for user authentication.

    Provides interface for users to log in with username and password.
    """

    def __init__(self, parent: tk.Tk, auth_service: AuthService):
        """
        Initialize login window.

        Args:
            parent: Parent window (root Tk instance)
            auth_service: Authentication service instance
        """
        super().__init__(parent, "Student Management - Login", 400, 500)
        self.auth_service = auth_service
        self.login_successful = False

        self.setup_ui()
        self.center_window()

    def setup_ui(self) -> None:
        """Set up login window UI."""
        # Main frame
        main_frame = ttk.Frame(self, padding=PADDING["lg"])
        main_frame.pack(fill="both", expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Student Management System",
            font=FONTS["title"],
            foreground=COLORS["primary"],
        )
        title_label.pack(pady=PADDING["lg"])

        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Login to your account",
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

        # Button frame
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x", pady=PADDING["lg"])

        # Login button
        login_btn = ttk.Button(
            button_frame, text="Login", command=self.on_login, width=15
        )
        login_btn.pack(side="left", padx=PADDING["sm"])

        # Register button
        register_btn = ttk.Button(
            button_frame, text="Register", command=self.on_register, width=15
        )
        register_btn.pack(side="left", padx=PADDING["sm"])

        # Exit button
        exit_btn = ttk.Button(
            button_frame, text="Exit", command=self.on_exit, width=15
        )
        exit_btn.pack(side="left", padx=PADDING["sm"])

        # Bind Enter key to login
        self.bind("<Return>", lambda e: self.on_login())

    def on_login(self) -> None:
        """Handle login button click."""
        # Get input values
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Clear previous errors
        self.username_entry.clear_error()
        self.password_entry.clear_error()

        # Validate inputs
        if not username:
            self.username_entry.set_error("Username is required")
            self.username_entry.entry.focus()
            return

        if not password:
            self.password_entry.set_error("Password is required")
            self.password_entry.entry.focus()
            return

        # Attempt login
        try:
            user = self.auth_service.login(username, password)
            self.login_successful = True
            self.show_success("Success", f"Welcome, {user.username}!")
            self.parent.event_generate("<<LoginSuccess>>")
            self.close_window()
        except AuthenticationError as e:
            self.show_error("Login Failed", str(e))
            self.password_entry.clear()
            self.password_entry.entry.focus()

    def on_register(self) -> None:
        """Handle register button click."""
        from src.ui.user_registration_window import UserRegistrationWindow

        # Open registration window
        UserRegistrationWindow(self.parent, self.auth_service)

    def on_exit(self) -> None:
        """Handle exit button click."""
        if self.ask_confirmation(
            "Exit", "Are you sure you want to exit the application?"
        ):
            self.parent.quit()
