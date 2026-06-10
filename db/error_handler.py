import tkinter as tk
from tkinter import messagebox
from release import APP_NAME, RELEASE_DATE


class ErrorHandler:
    DB_INTEGRITY, DB_NOTFOUND, DB_CONSTRAINT = "DB-ERR-001", "DB-ERR-002", "DB-ERR-003"
    INP_MISSING, INP_INVALID, INP_FORMAT = "INP-ERR-001", "INP-ERR-002", "INP-ERR-003"
    BIZ_STATUS, BIZ_AVAIL, BIZ_DATE = "BIZ-ERR-001", "BIZ-ERR-002", "BIZ-ERR-003"

    @staticmethod
    def show_error(code, message, detail=""):
        full_msg = f"{APP_NAME} ({RELEASE_DATE})\n[{code}] {message}"
        if detail:
            full_msg += f"\nDetail: {detail}"
        messagebox.showerror("Error", full_msg)

    @staticmethod
    def db_error(e, context=""):
        err = str(e).lower()
        if "unique" in err or "constraint" in err:
            code, msg = ErrorHandler.DB_CONSTRAINT, "A record with the same unique value already exists."
        elif "no such" in err:
            code, msg = ErrorHandler.DB_NOTFOUND, "The requested data was not found."
        else:
            code, msg = ErrorHandler.DB_INTEGRITY, "A database error occurred."
        ErrorHandler.show_error(code, msg, f"{context}: {e}")
