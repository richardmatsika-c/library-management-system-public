# main.py
# ─────────────────────────────────────────────────────────────────────────────
# Application Entry Point
# ─────────────────────────────────────────────────────────────────────────────

# from gui import LibraryApp
from morden_gui import ModernLibraryApp

if __name__ == "__main__":
    app = ModernLibraryApp()
    app.mainloop()
