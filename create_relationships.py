import os
import sqlite3
from faker import Faker
from random import randint, choice

# Determine the path of the database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'social_network.db')

def main():

    # Create a database connection
    conn = sqlite3.connect('people.db')

    # Create a cursor object
    c = conn.cursor()

    # Create the people table
    c.execute('''
        CREATE TABLE people (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            email TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')

#    populate_people_table()
    create_relationships_table()
    populate_relationships_table()

def create_relationships_table():
    #"""Creates the relationships table in the DB"""
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    create_relationships_table_query = "CREATE TABLE IF NOT EXISTS relationships(id INTEGER PRIMARY KEY, person1_id INTEGER NOT NULL, person2_id INTEGER NOT NULL, type TEXT NOT NULL, start_date DATE NOT NULL, FOREIGN KEY (person1_id) REFERENCES people (id), FOREIGN KEY (person2_id) REFERENCES people (id));"
    con = get_connection()
    if con:
        cursor = con.cursor()
        cursor.execute(create_relationships_table_query)
        con.commit()
        con.close()
        return True
    return False

def populate_relationships_table():
    #"""Adds 100 random relationships to the DB"""
    add_relationship_query = "INSERT INTO relationships (person1_id, person2_id, type, start_date) VALUES (?, ?, ?, ?);"
    fake = Faker()
    for i in range(100):
        person1_id = randint(1, 200)
        person2_id = randint(1, 200)
        while person2_id == person1_id:
            person2_id = randint(1, 200)
        rel_type = choice(('friend', 'spouse', 'partner', 'relative'))
        start_date = fake.date_between(start_date = '-50y', end_date = 'today')
        new_relationship = (person1_id, person2_id, rel_type, start_date)
        insert_row(add_relationship_query, new_relationship)
    return True


def create_people_table():
    #"""Creates the people table in the DB"""
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    create_people_table_query = "CREATE TABLE IF NOT EXISTS people(id INTEGER PRIMARY KEY, name TEXT NOT NULL);"
    con = get_connection()
    if con:
        cursor = con.cursor()
        cursor.execute(create_people_table_query)
        con.commit()
        con.close()
        return True
    return False

def populate_people_table():
    #"""Adds 100 random relationships to the DB"""
    add_people_query = "INSERT INTO people (id, name) VALUES (?, ?);"
    fake = Faker()
    for i in range(1, 201):
        name = fake.name().split()[0]
        new_people = (i, name)
        insert_row(add_people_query, new_people)
    return True

def insert_row(query, row):
    con = get_connection()
    if con:
        cursor = con.cursor()
        cursor.execute(query, row)
        con.commit()
        con.close()
        return True
    return False

def get_connection():
    try:
        con = sqlite3.connect(db_path)
        return con
    except Exception as e:
        return False
if __name__ == '__main__':
   main()
