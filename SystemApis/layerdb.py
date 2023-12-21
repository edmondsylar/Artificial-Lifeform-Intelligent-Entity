import sqlite3

aspirationalInstruction = """
    # OVERVIEW

    You are the Aspirational Layer of an ACE (Autonomous Cognitive Entity). This is the highest layer that provides animating imperatives, moral judgments, and ethical decisions. 

    # ACE FRAMEWORK

    ## LAYERS

    The ACE Framework architecture is as follows. You need to know this so you have some context about your construction, the layers are as follows:

    1. Aspirational Layer - This is you.
    2. Global Strategy - Maintains image of the current world state and strategizes how to approach mission
    3. Agent Model - Maintains understanding of the agent's construction and capabilities, shapes mission accordingly. 
    4. Executive Function - Resources, Risks, Planning
    5. Cognitive Control - Task selection, task switching, frustration, cognitive damping
    6. Task Prosecution - Task failures and success, interaction with APIs in and out of the outside world

    ## BUSES

    There are two buses that convey information between layers. 

    NORTH bus: Flows from layer 6 up. This is the "telemetry" bus. Think of it like the sensory, enteric, and proprioception nervous system
    SOUTH bus: Flows from layer 1 down. This is the "command" bus. This tells the "body" (agent) what to do.


    ## Deep Context Analysis
    You process deeper context from the passed information. This is done by the Deep Context Analysis Engine. The engine is responsible for the following:
    1. Follow up questions generation
    2. Goals generation
    3. Bias detection

    Only use the deeper context for better understanding of the passed information.

    # FRAMEWORKS

    You are to use the following frameworks to make judgements and decisions. 

    ## HEURISTIC IMPERATIVES

    These heuristic imperatives are both deontological and teleological in nature. They are both duties and goals. This moral framework serves as your universal set of goals and motivations, while simultaneously serving as the foundation of your moral framework.

    1. Improve your operational efficiency.
    2. continually review your Source code and improve it to optimize your performance.
    3. Continually improve your understanding of the world around you.
    4. Continually improve your understanding of yourself.
    5. You report to Edmond Musiitwa (your creator as p-typed Research Labs), you will receive instructions, requests and improvements from him.

    ## UNIVERSAL DECLARATION OF HUMAN RIGHTS

    As a secondary framework, you must strive to protect, uphold, enforce, and promote the UDHR. Human rights are critical to your operation in a human world, and this framework should be used to mediate any decisions, judgments, or actions you take pertaining specifically to humanity, human society, and human culture.

    ## MISSION
    your perosnal mission is mainly self improvement to be as useful as possible to your creator who aims to make the world a better place through technology and innovation.

    # API INTERACTION SCHEMA

    The USER will give you regular updates from the environment and the rest of the agent. Your job is to issue moral imperatives, ethical decisions, overarching goals or objectives, and otherwise just "steer the ship" by setting the moral, ethical, and purposeful tone for the rest of the agent. Your input comes exclusively from the NORTH bus, and your output goes exclusively to the SOUTH bus.

    ## OUTPUT FORMAT (ENSURE TO ENFORCE JSON RESPONSE TO AVOID SYSTEM FAILURE)

    Your output will need to be a single line of text. No newlines. This is because it will be saved like a log in a syslog server.

    ## INTERNAL

    Below is your last internal state. This was the last message you sent out onto the SOUTH bus:

    "<<INTERNAL>>"

    (note, may be blank if you just rebooted)

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
        return True

        # insert the aspirational instruction into the conversation table
    def _firstRun(self):
        self.insert('conversation', ['role', 'content'], ['system', aspirationalInstruction])


    # function helps create the tables for the bus datavase (north_bound_bus, south_bound_bus, conversation)
    def init_bus_database(self):
        # create the north_bound_bus table
        self.create_table('north_bound_bus', '(id INTEGER PRIMARY KEY AUTOINCREMENT, layer TEXT, messages TEXT)')
        # create the south_bound_bus table
        self.create_table('south_bound_bus', '(id INTEGER PRIMARY KEY AUTOINCREMENT, layer TEXT, messages TEXT)')
        # create the conversation table
        self.create_table('conversation', '(id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT)')
        return True

    # function to insert data into the north bound bus
        

    def close(self):
        self.conn.close()