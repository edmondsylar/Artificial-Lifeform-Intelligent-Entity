# this file is going to handle the Database connections and any configurations.
import sqlite3

# database = database_1.db
conn = sqlite3.connect(
    database="database_1.db"
)

cur = conn.cursor()

def _create_table(table_name, columns):
    col_list = []
    for col in columns:
        col_list.append(col[0] + " " + col[1])
    # Join the list elements with commas
    col_str = ", ".join(col_list)
    # Create the SQL statement to create the table
    sql = f"CREATE TABLE {table_name} ({col_str})"
    print(sql)
    input(":")

    # Execute the SQL statement
    cur.execute(sql)
    # Commit the changes to the database
    conn.commit()
    # Close the connection
    conn.close()

    pass

def _insert_information(table, data):
    pass

def _update_table_information(table, id, information):
    pass

def delete_table_information(table, id):
    pass

# create messages table
_create_table(
    'messages',
    [('author_1_content', 'TEXT'), ('author_2_content', "TEXT"), ('conversation_id', 'id'), ('conversation Context', "TEXT")]
)

# create live context table
_create_table(
    'live_context',
    [('context', "TEXT"), ('context_id', "id")]
)