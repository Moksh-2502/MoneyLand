import sqlite3

def create_bookmark_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Create bookmark table
    c.execute('''CREATE TABLE IF NOT EXISTS bookmark
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  property_id INTEGER)''')  # Added a closing parenthesis here
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_bookmark_table()

