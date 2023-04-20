import os
import sqlite3
import csv
from create_relationships import db_path, get_connection

def main():
    # Query DB for list of married couples
    married_couples = get_married_couples()

    # Save all married couples to CSV file
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'married_couples.csv')
    save_married_couples_csv(married_couples, csv_path)

def get_married_couples():
    all_relationship_query = "SELECT person1.name, person2.name, start_date FROM relationships JOIN people person1 ON person1_id = person1.id JOIN people person2 ON person2_id = person2.id WHERE relationships.type = 'spouse';"
    con = get_connection()
    if con:
        cursor = con.cursor()
        cursor.execute(all_relationship_query)
        all_relationships = cursor.fetchall()
        con.close()
        return all_relationships
    return False

def save_married_couples_csv(married_couples, csv_path):
    csv_header = ["Person 1", 'Person 2', 'Anniversery']
    csv_file = open(csv_path, 'w+', newline='')
    with csv_file:
        write = csv.writer(csv_file)
        write.writerow(csv_header)
        for couple in married_couples:
            write.writerow(couple)
    return csv_path

if __name__ == '__main__':
   main()
