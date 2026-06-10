import tkinter as tk
from tkinter import messagebox
from ui import NexusTheme, BaseFrame
from models import Billing
from db import ErrorHandler


class BillingFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        tk.Label(self, text="Billing & Payments", bg=NexusTheme.BG, fg=NexusTheme.ACCENT, font=NexusTheme.HEADING_FONT).pack(pady=10)
        self.create_search_bar(self)
        self.tree = self.create_tree(("Bill ID", "Booking ID", "Customer", "Room", "Total Amount", "Status", "Payment Date"), ("Bill ID", "Booking ID", "Customer", "Room", "Total Amount", "Status", "Payment Date"), height=12)
        tk.Button(tk.Frame(self, bg=NexusTheme.BG).pack(pady=5) or tk.Frame(self, bg=NexusTheme.BG), text="MARK AS SETTLED", command=self.mark_paid, bg=NexusTheme.DARK, fg=NexusTheme.SUCCESS, activebackground=NexusTheme.ACCENT, activeforeground="#FFFFFF", font=NexusTheme.FONT_BOLD, relief="flat", padx=20).pack()

    def populate_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.filtered_data:
            self.tree.insert("", "end", values=row)

    def refresh(self):
        self.all_data = Billing.get_all() or []
        self.apply_filter_sort()

    def mark_paid(self):
        sel = self.tree.focus()
        if not sel:
            return ErrorHandler.show_error(ErrorHandler.INP_MISSING, "Select a bill.")
        bill_id = self.tree.item(sel)["values"][0]
        if self.tree.item(sel)["values"][5] == "settled":
            return messagebox.showinfo("Info", "Bill is already settled.")
        if Billing.mark_paid(bill_id):
            messagebox.showinfo("Success", "Payment recorded. Status: settled."), self.refresh()
