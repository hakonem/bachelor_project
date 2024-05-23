# USER MANUAL for TabulAI
With this user manual we aim to provide clear and concise instructions to ensure users can easily install, run, and utilize our application.

## Installation Instructions:

1.	Install necessary dependencies using 

``` pip install -r requirements.txt ```

* This will install the following requirements:
   - streamlit==1.32
   - pandas==2.2.1
   - numpy==1.26.4
   - plotly==5.19.0
   - ete3~=3.1.3
   - anytree~=2.12.1
   - networkx~=3.2.1
   - matplotlib~=3.8.0
   - seaborn~=0.13.0
   - wordcloud~=1.9.3
   - Pillow~=10.0.1
   - pygwalker~=0.4.8.3
   - SQLAlchemy~=2.0.29

2.	Set up the database by running the provided SQL scripts.

## Running the Application:
To run the application locally, Streamlit provides a convenient localhost environment.

Follow these steps:
1.	Open your terminal.
2.	Navigate to the directory with the application.
3.	Execute the following command on your terminal:
   
``` streamlit run Home.py ```

This command will start the Streamlit server and launch the application on your local machine. You can access it by opening a web browser and navigating to http://localhost:8501 

## Using the Features:
* **Topic Search**: Choose up to five topics to search and visualize.
* **Top Trends**: Choose up to ten topics to display.
* **Paper Search**: Use the drop-down menu on sidebar to search relevant papers within the database
* **Sunburst Chart**: Use the interactive Sunburst chart to explore the hierarchical topic tree by clicking on segments to zoom in and reveal subtopics, and hover over segments to view detailed information about each topic.
---

TabulAI © | Bachelor Thesis Project by Group 40 | Oslo Metropolitan University 2024
