import streamlit as st

st.set_page_config(
    page_title="ASTRA",
    page_icon="🛰️",
)

st.write("# ASTRA Web Application")

st.sidebar.success("Select an application in this sidebar.")

st.markdown(
    """
    Studying the technological developments of innovative NASA projects through quantitative methods.
    **👈 We have the following pages.
    ### 1. Download Data
    - Download web-scraped data from Techport, SBIR, etc. into one csv file for any search term.
    ### 2. Generate Graphs
    - Conveniently generate multiple visuals given a search term to produce graphs, heat maps, etc.
    ### 3. Markowitz Portfolio Theory (MPT)
    - Automating the process of calculating portfolio investments for technology projects
    ### 4. References
    - Review publications made by the ASTRA team and resources used to create this application.
"""
)