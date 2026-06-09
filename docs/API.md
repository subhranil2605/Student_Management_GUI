# API Reference - Student Management GUI

**Version**: 1.0.0  
**Date**: 2026-06-10  
**Status**: Complete

---

## Table of Contents

1. [Configuration API](#configuration-api)
2. [Database API](#database-api)
3. [Validation API](#validation-api)
4. [Services API](#services-api)
5. [UI API](#ui-api)
6. [Utilities API](#utilities-api)
7. [Code Examples](#code-examples)

---

## Configuration API

### src.config.settings

Application constants and settings.

#### Constants

```python
from src.config.settings import (
    DB_PATH,
    ROLES,
    DEFAULT_CATEGORIES,
    VALIDATION_RULES,
    SESSION_TYPES,
    DISABILITY_CATEGORIES,
    MARITAL_STATUSES
)

# Database Configuration
DB_PATH: str  # Path to SQLite database

# User Roles
ROLES = {
    'ADMIN': 'Admin',      # Full system access
    'TEACHER': 'Teacher',  # Student management
    'STAFF': 'Staff'       # Limited access
}

# Student Categories
DEFAULT_CATEGORIES = [
    'General',
    'OBC',
    'SC',
    'ST',
    'Minority'
]

# Validation Rules
VALIDATION_RULES = {
    'NAME_MIN_LENGTH': 2,
    'NAME_MAX_LENGTH': 100,
    'EMAIL_PATTERN': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'PHONE_LENGTH': 10,
    'PHONE_PATTERN': r'^\d{10}$',
    'AADHAAR_LENGTH': 12,
    'AGE_MIN': 5,
    'AGE_MAX': 100,
    'PASSWORD_MIN_LENGTH': 8,
    'MARKS_MIN': 0,
    'MARKS_MAX': 100,
    'GPA_MIN': 0,
    'GPA_MAX': 10,
    'CGPA_MIN': 0,
    'CGPA_MAX': 10
}

# Session Types
SESSION_TYPES = ['2024-25', '2025-26', '2026-27']

# Disability Categories
DISABILITY_CATEGORIES = [
    'None',
    'Physical',
    'Visual',
    'Hearing',
    'Learning',
    'Other'
]

# Marital Status
MARITAL_STATUSES = [
    'Single',
    'Married',
    'Divorced',
    'Widowed'
]
```

### src.config.ui_config

UI theme and styling configuration.

#### Constants

```python
from src.config.ui_config import (
    COLORS,
    FONTS,
    SIZES,
    PADDING,
    THEME
)

# Color Scheme
COLORS = {
    'primary': '#007ACC',
    'secondary': '#6C757D',
    'success': '#28A745',
    'warning': '#FFC107',
    'error': '#D32F2F',
    'background': '#FFFFFF',
    'foreground': '#000000',
    'border': '#CCCCCC'
}

# Fonts
FONTS = {
    'header': ('Arial', 14, 'bold'),
    'subheader': ('Arial', 12, 'bold'),
    'body': ('Arial', 10),
    'monospace': ('Courier', 10)
}

# Sizes
SIZES = {
    'window_width': 1200,
    'window_height': 800,
    'button_width': 100,
    'button_height': 30,
    'entry_height': 25
}

# Padding and Spacing
PADDING = {
    'small': 5,
    'medium': 10,
    'large': 20,
    'xlarge': 30
}

# Theme Name
THEME = 'clam'  # ttk theme name
```

---

## Database API

### src.database.models

Data models and dataclasses.

#### User

```python
from src.database.models import User
from dataclasses import dataclass

@dataclass
class User:
    """User account model."""
    user_id: str
    username: str
    password_hash: str
    role: str  # 'Admin', 'Teacher', 'Staff'
    created_at: str  # ISO format datetime

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        ...
```

#### Student

```python
from src.database.models import Student

@dataclass
class Student:
    """Student profile model."""
    student_id: str
    name: str
    email: str
    phone: str
    dob: str  # YYYY-MM-DD
    sex: str  # 'M' or 'F'
    category: str
    nationality: str
    address: str
    city: str
    state: str
    country: str
    session: str  # e.g., '2024-25'
    stream: str  # e.g., 'Science'
    house: str
    disability: str
    disability_percentage: float
    marital_status: str
    created_at: str
    updated_at: str

    def get_age(self) -> int:
        """Calculate age from DOB."""
        ...

    def get_email(self) -> str:
        """Get email address."""
        ...

    def get_full_name(self) -> str:
        """Get full name with formatting."""
        ...

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        ...
```

#### ExamMarks

```python
from src.database.models import ExamMarks

@dataclass
class ExamMarks:
    """Exam marks model."""
    mark_id: int
    student_id: str
    subject: str
    marks: float
    semester: str  # e.g., 'Sem-I'
    exam_type: str  # 'Midterm', 'Final', etc.
    created_at: str

    def get_grade(self) -> str:
        """Get letter grade from marks."""
        ...

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        ...
```

### src.database.db_manager

Database connection and initialization.

```python
from src.database.db_manager import DatabaseManager

class DatabaseManager:
    """Manages database connections and initialization."""

    def __init__(self, db_path: str):
        """Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        ...

    def initialize_database(self) -> None:
        """Initialize database schema and tables."""
        ...

    def get_connection(self) -> contextmanager:
        """Get database connection context manager.
        
        Usage:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                ...
        """
        ...

    def table_exists(self, table_name: str) -> bool:
        """Check if table exists in database."""
        ...

    def execute(self, query: str, params: tuple = ()) -> list:
        """Execute query and return results.
        
        Args:
            query: SQL query string
            params: Query parameters (for parameterized queries)
            
        Returns:
            List of result rows
        """
        ...

    def execute_many(self, query: str, params_list: list) -> None:
        """Execute query with multiple parameter sets.
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
        """
        ...

    def delete_all_data(self) -> None:
        """Delete all data (dangerous - use with caution)."""
        ...
```

### src.database.queries

Database query operations.

```python
from src.database.queries import DatabaseQueries, QueryError

class DatabaseQueries:
    """Encapsulates all database query operations."""

    def __init__(self, db_manager: DatabaseManager):
        """Initialize with database manager."""
        ...

    # User Operations
    def create_user(self, user_id: str, username: str, 
                   password_hash: str, role: str, 
                   created_at: str) -> None:
        """Create new user account."""
        ...

    def get_user_by_id(self, user_id: str) -> User | None:
        """Get user by ID."""
        ...

    def get_user_by_username(self, username: str) -> User | None:
        """Get user by username."""
        ...

    def get_all_users(self) -> list[User]:
        """Get all users."""
        ...

    def update_user(self, user_id: str, **kwargs) -> None:
        """Update user information."""
        ...

    def delete_user(self, user_id: str) -> None:
        """Delete user account."""
        ...

    # Student Operations
    def create_student(self, student_id: str, name: str, email: str,
                      phone: str, **kwargs) -> None:
        """Create new student record."""
        ...

    def get_student_by_id(self, student_id: str) -> Student | None:
        """Get student by ID."""
        ...

    def get_all_students(self) -> list[Student]:
        """Get all students."""
        ...

    def update_student(self, student_id: str, **kwargs) -> None:
        """Update student information."""
        ...

    def delete_student(self, student_id: str) -> None:
        """Delete student record."""
        ...

    def search_students(self, query: str) -> list[Student]:
        """Search students by name or ID."""
        ...

    def student_exists(self, student_id: str) -> bool:
        """Check if student exists."""
        ...

    def get_student_count(self) -> int:
        """Get total number of students."""
        ...

    def get_students_by_session(self, session: str) -> list[Student]:
        """Get students by session/year."""
        ...

    # Marks Operations
    def add_student_marks(self, student_id: str, subject: str,
                         marks: float, semester: str,
                         exam_type: str) -> int:
        """Add marks for student. Returns mark_id."""
        ...

    def get_student_marks(self, student_id: str) -> list[ExamMarks]:
        """Get all marks for student."""
        ...

    def get_marks_by_subject(self, student_id: str,
                            subject: str) -> list[ExamMarks]:
        """Get marks for student in specific subject."""
        ...

    def update_student_marks(self, mark_id: int, marks: float) -> None:
        """Update marks for a student."""
        ...

    def delete_student_marks(self, mark_id: int) -> None:
        """Delete marks record."""
        ...

    # Photo Operations
    def add_student_photo(self, student_id: str, photo_data: bytes) -> None:
        """Add student photo."""
        ...

    def get_student_photo(self, student_id: str) -> bytes | None:
        """Get student photo."""
        ...

    def update_student_photo(self, student_id: str, photo_data: bytes) -> None:
        """Update student photo."""
        ...

class QueryError(Exception):
    """Custom exception for query errors."""
    pass
```

---

## Validation API

### src.validators.form_validator

Form field validation.

```python
from src.validators.form_validator import FormValidator, ValidationError

class FormValidator:
    """Validates form input fields."""

    def validate_name(self, name: str) -> str:
        """Validate name field.
        
        Rules:
        - Not empty
        - 2-100 characters
        - Only letters, spaces, hyphens
        
        Raises:
            ValidationError: If validation fails
            
        Returns:
            Validated name
        """
        ...

    def validate_email(self, email: str) -> str:
        """Validate email format."""
        ...

    def validate_phone(self, phone: str) -> str:
        """Validate phone number.
        
        Rules:
        - 10 digits
        - Only numeric
        """
        ...

    def validate_date(self, date_str: str) -> str:
        """Validate date format (DD/MM/YYYY)."""
        ...

    def validate_dob(self, dob_str: str) -> str:
        """Validate date of birth.
        
        Rules:
        - Valid date
        - Age between 5 and 100
        """
        ...

    def validate_percentage(self, percentage: float) -> float:
        """Validate percentage (0-100)."""
        ...

    def validate_marks(self, marks: float) -> float:
        """Validate exam marks (0-100)."""
        ...

    def validate_gpa(self, gpa: float) -> float:
        """Validate GPA (0-10)."""
        ...

    def validate_cgpa(self, cgpa: float) -> float:
        """Validate CGPA (0-10)."""
        ...

    def validate_password(self, password: str) -> str:
        """Validate password.
        
        Rules:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        """
        ...

    def validate_aadhaar(self, aadhaar: str) -> str:
        """Validate AADHAAR (12 digits)."""
        ...

    def validate_required_field(self, value: str, 
                               field_name: str) -> str:
        """Validate field is not empty."""
        ...

    def validate_dropdown_selection(self, value: str) -> str:
        """Validate dropdown not set to default."""
        ...

    def validate_text_area(self, text: str) -> str:
        """Validate text area (max 500 chars)."""
        ...

class ValidationError(Exception):
    """Raised when validation fails."""
    pass
```

### src.validators.business_rules

Business rule validation.

```python
from src.validators.business_rules import BusinessRuleValidator

class BusinessRuleValidator:
    """Validates business rules and complex validations."""

    def __init__(self, db_queries: DatabaseQueries):
        """Initialize with database queries instance."""
        ...

    def validate_student_id_unique(self, student_id: str, 
                                  queries: DatabaseQueries) -> None:
        """Verify student ID is unique."""
        ...

    def validate_student_age_range(self, dob: str) -> None:
        """Verify student is in valid age range."""
        ...

    def validate_marks_range(self, marks: float) -> None:
        """Verify marks are in valid range."""
        ...

    def validate_cgpa_calculation(self, subjects: list[dict]) -> float:
        """Validate and calculate CGPA."""
        ...

    def validate_gpa_from_percentage(self, percentage: float) -> float:
        """Convert percentage to GPA."""
        ...

    def validate_disability_percentage(self, has_disability: bool,
                                       percentage: float) -> None:
        """Validate disability percentage if applicable."""
        ...

    def validate_nationality_country(self, nationality: str,
                                     country: str) -> None:
        """Verify nationality and country match."""
        ...

    def validate_address_fields(self, same_address: bool,
                               address: str,
                               permanent_address: str) -> None:
        """Validate address fields based on flag."""
        ...

    def validate_duplicate_registration(self, email: str,
                                       phone: str) -> None:
        """Check for duplicate student registration."""
        ...

    def validate_marks_prerequisites(self, student_id: str,
                                    subject: str) -> None:
        """Verify marks entry prerequisites."""
        ...
```

---

## Services API

### src.services.auth_service

Authentication and authorization.

```python
from src.services.auth_service import AuthService

class AuthService:
    """Manages user authentication and authorization."""

    def __init__(self, db_queries: DatabaseQueries):
        """Initialize with database queries."""
        ...

    def register_user(self, username: str, password: str,
                     role: str) -> None:
        """Register new user account.
        
        Args:
            username: Unique username
            password: Plain text password (will be hashed)
            role: 'Admin', 'Teacher', or 'Staff'
        """
        ...

    def login(self, username: str, password: str) -> bool:
        """Authenticate user.
        
        Args:
            username: User username
            password: Plain text password
            
        Returns:
            True if login successful, False otherwise
        """
        ...

    def logout(self) -> None:
        """End current session."""
        ...

    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        ...

    def get_current_user(self) -> User | None:
        """Get currently logged-in user."""
        ...

    def change_password(self, old_password: str,
                       new_password: str) -> bool:
        """Change user password."""
        ...

    def is_admin(self) -> bool:
        """Check if current user is admin."""
        ...

    def is_teacher(self) -> bool:
        """Check if current user is teacher."""
        ...

    def is_staff(self) -> bool:
        """Check if current user is staff."""
        ...

    def verify_admin_access(self) -> bool:
        """Verify admin access."""
        ...

    def verify_teacher_access(self) -> bool:
        """Verify teacher access."""
        ...

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256."""
        ...

    @staticmethod
    def verify_password(plain_password: str,
                       hashed_password: str) -> bool:
        """Verify password against hash."""
        ...
```

### src.services.student_service

Student management.

```python
from src.services.student_service import StudentService

class StudentService:
    """Manages student operations."""

    def __init__(self, db_queries: DatabaseQueries,
                auth_service: AuthService):
        """Initialize with dependencies."""
        ...

    def register_student(self, student_data: dict) -> None:
        """Register new student.
        
        Args:
            student_data: Dictionary with student information
                Required keys: student_id, name, email, phone, dob,
                              sex, category, nationality, address,
                              city, state, country
        """
        ...

    def get_student(self, student_id: str) -> Student | None:
        """Get student by ID."""
        ...

    def update_student(self, student_id: str,
                      student_data: dict) -> None:
        """Update student information."""
        ...

    def delete_student(self, student_id: str) -> None:
        """Delete student record."""
        ...

    def search_students(self, query: str) -> list[Student]:
        """Search students by name or ID.
        
        Args:
            query: Search string
            
        Returns:
            List of matching students
        """
        ...

    def filter_students(self, filters: dict) -> list[Student]:
        """Filter students by criteria.
        
        Args:
            filters: Dictionary with filter criteria
                e.g., {'session': '2024-25', 'stream': 'Science'}
        """
        ...

    def get_all_students(self) -> list[Student]:
        """Get all students."""
        ...

    def get_student_count(self) -> int:
        """Get total number of students."""
        ...

    def get_students_by_session(self, session: str) -> list[Student]:
        """Get students by session."""
        ...

    def add_student_photo(self, student_id: str,
                         photo_path: str) -> None:
        """Add student photo from file."""
        ...

    def get_student_photo(self, student_id: str) -> bytes | None:
        """Get student photo."""
        ...
```

### src.services.marks_service

Marks management.

```python
from src.services.marks_service import MarksService

class MarksService:
    """Manages student marks and academic records."""

    def __init__(self, db_queries: DatabaseQueries,
                student_service: StudentService):
        """Initialize with dependencies."""
        ...

    def add_marks(self, marks_data: dict) -> None:
        """Add marks for student.
        
        Args:
            marks_data: Dictionary with:
                - student_id
                - subject
                - marks (0-100)
                - semester
                - exam_type
        """
        ...

    def get_marks(self, student_id: str) -> list[dict]:
        """Get all marks for student."""
        ...

    def update_marks(self, mark_id: int, marks: float) -> None:
        """Update marks."""
        ...

    def delete_marks(self, mark_id: int) -> None:
        """Delete marks record."""
        ...

    def calculate_cgpa(self, student_id: str) -> float:
        """Calculate CGPA for student.
        
        Returns:
            CGPA on scale of 0-10
        """
        ...

    def calculate_gpa(self, student_id: str,
                     semester: str) -> float:
        """Calculate GPA for student in semester."""
        ...

    def get_average_marks(self, student_id: str) -> float:
        """Get average marks across all subjects."""
        ...

    def get_best_subject(self, student_id: str) -> dict:
        """Get subject with highest marks."""
        ...

    def get_worst_subject(self, student_id: str) -> dict:
        """Get subject with lowest marks."""
        ...

    def assign_grade_by_percentage(self, percentage: float) -> str:
        """Assign letter grade based on percentage.
        
        Grading Scale:
        - 90+ : A+
        - 80-89 : A
        - 70-79 : B
        - 60-69 : C
        - 50-59 : D
        - Below 50 : F
        """
        ...
```

---

## UI API

### src.ui.base

Base classes for UI components.

```python
from src.ui.base import BaseWindow, BaseFrame
import tkinter as tk

class BaseWindow(tk.Toplevel):
    """Base class for all application windows."""

    def __init__(self, parent: tk.Tk | None = None):
        """Initialize base window."""
        ...

    def apply_theme(self) -> None:
        """Apply application theme to window."""
        ...

    def show_error(self, title: str, message: str) -> None:
        """Show error dialog."""
        ...

    def show_success(self, title: str, message: str) -> None:
        """Show success dialog."""
        ...

    def show_warning(self, title: str, message: str) -> None:
        """Show warning dialog."""
        ...

    def confirm_action(self, title: str,
                      message: str) -> bool:
        """Show confirmation dialog."""
        ...

    def navigate_to(self, window_class: type) -> None:
        """Navigate to another window."""
        ...

class BaseFrame(tk.Frame):
    """Base class for all application frames."""

    def __init__(self, parent: tk.Widget, **kwargs):
        """Initialize base frame."""
        ...

    def apply_theme(self) -> None:
        """Apply application theme to frame."""
        ...

    def get_values(self) -> dict:
        """Get all form values."""
        ...

    def clear_values(self) -> None:
        """Clear all form fields."""
        ...

    def set_values(self, data: dict) -> None:
        """Set form values from dictionary."""
        ...
```

### src.ui.components

Reusable UI components.

```python
from src.ui.components import (
    FormEntry, FormCombobox, FormTextArea, TableFrame
)
import tkinter as tk

class FormEntry(tk.Frame):
    """Entry field with label and validation."""

    def __init__(self, parent: tk.Widget, label: str,
                required: bool = False):
        """Create form entry."""
        ...

    def get(self) -> str:
        """Get entry value."""
        ...

    def set(self, value: str) -> None:
        """Set entry value."""
        ...

    def show_error(self, message: str) -> None:
        """Show validation error."""
        ...

    def clear_error(self) -> None:
        """Clear error message."""
        ...

class FormCombobox(tk.Frame):
    """Dropdown with label."""

    def __init__(self, parent: tk.Widget, label: str,
                values: list):
        """Create form combobox."""
        ...

    def get(self) -> str:
        """Get selected value."""
        ...

    def set(self, value: str) -> None:
        """Set selected value."""
        ...

class FormTextArea(tk.Frame):
    """Multi-line text input."""

    def __init__(self, parent: tk.Widget, label: str,
                height: int = 5):
        """Create text area."""
        ...

    def get(self) -> str:
        """Get text value."""
        ...

    def set(self, value: str) -> None:
        """Set text value."""
        ...

class TableFrame(tk.Frame):
    """Data table with scrollbar."""

    def __init__(self, parent: tk.Widget, columns: list):
        """Create table frame."""
        ...

    def insert_row(self, values: list) -> str:
        """Insert row. Returns row ID."""
        ...

    def delete_row(self, row_id: str) -> None:
        """Delete row by ID."""
        ...

    def get_selected(self) -> dict | None:
        """Get currently selected row."""
        ...

    def clear(self) -> None:
        """Clear all rows."""
        ...
```

### src.ui.login_window

Login screen.

```python
from src.ui.login_window import LoginWindow
import tkinter as tk

class LoginWindow(BaseWindow):
    """Login window for user authentication."""

    def __init__(self, parent: tk.Tk | None = None):
        """Initialize login window."""
        ...

    def on_login(self) -> None:
        """Handle login button click."""
        ...
```

### src.ui.registration_window

Student registration.

```python
from src.ui.registration_window import RegistrationWindow
import tkinter as tk

class RegistrationWindow(BaseWindow):
    """Student registration window with 3 tabs."""

    def __init__(self, parent: tk.Tk | None = None,
                student_service: StudentService = None):
        """Initialize registration window."""
        ...

    def get_form_data(self) -> dict:
        """Get all form data."""
        ...

    def validate_and_submit(self) -> None:
        """Validate and submit registration."""
        ...
```

### src.ui.admin_panel

Admin dashboard.

```python
from src.ui.admin_panel import AdminPanel
import tkinter as tk

class AdminPanel(BaseWindow):
    """Admin dashboard for student management."""

    def __init__(self, parent: tk.Tk | None = None):
        """Initialize admin panel."""
        ...

    def refresh_student_list(self) -> None:
        """Refresh student table."""
        ...

    def on_search(self, query: str) -> None:
        """Handle search."""
        ...

    def on_delete(self) -> None:
        """Handle student deletion."""
        ...
```

---

## Utilities API

### src.utils.file_handler

File operations.

```python
from src.utils.file_handler import FileHandler

class FileHandler:
    """Handles file operations."""

    @staticmethod
    def validate_file(file_path: str, 
                     allowed_extensions: list) -> bool:
        """Validate file exists and has allowed extension."""
        ...

    @staticmethod
    def read_file(file_path: str) -> bytes:
        """Read file content."""
        ...

    @staticmethod
    def write_file(file_path: str, content: bytes) -> None:
        """Write content to file."""
        ...

    @staticmethod
    def delete_file(file_path: str) -> None:
        """Delete file."""
        ...

    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if file exists."""
        ...
```

### src.utils.image_handler

Image processing.

```python
from src.utils.image_handler import ImageHandler
from PIL import Image

class ImageHandler:
    """Handles image operations."""

    @staticmethod
    def validate_image(file_path: str) -> bool:
        """Validate image file."""
        ...

    @staticmethod
    def resize_image(image: Image, size: tuple) -> Image:
        """Resize image to specified size."""
        ...

    @staticmethod
    def load_image(file_path: str, 
                  size: tuple = None) -> Image:
        """Load image from file."""
        ...

    @staticmethod
    def image_to_bytes(image: Image,
                      format: str = 'PNG') -> bytes:
        """Convert PIL Image to bytes."""
        ...

    @staticmethod
    def bytes_to_image(data: bytes) -> Image:
        """Convert bytes to PIL Image."""
        ...
```

### src.utils.helpers

Helper functions.

```python
from src.utils.helpers import (
    format_date, parse_date, calculate_cgpa
)

def format_date(date_obj: datetime.date) -> str:
    """Format date as DD/MM/YYYY."""
    ...

def parse_date(date_str: str) -> datetime.date:
    """Parse date string to date object."""
    ...

def calculate_age(dob: str) -> int:
    """Calculate age from DOB string."""
    ...

def calculate_cgpa(marks_list: list[float]) -> float:
    """Calculate CGPA from marks."""
    ...

def percentage_to_gpa(percentage: float) -> float:
    """Convert percentage to GPA."""
    ...
```

---

## Code Examples

### Example 1: Login with Error Handling

```python
from src.services.auth_service import AuthService
from src.database.queries import DatabaseQueries
from src.database.db_manager import DatabaseManager

# Initialize
db = DatabaseManager("app.db")
queries = DatabaseQueries(db)
auth = AuthService(queries)

# Login
username = "teacher1"
password = "SecurePass123!"

if auth.login(username, password):
    current_user = auth.get_current_user()
    print(f"Logged in as: {current_user.username}")
    print(f"Role: {current_user.role}")
else:
    print("Login failed: Invalid credentials")
```

### Example 2: Register Student with Validation

```python
from src.services.student_service import StudentService
from src.validators.form_validator import FormValidator, ValidationError

validator = FormValidator()
student_service = StudentService(queries, auth)

try:
    # Validate input
    name = validator.validate_name("John Doe")
    email = validator.validate_email("john@example.com")
    phone = validator.validate_phone("9876543210")
    
    # Register student
    student_data = {
        "student_id": "STU001",
        "name": name,
        "email": email,
        "phone": phone,
        "dob": "2005-01-15",
        "sex": "M",
        "category": "General",
        "nationality": "Indian",
        "address": "123 Main St",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India"
    }
    
    student_service.register_student(student_data)
    print("Student registered successfully")
    
except ValidationError as e:
    print(f"Validation error: {e}")
```

### Example 3: Add Marks and Calculate CGPA

```python
from src.services.marks_service import MarksService

marks_service = MarksService(queries, student_service)

# Add marks
marks_data = {
    "student_id": "STU001",
    "subject": "Mathematics",
    "marks": 85,
    "semester": "Sem-I",
    "exam_type": "Final"
}

marks_service.add_marks(marks_data)

# Calculate CGPA
cgpa = marks_service.calculate_cgpa("STU001")
print(f"CGPA: {cgpa:.2f}")

# Get grade
marks_percentage = 85
grade = marks_service.assign_grade_by_percentage(marks_percentage)
print(f"Grade: {grade}")
```

### Example 4: Search and Filter Students

```python
# Search by name
results = student_service.search_students("John")
print(f"Found {len(results)} students")

# Filter by session
session_students = student_service.get_students_by_session("2024-25")
print(f"Students in 2024-25: {len(session_students)}")

# Get all students
all_students = student_service.get_all_students()
for student in all_students:
    print(f"{student.student_id}: {student.name}")
```

### Example 5: Create UI Component

```python
from src.ui.components import FormEntry, FormCombobox
from src.config.ui_config import COLORS, FONTS
import tkinter as tk

root = tk.Tk()

# Create entry field
name_entry = FormEntry(root, label="Student Name", required=True)
name_entry.pack(pady=10)

# Create dropdown
category_combo = FormCombobox(
    root,
    label="Category",
    values=["General", "OBC", "SC", "ST"]
)
category_combo.pack(pady=10)

# Get values
name = name_entry.get()
category = category_combo.get()

# Show error if validation fails
if not name:
    name_entry.show_error("Name is required")
```

---

## Error Handling

### Common Exceptions

```python
from src.validators.form_validator import ValidationError
from src.database.queries import QueryError

# Validation error
try:
    validator.validate_email("invalid-email")
except ValidationError as e:
    print(f"Validation failed: {e}")

# Database error
try:
    queries.get_student_by_id("INVALID")
except QueryError as e:
    print(f"Query failed: {e}")
except Exception as e:
    print(f"Database error: {e}")
```

---

## Type Hints & Type Safety

All APIs use type hints for clarity:

```python
def validate_email(email: str) -> str:
    """Returns validated email."""
    ...

def get_students(session: str) -> list[Student]:
    """Returns list of students."""
    ...

def calculate_cgpa(marks: list[float]) -> float | None:
    """Returns CGPA or None if not calculable."""
    ...
```

---

**Last Updated**: 2026-06-10  
**Version**: 1.0.0  
**Status**: Complete
