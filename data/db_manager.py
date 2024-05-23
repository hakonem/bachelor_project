import streamlit as st
import sqlite3
import pandas as pd


def create_connection(db_file):
    #Create a database connection to a SQLite database
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    return conn

def fetch_data(db_file='topics_data.db', table_name='topics_data'):
    #Fetch data from the database and return it as a DataFrame
    try:
        conn = sqlite3.connect(db_file)
        data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        #Convert the 'date' column from string to datetime format
        data['date'] = pd.to_datetime(data['date'])
        return data
    except sqlite3.Error as e:
        print(e)
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

def create_table(conn):
    create_table_sql = """ 
    CREATE TABLE IF NOT EXISTS topics_data (
    url TEXT, 
    date DATETIME, 
    title TEXT, 
    abstract TEXT, 
    topic1 TEXT, 
    topic2 TEXT, 
    topic3 TEXT, 
    topic4 TEXT, 
    topic5 TEXT
);
"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

# Function to close the connection
def close_connection(conn):
    if conn is not None:
        conn.close()
        
