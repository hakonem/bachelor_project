import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3


# Database connection
def create_connection():
    """Create and return a database connection."""
    try:
        conn = sqlite3.connect('data/app_data.db')
        return conn
    except sqlite3.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None


# Fetching data from the "topics" table in the database
@st.cache_data
def fetch_topics():
    """Fetch topics from the database and return as DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing the topics data.
    """
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()  # Return an empty DataFrame on connection error

    try:
        query = "SELECT s, prefLabel, broader, level FROM topics"
        df = pd.read_sql(query, conn)
    except pd.io.sql.DatabaseError as e:
        st.error(f"Error fetching data from database: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on query error
    finally:
        conn.close()
    return df


def prepare_data(df):
    """Prepare data for the sunburst chart.

    Args:
        df (pd.DataFrame): DataFrame containing the original topics data.

    Returns:
        pd.DataFrame: DataFrame prepared for the sunburst chart visualization.
    """
    try:
        # Adding the root node manually because our dataset (AI Topic List) didn't have a root-node,
        # so it doesn't exist in the dataset
        ai_root = pd.DataFrame([{
            's': 'AI_Root',
            'prefLabel': 'Innovation',
            'broader': pd.NA,  # Set the broader field to NA for the root
            'level': 0  # Root level 0 (the center of the sunburst)
        }])
        # Concatenate the root node with the existing DataFrame
        df = pd.concat([ai_root, df], ignore_index=True)
        # Update the 'broader' field of top-level nodes to point to the AI root node
        df.loc[df['level'] == 1, 'broader'] = 'AI_Root'
        # Rename 'prefLabel' to 'topic'
        df = df.rename(columns={'prefLabel': 'topic'})
        # Map broader to topic to create parent column
        broader_map = df.set_index('s')['topic'].to_dict()
        df['parent'] = df['broader'].map(broader_map).fillna('')
        return df[['topic', 'parent']]
    except Exception as e:
        st.error(f"Error preparing data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on preparation error


# MAIN SUNBURST CHART - The Topic Tree
def create_sunburst_chart(df):
    """Create and return a sunburst chart.

    Args:
        df (pd.DataFrame): DataFrame containing the prepared data.

    Returns:
        plotly.graph_objects.Figure: Sunburst chart figure.
    """
    try:
        fig = px.sunburst(
            df,
            names='topic',
            parents='parent',
            width=800,
            height=800
        )
        fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
        return fig
    except Exception as e:
        st.error(f"Error creating sunburst chart: {e}")
        return None


# MAIN function to display the sunburst chart
def main():
    """Main function to run the Streamlit app."""
    st.title("Sunburst of AI Topic List")
    st.write("Note: This chart fetches data from the topics-table from our database. "
             "The topics-table is created based on the CSV file (AI Topic List).")

    # Fetch the dataset from the database
    df = fetch_topics()

    if df.empty:
        st.warning("No data available to display.")
        return

    # Prepare the data for visualization
    df_prepared = prepare_data(df)

    if df_prepared.empty:
        st.warning("Data preparation failed.")
        return

    # Create the sunburst chart
    fig = create_sunburst_chart(df_prepared)

    if fig:
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
