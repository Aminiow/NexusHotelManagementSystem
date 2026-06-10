import tkinter as tk
import webbrowser
from ui import NexusTheme
from release import APP_NAME, APP_SUBTITLE, RELEASE_DATE, AUTHOR, GITHUB_REPO


class HelpPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Help – User Manual")
        self.geometry("600x480")
        self.configure(bg=NexusTheme.BG)
        self.resizable(False, False)
        tk.Label(self, text="Nexus – User Guide", bg=NexusTheme.BG, fg=NexusTheme.ACCENT, font=NexusTheme.TITLE_FONT).pack(pady=10)
        self.help_text = tk.Text(self, bg=NexusTheme.DARK, fg=NexusTheme.FG, font=NexusTheme.FONT, wrap="word", padx=15, pady=15, borderwidth=0, highlightthickness=1, highlightbackground=NexusTheme.BORDER, highlightcolor=NexusTheme.ACCENT)
        self.help_text.pack(expand=True, fill="both", padx=20, pady=(0, 10))
        static_text = (
            "Welcome to Nexus, your modern hotel management tool.\n\n"
            f"{APP_NAME} – {APP_SUBTITLE}\n"
            f"Release Date: {RELEASE_DATE}\n"
            f"Author: {AUTHOR}\n\n"
            "[DASHBOARD OVERVIEW]\n"
            "Use the sidebar to navigate between sections:\n"
            "  • Rooms – Add, edit, remove rooms.\n"
            "  • Customers – Register and manage guest profiles.\n"
            "  • Booking – Reserve rooms, check-in guests, void bookings.\n"
            "  • Checkout – Process departures and generate bills.\n"
            "  • Billing – View and settle invoices.\n\n"
            "[STATUS GLOSSARY]\n"
            "  Rooms: vacant, occupied, maintenance\n"
            "  Bookings: reserved → in_house → departed (or voided)\n"
            "  Billing: pending → settled\n\n"
            "[COMMON WORKFLOW]\n"
            "  1. Add rooms (Rooms tab).\n"
            "  2. Register customers (Customers tab).\n"
            "  3. Create booking: select guest + vacant room, pick dates, click Book.\n"
            "  4. On arrival: select the reserved booking → Check-In.\n"
            "  5. On departure: go to Checkout tab, select → Checkout.\n"
            "  6. The bill is generated; go to Billing to mark as Settled.\n\n"
            "[SEARCH & SORT]\n"
            "  • Each table has a search bar – type to filter in real time.\n"
            "  • Click any column header to sort; click again to reverse order.\n"
            "  • Sorting works on the currently filtered set.\n\n"
            "[TIPS]\n"
            "  • Dates format: YYYY-MM-DD.\n"
            "  • Prices are per night.\n"
            "  • Error codes appear in messages for easy troubleshooting.\n\n"
            "[SUPPORT & UPDATES]\n"
            "  • Found a bug or have a feature request? Visit the GitHub repository:\n"
        )
        self.help_text.insert("1.0", static_text, "normal")
        link_start = self.help_text.index("end-1c")
        self.help_text.insert("end", "    " + GITHUB_REPO + "\n", "link")
        link_end = self.help_text.index("end-1c")
        after_link = "  • There you can report issues, see what's new, and download the latest updates.\n" "  • Contributions and feedback are always welcome!"
        self.help_text.insert("end", after_link, "normal")
        self.help_text.tag_config("link", foreground=NexusTheme.ACCENT, underline=True, font=("Segoe UI", 10, "underline"))
        self.help_text.tag_bind("link", "<Button-1>", self._open_github)
        self.help_text.config(state="disabled")
        self.help_text.tag_bind("link", "<Enter>", lambda e: self.help_text.config(cursor="hand2"))
        self.help_text.tag_bind("link", "<Leave>", lambda e: self.help_text.config(cursor=""))
        tk.Button(self, text="CLOSE", command=self.destroy, bg=NexusTheme.DARK, fg=NexusTheme.FG, activebackground=NexusTheme.ACCENT, activeforeground="#FFFFFF", font=NexusTheme.FONT_BOLD, relief="flat", borderwidth=0, padx=20, pady=6, highlightthickness=1, highlightbackground=NexusTheme.BORDER).pack(pady=10)

    def _open_github(self, event):
        webbrowser.open_new(GITHUB_REPO)
