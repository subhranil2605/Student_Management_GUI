# System Architecture - Student Management GUI

**Version**: 1.0.0  
**Date**: 2026-06-10  
**Status**: Complete

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Module Responsibilities](#module-responsibilities)
4. [Data Flow](#data-flow)
5. [Design Patterns](#design-patterns)
6. [Dependencies](#dependencies)
7. [Database Schema](#database-schema)
8. [API Reference](#api-reference)

---

## Overview

The Student Management GUI is a modern, modularized desktop application built with Python and Tkinter. It follows clean architecture principles with clear separation of concerns across configuration, data access, business logic, and presentation layers.

### Key Characteristics

- **Modular Design**: 20+ independent modules with single responsibilities
- **Clean Architecture**: Separated layers (UI, Services, Database)
- **Type Safe**: 100% type hints on public APIs
- **Well Tested**: 80%+ test coverage with 189+ passing tests
- **Modern UI**: Uses ttk widgets instead of classic Tk
- **PEP 8 Compliant**: Follows Python style guidelines

### Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│           User Interface Layer (UI)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │ LoginWindow  │  │Registration  │  │ AdminPanel ││
│  │              │  │              │  │            ││
│  │StudentView   │  │  MarksView   │  │   Themes   ││
│  └──────────────┘  └──────────────┘  └────────────┘│
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│         Services Layer (Business Logic)              │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │ AuthService  │  │StudentService│  │MarksService││
│  │              │  │              │  │            ││
│  │ Password     │  │ CRUD Ops     │  │ CGPA Calc  ││
│  │ Sessions     │  │ Search/Filter│  │ Grading    ││
│  └──────────────┘  └──────────────┘  └────────────┘│
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│      Validators Layer (Input Validation)             │
│  ┌──────────────────────┐  ┌───────────────────────┐│
│  │  FormValidator       │  │ BusinessRuleValidator ││
│  │                      │  │                       ││
│  │ Field validation     │  │ Business rule checks  ││
│  │ Format validation    │  │ Dependency validation ││
│  └──────────────────────┘  └───────────────────────┘│
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│       Database Layer (Data Access)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │ DatabaseMgr  │  │   Queries    │  │   Models   ││
│  │              │  │              │  │            ││
│  │ Connection   │  │ SQL Ops      │  │ Dataclasses││
│  │ Pooling      │  │ Transactions │  │ Validation ││
│  └──────────────┘  └──────────────┘  └────────────┘│
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│     Utilities Layer (Helpers & Infrastructure)       │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │ FileHandler  │  │ImageHandler  │  │   Helpers  ││
│  │              │  │              │  │            ││
│  │ File ops    │  │ Image resize  │  │ Date fmt   ││
│  │ Validation   │  │ Format check  │  │ Calculations││
│  └──────────────┘  └──────────────┘  └────────────┘│
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│       Configuration Layer (Settings & Constants)     │
│  ┌──────────────┐  ┌──────────────────────────────┐│
│  │  settings.py │  │      ui_config.py            ││
│  │              │  │                              ││
│  │ App constants│  │ Theme, colors, fonts, dimensions││
│  │ DB paths     │  │ UI component spacing         ││
│  └──────────────┘  └──────────────────────────────┘│
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│       SQLite Database (Data Persistence)             │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │   users      │  │   students   │  │   marks    ││
│  │              │  │              │  │            ││
│  │ auth info    │  │ personal data│  │ exam marks ││
│  └──────────────┘  └──────────────┘  └────────────┘│
└──────────────────────────────────────────────────────┘
```

---

## System Architecture

### Core Principles

1. **Separation of Concerns**
   - Each module has a single, well-defined responsibility
   - Clear boundaries between layers
   - Minimal coupling between components

2. **Dependency Injection**
   - Services receive dependencies through constructors
   - Testable without tight coupling
   - Easy to swap implementations

3. **Type Safety**
   - All public APIs have type hints
   - Dataclasses for type-safe data models
   - Enables IDE auto-completion and type checking

4. **Error Handling**
   - Custom exceptions for application errors
   - Graceful error recovery
   - Meaningful error messages

5. **Configuration Externalization**
   - All hardcoded values in config modules
   - Environment-specific overrides possible
   - Single source of truth for constants

### Architectural Layers

#### 1. Configuration Layer

**Responsibility**: Centralize application constants and settings

**Files**:
- `src/config/settings.py` - Application constants
- `src/config/ui_config.py` - UI theme and styling

**Key Exports**:
- Database paths
- User roles and permissions
- Validation rules
- UI colors, fonts, dimensions

**Usage Pattern**:
```python
from src.config.settings import ROLES, VALIDATION_RULES
from src.config.ui_config import COLORS, FONTS
```

#### 2. Database Layer

**Responsibility**: Abstract all database operations

**Files**:
- `src/database/db_manager.py` - Connection management
- `src/database/models.py` - Data models
- `src/database/queries.py` - CRUD operations

**Key Classes**:
- `DatabaseManager` - Connection pooling, initialization
- `User`, `Student`, `ExamMarks` - Data models
- `DatabaseQueries` - SQL operations

**Usage Pattern**:
```python
db = DatabaseManager("app.db")
queries = DatabaseQueries(db)
student = queries.get_student_by_id("STU001")
```

#### 3. Validators Layer

**Responsibility**: Validate user input and business rules

**Files**:
- `src/validators/form_validator.py` - Form field validation
- `src/validators/business_rules.py` - Business rule validation

**Key Classes**:
- `FormValidator` - Email, date, phone, etc. validation
- `BusinessRuleValidator` - Complex business logic validation
- `ValidationError` - Custom exception

**Usage Pattern**:
```python
validator = FormValidator()
try:
    email = validator.validate_email(user_input)
except ValidationError as e:
    show_error(str(e))
```

#### 4. Services Layer

**Responsibility**: Implement business logic independent of UI

**Files**:
- `src/services/auth_service.py` - Authentication
- `src/services/student_service.py` - Student management
- `src/services/marks_service.py` - Marks management

**Key Classes**:
- `AuthService` - Login, sessions, permissions
- `StudentService` - Student CRUD, search, filter
- `MarksService` - Marks entry, CGPA calculation

**Usage Pattern**:
```python
auth = AuthService(queries)
if auth.login(username, password):
    auth_service.get_current_user()
```

#### 5. UI Layer

**Responsibility**: Display and interact with user

**Files**:
- `src/ui/base.py` - Base window/frame classes
- `src/ui/components.py` - Reusable UI components
- `src/ui/login_window.py` - Login screen
- `src/ui/registration_window.py` - Registration screen
- `src/ui/admin_panel.py` - Admin dashboard
- `src/ui/student_view.py` - Student details
- `src/ui/marks_view.py` - Marks management
- `src/ui/themes.py` - Theme configuration
- `src/main.py` - Application orchestrator

**Key Classes**:
- `BaseWindow` - Base class for all windows
- `BaseFrame` - Base class for all frames
- `FormEntry`, `FormCombobox`, `FormTextArea` - Input components
- `Application` - Main application orchestrator

**Key Features**:
- Modern ttk widgets
- Grid-based layout
- Consistent theming
- Input validation on UI
- Error dialogs with helpful messages

#### 6. Utilities Layer

**Responsibility**: Provide reusable helper functions

**Files**:
- `src/utils/file_handler.py` - File operations
- `src/utils/image_handler.py` - Image processing
- `src/utils/helpers.py` - General utilities

**Key Classes**:
- `FileHandler` - File upload/download
- `ImageHandler` - Image resizing, format conversion
- Helper functions for dates, calculations

---

## Module Responsibilities

### config/settings.py

```
Database Configuration
  ├── Database path
  ├── Connection parameters
  └── Table names

Application Constants
  ├── User roles (ADMIN, TEACHER, STAFF)
  ├── Student categories
  ├── Session types
  ├── Disability categories
  └── Marital status options

Validation Rules
  ├── Name rules (min/max length)
  ├── Email format
  ├── Phone format
  ├── Password requirements
  ├── AADHAAR format
  ├── Age limits
  └── Marks range
```

### config/ui_config.py

```
Colors
  ├── Primary colors
  ├── Secondary colors
  ├── Error/warning colors
  └── Background colors

Fonts
  ├── Header font
  ├── Body font
  └── Monospace font

Dimensions
  ├── Window sizes
  ├── Button sizes
  └── Padding/spacing

Theme Configuration
  ├── Widget styles
  ├── Color schemes
  └── Visual preferences
```

### database/models.py

```
Data Models
  ├── User
  │   ├── user_id
  │   ├── username
  │   ├── password_hash
  │   ├── role
  │   └── created_at
  │
  ├── Student
  │   ├── Personal info (name, DOB, sex, category)
  │   ├── Contact info (email, phone, address)
  │   ├── Academic info (session, stream, house)
  │   └── Additional info (nationality, disability, etc.)
  │
  ├── ExamMarks
  │   ├── student_id
  │   ├── subject
  │   ├── marks
  │   ├── semester
  │   └── exam_type
  │
  └── Support Models
      ├── BasicInfo
      ├── ContactInfo
      └── AcademicInfo
```

### database/db_manager.py

```
DatabaseManager
  ├── Connection management
  │   ├── Connection pooling
  │   ├── Context managers
  │   └── Error handling
  │
  ├── Database initialization
  │   ├── Table creation
  │   ├── Schema management
  │   └── Constraint setup
  │
  └── Helper methods
      ├── Execute queries
      ├── Execute bulk operations
      └── Table existence checks
```

### database/queries.py

```
DatabaseQueries
  ├── User operations (17 methods)
  │   ├── create_user, get_user, update_user
  │   ├── authenticate, get_all_users
  │   └── Custom user queries
  │
  ├── Student operations (15 methods)
  │   ├── CRUD (Create, Read, Update, Delete)
  │   ├── Search and filter
  │   ├── Count operations
  │   └── Session-based queries
  │
  ├── Marks operations (10 methods)
  │   ├── Add, get, update marks
  │   ├── CGPA calculations
  │   └── Grade-related queries
  │
  ├── Photo operations (6 methods)
  │   ├── Student photo CRUD
  │   ├── Email photo CRUD
  │   └── Photo validation
  │
  └── Utility methods
      ├── Transaction management
      ├── Error handling
      └── Query building
```

### validators/form_validator.py

```
FormValidator (15+ methods)
  ├── Text validation
  │   ├── validate_name (length, characters)
  │   ├── validate_required_field
  │   └── validate_text_area
  │
  ├── Format validation
  │   ├── validate_email (RFC format)
  │   ├── validate_phone (10 digits)
  │   ├── validate_date (DD/MM/YYYY)
  │   └── validate_aadhaar (12 digits)
  │
  ├── Numeric validation
  │   ├── validate_marks (0-100)
  │   ├── validate_percentage (0-100)
  │   ├── validate_gpa (0-10)
  │   └── validate_cgpa (0-10)
  │
  ├── Selection validation
  │   ├── validate_dropdown_selection
  │   └── validate_checkbox
  │
  └── Custom validation
      ├── validate_password (strength)
      ├── validate_date_of_birth (age)
      └── validate_percentage
```

### validators/business_rules.py

```
BusinessRuleValidator (12+ methods)
  ├── Student validation
  │   ├── validate_student_id_unique
  │   ├── validate_student_age_range
  │   ├── validate_duplicate_registration
  │   └── validate_marks_prerequisites
  │
  ├── Address validation
  │   ├── validate_address_fields
  │   ├── validate_nationality_country
  │   └── validate_same_permanent_address
  │
  ├── Academic validation
  │   ├── validate_marks_range
  │   ├── validate_cgpa_calculation
  │   ├── validate_gpa_from_percentage
  │   └── validate_grade_assignment
  │
  └── Special validation
      ├── validate_disability_percentage
      └── validate_category_eligibility
```

### services/auth_service.py

```
AuthService (17+ methods)
  ├── User management
  │   ├── register_user
  │   ├── login
  │   ├── logout
  │   └── change_password
  │
  ├── Session management
  │   ├── is_logged_in
  │   ├── get_current_user
  │   ├── verify_admin_access
  │   └── verify_teacher_access
  │
  ├── Security
  │   ├── hash_password
  │   ├── verify_password
  │   └── generate_session_token
  │
  └── Role-based access
      ├── is_admin
      ├── is_teacher
      ├── is_staff
      └── get_user_role
```

### services/student_service.py

```
StudentService (11+ methods)
  ├── CRUD operations
  │   ├── register_student
  │   ├── get_student
  │   ├── update_student
  │   └── delete_student
  │
  ├── Query operations
  │   ├── search_students
  │   ├── get_all_students
  │   ├── filter_students
  │   └── get_student_count
  │
  ├── Photo operations
  │   ├── add_student_photo
  │   ├── get_student_photo
  │   └── update_student_photo
  │
  └── Session operations
      └── get_students_by_session
```

### services/marks_service.py

```
MarksService (12+ methods)
  ├── Marks operations
  │   ├── add_marks
  │   ├── get_marks
  │   ├── update_marks
  │   └── delete_marks
  │
  ├── Calculation methods
  │   ├── calculate_cgpa
  │   ├── calculate_gpa
  │   ├── get_average_marks
  │   ├── assign_grade_by_percentage
  │   └── get_subject_statistics
  │
  ├── Query methods
  │   ├── get_marks (filtered)
  │   ├── get_best_subject
  │   └── get_worst_subject
  │
  └── Analysis methods
      ├── get_class_average
      └── get_performance_analysis
```

---

## Data Flow

### User Authentication Flow

```
User Input → LoginWindow
    ↓
FormValidator.validate_email() ✓
FormValidator.validate_password() ✓
    ↓
AuthService.login(username, password)
    ↓
DatabaseQueries.get_user_by_username()
    ↓
AuthService.verify_password()
    ↓
AuthService.create_session()
    ↓
Navigate to AdminPanel or appropriate window
```

### Student Registration Flow

```
Registration Form → RegistrationWindow (3 tabs)
    ↓
Tab 1: Personal Info
  ├─ FormValidator.validate_name()
  ├─ FormValidator.validate_date_of_birth()
  ├─ FormValidator.validate_email()
  └─ FormValidator.validate_phone()
    ↓
Tab 2: Contact Info
  ├─ FormValidator.validate_address()
  └─ FormValidator.validate_city()
    ↓
Tab 3: Academic Info
  ├─ FormValidator.validate_dropdown_selection()
  ├─ BusinessRuleValidator.validate_student_id_unique()
  └─ BusinessRuleValidator.validate_duplicate_registration()
    ↓
StudentService.register_student(data)
    ↓
DatabaseQueries.create_student()
    ↓
Student Record Created in Database
```

### Marks Entry & CGPA Calculation Flow

```
Marks Entry Form → MarksWindow
    ↓
FormValidator.validate_marks() ✓
BusinessRuleValidator.validate_marks_range() ✓
    ↓
MarksService.add_marks(marks_data)
    ↓
DatabaseQueries.add_student_marks()
    ↓
MarksService.calculate_cgpa(student_id)
    ↓
MarksService.assign_grade_by_percentage()
    ↓
Update Display with CGPA and Grade
```

### Admin Panel Data Flow

```
AdminPanel Window
    ↓
StudentService.get_all_students()
    ↓
DatabaseQueries.get_all_students()
    ↓
Display in Treeview
    ↓
User action (search/filter/delete)
    ├─ Search: StudentService.search_students()
    ├─ Filter: StudentService.filter_students()
    └─ Delete: StudentService.delete_student()
    ↓
Update Database and Display
```

---

## Design Patterns

### 1. Model-View-Separator Pattern

**Where Applied**: Throughout the architecture

```
Model (Database Layer)
  ├─ DatabaseManager
  ├─ DatabaseQueries
  └─ Models (dataclasses)

Separator (Services Layer)
  ├─ AuthService
  ├─ StudentService
  └─ MarksService

View (UI Layer)
  ├─ Windows (LoginWindow, etc.)
  ├─ Frames (Forms, tables)
  └─ Components (Inputs, dialogs)
```

**Benefit**: Decouples UI from business logic

### 2. Dependency Injection

**Where Applied**: Service classes constructor

```python
class StudentService:
    def __init__(self, queries: DatabaseQueries, auth: AuthService):
        self.queries = queries
        self.auth = auth
```

**Benefit**: Testable, loosely coupled, flexible

### 3. Validation Pipeline

**Where Applied**: Form processing

```
User Input → FormValidator → BusinessRuleValidator → Service → Database
```

**Benefit**: Layered validation, early error detection

### 4. Context Manager Pattern

**Where Applied**: Database connections

```python
with db.get_connection() as conn:
    # Use connection
    # Auto-closes on exit
```

**Benefit**: Safe resource management

### 5. Decorator Pattern

**Where Applied**: UI styling, validation

```python
@apply_theme
def create_button(): pass

@validate_input
def process_form(): pass
```

**Benefit**: Separation of concerns, reusability

### 6. Factory Pattern

**Where Applied**: Service creation

```python
auth = AuthService(queries)
student_svc = StudentService(queries, auth)
marks_svc = MarksService(queries, student_svc)
```

**Benefit**: Centralized object creation

### 7. Observer Pattern

**Where Applied**: UI event binding

```python
button.bind("<Button-1>", self.on_button_click)
entry.bind("<KeyRelease>", self.on_text_changed)
```

**Benefit**: Event-driven UI updates

---

## Dependencies

### Core Dependencies

```
tkinter (built-in)     ← GUI framework
sqlite3 (built-in)     ← Database
dataclasses (built-in) ← Data models
typing (built-in)      ← Type hints
```

### External Dependencies

```
Pillow >= 10.0.0       ← Image processing
tkcalendar >= 1.6.1    ← Date picker widget
Babel >= 2.12.1        ← Internationalization
```

### Development Dependencies

```
pytest >= 7.4.0        ← Testing framework
pytest-cov >= 4.1.0    ← Code coverage
mypy >= 1.5.0          ← Type checking
flake8 >= 6.1.0        ← Linting
pylint >= 2.17.0       ← Code analysis
black >= 23.9.0        ← Code formatting
```

### Dependency Graph

```
UI Layer
  ├─ depends on Services
  ├─ depends on Config
  └─ depends on Utils

Services Layer
  ├─ depends on Database
  ├─ depends on Validators
  └─ depends on Config

Validators Layer
  ├─ depends on Database (for rules)
  └─ depends on Config

Database Layer
  ├─ depends on Models
  └─ depends on Config

Utils Layer
  └─ depends on Config

Config Layer
  └─ no dependencies (foundation)
```

---

## Database Schema

### Users Table

```sql
CREATE TABLE users (
  user_id TEXT PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Fields**:
- `user_id`: Unique identifier
- `username`: Login username
- `password_hash`: SHA256 hashed password
- `role`: ADMIN, TEACHER, or STAFF
- `created_at`: Account creation timestamp

### Students Table

```sql
CREATE TABLE students (
  student_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT,
  phone TEXT,
  dob TEXT,
  sex TEXT,
  category TEXT,
  nationality TEXT,
  address TEXT,
  city TEXT,
  state TEXT,
  country TEXT,
  session TEXT,
  stream TEXT,
  house TEXT,
  disability TEXT,
  disability_percentage REAL,
  marital_status TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
)
```

**Fields**: All student personal, contact, and academic information

### Student Marks Table

```sql
CREATE TABLE student_marks (
  mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id TEXT NOT NULL,
  subject TEXT NOT NULL,
  marks REAL NOT NULL,
  semester TEXT,
  exam_type TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(student_id)
    ON DELETE CASCADE
)
```

**Fields**: Exam marks, subject, semester, exam type

### Additional Tables

- `student_photos` - Student photo storage
- `email_photos` - Email template photos

---

## API Reference

### Key Service Methods

#### AuthService

```python
def login(username: str, password: str) -> bool: ...
def logout() -> None: ...
def is_logged_in() -> bool: ...
def get_current_user() -> User | None: ...
def is_admin() -> bool: ...
def change_password(old_pwd: str, new_pwd: str) -> bool: ...
```

#### StudentService

```python
def register_student(data: dict) -> None: ...
def get_student(student_id: str) -> Student | None: ...
def update_student(student_id: str, data: dict) -> None: ...
def search_students(query: str) -> list[Student]: ...
def filter_students(filters: dict) -> list[Student]: ...
```

#### MarksService

```python
def add_marks(data: dict) -> None: ...
def get_marks(student_id: str) -> list[dict]: ...
def calculate_cgpa(student_id: str) -> float: ...
def assign_grade_by_percentage(percentage: float) -> str: ...
```

#### Validators

```python
def validate_email(email: str) -> str: ...  # raises ValidationError
def validate_date(date_str: str) -> str: ...
def validate_marks(marks: float) -> float: ...
```

---

## Testing Strategy

### Test Coverage

```
Unit Tests
  ├─ Database tests (18 tests)
  ├─ Validator tests (59 tests)
  └─ Service tests (31 tests)

Integration Tests
  ├─ Authentication workflows
  ├─ Student registration workflows
  ├─ Marks management workflows
  └─ Data persistence tests

Overall Coverage: 80%+
Total Tests: 189+
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src

# Run specific test file
pytest tests/test_validators.py

# Run with verbose output
pytest tests/ -v
```

---

## Best Practices Implemented

1. **Type Safety**: All public APIs have type hints
2. **Error Handling**: Custom exceptions with meaningful messages
3. **Code Organization**: Single responsibility per module
4. **DRY Principle**: No code duplication
5. **Testing**: Comprehensive unit and integration tests
6. **Documentation**: Docstrings on all public APIs
7. **PEP 8 Compliance**: Follows Python style guidelines
8. **Configuration Management**: Externalized configuration

---

## Performance Considerations

1. **Database Connection Pooling**: Reuses connections
2. **Query Optimization**: Parameterized queries, proper indexes
3. **UI Responsiveness**: Async operations where needed
4. **Memory Management**: Proper resource cleanup
5. **Search Efficiency**: Optimized search algorithms

---

## Security Considerations

1. **SQL Injection Prevention**: Parameterized queries
2. **Password Security**: SHA256 hashing
3. **Session Management**: Secure token handling
4. **Input Validation**: Multi-layer validation
5. **Error Messages**: No sensitive data leaks

---

## Future Enhancements

1. Database migrations framework
2. API layer (REST/GraphQL)
3. Web UI (Flask/FastAPI)
4. Advanced reporting
5. Data export features
6. Backup and restore
7. Multi-user support
8. Role-based access control refinements

---

**Last Updated**: 2026-06-10  
**Maintainer**: Subhranil Sarkar
