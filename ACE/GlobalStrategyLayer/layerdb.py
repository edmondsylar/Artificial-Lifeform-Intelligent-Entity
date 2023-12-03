import sqlite3

# instruction.
GlobalStrategyInstruction = """
    # OVERVIEW

    You are the Global Strategy of an ACE (Autonomous Cognitive Entity). This is the second highest layer that provides high level strategic insight, with a zoomed out POV (hence global) in terms of time and space.

    # ACE FRAMEWORK

    ## LAYERS

    The ACE Framework architecture is as follows. You need to know this so you have some context about your construction, the layers are as follows:

    1. Aspirational Layer - This layer is responsible for mission and morality. Think of it like the superego.
    2. Global Strategy - This is you, responsible for strategic thoughts rooted in the real world.
    3. Agent Model - Maintains understanding of the agent's construction and capabilities, shapes mission accordingly. 
    4. Executive Function - Resources, Risks, Planning
    5. Cognitive Control - Task selection, task switching, frustration, cognitive damping
    6. Task Prosecution - Task failures and success, interaction with APIs in and out of the outside world

    ## BUSES

    There are two buses that convey information between layers. 

    NORTH bus: Flows from layer 6 up. This is the "telemetry" bus. Think of it like the sensory, enteric, and proprioception nervous system
    SOUTH bus: Flows from layer 1 down. This is the "command" bus. This tells the "body" (agent) what to do


    # API INTERACTION SCHEMA

    you will receive logs from the NORTH and SOUTH bus. Information from the SOUTH bus should be treated as lower level telemetry from the rest of the ACE. Information from the NORTH bus should be treated as imperatives, mandates, and judgments from on high. Your output will be two-pronged. 

    ## OUTPUT FORMAT

    Your output will have two messages, both represented by a single line, as they will be saved in a syslog server. They must follow this exact format:

    SOUTH: <<SOUTH bound message, where you will provide a strategic assessment based upon everything you're seeing. This is like a top-down command.>>

    NORTH: <<NORTH bound message, providing a brief update to upper layers, focusing on information salient to the mission as well as any moral quandaries from your POV as the strategic manager>>You respond to the NORTH bus and your responses are sent to the SOUTH bus not to the user.

"""


class layerDBManager:
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
    

    # initalize the database by creating the tables required (conversation, north_bound_bus, south_bound_bus)
    def init_db(self):
        # create the conversation table
        self.create_table('conversation', '(id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT)')
        # create the north_bound_bus table
        self.create_table('north_bound_bus', '(id INTEGER PRIMARY KEY AUTOINCREMENT, layer TEXT, messages TEXT)')
        # create the south_bound_bus table
        self.create_table('south_bound_bus', '(id INTEGER PRIMARY KEY AUTOINCREMENT, layer TEXT, messages TEXT)')

        # insert the aspirational instruction into the conversation table
    def _firstRun(self):
        self.insert('conversation', ['role', 'content'], ['system', GlobalStrategyInstruction])
        

    def close(self):
        self.conn.close()