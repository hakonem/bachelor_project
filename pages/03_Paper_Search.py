import streamlit as st
import datetime
import pandas as pd
from Home import create_connection, close_connection

st.header('PAPER SEARCH')
st.subheader('Search for papers submitted to arXiv.org using various search criteria.')
st.markdown('Use the sidebar to filter papers by topics and date range.')

conn = create_connection()
cursor = conn.cursor()

# Fetch topics and date range
cursor.execute("SELECT prefLabel FROM topics")
topics = cursor.fetchall()
topic_list = [topic[0] for topic in topics]

cursor.execute("SELECT MIN(date), MAX(date) FROM tagged_papers")
min_date, max_date = cursor.fetchone()
start_date = datetime.datetime.strptime(min_date, "%Y-%m-%d")
end_date = datetime.datetime.strptime(max_date, "%Y-%m-%d")


# WIDGET

selected_topic = st.sidebar.multiselect(
    'Select topics',
    topic_list,
    help='Start typing to see matching topics',
    key='selected_topic',
    placeholder='Choose a topic',
)


def get_data_for_papers(descendants, start_date_str, end_date_str):
    """
    SQL query to fetch data from database

    Parameters:
    descendants (list): List of topics that are subtopics of the topic input by the user in the multiselect widget
    start_date_str (str): Start date from slider converted to string
    end_date_str (str): End date from slider converted to string

    Returns:
    data: Values returned by the SQL query
    len(data): Length of the data list
    
    """
    
    conn = create_connection()
    cursor = conn.cursor()

    # Prepare the query with the correct number of placeholders for descendants
    # Since we are checking five topic columns, we need to repeat the list of placeholders for each topic column.
    placeholders = ','.join(['?'] * len(descendants))
    all_placeholders = ', '.join([placeholders] * 5)  # Repeat placeholders for each of the five topic columns
    query = f"""
    SELECT DISTINCT title, url, strftime('%Y-%m-%d', date) as date
    FROM tagged_papers
    WHERE (topic1 IN ({placeholders}) OR
           topic2 IN ({placeholders}) OR
           topic3 IN ({placeholders}) OR
           topic4 IN ({placeholders}) OR
           topic5 IN ({placeholders}))
          AND date BETWEEN ? AND ?
    """

    # Parameters include the descendants repeated for each topic column and the date range
    params = descendants * 5 + [start_date_str, end_date_str]  # Repeat the list of descendants for each topic column

    # Execute the query
    cursor.execute(query, tuple(params))
    data = cursor.fetchall()

    close_connection(conn)

    return data, len(data)


if selected_topic:
    # Fetch precomputed descendants for the selected topics
    placeholders = ','.join(['?'] * len(selected_topic))
    cursor.execute(f"SELECT DISTINCT descendant FROM topic_descendants WHERE topic IN ({placeholders})", tuple(selected_topic))
    descendants = [desc[0] for desc in cursor.fetchall()]
    descendants.extend(selected_topic)  # Include the main topics themselves

    date_interval = st.sidebar.slider(
        'Do you want to narrow down the search by date range (MM-YYYY)?',
        value=(start_date, end_date),
        min_value=start_date,
        max_value=end_date,
        format='MM-YYYY',
        key='date_interval',
    )
    start_date, end_date = date_interval
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    data, number_papers_found = get_data_for_papers(descendants, start_date_str, end_date_str)

    if not data:
        st.write('No papers found.')
    else:
        # Convert search output into dataframe for display
        df = pd.DataFrame(data, columns=['Title', 'URL', 'Submission date'])

        # Display results
        st.write('Number of papers found:', str(number_papers_found))
        st.dataframe(
            df,
            column_config={
                "URL": st.column_config.LinkColumn(
                )
            },
            use_container_width=True,
            hide_index=True,
        )

close_connection(conn)

# FOOTER with logo at the bottom
with st.container():
    st.write("---")  # A horizontal line to separate the footer

    # enrichMyData logo:
    logo_path = "./images/enrichmydata-logo.png"  # Update this path
    st.image(logo_path, use_column_width=False, width=100)

