import sqlite3

def connect_to_database():
    return sqlite3.connect('../database/users.db')

def create_user(cursor, data: dict) -> bool:
    """
    Insert a new user into the database.
    Args:
        cursor: The database cursor object.
        data: A tuple containing the user data (name, email, password, pro_plan).
    Returns:
        bool: True if the user was successfully inserted, False otherwise.
    """
    print(data)
  
    # Check if the email already exists in the database
    if read_user(cursor, data["email"]):
        return False
    
    try:
        cursor.execute("""INSERT INTO users (name, email, password) VALUES (?, ?, ?)""", (data["username"], data["email"], data["password"]))
        return True
    except:
        return False
    
def set_token(cursor, data: dict) -> bool:
    """
    Set the token for a user in the database.
    Args:
        cursor: The database cursor object.
        data: A tuple containing the user ID and token.
    Returns:
        bool: True if the token was successfully set, False otherwise.
    """
    try:
        cursor.execute("""UPDATE users SET token = ? WHERE id = ?""", (data["token"], data["user_id"]))
        return True
    except:
        return False
    
def read_user(cursor, email: str) -> any:
    """
    Retrieve a user from the database using their email.
    Parameters:
        cursor (any): The database cursor object.
        user_id (str): The email of the user to retrieve.
    Returns:
        any: The user data as a tuple if found, or None if not found.
    """
    try:
        cursor.execute("""SELECT * FROM users WHERE email = ?""", (email,))
        return cursor.fetchone()
    except:
        return None
    
def read_user_by_id(cursor, user_id: int):
    """
    Retrieve a user from the database using their ID.
    Parameters:
        cursor (any): The database cursor object.
        user_id (str): The email of the user to retrieve.
    Returns:
        any: The user data as a tuple if found, or None if not found.
    """
    try:
        cursor.execute("""SELECT * FROM users WHERE id = ?""", (user_id,))
        return cursor.fetchone()
    except:
        return None
    
def update_user(cursor, data) -> bool:
    """
    Update the user information in the database.
    Parameters:
    - cursor: The database cursor object.
    - data: A tuple containing the updated user information in the format (name, email, password, pro_plan, id).
    Returns:
    - bool: True if the user information was successfully updated, False otherwise.
    """
    try:
        cursor.execute("""
            UPDATE users 
            SET name = ?, email = ?, pro_plan = ? 
            WHERE id = ?
        """, (data['name'], data['email'], data['pro_plan'], data['id']))
        return True
    except:
        return False
    
def update_user_pass(cursor, data) -> bool:
    """
    Update the user information in the database.
    Parameters:
    - cursor: The database cursor object.
    - data: A tuple containing the updated user information in the format (name, email, password, pro_plan, id).
    Returns:
    - bool: True if the user information was successfully updated, False otherwise.
    """
    try:
        cursor.execute("""
            UPDATE users 
            SET name = ?, email = ?, password = ?, pro_plan = ? 
            WHERE id = ?
        """, (data['name'], data['email'], data["password"], data['pro_plan'], data['id']))
        return True
    except:
        return False
    
def delete_user(cursor, user_id) -> bool:
    """
    Deletes a user from the database.
    Args:
        cursor: The database cursor to execute the delete query.
        user_id: The ID of the user to be deleted.
    Returns:
        bool: True if the user was successfully deleted, False otherwise.
    """
    try:
        cursor.execute("""DELETE FROM users WHERE id = ?""", (user_id,))
        return True
    except:
        return False
