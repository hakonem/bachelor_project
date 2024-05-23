import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# DATASET3: The result of our work after tagging arXiv papers with AI topics
# The "tagged_papers" dataset is fetched from "tagged_papers" table in the database
st.subheader("Dataset 3: Tagged Papers")


def load_data():
    # Create a database connection
    engine = create_engine('sqlite:///data/app_data.db')

    # Load the dataset from the database
    query = "SELECT * FROM tagged_papers"
    data = pd.read_sql_query(query, engine)
    return data


# MAIN
def main():
    # Call the load_data function
    df = load_data()
    df.shape

    st.markdown("""
    #### Name of the List: 
    :blue_book: **Database Table**: tagged_papers """, unsafe_allow_html=True)

    # Print the shape of the dataset (number of rows and columns)
    st.write("Shape of the dataset (row, col):", df.shape)

    # Count and print the number of unique topics
    st.write("Number of unique titles:", df['title'].nunique())

    # Organizing in containers and columns
    with st.container():
        col1, col2 = st.columns(2)

        # Basic analysis
        with col1:
            # Print the names of the columns
            st.subheader("Column Names:")
            column_descriptions = {
                "url": "Link to the paper.",
                "date": "Title of the paper",
                "title": "Arxiv categories the paper belongs to",
                "abstract": "Abstract of the paper",
                "topic1 to topic5": "Relevant AI topics which is used to tagg the paper."
            }
            st.write(column_descriptions)

        with col2:
            st.subheader("Data Creation Process")
            st.write("""
                This CSV file was generated using advanced data vectorization and similarity search techniques. Each paper is analyzed to extract meaningful topics from its content, using a combination of natural language processing (NLP) and machine learning algorithms. The topics reflect both broad and specific aspects of the papers, showcasing the depth of AI research covered.
                """)

    # Display the dataframe on the page
    st.write("Sample Data from CSV File:")
    st.dataframe(df.head())


if __name__ == '__main__':
    main()
