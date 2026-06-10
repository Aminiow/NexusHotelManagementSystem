import tkinter as tk, sys, os, sqlite3
from tkinter import filedialog, messagebox
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from db.error_handler import ErrorHandler

seed_errors = []
ErrorHandler.show_error = staticmethod(lambda code, msg, detail="": seed_errors.append(f"[{code}] {msg}" + (f" ({detail})" if detail else "")))

from db.database import DatabaseManager
from models.room import Room
from models.customer import Customer
from models.booking import Booking
from models.billing import Billing


def database_locked(db_path):
    """Try a quick write to see if another process locks the DB."""
    try:
        test_conn = sqlite3.connect(db_path, timeout=0.2)
        test_conn.execute("CREATE TABLE IF NOT EXISTS _seed_lock_test (id int)")
        test_conn.execute("DROP TABLE IF EXISTS _seed_lock_test")
        test_conn.close()
        return False
    except sqlite3.OperationalError:
        return True


def safe_call(func, *args, err_msg=""):
    try:
        func(*args)
    except Exception as e:
        seed_errors.append(f"{err_msg}: {e}")


def seed(db_path):
    if database_locked(db_path):
        messagebox.showerror("Database Locked", "The database is in use.\nClose the Nexus Hotel app before seeding.")
        return

    DatabaseManager._instance = None
    db = DatabaseManager(db_path)

    rooms = [("101", "Single", 80.0, "vacant"), ("102", "Single", 80.0, "occupied"), ("201", "Double", 120.0, "vacant"), ("202", "Double", 120.0, "maintenance"), ("301", "Suite", 200.0, "vacant")]
    for r in rooms:
        safe_call(Room.add, *r, err_msg=f"Room {r[0]}")

    customers = [("Alice Johnson", "555-0101", "alice@example.com", "ID-1001"), ("Bob Smith", "555-0202", "bob@example.com", "ID-1002"), ("Carol Davis", "555-0303", "carol@example.com", "ID-1003")]
    for c in customers:
        safe_call(Customer.add, *c, err_msg=f"Customer {c[0]}")

    all_rooms = db.execute_query("SELECT id, room_number, status FROM rooms", fetch=True)
    all_cust = db.execute_query("SELECT id, name FROM customers", fetch=True)
    room_map = {num: (rid, st) for rid, num, st in all_rooms}
    cust_map = {name: cid for cid, name in all_cust}
    today = datetime.now().date()

    if "101" in room_map and room_map["101"][1] == "vacant":
        rid, cid = room_map["101"][0], cust_map["Alice Johnson"]
        ci, co = (today - timedelta(days=2)).strftime("%Y-%m-%d"), (today + timedelta(days=2)).strftime("%Y-%m-%d")
        if Booking.create(cid, rid, ci, co):
            db.execute_query("UPDATE bookings SET status='in_house' WHERE customer_id=? AND room_id=?", (cid, rid))
        else:
            seed_errors.append("Could not create booking for Alice (room 101).")
    else:
        seed_errors.append("Room 101 not vacant - skipping Alice's booking.")

    if "201" in room_map and room_map["201"][1] == "vacant":
        rid, cid = room_map["201"][0], cust_map["Bob Smith"]
        ci, co = (today - timedelta(days=5)).strftime("%Y-%m-%d"), (today - timedelta(days=3)).strftime("%Y-%m-%d")
        if Booking.create(cid, rid, ci, co):
            db.execute_query("UPDATE bookings SET status='departed' WHERE customer_id=? AND room_id=?", (cid, rid))
            db.execute_query("UPDATE rooms SET status='vacant' WHERE id=?", (rid,))
        else:
            seed_errors.append("Could not create booking for Bob (room 201).")
    else:
        seed_errors.append("Room 201 not vacant - skipping Bob's booking.")

    if "301" in room_map and room_map["301"][1] == "vacant":
        rid, cid = room_map["301"][0], cust_map["Carol Davis"]
        ci, co = (today + timedelta(days=1)).strftime("%Y-%m-%d"), (today + timedelta(days=4)).strftime("%Y-%m-%d")
        if not Booking.create(cid, rid, ci, co):
            seed_errors.append("Could not create booking for Carol (room 301).")
    else:
        seed_errors.append("Room 301 not vacant - skipping Carol's booking.")

    bob_book = db.execute_query("SELECT id FROM bookings WHERE customer_id=? AND status='departed'", (cust_map["Bob Smith"],), fetch=True)
    if bob_book:
        bid = bob_book[0][0]
        if not db.execute_query("SELECT id FROM billing WHERE booking_id=?", (bid,), fetch=True):
            ci_str, co_str, rid2 = db.execute_query("SELECT check_in_date, check_out_date, room_id FROM bookings WHERE id=?", (bid,), fetch=True)[0]
            days = max((datetime.strptime(co_str, "%Y-%m-%d") - datetime.strptime(ci_str, "%Y-%m-%d")).days, 1)
            price = db.execute_query("SELECT price FROM rooms WHERE id=?", (rid2,), fetch=True)[0][0]
            Billing.generate(bid, days * price)
    else:
        seed_errors.append("No departed booking for Bob found.")

    root = tk.Tk()
    root.withdraw()
    msg = ("Seeding completed with some issues:\n\n" + "\n".join(seed_errors)) if seed_errors else "Test data added successfully!\n\n" "If Nexus Hotel is open, switch to any other section and back\n" "to refresh the view. If data still doesn't appear, restart the app."
    (messagebox.showwarning if seed_errors else messagebox.showinfo)("Seeding Result", msg)
    root.destroy()


def main():
    root = tk.Tk()
    root.withdraw()
    db_path = filedialog.askopenfilename(title="Select the Nexus Hotel database file", filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")])
    if db_path:
        root.destroy()
        seed(db_path)
    else:
        messagebox.showinfo("Cancelled", "No database file selected. Exiting.")
        root.destroy()


if __name__ == "__main__":
    main()
