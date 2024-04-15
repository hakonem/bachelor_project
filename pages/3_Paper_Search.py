import streamlit as st
from datetime import datetime
from Home import papers, topics


#***************
# RESET FUNCTION
#***************

def reset_input():
    # Clear inputs for PAPER SEARCH
    st.session_state.selected_topic = []
    st.session_state.start_date = datetime.strptime('01-2018', '%m-%Y')
    st.session_state.end_date = datetime.strptime('01-2022', '%m-%Y')
    st.session_state.date_interval = (st.session_state.start_date, st.session_state.end_date)


#****************
# TITLE/HELP TEXT
#****************

st.header('PAPER SEARCH')
st.subheader('Search for papers submitted to arXiv.org using various search criteria.')
st.markdown('''You can select up to 5 topics - only papers matching ALL selections will be returned. You also have the option to narrow down your search by specifying a date range.  
            
Results are returned in a table which can be sorted by title and date, with links to the relevant arXiv page.
            ''')


#********
# WIDGET
#********

# Input for selected topics
selected_topics = st.sidebar.multiselect(
    'Select one or more topics',
    topics,
    help='Start typing to see matching topics',
    key='selected_topic',
    max_selections=5,
    placeholder='Choose a topic',
)

if selected_topics:
    start_date = datetime.strptime('01-2018', '%m-%Y')
    end_date = datetime.strptime('01-2022', '%m-%Y')

    date_interval = st.sidebar.slider(
        'Do you want to narrow down search by date range (MM-YYYY)?',
        value=(start_date, end_date),
        min_value=papers['date'].min(),
        max_value=papers['date'].max(),
        format='MM-YYYY',
        key='date_interval',
    )
    start_date, end_date = date_interval

reset = st.sidebar.button('Reset', on_click=reset_input, key='reset')


#**************
# VISUALIZATION 
#**************

# Initialize filtered_df
filtered_df = papers.copy()

if selected_topics:

    # Filter papers by selected topics
    for topic in selected_topics:
        filtered_df = filtered_df[(filtered_df['topic1'] == topic) | 
                                (filtered_df['topic2'] == topic) | 
                                (filtered_df['topic3'] == topic) | 
                                (filtered_df['topic4'] == topic) | 
                                (filtered_df['topic5'] == topic)]
    if date_interval:
        # Filter papers by selected date range
        filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]

    selected_cols=['url','title','date']
    filtered_df = filtered_df[selected_cols].reset_index(drop=True)
    filtered_df['date'] = filtered_df['date'].astype(str).str.split(' ').str[0]

    number_papers_found = f'Number of papers found: {filtered_df.shape[0]}'

    if filtered_df.shape[0] > 1:
        # User selection for sorting
        sort_table = st.radio(
            'Sort by:',
            options=['Title', 'Submission Date (newest to oldest)', 'Submission Date (oldest to newest)'],
            key='sort_table'
        )

        if sort_table:
            if sort_table == 'Title':
                filtered_df = filtered_df.sort_values(by='title')
            elif sort_table == 'Submission Date (newest to oldest)':
                filtered_df = filtered_df.sort_values(by='date', ascending=False)
            else:
                filtered_df = filtered_df.sort_values(by='date', ascending=True)

    # Begin HTML table
    html_table = "<table><tr><th></th><th>Title</th><th>Submission Date</th></tr>"
    # Add rows to HTML table with clickable URLs
    for i, row in enumerate(filtered_df.iterrows(), start=1):
        html_table += f"<tr><td>{i}</td><td><a href='{row[1]['url']}' target='_blank'>{row[1]['title']}</a></td><td>{row[1]['date']}</td></tr>"
    # End HTML table
    html_table += "</table>"

    placeholder = st.empty()

    # Display results
    placeholder.write(number_papers_found + '\n' + html_table, unsafe_allow_html=True)

    if reset:
        placeholder.empty()
