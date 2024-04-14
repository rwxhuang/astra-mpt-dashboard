import streamlit as st
from search import Search

st.error('Implementation still in progress!', icon="🚨")

st.header("Downloading Data")
st.write("Given a search term, web-scrape Techport and SBIR databases. The first option manually uses Selenium to access the websites to receive an up-to-date csv file. The second option uses pre-scraped data to greatly improve efficiency when a user wants to query data.")
st.write("#### Option 1. Generate up-to-date data from all available sources")
st.warning('Will take longer to run with use of Selenium web driver.', icon="⚠️")
search_phrase_1 = st.text_input('Enter your search phrase', key="1")
if search_phrase_1:
	s = Search(search_phrase_1)
	with st.spinner("Please wait for web scraper..."):
		download_data_1_csv = s.scrape_data()
	st.success('Success! Press below to download csv file of data.', icon="✅")
	st.download_button('Download CSV file of Techport projects.', data=download_data_1_csv, file_name='download_data_1.csv', mime='text/csv')
		
st.write("#### Option 2. Generate from stored data (can use boolean format)")
st.warning("""Must follow a boolean format! No spaces and you can use 'AND', 'OR', and 'NOT' operations. An example is the following: "heliophysics AND (laser OR NOT earth)" """, icon="⚠️")
search_phrase_2 = st.text_input('Enter your search phrase')
if search_phrase_2:
	s = Search(search_phrase_2)
	with st.spinner("Please wait for web scraper..."):
		download_data_2_csv = s.get_data()
	st.success('Press below to download csv file of data', icon="✅")
	st.download_button('Download CSV file of Techport projects.', data=download_data_2_csv, file_name='download_data_2.csv', mime='text/csv',)