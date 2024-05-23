import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# DATASET1: arXiv papers from "papers" table in the database
st.subheader("Dataset 1: The arXiv database with selected categories")


def main():
    # Create a database connection
    engine = create_engine('sqlite:///data/app_data.db')

    # Load the dataset from the database
    query = "SELECT * FROM papers"
    df = pd.read_sql_query(query, engine)

    st.markdown("""
    1. **Description**:
    This refined dataset from arXiv includes academic papers from only the chosen categories relevant to the project's 
    focus on AI trends. The categories are reflective of the various domains within artificial intelligence research.

    2. **Purpose**: By narrowing down to specific categories, the dataset's relevance is enhanced, ensuring that only papers 
    pertinent to AI research trends are analyzed and visualized.

    3. **Utilization**: The dataset has been filtered to include papers falling under the specified categories, 
    which allows for a more targeted and efficient tagging process using similarity search methods.
    """)

    # Print the names of the columns and the total papers in the dataset
    st.write(f"**Total papers in the dataset**: {len(df)}")

    st.write("#### Name of the List")
    st.markdown(":blue_book: **Database Table**: papers")

    # Streamlit page setup
    # Create a container for structured layout
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            # Print the shape of the dataset (number of rows and columns)
            st.write("Shape of the dataset (row, col):", df.shape)

            # Print the names of the columns
            st.write("##### Column Names:")
            column_descriptions = {
                "url": "URL of the paper",
                "title": "Title of the paper",
                "categories": "Arxiv categories the paper belongs to",
                "abstract": "Abstract of the paper",
                "submission_date": "Date when the paper was submitted",
                "authors_parsed": "List of authors of the paper"
            }
            st.write(column_descriptions)

            # Analyzing the data for presentation
            category_count = df['categories'].nunique()
            category_distribution = df['categories'].value_counts().sort_index()

        with col2:
            st.write(f"##### Number of Categories: {category_count}")
            st.write("##### Category Names:")
            category_descriptions = {
                "cs.CV": "Computer Vision",
                "cs.CL": "Computational Linguistics",
                "cs.LG": "Machine Learning",
                "cs.RO": "Robotics",
                "cs.AI": "Artificial Intelligence",
                "cs.NE": "Neural and Evolutionary Computing",
                "stat.ML": "Machine Learning Statistics",
                "cs.MA": "Multiagent Systems"
            }
            st.write(category_descriptions)

            # Swap the axes and make 'categories' a column and reset the index to display it correctly
            category_distribution_df = category_distribution.reset_index()
            category_distribution_df.columns = ['Category', 'Papers']  # Rename columns
            category_distribution_df = category_distribution_df.set_index('Papers')  # Set 'Papers' as index

    st.subheader("Dataframe: the arXiv dataset")
    st.dataframe(df.head(10))


if __name__ == '__main__':
    main()
