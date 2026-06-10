import tkinter as tk
from tkinter import messagebox
from ui import NexusTheme, BaseFrame
from db import DatabaseManager, ErrorHandler
from models import Booking


class CheckoutFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        tk.Label(self, text="Checkout (In-House Guests)", bg=NexusTheme.BG, fg=NexusTheme.ACCENT, font=NexusTheme.HEADING_FONT).pack(pady=10)
        self.create_search_bar(self)
        self.tree = self.create_tree(("Booking ID", "Customer", "Room", "Check-in", "Check-out", "Status"), ("Booking ID", "Customer", "Room", "Check-in", "Check-out", "Status"))
        tk.Button(tk.Frame(self, bg=NexusTheme.BG).pack(pady=5) or tk.Frame(self, bg=NexusTheme.BG), text="CHECKOUT", command=self.do_checkout, bg=NexusTheme.DARK, fg=NexusTheme.SUCCESS, activebackground=NexusTheme.ACCENT, activeforeground="#FFFFFF", font=NexusTheme.FONT_BOLD, relief="flat", padx=20).pack()

    def populate_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.filtered_data:
            self.tree.insert("", "end", values=row)

    def refresh(self):
        self.all_data = DatabaseManager().execute_query("SELECT b.id, c.name, r.room_number, b.check_in_date, b.check_out_date, b.status FROM bookings b JOIN customers c ON b.customer_id = c.id JOIN rooms r ON b.room_id = r.id WHERE b.status = 'in_house'", fetch=True) or []
        self.apply_filter_sort()

    def do_checkout(self):
        sel = self.tree.focus()
        if not sel:
            return ErrorHandler.show_error(ErrorHandler.INP_MISSING, "Select a checked-in booking.")
        if Booking.checkout(self.tree.item(sel)["values"][0]):
            messagebox.showinfo("Success", "Checkout complete. Bill generated (pending)."), self.refresh()
