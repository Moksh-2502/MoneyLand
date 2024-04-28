import sqlite3

def delete_data_from_table(table_name):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(f"DELETE FROM {table_name}")
        conn.commit()
        print(f"Data deleted from {table_name} table.")
    except sqlite3.Error as e:
        print(f"Error deleting data from {table_name} table:", e)
    finally:
        conn.close()

def delete_data_from_all_tables():
    tables = [ 'property', 'property_info', 'bookmark', 'investment', 'feedback']  # Add the names of all your tables here
    for table_name in tables:
        delete_data_from_table(table_name)

# Call the function to delete data from all tables
delete_data_from_all_tables()


import sqlite3

def reset_sequence(table_name):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        # SQL statement to delete rows from sqlite_sequence table
        c.execute("DELETE FROM sqlite_sequence WHERE name = ?", (table_name,))
        
        conn.commit()
        conn.close()
        print(f"Sequence reset for table '{table_name}' successfully.")
    except sqlite3.Error as e:
        print("Error resetting sequence:", e)

# Call the function with the name of the table you want to reset the sequence for
reset_sequence('property')
