import streamlit as st
import importlib.util
import sys
import sqlite3
from PIL import Image
import os

# TabulAI - An Interactive Trend Analysis and Visualization Tool for "Artificial Intelligence (AI) Research"
# Set up the page configuration for Home.py
st.set_page_config(
    layout="wide",  # Using the "wide" layout for more space horizontally
    initial_sidebar_state="expanded"  # To make the sidebar start off expanded
)


# Create a database connection to the SQLite database: app_data.db
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('data/app_data.db')
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    return conn


# Function to close the connection
def close_connection(conn):
    if conn is not None:
        conn.close()
        print('Database connection closed successfully.')


# Initialize session state
# session_state = st.session_state

# Check if database connection is already stored in session state
# if 'conn' not in session_state:
# If not, establish new connection and store in session state
# session_state.conn = create_connection()
# print('New database connection stored in session state')
# This created some issues during runtime, so I am commenting it out.

# Loading the modules
@st.cache_data
def load_module(module_name, file_path):
    """
    Loads a module dynamically given the module name and the file path.

    Args:
    module_name (str): The name to assign to the module.
    file_path (str): The path to the file containing the module's source code.

    Returns:
    module: The loaded module.
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


# Creating the layout for the homepage:
def home_page():
    """
    Renders the home page for the Streamlit app. Includes titles, markdowns, and images.
    """
    # PAGE TITLE
    st.title('TabulAI')
    popover = st.popover("Tabula")
    popover.markdown("'Tabula' is the latin word for 'map', with a little twist of AI (Artificial Intelligence) "
                     "it becomes 'TabulAI'. We think it encapsulates the essence of guiding academic insights through "
                     "advanced technology.",
                     unsafe_allow_html=True)

    st.markdown("""#### // :violet[A Data Science Project]""", unsafe_allow_html=True)

    # PAGE LAYOUT with COLUMNS
    col1, col2 = st.columns([2, 1])  # Adjusting the proportion of columns
    with col1:
        # Introductory text
        st.markdown(""" 
        **TabulAI** is a pioneering web application designed to explore the fast evolving landscape of 
        Artificial Intelligence (AI). 

        Developed by a dedicated team from Oslo Metropolitan University, in collaboration with SINTEF, 
        **TabulAI** leverages cutting-edge machine learning, similarity search and data 
        visualization techniques to provide a dynamic interface with fresh insights. The application provides 
        an interactive visualisation tool for academic publications tagged with an extensive list of AI topics 
        carefully curated from DBPedia. 

        Our application, stemming from the <a href="https://enrichmydata.eu/" target="_blank"> enRichMyData </a>
        project under the EU’s Horizon Europe research and innovation programme, aims to enhance monitoring fast 
        evolving field of AI research.""", unsafe_allow_html=True)

        # Invitation to explore
        st.markdown("""
        Explore **TabulAI**, where AI research meets insight for innovation.
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown("""      
        _<sub> * Bachelor Thesis Project - in collaboration with OsloMet, SINTEF and enrichMyData </sub>_""",
                    unsafe_allow_html=True)

    with col2:
        # IMAGE of SUNBURST - AI TOPIC LIST
        # Define the path to the image
        image_path = os.path.join("images", "main-sunburst.png")
        image = Image.open(image_path)
        # Display the image on Home page:
        st.image(image, width=400, use_column_width=False)
        # Using ALT text did not work in Streamlit:
        # caption="Sunburst chart showing the hierarchical topic " "tree of AI research. Main categories include "
        # "Artificial Intelligence, Computer Vision, Robot, " "Data Analysis, and Utility, with subcategories "
        # "visualized as segments."

    # FOOTER with logo at the bottom
    with st.container():
        st.write("---")  # A horizontal line to separate the footer
        # enrichMyData logo:
        logo_path = "./images/enrichmydata-logo.png"  # Correct path to the images folder under the project root
        st.image(logo_path, use_column_width=False, width=100)


# Main function to display the home page
if __name__ == "__main__":
    home_page()
