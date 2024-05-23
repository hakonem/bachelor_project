import pandas as pd
from db_manager import create_connection, create_table


def import_csv_to_db(csv_file_path):
    df = pd.read_csv(csv_file_path)
    conn = create_connection('topics_data.db')
    if conn is not None:
        try:
            # Create the table if it doesn't exist
            create_table(conn)
            # Check if data already exists in the table
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM topics_data")
            existing_data = cursor.fetchone()[0]
            if existing_data == 0:  # If there are no existing rows
                    df.to_sql('topics_data', conn, if_exists='append', index=False)
                    print("Data imported successfully.")
            else:
                print("Data already exists in the table. Skipping import.")
        finally:
            conn.close()
