from datetime import datetime
from db import DatabaseManager


class Billing:
    @staticmethod
    def generate(booking_id, total_amount):
        return DatabaseManager().execute_query("INSERT INTO billing (booking_id, total_amount, payment_status) VALUES (?,?,'pending')", (booking_id, total_amount))

    @staticmethod
    def get_all():
        return DatabaseManager().execute_query("SELECT b.id, bk.id as booking_id, c.name, r.room_number, b.total_amount, b.payment_status, b.payment_date FROM billing b JOIN bookings bk ON b.booking_id = bk.id JOIN customers c ON bk.customer_id = c.id JOIN rooms r ON bk.room_id = r.id ORDER BY b.id DESC", fetch=True)

    @staticmethod
    def mark_paid(bill_id):
        return DatabaseManager().execute_query("UPDATE billing SET payment_status='settled', payment_date=? WHERE id=?", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bill_id))
