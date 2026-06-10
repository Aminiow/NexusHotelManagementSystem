# 🏨 Nexus – Hotel Management System

**Nexus** is a modern, dark‑themed hotel management desktop application built with **Python/Tkinter** and **SQLite**.
It handles rooms, customers, bookings, check‑in/check‑out, and billing with an intuitive multi‑tab interface.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

**📅 Current Release:** v1.0.0 (2026‑06‑10, Build 3)

**🛠️ Author:** Aminiow

**🔗 Repository:** [Nexus-Hotel-Management-System (Nexus HMS)](https://github.com/Aminiow/NexusHotelManagementSystem)

---

## 📋 Requirements

- **Python 3.8 or newer** (3.10+ recommended)
- **Tkinter** – included with most Python distributions.
  If missing, install it via your system package manager (e.g., `sudo apt install python3-tk` on Debian/Ubuntu, or reinstall Python from [python.org](https://www.python.org/) with the Tcl/Tk option checked on Windows/macOS).

**No external libraries are needed.** The entire app runs on Python’s built‑in modules (`tkinter`, `sqlite3`, `datetime`, `re`, `os`, `sys`, `subprocess`, `shutil`).

---

## ✨ Features

- **Complete hotel workflow** – Rooms → Customers → Booking → Check‑In/Check‑Out → Billing
- **Dark UI theme** – modern, eye‑friendly interface with `NexusTheme`
- **Multi‑file architecture** – clean separation into `db`, `models`, `ui` packages
- **Live search & sort** – filter any table in real time, click column headers to sort
- **Error handling** – descriptive error codes for DB, input, and business logic, with app name and release date shown in every error
- **Migrations built‑in** – auto‑upgrades old database schemas on first run
- **Data seeder** – populates demo data (rooms, customers, bookings, bills) via a separate GUI tool
- **Built‑in Help** – user guide with application info, release date, author, and clickable GitHub link
- **Cross‑platform** – runs on Windows, macOS, Linux; buildable into a single `.exe` (or macOS/Linux executable) with PyInstaller

---

## 📸 Screenshots

> *(e.g., the main dashboard, booking screen).* (**NOT AVAILABLE**)

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/Aminiow/NexusHotelManagementSystem.git
cd NexusHotelManagementSystem
```

### 2. Verify Python & Tkinter
```bash
python --version
python -m tkinter    # a small Tk window should appear
```

### 3. Run the application
```bash
python main.py
```

The database file `nexus_hotel.db` is created automatically in the project folder on first launch.

---

## 🧭 Usage

| Tab         | What you can do                                                                   |
|-------------|-----------------------------------------------------------------------------------|
| **Rooms**   | Add, edit, delete rooms. Set status (vacant, occupied, maintenance).              |
| **Customers** | Register guests with name, phone, email, ID proof.                              |
| **Booking** | Create reservations, check‑in guests, void bookings.                              |
| **Checkout** | Process departures – auto‑generates a bill.                                      |
| **Billing** | View invoices, mark them as settled (paid).                                       |
| **Help**    | Built‑in user guide showing release info and GitHub link for issues & updates.   |

**Status flow**
Rooms: `vacant` → `occupied` / `maintenance`

Bookings: `reserved` → `in_house` → `departed` (or `voided`)

Billing: `pending` → `settled`

---

## 📁 Project structure

```
.
├── main.py                  # Application entry point (window title shows release date)
├── release.py               # App identity: name, release date, author, GitHub repo
├── seed_data.py             # Demo data seeder (GUI)
├── requirements.txt         # (empty – no external dependencies)
├── README.md
├── db/
│   ├── __init__.py
│   ├── database.py          # DatabaseManager (singleton, migrations)
│   └── error_handler.py     # ErrorHandler (errors include app name & release date)
├── models/
│   ├── __init__.py
│   ├── room.py
│   ├── customer.py
│   ├── booking.py
│   └── billing.py
├── ui/
│   ├── __init__.py
│   ├── theme.py             # NexusTheme (dark styling)
│   ├── base_frame.py        # BaseFrame (search, sort, tree)
│   ├── help_popup.py        # Help window with app info and clickable GitHub link
│   ├── rooms_frame.py
│   ├── customers_frame.py
│   ├── booking_frame.py
│   ├── checkout_frame.py
│   └── billing_frame.py
├── resources/
│   └── app/
│       ├── AppExecutableIcon.ico   # Icon for the .exe file
│       └── TitleBarIcon.ico        # Icon for the window title bar
├── CrossPlatformInstaller.py       # Python build script (cross‑platform)
├── LinuxInstaller.sh               # Bash build script (Linux/macOS)
├── WindowsInstaller.bat            # Batch build script (Windows)
├── NexusHotel.spec                 # PyInstaller spec (main app)
└── SeedNexusData.spec              # PyInstaller spec (seeder)
```

---

## 🔨 Building executables

You can create standalone executables for **NexusHotel** and **SeedNexusData** using PyInstaller.

### Prerequisites
```bash
pip install pyinstaller
```

### Option 1: Use spec files (recommended, cross‑platform)
```bash
pyinstaller NexusHotel.spec --distpath executable --workpath temp_build
pyinstaller SeedNexusData.spec --distpath executable --workpath temp_seed_build
```

### Option 2: Use pre‑written scripts
- **Windows** – double‑click `WindowsInstaller.bat`
- **Linux/macOS** – run `./LinuxInstaller.sh`
- **Any OS** – `python CrossPlatformInstaller.py`

The final executables will be placed in the `executable` folder (adjust `--distpath` as needed).
The app icon is automatically embedded from `resources/app/AppExecutableIcon.ico`.

---

## 🧪 Adding test data

The **SeedNexusData** tool populates your database with demo records so you can explore all features immediately.

1. **Close the main Nexus app** (database must not be locked).
2. Run `SeedNexusData`:
   - If you built the executable, launch `SeedNexusData.exe`.
   - Otherwise run `python seed_data.py`.
3. Select your `nexus_hotel.db` file when prompted.
4. A message box confirms the seeding.
   If the main app is already open, simply switch to another tab and back to refresh the data.

---

## 📅 Release information

All release data is stored in `release.py`:

```python
APP_NAME = "Nexus"
APP_SUBTITLE = "Hotel Management System"
RELEASE_DATE = "2026-06-10"
AUTHOR = "Aminiow"
GITHUB_REPO = "https://github.com/Aminiow/NexusHotelManagementSystem"
VERSION_TUPLE = (1, 0, 0)
VERSION_STRING = "1.0.0"
BUILD_ID = "20260610-3"
```

This information appears in:
- Window title: `Nexus – 2026-06-10`
- Error messages: `Nexus (2026-06-10) [ERR-CODE] description`
- Help window: displays app name, subtitle, release date, author, and a clickable GitHub link

---

## 📜 License

This project is open‑source under the [MIT License](LICENSE).
Feel free to use, modify, and distribute it.

---

## 🤝 Contributing

Pull requests and suggestions are welcome!
Please open an issue first to discuss any major changes.

---

## 🧰 Built With

- [Python 3](https://www.python.org/) + Tkinter
- [SQLite3](https://www.sqlite.org/) (via Python’s built‑in module)
- [PyInstaller](https://pyinstaller.org/) for standalone executables

```txt
# Nexus uses only the Python standard library.
# No external packages are required.
```
---

**Enjoy managing your hotel with Nexus!** 🛎️
