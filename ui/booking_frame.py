import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from ui import NexusTheme, BaseFrame
from models import Room, Customer, Booking
from db import ErrorHandler

class BookingFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        tk.Label(self, text="Booking Management", bg=NexusTheme.BG, fg=NexusTheme.ACCENT, font=NexusTheme.HEADING_FONT).pack(pady=10)
        self.create_search_bar(self)
        input_frame = tk.Frame(self, bg=NexusTheme.BG)
        input_frame.pack(pady=10)
        labels = ["Customer", "Room", "Check-in (YYYY-MM-DD)", "Check-out (YYYY-MM-DD)"]
        for i, text in enumerate(labels):
            tk.Label(input_frame, text=text, bg=NexusTheme.BG, fg=NexusTheme.FG, font=NexusTheme.FONT).grid(row=0, column=i * 2, padx=5, sticky="e")
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(input_frame, textvariable=self.customer_var, state="readonly", width=22)
        self.customer_combo.grid(row=0, column=1, padx=5)
        self.room_var = tk.StringVar()
        self.room_combo = ttk.Combobox(input_frame, textvariable=self.room_var, state="readonly", width=12)
        self.room_combo.grid(row=0, column=3, padx=5)
        self.checkin_entry = ttk.Entry(input_frame, width=12)
        self.checkin_entry.grid(row=0, column=5, padx=5)
        self.checkout_entry = ttk.Entry(input_frame, width=12)
        self.checkout_entry.grid(row=0, column=7, padx=5)
        btn_frame = tk.Frame(self, bg=NexusTheme.BG)
        btn_frame.pack(pady=5)
        for idx, (txt, cmd) in enumerate([("BOOK", self.create_booking), ("CHECK-IN", self.checkin_booking), ("VOID", self.cancel_booking)]):
            tk.Button(btn_frame, text=txt, command=cmd, bg=NexusTheme.DARK, fg=NexusTheme.FG, activebackground=NexusTheme.ACCENT, activeforeground="#FFFFFF", font=NexusTheme.FONT_BOLD, relief="flat", padx=12).grid(row=0, column=idx, padx=3)
        self.tree = self.create_tree(("ID", "Customer", "Room", "Check-in", "Check-out", "Status"), ("ID", "Customer", "Room", "Check-in", "Check-out", "Status"))

    def populate_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.filtered_data:
            self.tree.insert("", "end", values=row)

    def refresh(self):
        customers = Customer.get_all()
        self.customer_combo["values"] = [f"{c[0]} - {c[1]}" for c in customers] if customers else []
        rooms = Room.get_available()
        self.room_combo["values"] = [f"{r[0]} - {r[1]} ({r[2]})" for r in rooms] if rooms else []
        self.all_data = Booking.get_all() or []
        self.apply_filter_sort()

    def create_booking(self):
        cust_str, room_str, checkin, checkout = self.customer_combo.get(), self.room_combo.get(), self.checkin_entry.get(), self.checkout_entry.get()
        if not cust_str or not room_str or not checkin or not checkout:
            return ErrorHandler.show_error(ErrorHandler.INP_MISSING, "All fields required.")
        try:
            cust_id = int(cust_str.split(" - ")[0])
            room_id = int(room_str.split(" - ")[0])
        except:
            return ErrorHandler.show_error(ErrorHandler.INP_FORMAT, "Select valid customer and room.")
        try:
            ci = datetime.strptime(checkin, "%Y-%m-%d")
            co = datetime.strptime(checkout, "%Y-%m-%d")
            if co <= ci:
                raise ValueError
        except ValueError:
            return ErrorHandler.show_error(ErrorHandler.INP_FORMAT, "Invalid dates. Use YYYY-MM-DD, checkout after checkin.")
        if Booking.create(cust_id, room_id, checkin, checkout):
            messagebox.showinfo("Success", "Booking created.")
            self.refresh()
            self.customer_combo.set(""), self.room_combo.set(), self.checkin_entry.delete(0, "end"), self.checkout_entry.delete(0, "end")

    def checkin_booking(self):
        sel = self.tree.focus()
        if not sel:
            return ErrorHandler.show_error(ErrorHandler.INP_MISSING, "Select a booking.")
        vals = self.tree.item(sel)["values"]
        if vals[5] != "reserved":
            return ErrorHandler.show_error(ErrorHandler.BIZ_STATUS, "Only 'reserved' bookings can check in.")
        if Booking.checkin(vals[0]):
            messagebox.showinfo("Success", "Guest checked in. Status: in_house"), self.refresh()

    def cancel_booking(self):
        sel = self.tree.focus()
        if not sel:
            return ErrorHandler.show_error(ErrorHandler.INP_MISSING, "Select a booking.")
        if messagebox.askyesno("Confirm", "Void this booking?") and Booking.cancel(self.tree.item(sel)["values"][0]):
            messagebox.showinfo("Success", "Booking voided."), self.refresh()
