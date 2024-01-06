import sqlite3

def connect_to_database():
    """
    Connects to the database and returns a connection object.
    :return: A connection object to the database.
    """
    return sqlite3.connect('../database/assitants.db')

#____________________Assistants crud for openai___________________#
def create_assistant(cursor, data: dict) -> bool:
    """
    Inserts a new assistant into the database.
    Args:
        cursor: The database cursor object.
        data (dict): A dictionary containing the assistant data.
            - name (str): The name of the assistant.
            - assistant_id (str): The ID of the assistant.
            - gpt_model (str): The GPT model of the assistant.
    Returns:
        bool: True if the assistant was successfully inserted, False otherwise.
    """

    for file in data["files"]:
        fdata = {
            "file" : file,
            "assistant_id" : data["assistant_id"]
        }
        create_file(cursor, fdata)
    cursor.execute("""INSERT INTO assistants (name, assistant_id, gpt_model, user_id) VALUES (?, ?, ?, ?)""", (data["name"], data["assistant_id"], data["gpt-model"], data["user_id"]))
    return True
   

def read_assistants(cursor, user_id: str) -> any:
    """
    Retrieves all the assistants associated with a given user ID from the database.
    Parameters:
        cursor (Cursor): The database cursor object.
        user_id (str): The ID of the user.
    Returns:
        bool or list of tuples: False if an exception occurred during the execution of the SQL query, or a list of tuples representing the retrieved assistants.
    """
    try:
        cursor.execute("""SELECT * FROM assistants WHERE user_id = ?""", (user_id,))
        result = cursor.fetchall()
        assistants = list(map(lambda x : {"id": x[0], "name": x[1], "assistant_id": x[3], "gpt_model": x[4], "files": [{"id": file[0], "file_id" : file[1], "assistant_id" : file[2]} for file in read_files(cursor, x[3])]}, result))
        return assistants
    except Exception as e:
        print(e)
        return False
    
def read_assistant_by_id(cursor, assistant_id: str) -> any:
    """
    Retrieves an assistant from the database by its ID.
    :param cursor: The database cursor to execute the SQL query.
    :param assistant_id: The ID of the assistant to retrieve.
    :type assistant_id: str
    :return: The assistant retrieved from the database, or False if an error occurs.
    :rtype: bool or tuple
    """
    try:
        cursor.execute("""SELECT * FROM files WHERE assistant_id = ?""", (assistant_id,))
        files = list(map(lambda x : {"id": x[0], "file": x[1], "assistant_id": x[2]}, cursor.fetchall()))
        cursor.execute("""SELECT * FROM assistants WHERE assistant_id = ?""", (assistant_id,))

        x = cursor.fetchone()
        return {"id": x[0], "name": x[1], "assistant_id": x[3], "gpt_model": x[4], "files": files}
    except Exception as e:
        print(e)
        return False

def update_assistant(cursor, data: dict) -> bool:
    """
    Updates the information of an assistant in the database.
    Args:
        cursor: The database cursor used to execute the SQL query.
        data (dict): A dictionary containing the updated information for the assistant. It should have the following keys:
            - name (str): The new name of the assistant.
            - assistant_id (str): The ID of the assistant to be updated.
            - gpt_model (str): The new GPT model to be associated with the assistant.
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        cursor.execute("""UPDATE assistants SET name = ?, assistant_id = ?, gpt_model = ? WHERE assistant_id = ?""", (data["name"], data["assistant_id"], data["gpt_model"], data["assistant_id"]))
        return True
    except Exception as e:
        print(e)
        return False

def delete_assistants(cursor, user_id: str) -> bool:
    """
    Deletes assistants from the database based on the provided user_id.
    :param cursor: The database cursor object.
    :param user_id: The user_id of the assistants to be deleted.
    :return: True if the assistants were successfully deleted, False otherwise.
    """
    try:
        cursor.execute("""DELETE FROM assistants WHERE user_id = ?""", (user_id,))
        return True
    except Exception as e:
        print(e)
        return False

def delete_assistant(cursor, assistant_id: str) -> bool:
    """
    Delete an assistant from the assistants table based on the assistant_id.
    Parameters:
        cursor (object): The database cursor object.
        assistant_id (str): The ID of the assistant to be deleted.
    Returns:
        bool: True if the assistant is successfully deleted, False otherwise.
    """
    try:
        cursor.execute("""DELETE FROM assistants WHERE assistant_id = ?""", (assistant_id,))
        return True
    except Exception as e:
        print(e)
        return False

#____________________Files crud for openai___________________#

#-----------------It only stores the file_id-----------------#
#------it is connected to the user via the assistant_id------#

def create_file(cursor, data: dict) -> bool:
    """
    Creates a file entry in the database.
    Args:
        cursor: The database cursor object.
        data (dict): A dictionary containing the data for the file entry.
    Returns:
        bool: True if the file entry is successfully created, False otherwise.
    """
    try:
        cursor.execute("""INSERT INTO files (file_id, assistant_id) VALUES (?, ?)""", (data["file_id"], data["assistant_id"]))
        return True
    except:
        return False

def read_files(cursor, assistant_id: str) -> any:
    """
    Read files from the database based on the provided cursor and data.
    Args:
        cursor: The database cursor object.
        data: A dictionary containing the data needed to execute the query. It must have the
              "assistant_id" key.
    Returns:
        The result of the executed query as a list of tuples, where each tuple represents a row
        from the "files" table. If an error occurs during the execution of the query, False is
        returned.
    """
    try:
        cursor.execute("""SELECT * FROM files WHERE assistant_id = ?""", (assistant_id,))
        return cursor.fetchall()
    except:
        return False
    
def read_file_by_id(cursor, data: dict) -> any:
    """
    Reads a file from the database by its ID.
    Parameters:
        cursor (Cursor): The database cursor.
        data (dict): A dictionary containing the file ID.
    Returns:
        any: The file data if found, False otherwise.
    """
    try:
        cursor.execute("""SELECT * FROM files WHERE file_id = ?""", (data["file_id"],))
        return cursor.fetchone()
    except:
        return False

def update_file(cursor, data: dict) -> bool:
    """
    Updates a file in the database.
    Args:
        cursor: The database cursor.
        data (dict): The data for updating the file.
    Returns:
        bool: True if the file is updated successfully, False otherwise.
    """
    try:
        cursor.execute("""UPDATE files SET file_id = ? WHERE id = ?""", (data["file_id"]))
        return True
    except:
        return False

def delete_files(cursor, data: dict) -> bool:
    """
    Deletes files from the database based on the provided assistant ID.
    Args:
        cursor: The database cursor object.
        data (dict): A dictionary containing the assistant ID.
    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    try:
        cursor.execute("""DELETE FROM files WHERE assistant_id = ?""", (data["assistant_id"],))
        return True
    except:
        return False

def delete_file(cursor, file_id: str) -> bool:
    """
    Deletes a file from the database.
    Parameters:
        cursor (Cursor): The database cursor.
        data (dict): A dictionary containing the data of the file to be deleted. It should have the following key:
            - file_id (int): The ID of the file to be deleted.
    Returns:
        bool: True if the file is successfully deleted, False otherwise.
    """
    try:
        cursor.execute("""DELETE FROM files WHERE file_id = ?""", (file_id,))
        return True
    except:
        return False