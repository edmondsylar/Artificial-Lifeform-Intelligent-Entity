import sqlite3

class DatabaseManager:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def create_table(self, table_name, table_definition):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {table_definition}")
        self.conn.commit()

    def insert(self, table_name, column_names, data):
        placeholders = ', '.join('?' * len(data))
        sql = f"INSERT INTO {table_name}({', '.join(column_names)}) VALUES ({placeholders})"
        self.cur.execute(sql, data)
        self.conn.commit()

    def update(self, table_name, column_values, condition):
        set_clause = ', '.join(f"{col} = ?" for col in column_values.keys())
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self.cur.execute(sql, list(column_values.values()))
        self.conn.commit()

    def delete(self, table_name, condition):
        sql = f"DELETE FROM {table_name} WHERE {condition}"
        self.cur.execute(sql)
        self.conn.commit()

    def select(self, table_name, columns, condition=None):
        sql = f"SELECT {', '.join(columns)} FROM {table_name}"
        if condition:
            sql += f" WHERE {condition}"
        self.cur.execute(sql)
        return self.cur.fetchall()

    def close(self):
        self.conn.close()



def mainTest():
    # Create an instance of the DatabaseManager
    db = DatabaseManager('bus.db')

    # Insert some data
    db.insert('north_bound_bus', ['layer', 'messages'], ['Layer1', 'Hello, North!'])
    db.insert('south_bound_bus', ['layer', 'messages'], ['Layer1', 'Hello, South!'])

    # Select and print all data from the tables
    print(db.select('north_bound_bus', ['*']))
    print(db.select('south_bound_bus', ['*']))

    # Close the database connection
    db.close()
