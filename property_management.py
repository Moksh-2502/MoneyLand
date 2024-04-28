

import sqlite3


def init_property_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS property
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  address TEXT,
                  price REAL,
                  latitude REAL,
                  longitude REAL,
                  tenure INTEGER,  -- New column for tenure
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()


def add_property(user_id, address, price, latitude, longitude, tenure):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO property (user_id, address, price, latitude, longitude, tenure) VALUES (?, ?, ?, ?, ?, ?)", 
                  (user_id, address, price, latitude, longitude, tenure))
        property_id = c.lastrowid  # Get the ID of the last inserted row
        conn.commit()
        return property_id  # Return the property ID
    except sqlite3.Error as e:
        print("Error adding property:", e)
        return None
    finally:
        conn.close()
        
def get_properties():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM property")
    properties = c.fetchall()
    conn.close()
    return properties


def get_property_by_address(address):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM property WHERE address=?", (address,))
    property = c.fetchone()
    conn.close()
    if property:
        property_dict = {
            'id': property[0],
            'user_id': property[1],
            'address': property[2],
            'price': property[3],
            'latitude': property[4],
            'longitude': property[5],
            'tenure': property[6]
        }
        return property_dict
    else:
        return None
