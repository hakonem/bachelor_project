import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from Home import papers, topics


#***************
# RESET FUNCTION
#***************

def reset_input():
    # Clear inputs for TOPIC SEARCH
    st.session_state.selected_topic = []
    st.session_state.start_date = datetime.strptime('01-2018', '%m-%Y')
    st.session_state.end_date = datetime.strptime('01-2022', '%m-%Y')


#****************
# TITLE/HELP TEXT
#****************

st.header('TOPIC SEARCH')
st.subheader('Search for a specific topic and see how the interest in that topic has changed over time.')
st.markdown('It\'s possible to search for up to 9 optional topics for comparison. You can also narrow down the date range using the slider.')


#********
# WIDGET
#********

selected_topic = st.sidebar.multiselect(
    'Select one or more topics to explore',
    topics,
    help='Start typing to see matching topics',
    key='selected_topic',
    max_selections=10,
    placeholder='Choose a topic',
)

if selected_topic:
    start_date = datetime.strptime('01-2018', '%m-%Y')
    end_date = datetime.strptime('01-2022', '%m-%Y')

    topic_interval = st.sidebar.slider(
        'Select date range (MM-YYYY)',
        value=(start_date, end_date),
        min_value=papers['date'].min(),
        max_value=papers['date'].max(),
        format='MM-YYYY',
        key='topic_interval',
    )
    start_date, end_date = topic_interval


reset = st.sidebar.button('Reset', on_click=reset_input, key='reset')

 

#**************
# VISUALIZATION 
#**************

# EnrichMyData colours
custom_palette = ['#8b26e4', '#68a7e4', '#caa3f0', '#5bbce2', '#5c54dc', '#8448e3', '#ac7cec', '#d9dcf7', '#7375e4', '#6c8ce4']

if selected_topic:
    
    placeholder = st.empty()

    fig = px.line()

    for i, topic in enumerate(selected_topic, start=1):
        # Filter papers by selected topic and group by date
        selected_papers = papers[papers[['topic1', 'topic2', 'topic3', 'topic4', 'topic5']].eq(topic).any(axis=1)]
        selected_papers_by_date = selected_papers.groupby('date').size()

        # Set submission_date as the index
        selected_papers_by_date.index = pd.to_datetime(selected_papers_by_date.index)

        # Filter papers by selected date range
        selected_papers_by_date_filtered = selected_papers_by_date.loc[start_date:end_date]

        # Resample by week and sum to bin the submission dates by week
        selected_papers_by_week = selected_papers_by_date_filtered.resample('W').sum()

        # Check if the DataFrame is empty
        if selected_papers_by_week.empty:
            st.info(f"No data available for topic: {topic}")
        else:
            # Add to subplot with custom colour
            fig.add_scatter(x=selected_papers_by_week.index, y=selected_papers_by_week.values, mode='lines+markers', name=topic, line=dict(color=custom_palette[i % len(custom_palette)]))

            # Update axis labels and layout
            fig.update_xaxes(title_text="Submission date", title_font_size=16, tickfont=dict(size=14), tickformat='%b %Y', showgrid=True)
            fig.update_yaxes(title_text="Number of tagged papers", title_font_size=16, tickmode='linear', dtick=1, tickfont=dict(size=14), showgrid=True)

            # Update title
            if len(selected_topic) > 1:
                fig.update_layout(title=f'Tracking the trends of your selected topics...', title_font_size=24)
            else:
                fig.update_layout(title=f'Tracking the trend of your selected topic...', title_font_size=24)

            # Show plot
            placeholder.plotly_chart(fig)


    if reset:
        placeholder.empty()