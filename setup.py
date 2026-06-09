"""Setup configuration for Student Management GUI."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="student-management-gui",
    version="2.0.0",
    description="A modern, modular student management GUI application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Subhranil Sarkar",
    author_email="manaspratim122@gmail.com",
    url="https://github.com/username/student_management_gui",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=10.0.0",
        "tkcalendar>=1.6.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "mypy>=1.5.0",
            "flake8>=6.1.0",
            "pylint>=2.17.0",
            "black>=23.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "student-gui=src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
