import sqlite3

def create_property_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS property
                 (idb INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  address TEXT,
                  price REAL,
                  latitude REAL,
                  longitude REAL,
                  tenure INTEGER,  -- New column for tenure
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
        create_property_table()

