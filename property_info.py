import sqlite3
from flask import session


def init_property_info_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS property_info
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  property_id INTEGER,
                  user_id INTEGER,
                  description TEXT,
                  investing_reason TEXT,
                  profit_scope TEXT,
                  image_path TEXT,
                  FOREIGN KEY (property_id) REFERENCES property(idb),
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()


def add_property_info(property_id, user_id, description, investing_reason, profit_scope, image_paths):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("INSERT INTO property_info (property_id, user_id, description, investing_reason, profit_scope) VALUES (?, ?, ?, ?, ?)",
                  (property_id, user_id, description, investing_reason, profit_scope))
        property_info_id = c.lastrowid  

        for image_path in image_paths:
            c.execute("INSERT INTO property_images (property_id, image_path) VALUES (?, ?)",
                      (property_info_id, image_path))
        
        conn.commit()
    except sqlite3.Error as e:
        print("Error adding property information:", e)
    finally:
        conn.close()

def get_property_info_by_id(property_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM property_info WHERE property_id=?", (property_id,))
    property_info = c.fetchall()
    conn.close()
    return property_info


