import sqlite3

def init_db():
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

def add_user(name, email, phone, password):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        # Check if the email already exists in the users table
        c.execute("SELECT COUNT(*) FROM users WHERE email = ?", (email,))
        existing_user_count = c.fetchone()[0]
        if existing_user_count > 0:
            print("Error: Email address already exists.")
            return False
        
        # Insert the new user if the email is unique
        c.execute("INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)", (name, email, phone, password))
        conn.commit()
        print("User added successfully.")
        return True
        
    except sqlite3.Error as e:
        print("Error adding user:", e)
        return False
        
    finally:
        conn.close()

def get_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

def get_user_by_email(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()
    if user:
        user_dict = {
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'phone': user[3],
            'password': user[4]
        }
        return user_dict
    else:
        return None
