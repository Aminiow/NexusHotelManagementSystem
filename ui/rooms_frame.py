import tkinter as tk
from tkinter import ttk, messagebox
from ui import NexusTheme, BaseFrame
from models import Room
from db import ErrorHandler

class RoomsFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        tk.Label(self, text="Room Management", bg=NexusTheme.BG, fg=NexusTheme.ACCENT, font=NexusTheme.HEADING_FONT).pack(pady=10)
        self.create_search_bar(self)
        input_frame = tk.Frame(self, bg=NexusTheme.BG)
        input_frame.pack(pady=10)
        self.entries = []
        for i, text in enumerate(["Room Number", "Type", "Price/Night", "Status"]):
            tk.Label(input_frame, text=text, bg=NexusTheme.BG, fg=NexusTheme.FG, font=NexusTheme.FONT).grid(row=0, column=i * 2, padx=5, sticky="e")
            if i == 3:
                self.status_var = tk.StringVar(value="vacant")
                cb = ttk.Combobox(input_frame, textvariable=self.status_var, values=["vacant", "occupied", "maintenance"], state="readonly", width=12)
                cb.grid(row=0, column=i * 2 + 1, padx=5)
                self.entries.append(cb)
            else:
                entry = ttk.Entry(input_frame, width=15)
                entry.grid(row=0, column=i * 2 + 1, padx=5)
                self.entries.append(entry)
        btn_frame = tk.Frame(self, bg=NexusTheme.BG)
        btn_frame.pack(pady=5)
        for idx, (txt, cmd) in enumerate([("ADD", self.add_room), ("UPDATE", self.update_room), ("DELETE", self.delete_room), ("CLEAR", self.clear_form)]):
            tk.Button(btn_frame, text=txt, command=cmd, bg=NexusTheme.DARK, fg=NexusTheme.FG, activebackground=NexusTheme.ACCENT, activeforeground="#FFFFFF", font=NexusTheme.FONT_BOLD, relief="flat", padx=12).grid(row=0, column=idx, padx=3)
        self.tree = self.create_tree(("ID", "Number", "Type", "Price", "Status"), ("ID", "Number", "Type", "Price", "Status"))
        self.tree.bind("<ButtonRelease-1>", self.on_select)

    def populate_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.filtered_data:
            self.tree.insert("", "end", values=row)

    def refresh(self):
        self.all_data = Room.get_all() or []
        self.apply_filter_sort()

    def add_room(self):
        num, typ, price, status = self.entries[0].get(), self.entries[1].get(), self.entries[2].get(), self.status_var.get()
        if not num or not typ or not price:
            return ErrorHandler.show_error(ErrorHandler.INP_MISSING, "All fields except status are required.")
        try:
            price = float(price)
        except ValueError:
            return ErrorHandler.show_error(ErrorHandler.INP_FORMAT, "Price must be a number.")
        if Room.add(num, typ, price, status):
            messagebox.showinfo("Success", "Room added."), self.refresh(), self.clear_form()

    def update_room(self):
        sel = self.tree.focus()
        if not sel:
            return ErrorHandler.show_error(ErrorHandler.INP_MISSING, "Select a room to update.")
        room_id = self.tree.item(sel)["values"][0]
        num, typ, price, status = self.entries[0].get(), self.entries[1].get(), self.entries[2].get(), self.status_var.get()
        if not num or not typ or not price:
            return ErrorHandler.show_error(ErrorHandler.INP_MISSING, "All fields required.")
        try:
            price = float(price)
        except ValueError:
            return ErrorHandler.show_error(ErrorHandler.INP_FORMAT, "Price must be a number.")
        if Room.update(room_id, num, typ, price, status):
            messagebox.showinfo("Success", "Room updated."), self.refresh(), self.clear_form()

    def delete_room(self):
        sel = self.tree.focus()
        if not sel:
            return ErrorHandler.show_error(ErrorHandler.INP_MISSING, "Select a room to delete.")
        if messagebox.askyesno("Confirm", "Permanently delete this room?"):
            Room.delete(self.tree.item(sel)["values"][0])
            self.refresh()
            self.clear_form()

    def on_select(self, event):
        sel = self.tree.focus()
        if sel:
            vals = self.tree.item(sel)["values"]
            self.clear_form()
            self.entries[0].insert(0, vals[1])
            self.entries[1].insert(0, vals[2])
            self.entries[2].insert(0, vals[3])
            self.status_var.set(vals[4])

    def clear_form(self):
        self.entries[0].delete(0, "end")
        self.entries[1].delete(0, "end")
        self.entries[2].delete(0, "end")
        self.status_var.set("vacant")
