import streamlit as st
import pandas as pd
import plotly.express as px


# MODULE LOADING FUNCTION
@st.cache_data
def load_data():
    file_path = 'data/topic_tree_with_levels.csv'  # Update this path
    data = pd.read_csv(file_path)
    return data


# PIE CHART for TOPICS DISTRIBUTION
def prepare_chart(data):
    levels_distribution = data['level'].value_counts().sort_index(ascending=True)

    fig = px.pie(
        levels_distribution,
        values=levels_distribution.values,
        names=levels_distribution.index,
        title="Distribution of AI Topics Across Levels",
        color_discrete_sequence=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#c4e17f'],
        hole=0.2
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


# MAIN FUNCTION to DISPLAY THE PAGE
def main():
    # Load the dataset
    data = load_data()

    # TITLE - AI TOPICS DISTRIBUTION
    st.title("AI Topics Hierarchy")

    # Using container for layout
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(""" 
            #### Topics Distribution Across Levels

            **Displayed dataset**: `AI Topic List`
            
            This interactive pie chart visualizes the distribution of AI topics across various hierarchical levels 
            within the dataset. Each segment of the pie represents a different level, with the size of each segment 
            corresponding to the number of topics found at that level. Larger segments denote more populated levels, 
            providing a clear, intuitive view of where concentrations of topics exist.
            
            This dynamic interaction helps users explore the data more granularly, 
            enhancing understanding of how AI topics are categorized and distributed.
            
            The distribution of topics across hierarchy levels enables us to examine potential trends and focus areas 
            in AI research. As we update the dataset with new AI topics, the chart will reflect changes in real-time, 
            helping track the evolution of AI research focus over time.
            """, unsafe_allow_html=True)

        with col2:
            fig = prepare_chart(data)
            st.plotly_chart(fig, use_container_width=True)

    # FOOTER with logo at the bottom
    with st.container():
        st.write("---")  # A horizontal line to separate the footer
        # enrichMyData logo:
        logo_path = "./images/enrichmydata-logo.png"  # path to the "images" folder under the project root
        st.image(logo_path, use_column_width=False, width=100)


# Calling the main function
if __name__ == "__main__":
    main()
