"""Reusable UI components for forms and dialogs."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional

from src.config.ui_config import COLORS, FONTS, PADDING
from src.validators.form_validator import ValidationError


class FormEntry(ttk.Frame):
    """
    Entry field with label and validation.

    Combines label and entry widget with built-in validation feedback.
    """

    def __init__(
        self,
        parent: tk.Widget,
        label_text: str,
        width: int = 30,
        show: Optional[str] = None,
        required: bool = False,
    ):
        """
        Initialize form entry.

        Args:
            parent: Parent widget
            label_text: Label text
            width: Entry width
            show: Show character for passwords
            required: Whether field is required
        """
        super().__init__(parent)

        self.required = required
        self.variable = tk.StringVar()

        # Label
        label = ttk.Label(
            self, text=label_text + (" *" if required else ""), font=FONTS["normal"]
        )
        label.grid(row=0, column=0, sticky="w", padx=PADDING["sm"])

        # Entry
        self.entry = ttk.Entry(self, width=width, show=show, textvariable=self.variable)
        self.entry.grid(row=1, column=0, sticky="ew", padx=PADDING["sm"], pady=PADDING["sm"])

        # Error label
        self.error_label = ttk.Label(
            self, text="", font=FONTS["small"], foreground=COLORS["danger"]
        )
        self.error_label.grid(row=2, column=0, sticky="w", padx=PADDING["sm"])

        self.columnconfigure(0, weight=1)

    def get(self) -> str:
        """Get entry value."""
        return self.variable.get().strip()

    def set(self, value: str) -> None:
        """Set entry value."""
        self.variable.set(value)

    def set_error(self, message: str) -> None:
        """
        Display error message.

        Args:
            message: Error message to display
        """
        self.error_label.configure(text=message, foreground=COLORS["danger"])
        self.entry.configure(foreground=COLORS["danger"])

    def clear_error(self) -> None:
        """Clear error message."""
        self.error_label.configure(text="")
        self.entry.configure(foreground=COLORS["dark"])

    def clear(self) -> None:
        """Clear entry value."""
        self.variable.set("")
        self.clear_error()


class FormCombobox(ttk.Frame):
    """
    Combobox field with label.

    Combines label and combobox widget for selection fields.
    """

    def __init__(
        self,
        parent: tk.Widget,
        label_text: str,
        values: List[str],
        width: int = 27,
        required: bool = False,
    ):
        """
        Initialize form combobox.

        Args:
            parent: Parent widget
            label_text: Label text
            values: List of combobox values
            width: Combobox width
            required: Whether field is required
        """
        super().__init__(parent)

        self.required = required
        self.variable = tk.StringVar()

        # Label
        label = ttk.Label(
            self, text=label_text + (" *" if required else ""), font=FONTS["normal"]
        )
        label.grid(row=0, column=0, sticky="w", padx=PADDING["sm"])

        # Combobox
        self.combobox = ttk.Combobox(
            self,
            values=values,
            width=width,
            state="readonly",
            textvariable=self.variable,
        )
        self.combobox.grid(
            row=1, column=0, sticky="ew", padx=PADDING["sm"], pady=PADDING["sm"]
        )

        # Error label
        self.error_label = ttk.Label(
            self, text="", font=FONTS["small"], foreground=COLORS["danger"]
        )
        self.error_label.grid(row=2, column=0, sticky="w", padx=PADDING["sm"])

        self.columnconfigure(0, weight=1)

    def get(self) -> str:
        """Get combobox value."""
        return self.variable.get()

    def set(self, value: str) -> None:
        """Set combobox value."""
        self.variable.set(value)

    def set_error(self, message: str) -> None:
        """
        Display error message.

        Args:
            message: Error message
        """
        self.error_label.configure(text=message, foreground=COLORS["danger"])

    def clear_error(self) -> None:
        """Clear error message."""
        self.error_label.configure(text="")

    def clear(self) -> None:
        """Clear combobox value."""
        self.variable.set("")
        self.clear_error()


class FormTextArea(ttk.Frame):
    """
    Text area field with label.

    For multi-line text input with validation feedback.
    """

    def __init__(
        self,
        parent: tk.Widget,
        label_text: str,
        width: int = 40,
        height: int = 5,
        required: bool = False,
    ):
        """
        Initialize form text area.

        Args:
            parent: Parent widget
            label_text: Label text
            width: Text area width
            height: Text area height
            required: Whether field is required
        """
        super().__init__(parent)

        self.required = required

        # Label
        label = ttk.Label(
            self, text=label_text + (" *" if required else ""), font=FONTS["normal"]
        )
        label.grid(row=0, column=0, sticky="w", padx=PADDING["sm"])

        # Text area
        self.text = tk.Text(
            self,
            width=width,
            height=height,
            font=FONTS["small"],
            bg="white",
            relief="solid",
            borderwidth=1,
        )
        self.text.grid(row=1, column=0, sticky="ew", padx=PADDING["sm"], pady=PADDING["sm"])

        # Error label
        self.error_label = ttk.Label(
            self, text="", font=FONTS["small"], foreground=COLORS["danger"]
        )
        self.error_label.grid(row=2, column=0, sticky="w", padx=PADDING["sm"])

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def get(self) -> str:
        """Get text area value."""
        return self.text.get("1.0", tk.END).strip()

    def set(self, value: str) -> None:
        """Set text area value."""
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", value)

    def set_error(self, message: str) -> None:
        """
        Display error message.

        Args:
            message: Error message
        """
        self.error_label.configure(text=message, foreground=COLORS["danger"])

    def clear_error(self) -> None:
        """Clear error message."""
        self.error_label.configure(text="")

    def clear(self) -> None:
        """Clear text area."""
        self.text.delete("1.0", tk.END)
        self.clear_error()


class DialogFrame(ttk.Frame):
    """
    Base frame for dialog windows.

    Provides standard dialog layout with title and buttons.
    """

    def __init__(
        self,
        parent: tk.Widget,
        title: str,
        buttons: Optional[List[tuple]] = None,
    ):
        """
        Initialize dialog frame.

        Args:
            parent: Parent widget
            title: Dialog title
            buttons: List of (label, command) tuples for buttons
        """
        super().__init__(parent, padding=PADDING["lg"])

        # Title
        title_label = ttk.Label(
            self, text=title, font=FONTS["heading"], foreground=COLORS["primary"]
        )
        title_label.pack(pady=PADDING["md"])

        # Content frame
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True, padx=PADDING["md"])

        # Button frame
        if buttons:
            button_frame = ttk.Frame(self)
            button_frame.pack(pady=PADDING["md"])

            for label, command in buttons:
                btn = ttk.Button(button_frame, text=label, command=command)
                btn.pack(side="left", padx=PADDING["sm"])

    def add_content(self, widget: tk.Widget) -> None:
        """
        Add content widget to dialog.

        Args:
            widget: Widget to add
        """
        widget.pack(in_=self.content_frame, fill="both", expand=True)


class TableFrame(ttk.Frame):
    """
    Table/Treeview wrapper for displaying tabular data.

    Provides a clean interface for displaying and interacting with tables.
    """

    def __init__(
        self,
        parent: tk.Widget,
        columns: List[str],
        column_widths: Optional[List[int]] = None,
    ):
        """
        Initialize table frame.

        Args:
            parent: Parent widget
            columns: List of column names
            column_widths: Optional list of column widths
        """
        super().__init__(parent)

        # Create Treeview
        self.tree = ttk.Treeview(
            self, columns=columns, show="headings", height=15
        )

        # Configure columns
        for i, col in enumerate(columns):
            width = column_widths[i] if column_widths else 100
            self.tree.column(col, width=width, anchor="w")
            self.tree.heading(col, text=col)

        # Scrollbars
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def insert_row(self, values: List) -> str:
        """
        Insert row into table.

        Args:
            values: List of values for row

        Returns:
            Row ID
        """
        return self.tree.insert("", "end", values=values)

    def clear(self) -> None:
        """Clear all rows from table."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def get_selected(self) -> Optional[str]:
        """
        Get selected row ID.

        Returns:
            Row ID or None if no selection
        """
        selection = self.tree.selection()
        return selection[0] if selection else None

    def get_row_values(self, item_id: str) -> tuple:
        """
        Get values of a row.

        Args:
            item_id: Row ID

        Returns:
            Tuple of row values
        """
        return self.tree.item(item_id, "values")

    def delete_row(self, item_id: str) -> None:
        """
        Delete row from table.

        Args:
            item_id: Row ID to delete
        """
        self.tree.delete(item_id)
