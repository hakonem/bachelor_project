import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from datetime import date, timedelta
from Home import create_connection, close_connection

conn = create_connection()  # connect to the database
cursor = conn.cursor()  # get a cursor

# SQL query to return start and end dates from database (in string format)
cursor.execute("SELECT date(min(date)) date FROM tagged_papers")
start_date_str = cursor.fetchone()[0]
cursor.execute("SELECT date(max(date)) date FROM tagged_papers")
end_date_str = cursor.fetchone()[0]
# Convert string dates to datetime objects for use in widgets
start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")


# TITLE/HELP TEXT

st.header('TOP TRENDS')
st.subheader('Discover which AI topics were the top trending over the last week, month, year or the time interval of '
             'your choice.')
st.markdown('You can choose up to 10 top trends to show.')


# WIDGET

number_topics = st.sidebar.number_input(
    'Number of topics to display',
    min_value=0,
    max_value=10,
    key='number_topics',
)

timeframe = 0
if number_topics > 0:
    timeframe = st.sidebar.radio(
        'Select time interval',
        ['Last 7 days', 'Last month', 'Last year', 'Custom'],
        index=None,
        key='timeframe',
    )
print(number_topics)


if timeframe == 'Last 7 days':
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
elif timeframe == 'Last month':
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
elif timeframe == 'Last year':
    end_date = date.today()
    start_date = end_date - timedelta(days=365)
elif timeframe == 'Custom':
    # If custom timeframe supplied
    trend_interval = st.sidebar.slider(
        'Select date range (MM-YYYY)',
        min_value=start_date,
        max_value=end_date,
        value=(start_date, end_date),
        format='MM/YYYY',
        key='trend_interval'
    )
    start_date, end_date = trend_interval

# Convert start and end dates back to strings for SQL query
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')



# VISUALIZATION 

def get_data_for_timeframe(start_date_str, end_date_str, number_topics):
    """
    SQL query to fetch data from database

    Parameters:
    start_date_str (str): Start date from slider converted to string
    end_date_str (str): End date from slider converted to string
    number_topics (int): Value input by user in number input box

    Returns:
    data: Values returned by the SQL query
        
    """
    params = []

    # Append start and end date parameters for each topic column
    for _ in range(5):
        params.extend([start_date_str, end_date_str])

    # Append the number_topics parameter for the LIMIT clause
    params.append(number_topics)

    # SQL query template for each topic column
    query = f"""
        SELECT topic, COUNT(*) AS topic_count 
        FROM (
            SELECT topic1 AS topic FROM tagged_papers WHERE topic1 IS NOT NULL AND date BETWEEN ? AND ?
            UNION ALL
            SELECT topic2 AS topic FROM tagged_papers WHERE topic2 IS NOT NULL AND date BETWEEN ? AND ?
            UNION ALL
            SELECT topic3 AS topic FROM tagged_papers WHERE topic3 IS NOT NULL AND date BETWEEN ? AND ?
            UNION ALL
            SELECT topic4 AS topic FROM tagged_papers WHERE topic4 IS NOT NULL AND date BETWEEN ? AND ?
            UNION ALL
            SELECT topic5 AS topic FROM tagged_papers WHERE topic5 IS NOT NULL AND date BETWEEN ? AND ?
        ) AS subquery
        GROUP BY topic
        ORDER BY topic_count DESC
        LIMIT ?
    """

    print("Query:", query)
    print("Parameters:", params)

    cursor.execute(query, params)
    data = cursor.fetchall()

    return data


if number_topics:

    placeholder = st.empty()

    # Get data for the given date interval and number of trends
    data = get_data_for_timeframe(start_date_str, end_date_str, number_topics)
    print("Fetched data:", data)

    # Extract topics and counts from the data
    topics = [row[0] for row in data]
    counts = [row[1] for row in data]

    # EnrichMyData colour scheme
    start_color = (142, 45, 226, 255)  # (R, G, B, A)
    end_color = (94, 173, 225, 255)  # (R, G, B, A)

    if number_topics == 1:
        color_gradient = [start_color]
    else:
        color_gradient = [(start_color[0] + (end_color[0] - start_color[0]) * i / (number_topics - 1),
                           start_color[1] + (end_color[1] - start_color[1]) * i / (number_topics - 1),
                           start_color[2] + (end_color[2] - start_color[2]) * i / (number_topics - 1),
                           start_color[3] + (end_color[3] - start_color[3]) * i / (number_topics - 1))
                          for i in range(number_topics)]

    # Convert the color gradient to Plotly color format (rgba)
    colors = [f'rgba{color}' for color in color_gradient]

    if not data:
        st.subheader('No data to show for this timeframe')
    elif number_topics > 0:

        # Create a new plot
        fig = px.bar(data, x=counts, y=topics, orientation='h', color=topics, color_discrete_sequence=colors)

        fig.update_layout(
            title=f'Top {number_topics} AI topics from {start_date_str} to {end_date_str}',
            xaxis_title='Number of tagged papers',
            xaxis=dict(
                tickfont=dict(size=14),
                titlefont=dict(size=16),
                showgrid=True
            ),
            yaxis_title='Topic',
            yaxis=dict(
                tickfont=dict(size=14),
                titlefont=dict(size=16)
            ),
            yaxis_categoryorder='total ascending',  # Order bars by topic count
            title_font_size=24,
            showlegend=False
        )

        # Show plot
        placeholder.plotly_chart(fig)

close_connection(conn)

# FOOTER with logo at the bottom
with st.container():
    st.write("---")  # A horizontal line to separate the footer

    # enrichMyData logo:
    logo_path = "./images/enrichmydata-logo.png"  # Update this path
    st.image(logo_path, use_column_width=False, width=100)
