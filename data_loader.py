import streamlit as st
import pandas as pd
import random

def load_topics():
    topics = ['Machine translation', 'Artificial intelligence', 'Natural language processing', 'Data mining', 'Data analysis', 'Data science', 'Generative artificial intelligence', 
          'Chatbots', 'Machine learning', 'Prompt engineering', 'Feature engineering', 'Feature selection', 'Big data', 'Speech recognition', 'Semantic similarity', 
          'Knowledge representation', 'Computational linguistics', 'Computer vision', 'Large language models', 'Recommender systems', 'Sentiment analysis', 'Reinforcement learning', 
          'AI in healthcare', 'AI in education', 'AI in finance', 'Bias mitigation']
    return topics

# Function to randomly select topic from topics dataset
def select_random_topic():
    return random.choice(load_topics())

@st.cache_data
# Function to fetch and clean data
def fetch_and_clean_data():
    papers = pd.read_csv('../kaggle_dump_full.csv')
    papers['submission_date'] = pd.to_datetime(papers['submission_date'])

    # Select random topic for each paper and add it in three new columns 
    for i in range(1,6):
        papers[f'tag{i}'] = papers.apply(lambda row: select_random_topic(), axis=1)
   
    return papers