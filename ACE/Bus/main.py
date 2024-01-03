import sqlite3
from flask import Flask, request, jsonify

class BusConfig:
    def __init__(self):
        self.conn = sqlite3.connect('OchestratorDB.db')
        self.c = self.conn.cursor()

    def System_init(self):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()

        # Create the 'South_bound_bus' table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS South_bound_bus (
                id INTEGER PRIMARY KEY,
                layer TEXT,
                message TEXT,
                system_prompt TEXT
            )
        ''')

        # Create the 'north_bound_bus' table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS north_bound_bus (
                id INTEGER PRIMARY KEY,
                layer TEXT,
                message TEXT,
                system_prompt TEXT
            )
        ''')

        # Create the 'conversation' table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS conversation (
                id INTEGER PRIMARY KEY,
                role TEXT,
                content TEXT
            )
        ''')

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()

        print('Database Setup Complete')

    def close_connection(self):
        self.conn.close()

    def create_south_bound_bus(self, layer, message, system_prompt):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("INSERT INTO South_bound_bus (layer, message, system_prompt) VALUES (?, ?, ?)", (layer, message, system_prompt))
        conn.commit()
        conn.close()

    def read_south_bound_bus(self, id):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("SELECT * FROM South_bound_bus WHERE id = ?", (id,))
        result = c.fetchone()
        conn.close()
        return result

    def update_south_bound_bus(self, id, layer, message, system_prompt):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("UPDATE South_bound_bus SET layer = ?, message = ?, system_prompt = ? WHERE id = ?", (layer, message, system_prompt, id))
        conn.commit()
        conn.close()

    def delete_south_bound_bus(self, id):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("DELETE FROM South_bound_bus WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    def get_all_south_bound_bus(self, limit):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("SELECT * FROM South_bound_bus LIMIT ?", (limit,))
        results = c.fetchall()
        conn.close()
        return results

    def create_north_bound_bus(self, layer, message, system_prompt):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("INSERT INTO north_bound_bus (layer, message, system_prompt) VALUES (?, ?, ?)", (layer, message, system_prompt))
        conn.commit()
        conn.close()

    def read_north_bound_bus(self, id):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("SELECT * FROM north_bound_bus WHERE id = ?", (id,))
        result = c.fetchone()
        conn.close()
        return result

    def update_north_bound_bus(self, id, layer, message, system_prompt):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("UPDATE north_bound_bus SET layer = ?, message = ?, system_prompt = ? WHERE id = ?", (layer, message, system_prompt, id))
        conn.commit()
        conn.close()

    def delete_north_bound_bus(self, id):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("DELETE FROM north_bound_bus WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    def get_all_north_bound_bus(self, limit):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("SELECT * FROM north_bound_bus LIMIT ?", (limit,))
        results = c.fetchall()
        conn.close()
        return results

    def create_conversation(self, role, content):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("INSERT INTO conversation (role, content) VALUES (?, ?)", (role, content))
        conn.commit()
        conn.close()

    def read_conversation(self, id):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("SELECT * FROM conversation WHERE id = ?", (id,))
        result = c.fetchone()
        conn.close()
        return result

    def update_conversation(self, id, role, content):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("UPDATE conversation SET role = ?, content = ? WHERE id = ?", (role, content, id))
        conn.commit()
        conn.close()

    def delete_conversation(self, id):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("DELETE FROM conversation WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    def get_all_conversations(self, limit):
        conn = sqlite3.connect('OchestratorDB.db')
        c = conn.cursor()
        c.execute("SELECT * FROM conversation LIMIT ?", (limit,))
        results = c.fetchall()
        conn.close()
        return results
    


app = Flask(__name__)
db = BusConfig()

# create the db tables
db.System_init()

@app.route('/bus_p', methods=['POST'])
def post_data():
    data = request.get_json()
    table = data.get('table')
    record = data.get('data')

    if table == 'South_bound_bus':
        db.create_south_bound_bus(record['layer'], record['message'], record['system_prompt'])
    elif table == 'north_bound_bus':
        db.create_north_bound_bus(record['layer'], record['message'], record['system_prompt'])
    elif table == 'conversation':
        db.create_conversation(record['role'], record['content'])

    return jsonify({'message': 'Record created successfully'}), 201

@app.route('/bus_g', methods=['GET'])
def get_data():
    data = request.get_json()
    table = data.get('table')
    params = data.get('params')
    limit = params.get('limit')

    if table == 'South_bound_bus':
        result = db.get_all_south_bound_bus(limit)
    elif table == 'north_bound_bus':
        result = db.get_all_north_bound_bus(limit)
    else:
        result = []

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True, port=5012, host='0.0.0.0')