"""Application configuration and settings."""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Asset paths
ASSETS_DIR = PROJECT_ROOT / "img"
ICONS = {
    "app_icon": ASSETS_DIR / "icond.ico",
    "app_logo": ASSETS_DIR / "ico.png",
    "college_image": ASSETS_DIR / "college_image.png",
    "background": ASSETS_DIR / "background_1.png",
}

# Database configuration
DATABASE_PATH = PROJECT_ROOT / "student_mgt.db"
DATABASE_TIMEOUT = 10

# User roles
USER_ROLES = {
    "admin": "Administrator",
    "teacher": "Teacher",
    "staff": "Staff",
}

# Student categories
STUDENT_CATEGORIES = [
    "Select",
    "General",
    "OBC",
    "SC",
    "ST",
]

# Religions
RELIGIONS = [
    "Select",
    "Hindu",
    "Muslim",
    "Christian",
    "Sikh",
    "Buddhist",
    "Jain",
    "Others",
]

# Nationalities
NATIONALITIES = [
    "Select",
    "Indian",
    "Others",
]

# Sex/Gender
GENDERS = [
    "Select",
    "Male",
    "Female",
    "Other",
]

# Handicap options
HANDICAP_OPTIONS = [
    "yes",
    "no",
]

# Sessions (Academic years)
SESSIONS = [
    "Select",
    "2018-2022",
    "2019-2023",
    "2020-2024",
    "2021-2025",
    "2022-2026",
    "2023-2027",
    "2024-2028",
]

# Courses
COURSES = [
    "Select",
    "B.Tech",
    "B.Sc",
    "B.A",
    "M.Tech",
    "M.Sc",
    "M.A",
]

# Form validation rules
VALIDATION_RULES = {
    "name": {
        "min_length": 2,
        "max_length": 100,
        "pattern": r"^[a-zA-Z\s]+$",
    },
    "email": {
        "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    },
    "phone": {
        "min_length": 10,
        "max_length": 10,
        "pattern": r"^\d{10}$",
    },
    "aadhaar": {
        "min_length": 12,
        "max_length": 12,
        "pattern": r"^\d{12}$",
    },
    "pincode": {
        "min_length": 6,
        "max_length": 6,
        "pattern": r"^\d{6}$",
    },
    "student_id": {
        "min_length": 3,
        "max_length": 20,
    },
    "registration_number": {
        "min_length": 3,
        "max_length": 20,
    },
    "marks": {
        "min_value": 0,
        "max_value": 100,
    },
    "percentage": {
        "min_value": 0,
        "max_value": 100,
    },
    "age": {
        "min_age": 5,
        "max_age": 60,
    },
}

# File upload settings
FILE_UPLOAD = {
    "max_size_mb": 5,
    "allowed_extensions": [".jpg", ".jpeg", ".png", ".gif"],
    "upload_dir": PROJECT_ROOT / "student_photo",
    "thumbnail_size": (200, 200),
}

# Ensure upload directory exists
FILE_UPLOAD["upload_dir"].mkdir(parents=True, exist_ok=True)
