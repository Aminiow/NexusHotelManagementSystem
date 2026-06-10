from db import DatabaseManager

class Customer:
    @staticmethod
    def add(name, phone, email, id_proof):
        return DatabaseManager().execute_query("INSERT INTO customers (name, phone, email, id_proof) VALUES (?,?,?,?)", (name, phone, email, id_proof))

    @staticmethod
    def get_all():
        return DatabaseManager().execute_query("SELECT * FROM customers", fetch=True)

    @staticmethod
    def update(cust_id, name, phone, email, id_proof):
        return DatabaseManager().execute_query("UPDATE customers SET name=?, phone=?, email=?, id_proof=? WHERE id=?", (name, phone, email, id_proof, cust_id))

    @staticmethod
    def delete(cust_id):
        return DatabaseManager().execute_query("DELETE FROM customers WHERE id=?", (cust_id,))
