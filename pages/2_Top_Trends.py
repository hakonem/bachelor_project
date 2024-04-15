import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime, timedelta
from Home import papers


#***************
# RESET FUNCTION
#***************

def reset_input():
    # Clear inputs for TOP TRENDS
    st.session_state.timeframe = None
    if 'trend_interval' in st.session_state:
        del st.session_state['trend_interval']
    st.session_state.number_topics = 0
 

#****************
# TITLE/HELP TEXT
#****************

st.header('TOP TRENDS')
st.subheader('Discover which AI topics were the top trending over the last week, month, year or the time interval of your choice.')
st.markdown('You can choose up to 10 top trends to show.')


#********
# WIDGET
#********


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

# Define default values for start_interval and end_interval
start_interval = datetime.strptime('2018-01-01', '%Y-%m-%d')
end_interval = datetime.strptime('2022-01-01', '%Y-%m-%d')

if timeframe == 'Last 7 days':
    end_interval = date.today()
    start_interval = end_interval-timedelta(days=7)
elif timeframe == 'Last month':
    end_interval = date.today()
    start_interval = end_interval-timedelta(days=30)
elif timeframe == 'Last year':
    end_interval = date.today()
    start_interval = end_interval-timedelta(days=365)
elif timeframe == 'Custom':
    # If custom timeframe supplied
    trend_interval = st.sidebar.slider(
        'Select date range (MM-YYYY)',
        min_value=papers['date'].min(),
        max_value=papers['date'].max(),
        value=(start_interval, end_interval),
        format='MM/YYYY',
        key='trend_interval'
    )
    start_interval, end_interval = trend_interval

start_interval = pd.to_datetime(start_interval)
end_interval = pd.to_datetime(end_interval)

reset = st.sidebar.button('Reset', on_click=reset_input, key='reset')


#**************
# VISUALIZATION 
#**************

if number_topics:

    placeholder = st.empty()

    # Filter papers by selected date range
    filtered_papers = papers[(papers['date'] >= start_interval) & (papers['date'] <= end_interval)]

    # Stack the topic columns and count occurrences
    tag_counts = filtered_papers[['topic1', 'topic2', 'topic3', 'topic4', 'topic5']].stack().value_counts()

    # Sort the tag counts in descending order
    sorted_tag_counts = tag_counts.sort_values(ascending=False)

    if number_topics is not None:
        number_topics = int(number_topics)
    else:
        number_topics = 0
    
    tag_counts = sorted_tag_counts.head(number_topics)

    # EnrichMyData colour scheme
    start_color = (142, 45, 226, 255)  # (R, G, B, A)
    end_color = (94, 173, 225, 255)    # (R, G, B, A)

    if number_topics == 1:
        color_gradient = [start_color]
    else:
        color_gradient = [(start_color[0] + (end_color[0] - start_color[0]) * i / (number_topics - 1), start_color[1] + (end_color[1] - start_color[1]) * i / (number_topics - 1), 
                            start_color[2] + (end_color[2] - start_color[2]) * i / (number_topics - 1), start_color[3] + (end_color[3] - start_color[3]) * i / (number_topics - 1))
                        for i in range(number_topics)]

    # Convert the color gradient to Plotly color format (rgba)
    colors = [f'rgba{color}' for color in color_gradient]

    if sorted_tag_counts.empty: 
        st.subheader('No data to show for this timeframe')
    elif number_topics > 0:
        
        # Create a new plot
        fig = px.bar(tag_counts, x=tag_counts.values, y=tag_counts.index, orientation='h', color=tag_counts.index, color_discrete_sequence=colors)

        fig.update_layout(
            title=f'Top {number_topics} AI topics from {start_interval.strftime("%b %Y")} to {end_interval.strftime("%b %Y")}',
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

    if reset:
        placeholder.empty()
