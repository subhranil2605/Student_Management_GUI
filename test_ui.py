"""Test UI rendering without running full application."""

import tkinter as tk
from tkinter import messagebox

from src.ui.themes import setup_ttk_theme
from src.ui.login_window import LoginWindow
from src.database.db_manager import DatabaseManager
from src.database.queries import DatabaseQueries
from src.services.auth_service import AuthService

# Initialize minimal setup
db_manager = DatabaseManager()

queries = DatabaseQueries(db_manager)
auth_service = AuthService(queries)

# Create root window
root = tk.Tk()
root.title("Test UI")
root.geometry("500x400")

# Setup theme
setup_ttk_theme()

# Add test label
import tkinter.ttk as ttk
label = ttk.Label(root, text="Testing UI Components", font=("Arial", 16))
label.pack(pady=20)

# Create test components
from src.ui.components import FormEntry, FormCombobox

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

# Test form entry
entry = FormEntry(frame, "Test Entry", required=True)
entry.pack(fill="x", pady=5)
entry.set("Sample Text")

# Test combobox
combo = FormCombobox(frame, "Test Combo", ["Option 1", "Option 2", "Option 3"])
combo.pack(fill="x", pady=5)

# Test button
def on_click():
    messagebox.showinfo("Success", "UI Components Working!")

button = ttk.Button(frame, text="Test Button", command=on_click)
button.pack(pady=10)

# Close button
close_btn = ttk.Button(frame, text="Close", command=root.quit)
close_btn.pack(pady=5)

print("✓ UI Test window created successfully")
print("Components tested:")
print("  - FormEntry")
print("  - FormCombobox")
print("  - ttk Theme")
print("  - Basic widgets")

# Schedule window close after 2 seconds for automated testing
root.after(2000, root.quit)

try:
    root.mainloop()
    print("\n✓ Test completed successfully - UI is working!")
except Exception as e:
    print(f"\n✗ Error: {e}")
finally:
    db_manager.close()
