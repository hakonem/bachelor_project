import streamlit as st
from data_loader import fetch_and_clean_data, load_topics 
from widgets import topic_search_widget, top_trends_widget, paper_search_widget
from visualizations import welcome, render_topics, render_trends, render_papers


def main():
    # Fetch the data
    papers = fetch_and_clean_data()
    topics = load_topics()

    # Render welcome screen
    intro = welcome()

    # Render widgets
    topics_params = topic_search_widget(papers, topics)
    trends_params = top_trends_widget(papers)
    papers_params = paper_search_widget(papers, topics)

    # Render visualizations
    render_topics(intro, papers, **topics_params)
    render_trends(intro, papers, **trends_params)
    render_papers(intro, papers, **papers_params)

if __name__ == "__main__":
    main()






