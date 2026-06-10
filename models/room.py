from db import DatabaseManager

class Room:
    @staticmethod
    def add(room_number, room_type, price, status="vacant"):
        return DatabaseManager().execute_query("INSERT INTO rooms (room_number, type, price, status) VALUES (?,?,?,?)", (room_number, room_type, price, status))

    @staticmethod
    def get_all():
        return DatabaseManager().execute_query("SELECT * FROM rooms", fetch=True)

    @staticmethod
    def get_available():
        return DatabaseManager().execute_query("SELECT * FROM rooms WHERE status='vacant'", fetch=True)

    @staticmethod
    def update(room_id, room_number, room_type, price, status):
        return DatabaseManager().execute_query("UPDATE rooms SET room_number=?, type=?, price=?, status=? WHERE id=?", (room_number, room_type, price, status, room_id))

    @staticmethod
    def delete(room_id):
        return DatabaseManager().execute_query("DELETE FROM rooms WHERE id=?", (room_id,))

    @staticmethod
    def set_status(room_id, status):
        return DatabaseManager().execute_query("UPDATE rooms SET status=? WHERE id=?", (status, room_id))
