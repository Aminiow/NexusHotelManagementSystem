from datetime import datetime
from db import DatabaseManager, ErrorHandler
from models import Room, Billing


class Booking:
    @staticmethod
    def create(customer_id, room_id, check_in, check_out):
        db = DatabaseManager()
        room = db.execute_query("SELECT status FROM rooms WHERE id=?", (room_id,), fetch=True)
        if not room:
            return ErrorHandler.show_error(ErrorHandler.BIZ_AVAIL, "Room not found.")
        if room[0][0] != "vacant":
            return ErrorHandler.show_error(ErrorHandler.BIZ_AVAIL, "Selected room is not vacant.")
        if db.execute_query("INSERT INTO bookings (customer_id, room_id, check_in_date, check_out_date, status) VALUES (?,?,?,?,'reserved')", (customer_id, room_id, check_in, check_out)):
            Room.set_status(room_id, "occupied")
            return True

    @staticmethod
    def get_all():
        db = DatabaseManager()
        return db.execute_query("SELECT b.id, c.name, r.room_number, b.check_in_date, b.check_out_date, b.status FROM bookings b JOIN customers c ON b.customer_id = c.id JOIN rooms r ON b.room_id = r.id ORDER BY b.id DESC", fetch=True)

    @staticmethod
    def checkin(booking_id):
        db = DatabaseManager()
        booking = db.execute_query("SELECT * FROM bookings WHERE id=?", (booking_id,), fetch=True)
        if not booking:
            return ErrorHandler.show_error(ErrorHandler.BIZ_STATUS, "Booking not found.")
        if booking[0][5] != "reserved":
            return ErrorHandler.show_error(ErrorHandler.BIZ_STATUS, "Booking must be in 'reserved' status to check-in.")
        return db.execute_query("UPDATE bookings SET status='in_house' WHERE id=?", (booking_id,))

    @staticmethod
    def checkout(booking_id):
        db = DatabaseManager()
        booking = db.execute_query("SELECT * FROM bookings WHERE id=?", (booking_id,), fetch=True)
        if not booking:
            return ErrorHandler.show_error(ErrorHandler.BIZ_STATUS, "Booking not found.")
        if booking[0][5] != "in_house":
            return ErrorHandler.show_error(ErrorHandler.BIZ_STATUS, "Booking must be 'in_house' to check-out.")
        db.execute_query("UPDATE bookings SET status='departed' WHERE id=?", (booking_id,))
        room_id = booking[0][2]
        Room.set_status(room_id, "vacant")
        if not db.execute_query("SELECT id FROM billing WHERE booking_id=?", (booking_id,), fetch=True):
            room = db.execute_query("SELECT price FROM rooms WHERE id=?", (room_id,), fetch=True)
            if room:
                price_per_night = room[0][0]
                check_in = datetime.strptime(booking[0][3], "%Y-%m-%d")
                check_out = datetime.strptime(booking[0][4], "%Y-%m-%d")
                days = max((check_out - check_in).days, 1)
                Billing.generate(booking_id, price_per_night * days)
        return True

    @staticmethod
    def cancel(booking_id):
        db = DatabaseManager()
        booking = db.execute_query("SELECT * FROM bookings WHERE id=?", (booking_id,), fetch=True)
        if not booking:
            return False
        if booking[0][5] in ("in_house", "departed"):
            return ErrorHandler.show_error(ErrorHandler.BIZ_STATUS, "Cannot void an active/departed booking.")
        if booking[0][5] == "reserved":
            Room.set_status(booking[0][2], "vacant")
        return db.execute_query("UPDATE bookings SET status='voided' WHERE id=?", (booking_id,))
