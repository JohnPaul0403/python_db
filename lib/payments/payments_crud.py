import sqlite3

# Connect to the database
def connect_to_database():
    """
    Connects to the database and returns a connection object.
    :return: A connection object to the database.
    """
    return sqlite3.connect('../database/payments.db')

def create_payment(cursor, user_id: str, data: dict) -> bool:
    """
    Inserts a new payment into the database.
    Args:
        cursor: The database cursor object.
        data (dict): A dictionary containing the payment data.
            - name (str): The name of the payment.
            - payment_id (str): The ID of the payment.
            - user_id (str): The ID of the user.
    Returns:
        bool: True if the payment was successfully inserted, False otherwise.
    """
    try:
        cursor.execute("""INSERT INTO payments (name, payment_id, user_id, date) VALUES (?, ?, ?)""", (data["order_id"], data["id"], user_id, data["created_at"]))
        return True
    except Exception as e:
        print(e)
        return False

def read_payments(cursor, user_id: str) -> any:
    """
    Retrieves all the payments associated with a given user ID from the database.
    Parameters:
        cursor (Cursor): The database cursor object.
        user_id (str): The ID of the user.
    Returns:
        bool or list of tuples: False if an exception occurred during the execution of the SQL query, or a list of tuples representing the retrieved payments.
    """
    try:
        cursor.execute("""SELECT * FROM payments WHERE user_id = ?""", (user_id,))
        result = cursor.fetchall()
        payments = list(map(lambda x : {"id": x[0], "name": x[1], "payment_id": x[2], "user_id": x[3], "date": x[4]}, result))
        return payments
    except Exception as e:
        print(e)
        return False

def update_payment(cursor, data: dict) -> bool:
    """
    Updates a payment in the database.
    Args:
        cursor: The database cursor object.
        data (dict): A dictionary containing the updated payment data.
            - name (str): The name of the payment.
            - payment_id (str): The ID of the payment.
            - user_id (str): The ID of the user.
    Returns:
        bool: True if the payment was successfully updated, False otherwise.
    """
    try:
        cursor.execute("""UPDATE payments SET name = ?, payment_id = ? WHERE user_id = ?""", (data["name"], data["payment_id"], data["user_id"]))
        return True
    except Exception as e:
        print(e)
        return False
    
def delete_payments(cursor, user_id: str) -> bool:
    """
    Deletes all the payments associated with a given user ID from the database.
    Parameters:
        cursor (Cursor): The database cursor object.
        user_id (str): The ID of the user.
    Returns:
        bool: True if the payments were successfully deleted, False otherwise.
    """
    try:
        cursor.execute("""DELETE FROM payments WHERE user_id = ?""", (user_id,))
        return True
    except Exception as e:
        print(e)
        return False