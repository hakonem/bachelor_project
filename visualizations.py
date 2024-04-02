import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

    
#********************************************************************
# WELCOME SCREEN
# Introductory text that appears in the main window upon loading app.
#********************************************************************
def welcome():
    intro_text = '''Use the widgets in the sidebar to search for topics and papers.
        
- **TOPIC SEARCH**: Select one or more topics to explore to discover how their trends change over time.  
- **TOP TRENDS**: Select a date interval and the number of topics to display - find out the top # trends in this period.
'''
        
    intro = st.empty()
    with intro.container():
        st.title('AI PulsePoint')
        st.header('Interactive tool for visualizing AI topic trends in academic papers')
        st.markdown(intro_text)

    return intro

# ***************************************************************************************************************
# VISUALIZATION 1: TIME SERIES (TOPIC SEARCH)
# User searches for a specific topic and a line graph showing the trend for that topic is displayed.
# User can select an optional second topic for comparison - then both line graphs are displayed in the same plot.
# Line graph displays all dates found in the dataset unless user chooses custom date range. 
# ***************************************************************************************************************

def render_topics(intro, papers, selected_topic, topic_interval, clear1):
    # Unpack the topic_interval tuple
    topic_start_date, topic_end_date = topic_interval

    # Define EnrichMyData colours
    custom_palette = ['#8b26e4', '#68a7e4', '#caa3f0', '#5bbce2', '#5c54dc', '#8448e3', '#ac7cec', '#d9dcf7', '#7375e4', '#6c8ce4']

    if selected_topic:
        intro.empty()
        placeholder = st.empty()

        fig = px.line()

        for i, topic in enumerate(selected_topic, start=1):
           
            # Filter papers by selected topic and group by date
            selected_papers = papers[papers[['tag1', 'tag2', 'tag3', 'tag4', 'tag5']].eq(topic).any(axis=1)]
            selected_papers_by_date = selected_papers.groupby('submission_date').size()

            # Set submission_date as the index
            selected_papers_by_date.index = pd.to_datetime(selected_papers_by_date.index)

            # Filter papers by selected date range
            selected_papers_by_date_filtered = selected_papers_by_date.loc[topic_start_date:topic_end_date]

            # Resample by week and sum to bin the submission dates by week
            selected_papers_by_period = selected_papers_by_date_filtered.resample('M').sum()

            # Add to subplot with custom colour
            fig.add_scatter(x=selected_papers_by_period.index, y=selected_papers_by_period.values, mode='lines', name=topic, line=dict(color=custom_palette[i % len(custom_palette)]))

        # Update axis labels and layout
        fig.update_xaxes(title_text="Submission date", title_font_size=16, tickfont=dict(size=14), tickformat='%b %Y', showgrid=True)
        fig.update_yaxes(title_text="Number of tagged papers", title_font_size=16, tickfont=dict(size=14), showgrid=True)

        # Update title
        if len(selected_topic) > 1:
            fig.update_layout(title=f'Tracking the trends of your selected topics...', title_font_size=24)
        else:
            fig.update_layout(title=f'Tracking the trend of your selected topic...', title_font_size=24)

        # Show plot
        with placeholder.container():
            st.header('TOPIC SEARCH')
            st.plotly_chart(fig)

    if clear1:
        placeholder = st.empty()
        
# ***************************************************************************************
# VISUALIZATION 2: TOP TRENDS
# User selects a time interval (week, month, year or custom) and how many topics to show.
# The app displays a bar chart showing the top # topics over the given time interval.
# ***************************************************************************************
def render_trends(intro, papers, trend_interval, number_topics, clear2):
    if number_topics:
        intro.empty()
        placeholder = st.empty() 
        
    # Unpack the topic_interval tuple
    trend_start_date, trend_end_date = trend_interval

    # Filter papers by selected date range
    filtered_papers = papers[(papers['submission_date'] >= trend_start_date) & (papers['submission_date'] <= trend_end_date)]

    # Stack the tag columns and count occurrences
    tag_counts = filtered_papers[['tag1', 'tag2', 'tag3', 'tag4', 'tag4', 'tag5']].stack().value_counts()

    # Sort the tag counts in descending order
    sorted_tag_counts = tag_counts.sort_values(ascending=False)

    # Convert number_topics to an integer if it's not None
    if number_topics is not None:
        number_topics = int(number_topics)
    else:
        number_topics = 0

    tag_counts = sorted_tag_counts.head(number_topics)

    # EnrichMyData colour scheme
    start_color = (142, 45, 226, 255)  
    end_color = (94, 173, 225, 255)   

    # Convert the start and end colors to the range [0, 1]
    start_color_norm = np.array(start_color) / 255.0
    end_color_norm = np.array(end_color) / 255.0

    if number_topics == 1:
        color_gradient = [start_color]
    else:
        color_gradient = [tuple((start_color_norm * (1 - i/(number_topics - 1)) + end_color_norm * (i/(number_topics - 1))) * 255)
                        for i in range(number_topics)]

    # Convert the color gradient to Plotly color format (rgba)
    colors = [f'rgba{color}' for color in color_gradient]

    if sorted_tag_counts.empty:
        with placeholder.container():
            st.header('TOP TRENDS')
            st.subheader('No data to show for this timeframe')
    elif number_topics > 0:
        
        # Create a new plot
        fig = px.bar(tag_counts, x=tag_counts.values, y=tag_counts.index, orientation='h', color=tag_counts.index, color_discrete_sequence=colors)

        fig.update_layout(
            title=f'Top {number_topics} AI topics from {trend_start_date.strftime("%b %Y")} to {trend_end_date.strftime("%b %Y")}',
            xaxis_title='Number of tagged papers',
            xaxis=dict(
                tickfont=dict(size=14),
                titlefont=dict(size=16)
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
        with placeholder.container():
            st.header('TOP TRENDS')
            st.plotly_chart(fig)

    if clear2:
        placeholder = st.empty()

    
# *****************************************************************************************************************
# VISUALIZATION 3: PAPER SEARCH
# User selects one or more topics. They may also specify additional search parameters: time interval and author(s).
# The app returns a list of papers (displayed in a table) matching the search criteria.
# *****************************************************************************************************************

def render_papers(intro, papers, paper_topics, paper_interval, clear3):  

    # Initialize filtered_df
    filtered_df = papers.copy()

    if paper_topics:
        intro.empty()
        placeholder = st.empty()

        if paper_topics:
            # Filter papers by selected topics
            for topic in paper_topics:
                filtered_df = papers[(papers['tag1'] == topic) | 
                                        (papers['tag2'] == topic) | 
                                        (papers['tag3'] == topic) | 
                                        (papers['tag4'] == topic) | 
                                        (papers['tag5'] == topic)]
            if paper_interval:
                # Unpack the paper_interval tuple
                paper_start_date, paper_end_date = paper_interval
                # Filter papers by selected date range
                filtered_df = filtered_df[(filtered_df['submission_date'] >= paper_start_date) & (filtered_df['submission_date'] <= paper_end_date)]

        selected_cols=['url','title','submission_date']
        filtered_df = filtered_df[selected_cols].reset_index(drop=True)
        filtered_df['submission_date'] = filtered_df['submission_date'].astype(str).str.split(' ').str[0]

        # Show results in dataframe
        with placeholder.container():
            st.header('PAPER SEARCH')
            st.markdown(f'Number of papers found: {filtered_df.shape[0]}')

            # User selection for sorting
            sort_table = st.radio(
                'Sort by:',
                options=['Title', 'Submission Date']
            )

            if sort_table == 'Title':
                filtered_df = filtered_df.sort_values(by='title')
            elif sort_table == 'Submission Date':
                filtered_df = filtered_df.sort_values(by='submission_date')

            # Begin HTML table
            html_table = "<table><tr><th>Title</th><th>Submission Date</th></tr>"
            # Add rows to HTML table with clickable URLs
            for index, row in filtered_df.iterrows():
                html_table += f"<tr><td><a href='{row['url']}' target='_blank'>{row['title']}</a></td><td>{row['submission_date']}</td></tr>"
            # End HTML table
            html_table += "</table>"
            # Display HTML table
            st.write(html_table, unsafe_allow_html=True)
    
        if clear3:
            placeholder = st.empty()