import streamlit as st
import pandas as pd

@st.cache_data
def get_papers(file):
    papers = pd.read_csv(file)
    papers['date'] = pd.to_datetime(papers['date'])
    return papers

@st.cache_data
def get_topics(file):
    topics = pd.read_csv(file)
    topics = topics['prefLabel']
    return topics

papers = get_papers('../tagged_papers_with_topics.csv')
topics = get_topics('../topic_tree_with_levels.csv')

def main():
    intro = st.empty()
    with intro.container():
        st.title('AI PulsePoint')
        st.header('Interactive tool for visualizing AI topic trends')
   

if __name__ == "__main__":
    main()