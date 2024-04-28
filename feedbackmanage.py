import sqlite3

# Initialize the feedback database
def init_feedback_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  message TEXT,
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

def add_feedback(user_id, message):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO feedback (user_id, message) VALUES (?, ?)", (user_id, message))
        conn.commit()
    except sqlite3.Error as e:
        print("Error adding feedback:", e)
    finally:
        conn.close()

import sqlite3

def get_feedback():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT message FROM feedback")
    feedbacks = c.fetchall()
    conn.close()
    return feedbacks



# Initialize the feedback database
init_feedback_db()
