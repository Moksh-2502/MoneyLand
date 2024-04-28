import sqlite3

def init_property_info_db():
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS property_info
                     (property_id INTEGER,
                      user_id INTEGER,
                      description TEXT,
                      investing_reason TEXT,
                      profit_scope TEXT,
                      image_path TEXT,
                      FOREIGN KEY (property_id) REFERENCES property(id),
                      FOREIGN KEY (user_id) REFERENCES users(id))''')
        conn.commit()
        print("Property info table initialized successfully")
    except sqlite3.Error as e:
        print("Error initializing property info table:", e)
    finally:
        conn.close()

# Call the function to initialize the property info table
init_property_info_db()
