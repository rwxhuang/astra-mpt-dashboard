import streamlit as st

st.set_page_config(layout="centered")

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

    The rest of this documentation will detail the 4 main functional components of the web application: **Downloading Data** (1), **Generate Graphs** (2),
   **Pareto Frontiers** (3), and **Marokwitz Portfolio Theory** (4). 
    ## Function 1. Downloading Data
    Given a search term, the goal is to output a dataset that contains project information from the Techport and SBIR database. Currently, 
    the dataset only includes data from [Techport](https://techport.nasa.gov/home). In this function, we have two options where the 
    first option manually uses Selenium to access the websites to receive an up-to-date csv file. The second option uses pre-scraped data 
    to greatly improve efficiency when a user wants to query data. Additionally, the second option allows for the use of [boolean format](https://www.scribbr.com/working-with-sources/boolean-operators/).
    """)
st.image('./images/download_data.png', use_column_width="always", caption='Download web-scraped data from Techport, SBIR, etc. into one csv file for any search term.')
st.markdown("""
    ### Option 1. Generate up-to-date data with Selenium web-scraper
    While using the Selenium web-scraper generates the most up-to-date data from the NASA's database, it take significantly longer than Option 
    2 because Selenium has to browse through the pages of the database live. For the search term, `"heliophysics laser"`, Option 1 takes around
    15 seconds while Option 2 takes around 0.2 seconds.
            
    This option depends on the `Search` class from `search.py` and passes in the user-inputted search phrase into `search_phrase` and the 
    Chrome driver to launch Selenium into `driver`. Then, we call the `scrape_data(self)` method to scrape the data from multiple databases 
    (now only including Techport database). In the background, a web browser launches, browses the databases to extract the project data, and
    inputs the project information into the outputted csv.
            
    ### Option 2. Generate up-to-date data with Selenium web-scraper      

    This option also depends on the `Search` class from `search.py` and passes in the user-inputted search phrase into `search_phrase`. `None` 
    is passed into `driver` since there is no Selenium web driver. Instead, it accesses the pre-proccesed Techport csv file from 
    `/data/techport_all.csv`.
            

""")
st.markdown("""
            ## Function 2. Generate Graphs
            """)
st.image('./images/generate_graphs.png', use_column_width="always", caption='Conveniently generate multiple visuals given a search term to produce graphs, heat maps, etc.')
st.markdown("""
            ## Function 3. Pareto Frontiers
            """)
st.image('./images/pareto_frontiers.png', use_column_width="always", caption='Calculating efficient frontiers in the 2-dimensional case from technology projects.')
st.markdown("""
            ## Function 4. Markowitz Portfolio Theory (MPT)
            """)
st.image('./images/mpt.png', use_column_width="always", caption='Automating the process of making investment decisions for technology projects.')
