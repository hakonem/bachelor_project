import streamlit as st
import importlib.util
import sys


# MODULE LOADING FUNCTION
def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


# TOPIC TREE PAGE FUNCTION
def tree_page():
    # Page Title
    st.title('The Hierarchical Topic Tree Visualization')

    # Expander: Topic tree visualization options explanations
    with st.expander(" :blue[You can close / open this expander by clicking here ...]", expanded=True):
        st.markdown("""
        In our application we have chosen to use the **:orange[Sunburst Chart]** to presents a compelling circular 
        hierarchy. This is ideal for visualizing the broad spectrum of AI topics and their subdivisions. This 
        visualization stands out for its ability to reveal complex relationships at a glance, making it easier to 
        discern the overarching structure of AI research.
        
        :red[Data is loading ... Please wait.]
        
        We are working on performance issues of the app to improve the rendering/loading time.
        Thank you for being patient! 
        """, unsafe_allow_html=True)

    # TAB LAYOUT:
    # Page layout with TABS
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = (
        st.tabs(["| The Main Tree |",
                 "| Subplot 1 |",
                 "| Subplot 2 |",
                 "| Subplot 3 |",
                 "| Subplot 4 |",
                 "| Subplot 5 |",
                 "| Subplot 6 |",
                 "| Subplot 7 |",
                 "| Subplot 8 |"
                 ]))

    # Dynamically load and display charts for each tab
    # TAB1
    with tab1:
        main_tree_module = load_module("main_tree_module", "util/main_sunburst.py")
        main_tree_module.main()

    tab2.write("Sunburst for Natural language processing ...")
    tab3.write("Sunburst Artificial intelligence")
    tab4.write("Sunburst for Machine translation ...")
    tab5.write("Sunburst for Knowledge representation ...")
    tab6.write("Sunburst for Computational linguistics ...")
    tab7.write("Sunburst for Data mining ...")
    tab8.write("Sunburst for Data analysis ...")
    tab9.write("Sunburst for Data science ...")

    # FOOTER with logo at the bottom
    with st.container():
        st.write("---")  # A horizontal line to separate the footer

        # enrichMyData logo:
        logo_path = "./images/enrichmydata-logo.png"  # Update this path
        st.image(logo_path, use_column_width=False, width=100)


# Main function to display the page
if __name__ == "__main__":
    tree_page()
