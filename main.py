import os
import sys
import tkinter as tk
from tkinter import ttk
from db import DatabaseManager
from release import RELEASE_DATE, APP_NAME
from ui import NexusTheme, HelpPopup, RoomsFrame, CustomersFrame, BookingFrame, CheckoutFrame, BillingFrame


class HotelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} – {RELEASE_DATE}")
        self.geometry("1200x750")
        self.configure(bg=NexusTheme.BG)
        self.set_icon()
        NexusTheme.apply()
        self.db = DatabaseManager()
        self.sidebar = tk.Frame(self, bg=NexusTheme.SIDEBAR_BG, width=200, highlightbackground=NexusTheme.BORDER, highlightthickness=1)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar, text="NEXUS", bg=NexusTheme.SIDEBAR_BG, fg=NexusTheme.ACCENT, font=("Segoe UI", 18, "bold")).pack(pady=25)
        for text, cmd in [("Rooms", self.show_rooms), ("Customers", self.show_customers), ("Booking", self.show_booking), ("Checkout", self.show_checkout), ("Billing", self.show_billing), ("Help", self.show_help), ("Exit", self.quit)]:
            ttk.Button(self.sidebar, text=text, command=cmd, style="Sidebar.TButton").pack(pady=4, padx=15, fill="x")
        self.main_container = tk.Frame(self, bg=NexusTheme.BG)
        self.main_container.pack(side="right", expand=True, fill="both")
        self.frames = {}
        for F in (RoomsFrame, CustomersFrame, BookingFrame, CheckoutFrame, BillingFrame):
            frame = F(parent=self.main_container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.show_rooms()

    def set_icon(self):
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)
        icon_path = os.path.join(base_path, "resources", "app", "TitleBarIcon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(default=icon_path)
        else:
            print("Icon file not found:", icon_path)

    def show_frame(self, frame_name):
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()
            hasattr(frame, "refresh") and frame.refresh()

    def show_rooms(self):
        self.show_frame("RoomsFrame")

    def show_customers(self):
        self.show_frame("CustomersFrame")

    def show_booking(self):
        self.show_frame("BookingFrame")

    def show_checkout(self):
        self.show_frame("CheckoutFrame")

    def show_billing(self):
        self.show_frame("BillingFrame")

    def show_help(self):
        HelpPopup(self)


if __name__ == "__main__":
    HotelApp().mainloop()
