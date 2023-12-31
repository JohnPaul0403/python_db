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

#Create first user
#cursor.execute("""INSERT INTO users (name, email, password, pro_plan) VALUES ('admin', 'admin@admin.com', 'admin_pass', 1)""")
email = 'johnpar2004@gmail.com'
#cursor.execute("""INSERT INTO users (name, email, password, pro_plan) VALUES ('John Paredes', ?, 'my_pass', 1)""", (email,))

#get_user
cursor.execute("""SELECT * FROM users""")
print(cursor.fetchall())

#create assistant
#cursor_as.execute("INSERT INTO assistants (name, user_id, assistant_id, gpt_model) VALUES ('ProjectBot', 3, 'asst_x824apYmRJibSkPy2wsTxBbE', 'gpt-3.5-turbo-1106')")
cursor_as.execute("SELECT * FROM assistants")
print(cursor_as.fetchall())

#create file
#cursor_as.execute("""INSERT INTO files (file_id, assistant_id) VALUES ('file-zgD45ZrfmD8439jYTbAPddYO', 'asst_x824apYmRJibSkPy2wsTxBbE')""")
cursor_as.execute("SELECT * FROM files")
print(cursor_as.fetchall())

# Commit the changes
connection.commit()
connection_as.commit()

# Close the cursor
cursor.close()
cursor_as.close()
