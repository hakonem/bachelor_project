import streamlit as st
import importlib.util
import sys


# DATASETS PAGE
def load_module(module_name, file_path):
    """
    Load a Python module from a given file path and add it to sys.modules.

    Parameters:
    module_name (str): The name to assign to the loaded module.
    file_path (str): The file path to the module to load.

    Returns:
    module: The loaded module if successful, or None if an error occurred.
    """
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        st.write(f":green[Module {module_name} loaded successfully.]")
        return module
    except Exception as e:
        st.error(f"Failed to load module {module_name}: {str(e)}")
        return None


def main():
    """
    Main function to display the Streamlit interface for exploring data sources.

    It sets up the page title, expander with dataset descriptions, sidebar for dataset selection,
    and loads the selected dataset module to display its content. It also displays a footer with a logo.
    """
    st.title('Introducing Our Data Sources')

    with st.expander(" :blue[You can close / open this expander by clicking here ...]", expanded=True):
        st.markdown("""
        Explore and take a closer look at the datasets used in this project by selecting an option from the left panel.
        - **Dataset 1**: arXiv dataset with academic papers from [Kaggle](https://www.kaggle.com/)        
        - **Dataset 2**: AI Topic List derived from [DBPedia](https://www.dbpedia.org/)
        - **Dataset 3**: (The result) Tagged Papers with AI topics utilizing vector embeddings by [Kagi](https://kagi.com/)

        _**Note**_: You can download the entire dataset by clicking on the top-right CSV-button of each table.
        """)

    pages = {
        'arXiv Dataset': 'util/dataset1_arxiv.py',
        'AI Topics': 'util/dataset2_topics.py',
        'Tagged Papers': 'util/dataset3_tagged_papers.py',
    }

    # Sidebar selection to determine which page to load
    selected_page = st.sidebar.selectbox('Select a dataset:', options=list(pages.keys()), key='selected_page')

    # Loading the module with current selection
    module_name = selected_page.replace(' ', '_').lower()
    file_path = pages[selected_page]
    loaded_module = load_module(module_name, file_path)

    if loaded_module and hasattr(loaded_module, 'main'):
        loaded_module.main()
    else:
        st.error(f"No main() function found in {module_name}, or module failed to load.")

    # FOOTER
    with st.container():
        st.write("---")
        logo_path = "./images/enrichmydata-logo.png"
        st.image(logo_path, use_column_width=False, width=100)


if __name__ == "__main__":
    main()
