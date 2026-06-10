from tkinter import ttk


class NexusTheme:
    BG, SIDEBAR_BG, FG, ACCENT, SUCCESS, WARNING, DARK, ENTRY_BG, BORDER = "#0D1117", "#161B22", "#C9D1D9", "#58A6FF", "#3FB950", "#D29922", "#161B22", "#0D1117", "#30363D"
    FONT, FONT_BOLD, HEADING_FONT, TITLE_FONT = ("Segoe UI", 10), ("Segoe UI", 10, "bold"), ("Segoe UI", 12, "bold"), ("Segoe UI", 14, "bold")

    @classmethod
    def apply(cls):
        style = ttk.Style()
        style.theme_use("clam")
        for cfg, opts in [
            (".", {"background": cls.BG, "foreground": cls.FG, "fieldbackground": cls.ENTRY_BG}),
            ("TLabel", {"background": cls.BG, "foreground": cls.FG, "font": cls.FONT}),
            ("TButton", {"background": cls.DARK, "foreground": cls.FG, "borderwidth": 1, "focusthickness": 2, "focuscolor": cls.ACCENT, "font": cls.FONT_BOLD, "relief": "flat", "padding": 6}),
            ("TEntry", {"fieldbackground": cls.ENTRY_BG, "foreground": cls.FG, "insertcolor": cls.FG, "borderwidth": 1, "relief": "solid"}),
            ("Treeview", {"background": cls.DARK, "foreground": cls.FG, "fieldbackground": cls.DARK, "font": cls.FONT, "borderwidth": 0}),
            ("Treeview.Heading", {"background": cls.ACCENT, "foreground": "#FFFFFF", "font": cls.FONT_BOLD, "relief": "flat"}),
            ("TFrame", {"background": cls.BG}),
            ("TCombobox", {"fieldbackground": cls.ENTRY_BG, "background": cls.DARK, "foreground": cls.FG, "arrowcolor": cls.FG}),
            ("TLabelframe", {"background": cls.BG, "foreground": cls.FG, "borderwidth": 1, "relief": "solid"}),
            ("TLabelframe.Label", {"background": cls.BG, "foreground": cls.FG, "font": cls.FONT_BOLD}),
        ]:
            style.configure(cfg, **opts)
        style.map("TButton", background=[("active", cls.ACCENT), ("!active", cls.DARK)], foreground=[("active", "#FFFFFF")])
        style.map("Treeview", background=[("selected", cls.ACCENT)], foreground=[("selected", "#FFFFFF")])
        style.map("TCombobox", fieldbackground=[("readonly", cls.ENTRY_BG)], foreground=[("readonly", cls.FG)])
        style.configure("Sidebar.TButton", background=cls.SIDEBAR_BG, foreground=cls.FG, borderwidth=0, focuscolor=cls.ACCENT, font=cls.FONT_BOLD, anchor="w", padding=8)
        style.map("Sidebar.TButton", background=[("active", cls.ACCENT)], foreground=[("active", "#FFFFFF")])
