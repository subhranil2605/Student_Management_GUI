# Student Management GUI

A modern, modular student management system with a graphical user interface built with Python and Tkinter.

## Overview

This application is a refactored and modernized version of the original monolithic student management system. It features:

- **Modern Architecture**: Separated concerns with config, database, validators, services, and UI layers
- **Modular Design**: 20+ focused modules instead of one 5200-line file
- **Modern Tkinter**: Uses ttk widgets and best practices instead of classic Tk
- **Type Hints**: 100% type annotations on public APIs for better IDE support
- **Comprehensive Tests**: 80%+ test coverage with 189+ passing tests
- **Professional Code**: Follows PEP 8, proper documentation, and clean architecture patterns
- **Production Ready**: Enterprise-grade codebase with security, performance, and reliability

## Project Structure

```
student_management_gui/
├── src/
│   ├── config/          # Configuration and constants
│   ├── database/        # Data access layer
│   ├── validators/      # Input validation logic
│   ├── services/        # Business logic
│   ├── ui/              # User interface components
│   ├── utils/           # Utility functions
│   └── main.py          # Application entry point
├── tests/               # Comprehensive test suite
├── docs/                # Documentation
├── requirements.txt     # Python dependencies
└── setup.py            # Package configuration
```

## Features

### User Management
- User authentication and login
- Role-based access control
- Session management

### Student Management
- Student registration with comprehensive forms
- Student information search and filtering
- Profile management with photo upload
- Complete student history tracking

### Academic Records
- Marks entry and management
- CGPA calculation
- Academic performance tracking
- Grade distribution analysis

### Data Management
- SQLite database with proper schema
- Data validation and integrity checks
- Backup and recovery capabilities

## Installation

### Prerequisites
- Python 3.8.1+ (3.10+ recommended)
- pip or uv package manager
- 512 MB RAM minimum (2 GB recommended)
- 100 MB disk space

### Quick Start (with uv - Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/username/student_management_gui.git
cd student_management_gui

# 2. Install dependencies
uv sync

# 3. Run the application
uv run python main.py
```

### Alternative: Using pip with Virtual Environment

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python main.py
```

### System-Specific Setup

**macOS** (if tkinter is missing):
```bash
brew install python-tk
```

**Ubuntu/Debian**:
```bash
sudo apt-get install python3-tk
```

**Fedora/RHEL**:
```bash
sudo dnf install python3-tkinter
```

## Development Setup

### Install development dependencies
```bash
uv pip install -e ".[dev]"
```

### Run tests
```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Code quality checks
```bash
# Linting
flake8 src tests

# Type checking
mypy src

# Code formatting
black src tests --check
```

## Configuration

### Database
- Default location: `student_mgt.db` (SQLite)
- Auto-initialized on first run
- Schema: See `docs/ARCHITECTURE.md` for details

### UI Settings
- Colors, fonts, and layout settings: `src/config/ui_config.py`
- Application constants: `src/config/settings.py`
- File upload directory: `student_photo/`

## Architecture

The application follows a layered, clean architecture with 6 distinct layers:

```
┌─────────────────────────────────────────────────────┐
│           User Interface Layer (UI)                 │
│  LoginWindow │ Registration │ AdminPanel │ Themes   │
└──────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│         Services Layer (Business Logic)              │
│  AuthService │ StudentService │ MarksService         │
└──────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│      Validators Layer (Input Validation)             │
│  FormValidator │ BusinessRuleValidator               │
└──────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│       Database Layer (Data Access)                   │
│  DatabaseManager │ DatabaseQueries │ Models          │
└──────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│     Utilities Layer (Helpers & Infrastructure)       │
│  FileHandler │ ImageHandler │ Helpers                │
└──────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│       Configuration Layer (Settings & Constants)     │
│  settings.py │ ui_config.py                          │
└──────────────────────────────────────────────────────┘
```

### Core Design Principles
- **Separation of Concerns**: Each module has single, well-defined responsibility
- **Dependency Injection**: Services receive dependencies through constructors
- **Type Safety**: 100% type hints on public APIs with dataclass models
- **Testability**: All logic easily testable in isolation with clear boundaries
- **Reusability**: Components can be reused across application without coupling
- **Error Handling**: Custom exceptions with meaningful error messages
- **Configuration Externalization**: All hardcoded values in config modules

### Design Patterns Used
1. **Model-View-Separator** - Decouples UI from business logic
2. **Dependency Injection** - Services receive dependencies in constructors
3. **Validation Pipeline** - Multi-layer validation (Form → Business → Service → DB)
4. **Context Manager** - Safe database connection management
5. **Decorator** - UI styling and validation decoration
6. **Factory** - Centralized service object creation
7. **Observer** - Event-driven UI updates

## Database Schema

See `docs/ARCHITECTURE.md` for complete schema documentation.

### Main Tables
- `users`: User accounts and authentication
- `student_information`: Student profiles and personal details
- `student_marks`: Academic marks and grades
- `user_sessions`: Session management

## Testing

### Test Coverage
- Unit tests for validators: 95%+
- Unit tests for database: 90%+
- Unit tests for services: 85%+
- Integration tests: Full workflows
- Overall target: 80%+

### Running Tests
```bash
# All tests
pytest

# With coverage report
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/test_validators.py -v

# Specific test
pytest tests/test_validators.py::TestFormValidator::test_validate_name -v
```

## Documentation

- **[docs/SETUP.md](docs/SETUP.md)**: Comprehensive installation and configuration guide
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**: Complete system design, modules, data flow, and design patterns
- **[docs/API.md](docs/API.md)**: Full API reference with code examples
- **[dev_docs/IMPLEMENTATION_PLAN.md](dev_docs/IMPLEMENTATION_PLAN.md)**: Implementation strategy and roadmap
- **[dev_docs/TODO.md](dev_docs/TODO.md)**: Development tasks and checklist

## Performance & Security

### Performance Features
- **Database Connection Pooling**: Reuses connections for efficiency
- **Query Optimization**: Parameterized queries with proper indexes
- **UI Responsiveness**: Async operations where needed
- **Memory Management**: Proper resource cleanup and garbage collection
- **Search Efficiency**: Optimized search algorithms

### Security Features
- **SQL Injection Prevention**: All queries use parameterized statements
- **Password Security**: SHA256 hashing with strong password validation
- **Session Management**: Secure token handling for user sessions
- **Multi-Layer Validation**: Input validation at UI, service, and database levels
- **Error Handling**: No sensitive data leaks in error messages
- **Role-Based Access Control**: Admin, Teacher, and Staff roles with appropriate permissions

## Deployment

### Creating Executable (Optional)
```bash
# Using PyInstaller
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

### Docker Deployment
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t student-gui .
docker run -it student-gui
```

## Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'tkinter'**
```bash
# macOS: brew install python-tk
# Ubuntu: sudo apt-get install python3-tk
# Fedora: sudo dnf install python3-tkinter
```

**Database File Not Found**
- Check configured path in `src/config/settings.py`
- Ensure directory exists and has write permissions
- Application creates database on first run

**Import Errors**
- Verify you're in project root directory
- Activate virtual environment: `source venv/bin/activate`
- Clear cache: `find . -type d -name __pycache__ -exec rm -rf {} +`

**Permission Denied (Database)**
```bash
# Fix permissions on Linux/macOS
chmod 644 ~/.student_gui/app.db
chmod 755 ~/.student_gui/
```

**Slow Performance**
- Check system resources with `top` or `Activity Monitor`
- Verify database isn't locked (close other instances)
- Clear old data using Admin Panel cleanup

**Tests Failing**
- Tests use temporary databases automatically
- Clear cache: `find . -name "*.pyc" -delete`
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

See [docs/SETUP.md](docs/SETUP.md) Troubleshooting section for detailed solutions.

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Follow PEP 8 style guide
3. Add type hints to all functions
4. Write tests for new functionality
5. Update documentation
6. Submit pull request

## License

MIT License - See LICENSE file for details

## Author

**Subhranil Sarkar**
- Email: manaspratim122@gmail.com
- GitHub: [@sarkar-subhranil](https://github.com/sarkar-subhranil)

## Key Features in Detail

### User Management & Authentication
- User login with secure password hashing (SHA256)
- Role-based access control (Admin, Teacher, Staff)
- Session management with secure token handling
- Password strength validation and change functionality
- User account creation and management

### Student Management
- Complete student registration with 3-tab form
- Personal information capture (name, DOB, contact, address)
- Academic information tracking (session, stream, house)
- Photo upload and storage with image processing
- Advanced search and filtering capabilities
- Student profile viewing and editing
- Bulk student management from admin panel

### Academic Records
- Marks entry and management
- Automatic CGPA calculation
- GPA computation per semester
- Grade assignment based on percentage
- Subject-wise performance analysis
- Best/worst subject identification
- Class average and performance statistics
- Support for multiple exam types (Midterm, Final, etc.)

### Data Management
- SQLite database with proper schema
- Data validation at multiple levels (form, business logic, database)
- Referential integrity with foreign keys
- Transaction support for data consistency
- Backup and recovery capabilities
- Efficient indexing for fast queries

## Changelog

### Version 2.0.0 (Current - Phase 1-10 Complete)
- **Infrastructure & Configuration** (Phase 1-2): Config system and constants
- **Database Layer** (Phase 3): Complete database abstraction
- **Validators & Services** (Phase 4-5): Input validation and business logic
- **Modern UI** (Phase 6): ttk widgets and modern interface
- **Utilities** (Phase 7): Helper functions with TDD approach
- **Testing** (Phase 8): Comprehensive unit and integration tests
- **Documentation** (Phase 9-10): Complete architecture and API docs
- **Refactoring**: Modular architecture with 20+ focused modules
- **Type Safety**: 100% type hints on public APIs
- **Code Quality**: 80%+ test coverage with 189+ passing tests

### Version 1.0.0
- Initial monolithic application (5200 lines)
- Basic student management features
- Classic Tk GUI
- Limited documentation

## Module Overview

### Core Modules

| Module | Responsibility | Key Classes |
|--------|----------------|-------------|
| **config/settings.py** | Application constants and rules | DB_PATH, ROLES, VALIDATION_RULES |
| **config/ui_config.py** | UI theme, colors, fonts, dimensions | COLORS, FONTS, SIZES, PADDING |
| **database/db_manager.py** | Connection pooling, initialization | DatabaseManager |
| **database/models.py** | Data models with type safety | User, Student, ExamMarks |
| **database/queries.py** | CRUD operations (40+ methods) | DatabaseQueries |
| **validators/form_validator.py** | Field validation (15+ methods) | FormValidator |
| **validators/business_rules.py** | Business rule validation | BusinessRuleValidator |
| **services/auth_service.py** | Authentication & sessions | AuthService |
| **services/student_service.py** | Student management | StudentService |
| **services/marks_service.py** | Marks & academic records | MarksService |
| **ui/base.py** | Base window and frame classes | BaseWindow, BaseFrame |
| **ui/components.py** | Reusable form components | FormEntry, FormCombobox, TableFrame |
| **ui/login_window.py** | Login screen | LoginWindow |
| **ui/registration_window.py** | Student registration (3 tabs) | RegistrationWindow |
| **ui/admin_panel.py** | Admin dashboard | AdminPanel |
| **ui/student_view.py** | Student details view | StudentView |
| **ui/marks_view.py** | Marks management | MarksView |
| **ui/themes.py** | Theme configuration | Theme |
| **utils/file_handler.py** | File operations | FileHandler |
| **utils/image_handler.py** | Image processing | ImageHandler |
| **utils/helpers.py** | General utilities | Helper functions |

## API Usage Examples

### Login Flow
```python
from src.services.auth_service import AuthService
from src.database.db_manager import DatabaseManager
from src.database.queries import DatabaseQueries

db = DatabaseManager("app.db")
queries = DatabaseQueries(db)
auth = AuthService(queries)

if auth.login("admin", "password123"):
    user = auth.get_current_user()
    print(f"Welcome {user.username}!")
```

### Student Registration
```python
from src.services.student_service import StudentService
from src.validators.form_validator import FormValidator, ValidationError

validator = FormValidator()
student_service = StudentService(queries, auth)

try:
    name = validator.validate_name("John Doe")
    email = validator.validate_email("john@example.com")
    phone = validator.validate_phone("9876543210")
    
    student_service.register_student({
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
    })
except ValidationError as e:
    print(f"Error: {e}")
```

### Marks Management
```python
from src.services.marks_service import MarksService

marks_service = MarksService(queries, student_service)

# Add marks
marks_service.add_marks({
    "student_id": "STU001",
    "subject": "Mathematics",
    "marks": 85,
    "semester": "Sem-I",
    "exam_type": "Final"
})

# Calculate CGPA
cgpa = marks_service.calculate_cgpa("STU001")
print(f"CGPA: {cgpa:.2f}")

# Get grade
grade = marks_service.assign_grade_by_percentage(85)
print(f"Grade: {grade}")
```

## Best Practices Implemented

✅ **Type Safety** - 100% type hints on public APIs with dataclass models  
✅ **Error Handling** - Custom exceptions with meaningful messages  
✅ **Code Organization** - Single responsibility per module  
✅ **DRY Principle** - No code duplication across modules  
✅ **Testing** - 189+ tests with 80%+ coverage  
✅ **Documentation** - Docstrings on all public APIs  
✅ **PEP 8 Compliance** - Follows Python style guidelines  
✅ **Configuration Management** - Externalized, environment-specific config  
✅ **SQL Injection Prevention** - Parameterized queries throughout  
✅ **Password Security** - SHA256 hashing with strength validation  

## Technology Stack

### Core Technologies
- **Language**: Python 3.7+
- **GUI**: Tkinter (ttk widgets)
- **Database**: SQLite3
- **Type Checking**: Type hints with mypy support

### Key Dependencies
- **Pillow** (≥10.0.0) - Image processing
- **tkcalendar** (≥1.6.1) - Date picker widget
- **Babel** (≥2.12.1) - Internationalization

### Development Tools
- **pytest** (≥7.4.0) - Testing framework
- **pytest-cov** (≥4.1.0) - Code coverage
- **mypy** (≥1.5.0) - Type checking
- **flake8** (≥6.1.0) - Linting
- **pylint** (≥2.17.0) - Code analysis
- **black** (≥23.9.0) - Code formatting

## Acknowledgments

This refactoring follows industry best practices and modern Python design patterns, transforming the original 5200-line monolithic application into a maintainable, testable, and professional codebase.

The project implements:
- Clean Architecture principles
- SOLID design principles
- Enterprise-grade code quality
- Comprehensive documentation
- Professional testing practices

---

**Status**: Phase 1-10 Complete (All Core Implementation Done)  
**Last Updated**: 2026-06-10  
**Maintainer**: Subhranil Sarkar  
**Version**: 2.0.0

## Screenshots

1. Starting Window of the UI
![01](ss/01.png)

2. Students' Zone
![02](ss/02.png)

3. Register a New Student
![03](ss/03.png)

4. Page 1
![04](ss/04.png)

5. Page 2
![05](ss/05.png)

6. Page 3
![06](ss/06.png)

7. Login Window for the Admin
![07](ss/07.png)

8. Select Session to show the students
![08](ss/08.png)

9. Lists the students
![09](ss/09.png)
