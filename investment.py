import sqlite3
def create_property_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS investment
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  property_id INTEGER,
                  investment INTEGER,
                  FOREIGN KEY (user_id) REFERENCES users(id),
                  FOREIGN KEY (property_id) REFERENCES property(id))''')


    conn.commit()
    conn.close()

if __name__ == "__main__":
        create_property_table()
