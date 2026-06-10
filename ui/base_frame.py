import tkinter as tk
from tkinter import ttk
from datetime import datetime
import re
from ui import NexusTheme


class BaseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=NexusTheme.BG)
        self.controller = controller
        self.sort_column = None
        self.sort_reverse = False
        self.all_data, self.filtered_data = [], []
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self.on_search())

    def create_search_bar(self, parent_frame):
        f = tk.Frame(parent_frame, bg=NexusTheme.BG)
        f.pack(fill="x", padx=10, pady=5)
        tk.Label(f, text="Search:", bg=NexusTheme.BG, fg=NexusTheme.FG, font=NexusTheme.FONT).pack(side="left", padx=(0, 5))
        e = ttk.Entry(f, textvariable=self.search_var, width=30)
        e.pack(side="left")
        return e

    def create_tree(self, columns, headings, height=10):
        tree = ttk.Treeview(self, columns=columns, show="headings", height=height)
        for idx, (col, head) in enumerate(zip(columns, headings)):
            tree.heading(col, text=head, command=lambda c=idx: self.on_header_click(c))
            tree.column(col, width=120, anchor="center")
        tree.pack(fill="both", expand=True, pady=10, padx=10)
        tree.bind("<ButtonRelease-1>", self.on_tree_select)
        return tree

    def on_header_click(self, col_index):
        if self.sort_column == col_index:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col_index
            self.sort_reverse = False
        self.apply_filter_sort()

    def on_search(self, *args):
        self.apply_filter_sort()

    def apply_filter_sort(self):
        if not self.all_data:
            self.filtered_data = []
        else:
            q = self.search_var.get().strip().lower()
            self.filtered_data = [row for row in self.all_data if not q or any(q in str(cell).lower() for cell in row)]
        if self.sort_column is not None and self.filtered_data:
            try:
                col = self.sort_column
                rev = self.sort_reverse
                sample = self.filtered_data[0][col]
                if isinstance(sample, str) and re.match(r"\d{4}-\d{2}-\d{2}", sample):
                    self.filtered_data.sort(key=lambda x: datetime.strptime(x[col], "%Y-%m-%d"), reverse=rev)
                elif isinstance(sample, (int, float)):
                    self.filtered_data.sort(key=lambda x: x[col], reverse=rev)
                else:
                    self.filtered_data.sort(key=lambda x: str(x[col]).lower(), reverse=rev)
            except:
                pass
        self.populate_tree()

    def populate_tree(self):
        raise NotImplementedError

    def refresh(self):
        raise NotImplementedError

    def on_tree_select(self, event):
        pass
