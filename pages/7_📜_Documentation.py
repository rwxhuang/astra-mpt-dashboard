import streamlit as st

st.markdown(
    """
    # Documentation
    ## Introduction
    For the past 60 years, NASA has been pushing the boundaries of space exploration from Earth observation 
    to the Artemis missions. With all these ambitious projects, every dollar allocated must be strategically
    invested to maximize technological innovation and operational efficiency. With the current system, financial
    advisors make manual calculations and decisions to manage their investment decisions which takes significant time
    that could be used to jumpstart these projects. To combat this problem, our team built this web application which
    (1) web-scrapes publicly available NASA project data, (2) generates recommended visual graphs from NASA project 
    data, (3) automatically interacts with displaying efficient pareto frontiers, and (4) recommends a set of 
    portfolios using Markowitz Portfolio Theory (MPT).

    The design of this application prioritizes *efficiency* and *correctness*. Our primary goal is efficiency, which means
    that these functions have to be output results quickly so that the user can analyze data and make investment
    decisions in a timely manner. As mentioned before, we hope to reduce the time significantly needed to go from collecting
    data to allocating funds. Additionally, we want to prioritize *correctness* and want to ensure that the calculations made
    to analyze the data go through rigorous, but accurate, procedures. While not implemented yet, we hope to have validation 
    processes to minimize calculation errors.

    The rest of this documentation will detail the 4 main functional components of the web application. 
    ## Function 1. Downloading Data
    ## Function 2. Generate Graphs
    ## Function 3. Pareto Frontiers
    ## Function 4. Markowitz Portfolio Theory (MPT) 
"""
)