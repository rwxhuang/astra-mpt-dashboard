import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ASTRA",
    page_icon="🛰️",
)

st.write("# ASTRA Web Application")

st.sidebar.success("Select an application in this sidebar.")
st.markdown(
    """
    #### Studying the technological developments of innovative NASA projects through quantitative methods.
"""
)
tab1, tab2, tab3, tab4 = st.tabs(["🕵️‍♀️ Downloading Data", "📊 Generate Graphs", "📈 Markowitz Portfolio Theory (MPT)", "🏔️ Pareto Frontiers"])

with tab1:
    st.markdown(
    """
    Download web-scraped data from Techport, SBIR, etc. into one csv file for any search term.
    """
    )
    st.image('./images/download_data.png', use_column_width="always", caption='Choose out of two options to download data from the NASA Techport database.')

with tab2:
   st.markdown(
    """
    Conveniently generate multiple visuals given a search term to produce graphs, heat maps, etc.
    """
    )
   st.image('./images/generate_graphs.png', use_column_width="always", caption='Automatically generate graphs to understand data from the NASA Techport database.')

with tab3:
   st.markdown(
    """
    Automating the process of making investment decisions for technology projects.
    """
    )
   st.image('./images/mpt.png', use_column_width="always", caption='Automatically generate portfolios using Markowitz Portfolio Theory.')
   
with tab4:
   st.markdown(
    """
    Calculating efficient frontiers in the 2-dimensional case from technology projects
    """
    )
   st.image('./images/pareto_frontiers.png', use_column_width="always", caption='Experiment finding efficient frontiers with a given dataset.')
