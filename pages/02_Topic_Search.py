import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from Home import create_connection, close_connection

# Establish connection and get cursor
conn = create_connection()
cursor = conn.cursor()

# Fetch topics and date range
cursor.execute("SELECT prefLabel FROM topics")
topics = [topic[0] for topic in cursor.fetchall()]

cursor.execute("SELECT date(min(date)), date(max(date)) FROM tagged_papers")
start_date_str, end_date_str = cursor.fetchone()
start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")


# TITLE/HELP TEXT

# UI components
st.header('TOPIC SEARCH')
st.subheader('Search for a specific topic and see how the interest in that topic has changed over time.')
st.markdown(
    'It\'s possible to search for up to 5 topics for comparison. You can also narrow down the date range '
    'using the slider.')


# WIDGET

selected_topics = st.sidebar.multiselect(
    'Select one or more topics to explore',
    topics,
    help='Start typing to see matching topics',
    key='selected_topic',
    max_selections=5,
    placeholder='Choose a topic',
)


# VISUALIZATION

def get_data_for_topic(selected_topics, start_date_str, end_date_str):
    """
    SQL query to fetch data from database

    Parameters:
    selected_topics (list): Values of the user input from the topic multiselect widget
    start_date_str (str): Start date from slider converted to string
    end_date_str (str): End date from slider converted to string

    Returns:
    data: Values returned by the SQL query
    
    """
    
    # Join with the topic_descendants table to fetch data for selected topics and their descendants
    placeholders = ','.join(['?' for _ in selected_topics])
    query = f"""
        SELECT strftime('%Y-%m', tp.date) AS month, COUNT(*)
        FROM tagged_papers tp
        JOIN topic_descendants td ON td.descendant IN (tp.topic1, tp.topic2, tp.topic3, tp.topic4, tp.topic5)
        WHERE tp.date BETWEEN ? AND ?
            AND td.topic IN ({placeholders})
        GROUP BY month
        ORDER BY month
    """

    # Parameters include the start date, end date, and selected topics
    params = [start_date_str, end_date_str] + list(selected_topics)

    print("Query:", query)
    print("Parameters:", params)

    cursor.execute(query, params)
    data = cursor.fetchall()

    return data

# Only show the slider if at least one topic has been selected
if selected_topics:
    date_interval = st.sidebar.slider(
        'Select date range (MM-YYYY)',
        value=(start_date, end_date),
        min_value=start_date,
        max_value=end_date,
        format='MM-YYYY',
        key='date_interval',
    )
    start_date, end_date = date_interval
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Visualization placeholder
    placeholder = st.empty()
    fig = px.line()

    # Fetch and plot data for each selected topic
    for topic in selected_topics:
        data = get_data_for_topic([topic], start_date_str, end_date_str)  # Make sure to pass list of one topic
        if not data:
            st.info(f"No data available for topic: {topic}")
        else:
            df = pd.DataFrame(data, columns=['month', 'count'])
            df['month'] = pd.to_datetime(df['month'], format="%Y-%m")
            df.set_index('month', inplace=True)
            all_months = pd.date_range(start=df.index.min().replace(day=1), end=df.index.max().replace(day=1),
                                       freq='MS')
            df_all_months = pd.DataFrame(index=all_months)
            df_merged = df_all_months.merge(df, how='left', left_index=True, right_index=True)
            df_merged['count'].fillna(0, inplace=True)
            fig.add_scatter(x=df_merged.index, y=df_merged['count'], mode='lines+markers', name=topic)

    # Update and show plot
    fig.update_layout(title='Tracking the trends of your selected topics...')
    placeholder.plotly_chart(fig)

# Close connection
close_connection(conn)

# FOOTER with logo at the bottom
with st.container():
    st.write("---")  # A horizontal line to separate the footer

    # enrichMyData logo:
    logo_path = "./images/enrichmydata-logo.png"  # Update this path
    st.image(logo_path, use_column_width=False, width=100)
