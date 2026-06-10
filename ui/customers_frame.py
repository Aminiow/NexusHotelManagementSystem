import tkinter as tk
from tkinter import ttk, messagebox
from ui import NexusTheme, BaseFrame
from models import Customer
from db import ErrorHandler

class CustomersFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        tk.Label(self, text="Customer Management", bg=NexusTheme.BG, fg=NexusTheme.ACCENT, font=NexusTheme.HEADING_FONT).pack(pady=10)
        self.create_search_bar(self)
        input_frame = tk.Frame(self, bg=NexusTheme.BG)
        input_frame.pack(pady=10)
        self.entries = []
        for i, text in enumerate(["Name", "Phone", "Email", "ID Proof"]):
            tk.Label(input_frame, text=text, bg=NexusTheme.BG, fg=NexusTheme.FG, font=NexusTheme.FONT).grid(row=0, column=i * 2, padx=5, sticky="e")
            entry = ttk.Entry(input_frame, width=18)
            entry.grid(row=0, column=i * 2 + 1, padx=5)
            self.entries.append(entry)
        btn_frame = tk.Frame(self, bg=NexusTheme.BG)
        btn_frame.pack(pady=5)
        for idx, (txt, cmd) in enumerate([("ADD", self.add_customer), ("UPDATE", self.update_customer), ("DELETE", self.delete_customer), ("CLEAR", self.clear_form)]):
            tk.Button(btn_frame, text=txt, command=cmd, bg=NexusTheme.DARK, fg=NexusTheme.FG, activebackground=NexusTheme.ACCENT, activeforeground="#FFFFFF", font=NexusTheme.FONT_BOLD, relief="flat", padx=12).grid(row=0, column=idx, padx=3)
        self.tree = self.create_tree(("ID", "Name", "Phone", "Email", "ID Proof"), ("ID", "Name", "Phone", "Email", "ID Proof"))
        self.tree.bind("<ButtonRelease-1>", self.on_select)

    def populate_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.filtered_data:
            self.tree.insert("", "end", values=row)

    def refresh(self):
        self.all_data = Customer.get_all() or []
        self.apply_filter_sort()

    def add_customer(self):
        name = self.entries[0].get()
        if not name:
            return ErrorHandler.show_error(ErrorHandler.INP_MISSING, "Name is required.")
        if Customer.add(name, self.entries[1].get(), self.entries[2].get(), self.entries[3].get()):
            messagebox.showinfo("Success", "Customer added."), self.refresh(), self.clear_form()

    def update_customer(self):
        sel = self.tree.focus()
        if not sel:
            return ErrorHandler.show_error(ErrorHandler.INP_MISSING, "Select a customer.")
        cust_id = self.tree.item(sel)["values"][0]
        name = self.entries[0].get()
        if not name:
            return ErrorHandler.show_error(ErrorHandler.INP_MISSING, "Name is required.")
        if Customer.update(cust_id, name, self.entries[1].get(), self.entries[2].get(), self.entries[3].get()):
            messagebox.showinfo("Success", "Customer updated."), self.refresh(), self.clear_form()

    def delete_customer(self):
        sel = self.tree.focus()
        if not sel:
            return ErrorHandler.show_error(ErrorHandler.INP_MISSING, "Select a customer.")
        if messagebox.askyesno("Confirm", "Delete this customer?"):
            Customer.delete(self.tree.item(sel)["values"][0])
            self.refresh()
            self.clear_form()

    def on_select(self, event):
        sel = self.tree.focus()
        if sel:
            vals = self.tree.item(sel)["values"]
            self.clear_form()
            self.entries[0].insert(0, vals[1])
            self.entries[1].insert(0, vals[2] if vals[2] else "")
            self.entries[2].insert(0, vals[3] if vals[3] else "")
            self.entries[3].insert(0, vals[4] if vals[4] else "")

    def clear_form(self):
        for e in self.entries:
            e.delete(0, "end")
