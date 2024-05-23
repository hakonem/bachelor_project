import pandas as pd
import sqlite3
import os


# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("SQLite version:", sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    return conn


# Function to create tables
def create_tables(conn):
    # SQL statements for creating the tables with the corresponding column names
    papers_sql = """CREATE TABLE IF NOT EXISTS papers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT UNIQUE,
                        title TEXT,
                        categories TEXT,
                        abstract TEXT,
                        submission_date DATE,
                        authors_parsed TEXT
                    );"""

    topics_sql = """CREATE TABLE IF NOT EXISTS topics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        s TEXT UNIQUE,
                        prefLabel TEXT,
                        altLabel TEXT,
                        description TEXT,
                        broader TEXT,
                        level INTEGER
                    );"""

    tagged_papers_sql = """CREATE TABLE IF NOT EXISTS tagged_papers (
                               url TEXT,
                               date DATE,
                               title TEXT,
                               abstract TEXT,
                               topic1 TEXT,
                               topic2 TEXT,
                               topic3 TEXT,
                               topic4 TEXT,
                               topic5 TEXT,
                               FOREIGN KEY (url) REFERENCES papers (url)
                           );"""

    # Execute to create table statements
    try:
        c = conn.cursor()
        c.execute(papers_sql)
        c.execute(topics_sql)
        c.execute(tagged_papers_sql)
        conn.commit()
    except sqlite3.Error as e:
        print(e)


# Function to create indexes to speed up queries
def create_indexes(conn):
    try:
        c = conn.cursor()
        # Create indexes
        c.execute("CREATE INDEX IF NOT EXISTS idx_topics_s ON topics(s);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_topics_prefLabel ON topics(prefLabel);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_topics_broader ON topics(broader);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_topics_level ON topics(level);")
        conn.commit()
        print("Indexes created successfully.")
    except sqlite3.Error as e:
        print(e)


# Function to import CSV data into the database
def import_csv_to_db(csv_file_path, table_name, conn):
    df = pd.read_csv(csv_file_path)
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data imported successfully into {table_name}.")
    except sqlite3.Error as e:
        print(e)


# Main function to create and populate the database
def main():
    database = 'app_data.db'
    conn = create_connection(database)
    if conn is not None:
        create_tables(conn)

        # List of CSV files to populate the database tables
        csv_files = [
            ('kaggle_dump_full.csv', 'papers'),
            ('topic_tree_with_levels.csv', 'topics'),
            ('tagged_papers_full.csv', 'tagged_papers')
        ]

        # Checking each CSV file exists in the location before importing
        for csv_file_path, table_name in csv_files:
            if not os.path.isfile(csv_file_path):
                print(f"The file {csv_file_path} does not exist. Skipping import for {table_name}.")
            else:
                # If the file exists, import it into the corresponding table
                import_csv_to_db(csv_file_path, table_name, conn)

        # Create indexes after tables are populated
        create_indexes(conn)

        # Close the connection to the database
        conn.close()
    else:
        print("Error! Cannot create the database connection.")


if __name__ == '__main__':
    main()
