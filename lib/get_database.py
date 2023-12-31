import sqlite3

# Connect to the database
connection = sqlite3.connect('../database/users.db')
connection_as =  sqlite3.connect('../database/assitants.db')

# Create a cursor
cursor = connection.cursor()
cursor_as = connection_as.cursor()

#Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        pro_plan INTEGER DEFAULT 0
    )
""")

cursor_as.execute("""
    CREATE TABLE IF NOT EXISTS assistants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id TEXT NOT NULL,
        assistant_id TEXT NOT NULL,
        gpt_model TEXT NOT NULL
    )
""")

cursor_as.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id TEXT NOT NULL,
        assistant_id TEXT NOT NULL
    )
""")

# Commit the changes
connection.commit()
connection_as.commit()

# Close the cursor
cursor.close()
cursor_as.close()
