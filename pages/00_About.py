import streamlit as st
from PIL import Image
import os


# ABOUT PAGE
def about_page():
    """
    Displays the "About" page with detailed information on the methodologies
    and technologies used in the TabulAI project, along with visual elements
    and a roadmap for implementation.
    """
    st.header("Cutting-Edge Aspects of TabulAI")

    # OUR METHODOLOGY
    # Vectorisation image
    image_path = os.path.join("images", "vectorization.jpg")
    image = Image.open(image_path)
    # Display the image on Home page:
    st.image(image, use_column_width=True)

    # Split the page into two columns, with the first column being larger
    col1, col2 = st.columns([2, 1])

    with col1:
        # Vector Embeddings
        st.write("### Vector Embeddings")

        st.markdown("""
        **What are Vector Embeddings?**

        Vector embeddings are a way to represent text data (like words or documents) as dense vectors in a high-dimensional space.
        These vectors capture the semantic meaning of the text, allowing similar texts to have similar vector representations.
        """, unsafe_allow_html=True)

        st.markdown("""
        **How Are They Used in TabulAI?**

        In TabulAI, vector embeddings are generated for arXiv papers. This might involve using pre-trained models like Word2Vec, GloVe,
        or more advanced ones like BERT or transformers to convert the textual content of the papers into vector representations.
        """, unsafe_allow_html=True)

        # Similarity Search
        st.write("### Similarity Search")

        st.markdown("""
        **What is Similarity Search?**

        Similarity search involves finding items (papers, in this case) that are most similar to a given query.
        This is done by comparing their vector embeddings using distance metrics such as cosine similarity or Euclidean 
        distance.""", unsafe_allow_html=True)

        st.markdown("""
        **How Is It Applied in TabulAI?**

        TabulAI uses similarity search to tag arXiv papers with relevant AI topics. Once the papers are represented as vectors,
        the application calculates the similarity between the paper vectors and the topic vectors. The topics with the highest similarity
        scores are assigned to the papers.

        Similarity search improves tagging by ensuring that the most relevant topics are matched exactly, leading to 
        better organization, retrieval, and analysis. Although our project focused on academic articles, the methods 
        can be applied to any type of text data. Data scientists can use their own datasets or source different types 
        of datasets to implement a similar process in fields such as healthcare, finance, and marketing.
        """, unsafe_allow_html=True)

        # Tagging arXiv Papers with AI Topics
        st.write("### Tagging arXiv Papers with AI Topics")

        st.markdown("""
        **Process Overview:**
        - **Embedding Generation:** Convert the text of arXiv papers and AI topics into vector embeddings.
        - **Similarity Calculation:** Compute the similarity between each paper and the predefined AI topic vectors.
        - **Tag Assignment:** Assign tags to the papers based on the most similar AI topics.
        """, unsafe_allow_html=True)

        st.markdown("""
        **Technologies and Models:**
        - This stage involves NLP models and libraries such as TensorFlow, PyTorch, or Hugging Face Transformers for 
        embedding generation.
        - Efficient similarity search algorithms and data structures, possibly leveraging libraries like FAISS 
        (Facebook AI Similarity Search) or tools like KagiSearch.
        """, unsafe_allow_html=True)

        # Visualization with Streamlit
        st.write("### Visualization with Streamlit")

        st.markdown("""
        **Interactive Visualizations:**

        Streamlit is used to create interactive visualizations that allow users to explore the tagged papers and AI topics dynamically.
        Visual elements such as bar charts, sunburst charts, and topic trees help users intuitively understand the 
        distribution and trends of AI research.

        The app's user interface is designed with focus on the data representation and visualisaitons to provide a 
        seamless experience, with sidebar navigation, dropdown selections, and detailed data displays.
        """, unsafe_allow_html=True)

        # Final Thoughts Section
        st.write("### Final Thoughts")
        st.markdown("""
        As we conclude this project, we are grateful for the opportunities it presented for personal and professional 
        growth. We are confident that the methodologies and technologies we developed will contribute positively to 
        the ongoing discourse in AI research and application.
        """, unsafe_allow_html=True)

    with col2:
        # Column 2 - methodology roadmap
        st.subheader("Roadmap for TabulAI")
        st.markdown("""
        This roadmap provides a step-by-step guide to implementing the vectorization and labeling process for our data 
        science project. It outlines the essential stages, tools, and techniques used and emphasizes its applicability 
        across different domains and industries. By following these steps, others can create efficient, scalable, 
        and interactive applications for analyzing trends.
        """)

        # Data Collection and Preparation section
        st.markdown("""
        ##### 1. Data Collection and Preparation
        - **Collect Data:** Source textual data from databases like arXiv.org. Compile a list of topics of your choice 
        with labels and descriptions. 
        
        - **Clean and Preprocess:** Remove duplicates and irrelevant information. Standardize paper abstracts. 
        Ensure topic list consistency.
        """)

        # Vectorization section
        st.markdown("""
        ##### 2. Vectorization
        - **Select Model:** Choose an open-source language model from Hugging Face.
        - **Vectorize Topics:** Convert topic list into vector representations.
        - **Vectorize Abstracts:** Convert paper abstracts into vector representations using the same model.
        """)

        # Similarity Search and Tagging section
        st.markdown("""
        ##### 3. Similarity Search and Tagging
        - **Setup Search:** Utilize KagiSearch for cosine similarity or use another vectorisation metric.
        - **Perform Search:** Compare vectorized abstracts with topics. Rank top n (e.g., top 5) topics by similarity.
        - **Tag Papers:** Assign top n topics to each paper based on similarity scores.
        """)

        # Backend Processing section
        st.markdown("""
        ##### 4. Backend Processing
        - **Data Storage:** Store tagged papers and vectors in a database (e.g., SQLite).
        - **Indexing:** Create indexes for efficient data retrieval.
        """)

        # Frontend Integration section
        st.markdown("""
        ##### 5. Frontend Integration
        - **Develop Application:** Use Streamlit to build an interactive web app, or another web application framework of your choice.
        - **Display Results:** Show processed data with dynamic visualizations for exploring topics and trends.
        """)


# Main function to display the page
if __name__ == "__main__":
    about_page()
