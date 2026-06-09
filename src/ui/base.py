"""Base window class for all UI windows and frames."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from src.config.ui_config import COLORS, FONTS, PADDING, WINDOW_DIMENSIONS


class BaseWindow(tk.Toplevel):
    """
    Base class for all application windows.

    Provides consistent styling, theming, and common methods for all windows.
    """

    def __init__(
        self,
        parent: tk.Tk,
        title: str,
        width: int = 800,
        height: int = 600,
        resizable: bool = False,
    ):
        """
        Initialize base window.

        Args:
            parent: Parent window (root Tk instance)
            title: Window title
            width: Window width
            height: Window height
            resizable: Whether window is resizable
        """
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(resizable, resizable)

        # Configure style
        self.configure(bg=COLORS["light"])

        # Center window on screen
        self.center_window()

        # Store parent reference
        self.parent = parent

    def center_window(self) -> None:
        """Center window on screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_frame(
        self,
        parent: tk.Widget,
        bg: str = COLORS["light"],
        padding: int = PADDING["md"],
    ) -> ttk.Frame:
        """
        Create styled frame.

        Args:
            parent: Parent widget
            bg: Background color
            padding: Padding size

        Returns:
            Configured frame
        """
        frame = ttk.Frame(parent)
        frame.configure(padding=padding)
        return frame

    def create_label(
        self,
        parent: tk.Widget,
        text: str,
        font: tuple = FONTS["normal"],
        fg: str = COLORS["dark"],
    ) -> ttk.Label:
        """
        Create styled label.

        Args:
            parent: Parent widget
            text: Label text
            font: Font tuple
            fg: Foreground color

        Returns:
            Configured label
        """
        label = ttk.Label(parent, text=text, font=font)
        return label

    def create_entry(
        self,
        parent: tk.Widget,
        width: int = 30,
        show: Optional[str] = None,
    ) -> ttk.Entry:
        """
        Create styled entry.

        Args:
            parent: Parent widget
            width: Entry width in characters
            show: Character to show (e.g., '*' for passwords)

        Returns:
            Configured entry
        """
        entry = ttk.Entry(parent, width=width, show=show)
        return entry

    def create_button(
        self,
        parent: tk.Widget,
        text: str,
        command: Optional[Callable] = None,
        style: str = "primary",
    ) -> ttk.Button:
        """
        Create styled button.

        Args:
            parent: Parent widget
            text: Button text
            command: Command to execute on click
            style: Button style (primary, success, danger, etc.)

        Returns:
            Configured button
        """
        button = ttk.Button(parent, text=text, command=command)
        return button

    def create_combobox(
        self,
        parent: tk.Widget,
        values: list,
        width: int = 27,
    ) -> ttk.Combobox:
        """
        Create styled combobox.

        Args:
            parent: Parent widget
            values: List of values
            width: Combobox width

        Returns:
            Configured combobox
        """
        combobox = ttk.Combobox(
            parent, values=values, width=width, state="readonly"
        )
        return combobox

    def show_error(self, title: str, message: str) -> None:
        """
        Show error dialog.

        Args:
            title: Dialog title
            message: Error message
        """
        from tkinter import messagebox

        messagebox.showerror(title, message, parent=self)

    def show_success(self, title: str, message: str) -> None:
        """
        Show success dialog.

        Args:
            title: Dialog title
            message: Success message
        """
        from tkinter import messagebox

        messagebox.showinfo(title, message, parent=self)

    def ask_confirmation(self, title: str, message: str) -> bool:
        """
        Show confirmation dialog.

        Args:
            title: Dialog title
            message: Confirmation message

        Returns:
            True if user confirms, False otherwise
        """
        from tkinter import messagebox

        return messagebox.askyesno(title, message, parent=self)

    def close_window(self) -> None:
        """Close the window."""
        self.destroy()


class BaseFrame(ttk.Frame):
    """
    Base class for frames within windows.

    Provides common styling and methods for frames.
    """

    def __init__(self, parent: tk.Widget, **kwargs):
        """
        Initialize base frame.

        Args:
            parent: Parent widget
            **kwargs: Additional arguments for ttk.Frame
        """
        super().__init__(parent, **kwargs)
        self.configure(padding=PADDING["md"])

    def create_label(
        self,
        text: str,
        font: tuple = FONTS["normal"],
        fg: str = COLORS["dark"],
    ) -> ttk.Label:
        """
        Create styled label.

        Args:
            text: Label text
            font: Font tuple
            fg: Foreground color

        Returns:
            Configured label
        """
        return ttk.Label(self, text=text, font=font)

    def create_entry(
        self,
        width: int = 30,
        show: Optional[str] = None,
    ) -> ttk.Entry:
        """
        Create styled entry.

        Args:
            width: Entry width
            show: Show character for password fields

        Returns:
            Configured entry
        """
        return ttk.Entry(self, width=width, show=show)

    def create_button(
        self,
        text: str,
        command: Optional[Callable] = None,
    ) -> ttk.Button:
        """
        Create styled button.

        Args:
            text: Button text
            command: Command to execute

        Returns:
            Configured button
        """
        return ttk.Button(self, text=text, command=command)

    def create_combobox(
        self,
        values: list,
        width: int = 27,
    ) -> ttk.Combobox:
        """
        Create styled combobox.

        Args:
            values: List of values
            width: Combobox width

        Returns:
            Configured combobox
        """
        return ttk.Combobox(self, values=values, width=width, state="readonly")
