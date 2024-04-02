import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta


# Define global variables
DEFAULT_END_DATE = datetime.now()
DEFAULT_START_DATE = DEFAULT_END_DATE - timedelta(days=365)


#**************************
# FUNCTIONS TO RESET INPUT
#**************************
def clear_input1():
    # Clear inputs for TOPIC SEARCH
    st.session_state.selected_topic = []
    st.session_state.topic_interval = (DEFAULT_START_DATE, DEFAULT_END_DATE)

def clear_input2():
    # Clear inputs for TOP TRENDS
    st.session_state.timeframe = None
    st.session_state.number_topics = 0
    if 'trend_interval' in st.session_state:
        del st.session_state['trend_interval']

def clear_input3():
    # Clear inputs for PAPER SEARCH
    st.session_state. paper_topics = []
    st.session_state.paper_interval = (DEFAULT_START_DATE, DEFAULT_END_DATE)
   


#******************************************************************************************************
# TOPIC SEARCH
# User can search for one or more topics to display in a line graph.
# Once topics have been selected, user can also input a custom date range (default: Jan 2018-Jan 2022).
#******************************************************************************************************
def topic_search_widget(papers, topics): 
    with st.sidebar.expander('TOPIC SEARCH'):
        selected_topic = st.multiselect(
            'Select one or more topics to explore',
            topics,
            help='Start typing to see matching topics',
            key='selected_topic',
            max_selections=10,
            placeholder='Choose a topic',
        )

        # Initialize topic_interval with global variables
        topic_interval = (DEFAULT_START_DATE, DEFAULT_END_DATE)
        topic_start_date, topic_end_date = topic_interval

        if selected_topic:
            topic_interval = st.slider(
                'Select date range',
                min_value=papers['submission_date'].min(),
                max_value=papers['submission_date'].max(),
                value=(topic_start_date, topic_end_date),
                format='MM/YYYY',
                key='topic_interval',
            )
            topic_start_date, topic_end_date = topic_interval

        clear1 = st.button('Clear', on_click=clear_input1, key='clear1')

    topics_params = {
        'selected_topic': selected_topic,
        'topic_interval': topic_interval,
        'clear1': clear1
    }

    return topics_params
    
#*******************************************************************************************
# TOP TRENDS
# User selects a time interval (week, month, year or custom) and how many topics to display.
# The app displays a bar chart showing the top # topics over the given time interval.
#*******************************************************************************************
def top_trends_widget(papers):
    with st.sidebar.expander('TOP TRENDS'):
        number_topics = 0
        number_topics = st.number_input(
            'Number of topics to show',
            min_value=0,
            max_value=10,
            value=0,
            key='number_topics',
        )

        timeframe=None
        if number_topics > 0:
            timeframe = st.radio(
                'Select time interval',
                ['Last 7 days', 'Last month', 'Last year', 'Custom'],
                index=None,
                key='timeframe',
            )

        # Initialize default values for trend_interval
        trend_interval = (DEFAULT_START_DATE, DEFAULT_END_DATE)
        trend_start_date, trend_end_date = trend_interval

        if timeframe == 'Last 7 days':
            trend_end_date = date.today()
            trend_start_date = trend_end_date-timedelta(days=7)
        elif timeframe == 'Last month':
            trend_end_date = date.today()
            trend_start_date = trend_end_date-timedelta(days=30)
        elif timeframe == 'Last year':
            trend_end_date = date.today()
            trend_start_date = trend_end_date-timedelta(days=365)
        elif timeframe == 'Custom':
            # If custom timeframe supplied
            trend_interval = st.slider(
                'Select date range',
                min_value=papers['submission_date'].min(),
                max_value=papers['submission_date'].max(),
                value=(trend_start_date, trend_end_date),
                format='MM/YYYY',
                key='trend_interval'
            )
            trend_start_date, trend_end_date = trend_interval

        trend_start_date = pd.to_datetime(trend_start_date)
        trend_end_date = pd.to_datetime(trend_end_date)

        clear2 = st.button('Clear', on_click=clear_input2, key='clear2')

    trends_params = {
        'trend_interval': (trend_start_date, trend_end_date),
        'number_topics': number_topics,
        'clear2': clear2
    }

    return trends_params

# *****************************************************************************************************************
# PAPER SEARCH
# User selects one or more topics. They may also specify additional search parameters: time interval and author(s).
# The app returns a list of papers (displayed in a table) matching the search criteria.
# *****************************************************************************************************************

def paper_search_widget(papers, topics):
    with st.sidebar.expander('PAPER SEARCH'):
        # Input for selected topics
        paper_topics = st.multiselect(
            'Select one or more topics',
            topics,
            help='Start typing to see matching topics',
            key='paper_topics',
            max_selections=5,
            placeholder='Choose a topic',
        )
        
        # Initialize default values for trend_interval
        paper_interval = (DEFAULT_START_DATE, DEFAULT_END_DATE)
        paper_start_date, paper_end_date = paper_interval

        if paper_topics:
            # Input for additional date range
            paper_interval = st.slider(
                'Do you want to narrow down search by date range (MM-YYYY)?',
                value=(paper_start_date, paper_end_date),
                min_value=papers['submission_date'].min(),
                max_value=papers['submission_date'].max(),
                format='MM-YYYY',
                key='paper_interval',
            )
            paper_start_date, paper_end_date = paper_interval

        clear3 = st.button('Clear', on_click=clear_input3, key='clear3')

    papers_params = {
        'paper_topics': paper_topics,
        'paper_interval': (paper_start_date, paper_end_date),
        'clear3': clear3
    }

    return papers_params


