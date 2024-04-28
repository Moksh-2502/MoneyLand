import sqlite3

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

init_feedback_db()
