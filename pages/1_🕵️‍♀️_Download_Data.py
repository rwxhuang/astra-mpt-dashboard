import streamlit as st
from search import Search

st.error('Implementation still in progress!', icon="🚨")

st.header("Downloading Data")
st.write("Given a search term, web-scrape Techport and SBIR databases. The first option manually uses Selenium to access the websites to receive an up-to-date csv file. The second option uses pre-scraped data to greatly improve efficiency when a user wants to query data.")
st.write("#### Option 1. Generate up-to-date data from all available sources")
st.warning('Will take longer to run with use of Selenium web driver.', icon="⚠️")
with st.form(key='option_1'):
	search_phrase_1 = st.text_input(label='Enter search phrase')
	submit_button_1 = st.form_submit_button(label='Download data')
if submit_button_1:
	s = Search(search_phrase_1)
	s.scrape_data()

st.write("#### Option 2. Generate from stored data (can use boolean format)")
st.warning("""Must follow a boolean format! No spaces and you can use 'AND', 'OR', and 'NOT' operations. An example is the following: "heliophysics AND (laser OR NOT earth)" """, icon="⚠️")
with st.form(key='option_2'):
	search_phrase_2 = st.text_input(label='Enter search phrase')
	submit_button_2 = st.form_submit_button(label='Download data')