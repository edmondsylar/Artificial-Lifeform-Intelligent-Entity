# this is going to be controllers for the bridge.
import os
import sqlite3

# create database connection
conn = sqlite3.connect('bus.db')

def create_required_tables():
    cursor = conn.cursor()
    # create table if it does not exist (north bound bus)
    cursor.execute("""CREATE TABLE IF NOT EXISTS north_bound_bus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        layer TEXT NOT NULL,
        messages TEXT NOT NULL
    )""")


    # create table if it does not exist (south bound bus)
    cursor.execute("""CREATE TABLE IF NOT EXISTS south_bound_bus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        layer TEXT NOT NULL,
        messages TEXT NOT NULL
    )""")



    # create table if it does not exist (conversation)
    cursor.execute("""CREATE TABLE IF NOT EXISTS conversation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        layer TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL
    )""")

    conn.commit()
    conn.close()
    



# create function to insert messages into the bus
def insert_message(bus, layer, messages):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {bus} (layer, messages) VALUES (?, ?)", (layer, messages))
    conn.commit()
    conn.close()

# create function to get messages from the bus
def get_messages(bus, layer, limit):
    cursor = conn.cursor()
    cursor.execute(f"SELECT messages FROM {bus} WHERE layer = ? LIMIT ?", (layer, limit))
    results = cursor.fetchall()
    conn.close()
    return results[0][0]



# create function to insert messages into the conversation
def insert_conversation(layer, role, content):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO conversation (layer, role, content) VALUES (?, ?)", (layer, role, content))
    conn.commit()
    conn.close()

# create function to get a given number of messages from the conversation
def get_conversation(layer, limit):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM conversation WHERE layer = ? LIMIT ?", (layer, limit))
    results = cursor.fetchall()
    conn.close()
    return results