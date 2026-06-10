import sqlite3
from db import ErrorHandler


class DatabaseManager:
    _instance = None

    def __new__(cls, db_name="nexus_hotel.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_name="nexus_hotel.db"):
        if self._initialized:
            return
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.run_migrations()
        self.create_tables()
        self._initialized = True

    def run_migrations(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER)")
        self.cursor.execute("SELECT MAX(version) FROM schema_version")
        current = self.cursor.fetchone()[0] or 0
        if current < 2:
            try:
                self.cursor.execute("UPDATE rooms SET status = 'vacant' WHERE status = 'available'")
                self.cursor.execute("UPDATE bookings SET status = 'reserved' WHERE status = 'booked'")
                self.cursor.execute("UPDATE bookings SET status = 'in_house' WHERE status = 'checked_in'")
                self.cursor.execute("UPDATE bookings SET status = 'departed' WHERE status = 'checked_out'")
                self.cursor.execute("UPDATE bookings SET status = 'voided' WHERE status = 'cancelled'")
                self.cursor.execute("UPDATE billing SET payment_status = 'pending' WHERE payment_status = 'unpaid'")
                self.cursor.execute("UPDATE billing SET payment_status = 'settled' WHERE payment_status = 'paid'")
                self.conn.commit()
            except sqlite3.Error:
                pass
            self.cursor.execute("INSERT OR REPLACE INTO schema_version (version) VALUES (2)")
            self.conn.commit()
        self.create_tables()

    def create_tables(self):
        self.cursor.executescript("""
      CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY AUTOINCREMENT, room_number TEXT UNIQUE NOT NULL, type TEXT NOT NULL, price REAL NOT NULL, status TEXT DEFAULT 'vacant' CHECK(status IN ('vacant','occupied','maintenance')));
      CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone TEXT, email TEXT, id_proof TEXT);
      CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL, room_id INTEGER NOT NULL, check_in_date TEXT NOT NULL, check_out_date TEXT NOT NULL, status TEXT DEFAULT 'reserved' CHECK(status IN ('reserved','in_house','departed','voided')), FOREIGN KEY (customer_id) REFERENCES customers(id), FOREIGN KEY (room_id) REFERENCES rooms(id));
      CREATE TABLE IF NOT EXISTS billing (id INTEGER PRIMARY KEY AUTOINCREMENT, booking_id INTEGER NOT NULL UNIQUE, total_amount REAL NOT NULL, payment_status TEXT DEFAULT 'pending' CHECK(payment_status IN ('pending','settled')), payment_date TEXT, FOREIGN KEY (booking_id) REFERENCES bookings(id));
    """)
        self.conn.commit()

    def execute_query(self, query, params=(), fetch=False):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.fetchall() if fetch else True
        except sqlite3.Error as e:
            ErrorHandler.db_error(e, query.split()[0])
            return None

    def close(self):
        self.conn.close()
