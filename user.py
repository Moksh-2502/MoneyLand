import sqlite3

def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  email TEXT UNIQUE,
                  phone TEXT,
                  password TEXT)''')
    conn.commit()
    conn.close()

def delete_entry():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''DELETE FROM users
                 WHERE id=3;''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    delete_entry()
