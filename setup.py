import sys
from cx_Freeze import setup, Executable
import os
import tkinter
import sqlite3
import tkcalendar
import PIL
from tkinter import ttk
from PIL import Image, ImageTk
import babel



os.environ['TCL_LIBRARY'] =r"G:\pyhton3.7\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r'G:\pyhton3.7\tcl\tk8.6'

# GUI applications require a different base on Windows (the default is for a
# console application).

base = None
if sys.platform == "win32":
    base = "Win32GUI"



# Dependencies are automatically detected, but it might need fine tuning.
#build_exe_options = {"packages": ["os", "tkinter"],
                     #"includes": ["tkinter"],
                     #'include_files': [],
                     #'excludes': ['mpl_toolkits']}

includes = ["tkinter"]
excludes = []
packages = ["os", "tkinter"]
path = []
include_files = ['tk86t.dll', 'tcl86t.dll', 'college_image.png', 'background_1.png', 'ico.png']


setup(  name = "Student Management System",
        version = "1.0",
        description = "Developed by Subhranil Sarkar",
        options = {"build_exe": {"includes": includes,
                                            "excludes": excludes,
                                            "include_files": include_files,
                                            "path": path},
                   },
        executables = [Executable("main.py", base=base, icon="icond.ico", targetName="Student Management - KGC.exe")])
