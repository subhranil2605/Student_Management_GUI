"""UI configuration including colors, fonts, and dimensions."""

# Color scheme
COLORS = {
    "primary": "#2C3E50",
    "secondary": "#3498DB",
    "success": "#27AE60",
    "danger": "#E74C3C",
    "warning": "#F39C12",
    "info": "#3498DB",
    "light": "#ECF0F1",
    "dark": "#2C3E50",
    "white": "#FFFFFF",
    "black": "#000000",
    "gray": "#95A5A6",
    "light_gray": "#BDC3C7",
    "dark_gray": "#7F8C8D",
}

# Font configurations
FONTS = {
    "title": ("times", 20, "bold"),
    "heading": ("times", 15, "bold"),
    "subheading": ("times", 13, "bold"),
    "normal": ("times", 13),
    "small": ("times", 11),
    "tiny": ("times", 9),
    "monospace": ("courier", 11),
}

# Widget padding and spacing
PADDING = {
    "xs": 2,
    "sm": 5,
    "md": 10,
    "lg": 15,
    "xl": 20,
    "xxl": 30,
}

# Window dimensions
WINDOW_DIMENSIONS = {
    "root": {
        "width": 800,
        "height": 600,
    },
    "login": {
        "width": 400,
        "height": 300,
    },
    "registration": {
        "width": 900,
        "height": 700,
    },
    "admin_panel": {
        "width": 1000,
        "height": 700,
    },
    "student_view": {
        "width": 800,
        "height": 600,
    },
    "marks_view": {
        "width": 900,
        "height": 650,
    },
}

# Widget styling
WIDGET_STYLES = {
    "entry": {
        "bg": "white",
        "font": FONTS["normal"],
        "bd": 1,
    },
    "button": {
        "font": FONTS["normal"],
        "fg": "white",
    },
    "label": {
        "font": FONTS["normal"],
    },
    "text": {
        "font": FONTS["small"],
        "wrap": "word",
    },
}

# Theme configuration (for ttk)
TTK_THEME = "clam"

# Button styles
BUTTON_STYLES = {
    "primary": {
        "bg": COLORS["primary"],
        "fg": COLORS["white"],
    },
    "success": {
        "bg": COLORS["success"],
        "fg": COLORS["white"],
    },
    "danger": {
        "bg": COLORS["danger"],
        "fg": COLORS["white"],
    },
    "warning": {
        "bg": COLORS["warning"],
        "fg": COLORS["white"],
    },
}

# Disabled state colors
DISABLED_COLORS = {
    "bg": "#2C3E50",
    "fg": "#95A5A6",
}

# Image sizes
IMAGE_SIZES = {
    "thumbnail": (100, 120),
    "small": (200, 250),
    "medium": (400, 500),
    "large": (600, 750),
}
