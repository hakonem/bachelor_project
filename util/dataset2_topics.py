import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# DATASET2: AI topics list from "topics" table in the database
st.subheader("Dataset 2: AI Topics")


@st.cache_resource
def load_data():
    # Create a database connection
    engine = create_engine('sqlite:///data/app_data.db')  # Adjust the path if necessary

    # Load the dataset from the database
    query = "SELECT * FROM topics"
    data = pd.read_sql_query(query, engine)
    return data


def main():
    # Call the load_data function
    data = load_data()

    # Analyzing the data for presentation
    levels_count = data['level'].nunique()
    levels_distribution = data['level'].value_counts().sort_index()

    # Streamlit page setup
    # Create a container for structured layout
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.write("#### Name of the List")
            st.markdown(":blue_book: **Database Table**: topics")
            st.write("#### Column Names and Descriptions")
            st.markdown("""
            - **Unnamed: 0**: Numerical index.
            - **s**: Unique identifier/URL from DBpedia.
            - **prefLabel**: Preferred name of the topic.
            - **wdEntity**: Corresponding Wikidata entity URL.
            - **wdType**: Type of Wikidata entity.
            - **broader**: Broader topic category.
            - **altLabel**: Alternative labels/names.
            - **description**: Brief description of the topic.
            - **level**: Hierarchical level within the AI domain.
            """)

        with col2:
            st.write(f"#### Number of Levels: {levels_count}")
            st.write("#### Topics Distribution Across Levels")
            st.bar_chart(levels_distribution)

    st.subheader("AI Topics List with Levels:")
    st.dataframe(data.head(10))


if __name__ == "__main__":
    main()
