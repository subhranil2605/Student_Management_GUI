"""Tkinter ttk theme configuration."""

from tkinter import ttk

from src.config.ui_config import COLORS, FONTS


def setup_ttk_theme() -> None:
    """
    Set up ttk theme configuration.

    Configures colors, fonts, and styles for modern UI appearance.
    """
    style = ttk.Style()

    # Set theme to clam for better customization
    try:
        style.theme_use("clam")
    except ttk.TclError:
        # Fallback if clam theme not available
        style.theme_use("alt")

    # Configure Label style
    style.configure(
        "TLabel",
        background=COLORS["light"],
        foreground=COLORS["dark"],
        font=FONTS["normal"],
    )

    # Configure Button style
    style.configure(
        "TButton",
        background=COLORS["primary"],
        foreground=COLORS["white"],
        font=FONTS["normal"],
        borderwidth=1,
        relief="solid",
        padding=5,
    )

    style.map(
        "TButton",
        background=[
            ("active", COLORS["secondary"]),
            ("pressed", COLORS["dark"]),
            ("disabled", COLORS["gray"]),
        ],
        foreground=[
            ("disabled", COLORS["light_gray"]),
        ],
    )

    # Configure Entry style
    style.configure(
        "TEntry",
        fieldbackground="white",
        background=COLORS["light"],
        foreground=COLORS["dark"],
        borderwidth=1,
        relief="solid",
        font=FONTS["normal"],
    )

    # Configure Frame style
    style.configure(
        "TFrame",
        background=COLORS["light"],
        relief="flat",
    )

    # Configure Notebook style
    style.configure(
        "TNotebook",
        background=COLORS["light"],
        borderwidth=0,
    )

    style.configure(
        "TNotebook.Tab",
        background=COLORS["light"],
        foreground=COLORS["dark"],
        padding=[20, 10],
        font=FONTS["normal"],
    )

    style.map(
        "TNotebook.Tab",
        background=[
            ("selected", COLORS["primary"]),
            ("active", COLORS["secondary"]),
        ],
        foreground=[
            ("selected", COLORS["white"]),
        ],
    )

    # Configure Combobox style
    style.configure(
        "TCombobox",
        fieldbackground="white",
        background=COLORS["light"],
        foreground=COLORS["dark"],
        borderwidth=1,
        relief="solid",
        font=FONTS["normal"],
    )

    style.map(
        "TCombobox",
        fieldbackground=[
            ("readonly", COLORS["light"]),
        ],
        background=[
            ("readonly", COLORS["light"]),
        ],
    )

    # Configure Treeview style
    style.configure(
        "Treeview",
        background="white",
        foreground=COLORS["dark"],
        fieldbackground="white",
        borderwidth=1,
        relief="solid",
        font=FONTS["small"],
    )

    style.configure(
        "Treeview.Heading",
        background=COLORS["primary"],
        foreground=COLORS["white"],
        font=FONTS["subheading"],
        borderwidth=1,
        relief="solid",
    )

    style.map(
        "Treeview",
        background=[
            ("selected", COLORS["secondary"]),
        ],
        foreground=[
            ("selected", COLORS["white"]),
        ],
    )

    # Configure Scrollbar style
    style.configure(
        "Vertical.TScrollbar",
        background=COLORS["light"],
        troughcolor=COLORS["light_gray"],
        bordercolor=COLORS["light_gray"],
        arrowcolor=COLORS["dark"],
        darkcolor=COLORS["dark_gray"],
        lightcolor=COLORS["light_gray"],
    )

    style.configure(
        "Horizontal.TScrollbar",
        background=COLORS["light"],
        troughcolor=COLORS["light_gray"],
        bordercolor=COLORS["light_gray"],
        arrowcolor=COLORS["dark"],
        darkcolor=COLORS["dark_gray"],
        lightcolor=COLORS["light_gray"],
    )

    # Configure success button style
    style.configure(
        "Success.TButton",
        background=COLORS["success"],
        foreground=COLORS["white"],
    )

    style.map(
        "Success.TButton",
        background=[
            ("active", "#229954"),
            ("pressed", "#186a3b"),
        ],
    )

    # Configure danger button style
    style.configure(
        "Danger.TButton",
        background=COLORS["danger"],
        foreground=COLORS["white"],
    )

    style.map(
        "Danger.TButton",
        background=[
            ("active", "#cb4335"),
            ("pressed", "#922b21"),
        ],
    )

    # Configure warning button style
    style.configure(
        "Warning.TButton",
        background=COLORS["warning"],
        foreground=COLORS["white"],
    )

    style.map(
        "Warning.TButton",
        background=[
            ("active", "#d68910"),
            ("pressed", "#a04000"),
        ],
    )


def get_color(color_name: str) -> str:
    """
    Get color from configuration.

    Args:
        color_name: Name of color

    Returns:
        Color hex value
    """
    return COLORS.get(color_name, COLORS["primary"])


def get_font(font_name: str) -> tuple:
    """
    Get font from configuration.

    Args:
        font_name: Name of font

    Returns:
        Font tuple (family, size, style)
    """
    return FONTS.get(font_name, FONTS["normal"])
