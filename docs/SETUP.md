# Setup & Installation Guide - Student Management GUI

**Version**: 1.0.0  
**Date**: 2026-06-10  
**Status**: Complete

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Running Tests](#running-tests)
6. [Development Setup](#development-setup)
7. [Troubleshooting](#troubleshooting)
8. [Project Structure](#project-structure)

---

## System Requirements

### Minimum Requirements

- **Python**: 3.7 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 512 MB minimum
- **Disk Space**: 100 MB for application and dependencies
- **Display**: 1024x768 minimum resolution

### Recommended Requirements

- **Python**: 3.10 or higher
- **RAM**: 2 GB
- **CPU**: Modern multi-core processor
- **Display**: 1920x1080 or higher

### Supported Platforms

- **Windows 10/11**
- **macOS 10.15+**
- **Ubuntu 18.04+**
- **Debian 10+**
- **Other Linux distributions** (with Python 3.7+)

---

## Installation

### Option 1: Using uv (Recommended)

#### Prerequisites

- [uv](https://github.com/astral-sh/uv) installed
- Python 3.7+ available

#### Steps

```bash
# 1. Navigate to project directory
cd student_management_gui

# 2. Install dependencies using uv
uv sync

# 3. Verify installation
uv run python -m pytest tests/ -v

# 4. Run the application
uv run python main.py
```

### Option 2: Using pip with Virtual Environment

#### Steps

```bash
# 1. Navigate to project directory
cd student_management_gui

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installation
python -m pytest tests/ -v

# 6. Run the application
python main.py
```

### Option 3: Using pip (Global Installation)

#### Steps

```bash
# 1. Navigate to project directory
cd student_management_gui

# 2. Install dependencies globally
pip install -r requirements.txt

# 3. Run the application
python main.py
```

#### ⚠️ Warning
Global installation may cause version conflicts. Virtual environment recommended.

---

## Configuration

### Default Configuration

The application uses sensible defaults. No configuration required for basic usage.

**Configuration Files**:
- `src/config/settings.py` - Application constants and settings
- `src/config/ui_config.py` - UI theme and styling

### Database Configuration

#### Default Database Location

- **Windows**: `C:\Users\<username>\AppData\Local\student_gui\app.db`
- **macOS**: `~/Library/Application Support/student_gui/app.db`
- **Linux**: `~/.local/share/student_gui/app.db`

#### Custom Database Location

Modify `src/config/settings.py`:

```python
# Change this line:
DB_PATH = str(Path.home() / ".student_gui" / "app.db")

# To your desired path:
DB_PATH = "/path/to/your/database.db"
```

### UI Theme Configuration

Edit `src/config/ui_config.py` to customize:

```python
# Colors
COLORS = {
    'primary': '#007ACC',      # Change primary color
    'background': '#FFFFFF',   # Change background
    'error': '#D32F2F',        # Change error color
}

# Fonts
FONTS = {
    'header': ('Arial', 14, 'bold'),
    'body': ('Arial', 10),
}

# Window dimensions
WINDOW_WIDTH = 1200      # Customize width
WINDOW_HEIGHT = 800      # Customize height
```

### User Roles Configuration

Edit `src/config/settings.py`:

```python
ROLES = {
    'ADMIN': 'Admin',      # Full access
    'TEACHER': 'Teacher',  # Student management
    'STAFF': 'Staff',      # Limited access
}
```

---

## Running the Application

### Starting the Application

#### Using uv

```bash
uv run python main.py
```

#### Using Virtual Environment

```bash
# Activate virtual environment first
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Run application
python main.py
```

### First Run

On first run, the application will:

1. Create database file at configured location
2. Initialize database schema
3. Create initial tables (users, students, marks, etc.)
4. Display login screen

### Initial Login

**Default Admin Credentials** (if seed data exists):

```
Username: admin
Password: (set during setup)
```

⚠️ **Security Note**: Change admin password immediately after first login.

### Application Usage

1. **Login Screen**: Enter credentials and click "Login"
2. **Admin Panel**: View, search, and manage students
3. **Registration**: Add new students to system
4. **Marks Entry**: Record student exam marks
5. **Student Details**: View and update student information
6. **Logout**: Click logout to end session

---

## Running Tests

### All Tests

```bash
# Using uv
uv run pytest tests/ -v

# Using pip (with activated venv)
pytest tests/ -v
```

### Specific Test Categories

```bash
# Database tests only
pytest tests/test_database.py -v

# Validator tests only
pytest tests/test_validators.py -v

# Service tests only
pytest tests/test_services.py -v

# Integration tests only
pytest tests/test_integration.py -v

# Utility tests only
pytest tests/test_utils.py -v
```

### With Code Coverage

```bash
# Generate coverage report
pytest tests/ --cov=src --cov-report=html

# View HTML report
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
```

### Test Results

Expected output:
```
======================== 189 passed in 0.17s ========================
```

### Individual Test Functions

```bash
# Run specific test
pytest tests/test_validators.py::TestFormValidator::test_validate_email_valid -v

# Run tests matching pattern
pytest tests/ -k "test_validate_email" -v
```

---

## Development Setup

### Development Tools Installation

The project includes development tools. Install with:

```bash
# Using uv
uv sync

# Using pip
pip install -r requirements.txt
```

### Available Tools

1. **pytest** - Test framework
2. **pytest-cov** - Code coverage
3. **mypy** - Type checking
4. **flake8** - Linting
5. **pylint** - Code analysis
6. **black** - Code formatting

### Code Quality Checks

#### Type Checking with mypy

```bash
# Check all Python files
mypy src/ tests/

# Check specific file
mypy src/services/auth_service.py
```

#### Linting with flake8

```bash
# Check all Python files
flake8 src/ tests/ --max-line-length=100

# Check specific directory
flake8 src/database/

# Generate report with statistics
flake8 src/ --statistics --count
```

#### Code Analysis with pylint

```bash
# Analyze all modules
pylint src/

# Analyze specific module
pylint src/database/queries.py
```

#### Code Formatting with black

```bash
# Format all files
black src/ tests/

# Format specific file
black src/utils/helpers.py

# Check without modifying (dry-run)
black --check src/ tests/
```

### IDE Setup

#### VS Code

1. **Install Python Extension**
   - Search: "Python" by Microsoft
   - Install and reload

2. **Configure Python Interpreter**
   - Press Cmd/Ctrl + Shift + P
   - Search: "Python: Select Interpreter"
   - Choose venv interpreter

3. **Install Pylance** (recommended)
   - Better type checking and autocomplete

4. **Create `.vscode/settings.json`**
   ```json
   {
     "python.linting.enabled": true,
     "python.linting.flake8Enabled": true,
     "python.linting.mypyEnabled": true,
     "python.formatting.provider": "black",
     "python.testing.pytestEnabled": true,
     "python.testing.pytestArgs": ["tests"]
   }
   ```

#### PyCharm

1. **Configure Project Interpreter**
   - File → Settings → Project → Python Interpreter
   - Select venv interpreter

2. **Enable Code Quality Tools**
   - Settings → Tools → Python Integrated Tools
   - Set pytest as default test runner

3. **Run Tests**
   - Right-click test file → Run Pytest

#### Vim/Neovim

See `docs/IDE_SETUP.md` for detailed Vim configuration.

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tkinter'"

**Solution**:

```bash
# macOS
brew install python-tk

# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# Windows
# Reinstall Python, ensure "tcl/tk and IDLE" is checked
```

### Issue: "Database file not found"

**Solution**:

1. Check configured path in `src/config/settings.py`
2. Ensure directory exists:
   ```bash
   mkdir -p ~/.student_gui
   ```
3. Application will create database on first run

### Issue: "Permission denied" when accessing database

**Solution**:

```bash
# Linux/macOS: Fix file permissions
chmod 644 ~/.student_gui/app.db
chmod 755 ~/.student_gui/

# Or run application with appropriate permissions
sudo python main.py  # Not recommended long-term
```

### Issue: "ImportError" on startup

**Solution**:

```bash
# Verify virtual environment is activated
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete
```

### Issue: Tests fail with "DatabaseError"

**Solution**:

1. Clean test database:
   ```bash
   # Tests use temporary databases, no action needed
   # But if persistent issue:
   rm -rf /tmp/test_*.db
   ```

2. Reset test fixtures:
   ```bash
   pytest tests/ --fixtures  # Check fixture setup
   ```

### Issue: UI appears broken or misaligned

**Solution**:

1. Check minimum window size:
   - Resize window to at least 1024x768
   - Restart application

2. Reset UI configuration:
   - Edit `src/config/ui_config.py`
   - Restore default values

3. Try different theme:
   - Modify `THEME` in `ui_config.py`

### Issue: Performance is slow

**Solution**:

1. Check system resources:
   ```bash
   # macOS
   top -stats pid,command,%cpu,%mem
   
   # Linux
   top
   ```

2. Optimize database:
   ```python
   # In Python shell
   import src.database.db_manager as db
   manager = db.DatabaseManager()
   manager.optimize_database()
   ```

3. Clear old data:
   - Use Admin Panel → Settings → Cleanup

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid credentials" | Wrong password | Verify credentials |
| "Student ID exists" | Duplicate ID | Use unique ID |
| "Invalid email format" | Email format | Use valid email |
| "Database locked" | Concurrent access | Wait and retry |
| "Connection refused" | Database not running | Restart app |

---

## Project Structure

### Directory Layout

```
student_management_gui/
├── src/                           # Source code
│   ├── __init__.py
│   ├── main.py                   # Application entry point
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py           # App constants
│   │   └── ui_config.py          # UI configuration
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db_manager.py         # Connection pooling
│   │   ├── models.py             # Data models
│   │   └── queries.py            # CRUD operations
│   │
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── form_validator.py     # Field validation
│   │   └── business_rules.py     # Business logic
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py       # Authentication
│   │   ├── student_service.py    # Student management
│   │   └── marks_service.py      # Marks management
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── base.py               # Base classes
│   │   ├── components.py         # UI components
│   │   ├── login_window.py       # Login screen
│   │   ├── registration_window.py
│   │   ├── admin_panel.py        # Admin dashboard
│   │   ├── student_view.py       # Student details
│   │   ├── marks_view.py         # Marks management
│   │   ├── themes.py             # Theme config
│   │   └── dialogs.py            # Dialog windows
│   │
│   └── utils/
│       ├── __init__.py
│       ├── file_handler.py       # File operations
│       ├── image_handler.py      # Image processing
│       └── helpers.py            # Utilities
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration
│   ├── test_database.py         # DB tests
│   ├── test_validators.py       # Validator tests
│   ├── test_services.py         # Service tests
│   ├── test_integration.py      # Integration tests
│   ├── test_utils.py            # Utility tests
│   └── fixtures/                # Test fixtures
│
├── docs/                        # Documentation
│   ├── SETUP.md                # This file
│   ├── ARCHITECTURE.md          # System design
│   └── API.md                   # API reference
│
├── dev_docs/                    # Development docs
│   ├── IMPLEMENTATION_PLAN.md
│   ├── TODO.md
│   └── implementation_summary/
│
├── main.py                      # Application launcher
├── requirements.txt             # Dependencies
├── pyproject.toml              # Project config
├── setup.py                    # Setup script
├── README.md                   # Project README
├── .gitignore                  # Git ignore rules
└── .env.example                # Environment template
```

### Key Files

| File | Purpose |
|------|---------|
| `main.py` | Application entry point |
| `src/main.py` | Application orchestrator |
| `src/config/settings.py` | Application constants |
| `src/config/ui_config.py` | UI configuration |
| `requirements.txt` | Pip dependencies |
| `pyproject.toml` | Project metadata |
| `README.md` | Project overview |

---

## Environment Variables

### Optional Configuration

Create `.env` file in project root:

```bash
# Database configuration
DATABASE_PATH=/custom/path/app.db

# Debug mode (1 = enabled, 0 = disabled)
DEBUG=0

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# UI configuration
THEME=default
WINDOW_WIDTH=1200
WINDOW_HEIGHT=800
```

Then in code:

```python
import os
db_path = os.getenv('DATABASE_PATH', default_path)
debug = os.getenv('DEBUG', '0') == '1'
```

---

## Docker Setup (Optional)

Create `Dockerfile`:

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

---

## Upgrade & Maintenance

### Update Dependencies

```bash
# Using uv
uv pip install --upgrade -r requirements.txt

# Using pip
pip install --upgrade -r requirements.txt
```

### Check for Outdated Packages

```bash
# Using uv
uv pip list --outdated

# Using pip
pip list --outdated
```

### Uninstall Application

```bash
# Using uv
rm -rf .venv

# Using pip
deactivate
rm -rf venv

# Remove database (optional)
rm -rf ~/.student_gui/
```

---

## Next Steps

1. **Learn the Application**
   - Read [README.md](../README.md)
   - Review [ARCHITECTURE.md](./ARCHITECTURE.md)

2. **Start Using It**
   - Run: `python main.py`
   - Login with default credentials
   - Explore features

3. **Develop Further**
   - Review code structure
   - Read [API.md](./API.md)
   - Check `docs/` for more details

4. **Run Tests**
   - Execute: `pytest tests/ -v`
   - Verify all pass

---

## Support & Help

### Documentation

- **ARCHITECTURE.md** - System design and modules
- **API.md** - API reference and examples
- **README.md** - Project overview
- **TODO.md** - Development tasks

### Common Issues

See [Troubleshooting](#troubleshooting) section above.

### Getting Help

1. Check documentation first
2. Review test cases for examples
3. Check GitHub issues
4. Review code comments

---

**Last Updated**: 2026-06-10  
**Maintainer**: Subhranil Sarkar  
**Version**: 1.0.0
