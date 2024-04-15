import streamlit as st
from db_manager import fetch_data
import pandas as pd


st.set_page_config(layout="wide")

def get_topics(file):
    topics = pd.read_csv(file)
    topics = topics['prefLabel']
    return topics

papers = fetch_data()
topics = get_topics('../topic_tree_with_levels.csv')

def main():
    intro = st.empty()
    with intro.container():
        st.title('AI PulsePoint')
        st.header('Interactive tool for visualizing AI topic trends')
        st.markdown('''Welcome to AI PulsePoint! This app will allow you to visualize and explore trends in AI topics across scientific papers submitted to [arXiv.org](https://arxiv.org/).
                Use the widgets in the sidebar to get started.
        
- **TOPIC SEARCH**: Select one or more topics to discover how their trends change over time.  
- **TOP TRENDS**: Select the number of topics to display and a date interval - find out the top trends in this period.
- **PAPER SEARCH**: Search for relevant papers based on topic, with the option to narrow down the serch by date interval.
                    ''')
   

if __name__ == "__main__":
    main()
    print(papers.shape)