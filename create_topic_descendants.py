import sqlite3
import csv
import os


def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def find_and_store_descendants(cursor, conn, topic):
    cursor.execute("SELECT s FROM topics WHERE prefLabel = ?", (topic,))
    topic_url = cursor.fetchone()
    if topic_url:
        cursor.execute("SELECT prefLabel FROM topics WHERE broader = ?", (topic_url[0],))
        children = cursor.fetchall()
        for child in children:
            child_topic = child[0]
            # Check if the pair already exists
            cursor.execute("SELECT COUNT(*) FROM topic_descendants WHERE topic = ? AND descendant = ?", (topic, child_topic))
            if cursor.fetchone()[0] == 0:  # If no entry exists, insert new pair
                cursor.execute("INSERT INTO topic_descendants (topic, descendant) VALUES (?, ?)", (topic, child_topic))
            find_and_store_descendants(cursor, conn, child_topic)


def main():
    # Direct path specification for clarity
    database_path = '/Users/ahmetokur/Desktop/bachelor_app/data/app_data.db'
    conn = create_connection(database_path)
    if conn is not None:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topic_descendants (
                topic TEXT NOT NULL,
                descendant TEXT NOT NULL,
                PRIMARY KEY (topic, descendant)
            );
        """)
        conn.commit()

        cursor.execute("SELECT prefLabel FROM topics")
        topics = cursor.fetchall()

        for topic_tuple in topics:
            topic = topic_tuple[0]
            find_and_store_descendants(cursor, conn, topic)
            conn.commit()

        conn.close()  # Ensure the connection is closed after operations
        print("Finished populating the topic_descendants table.")
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
