import streamlit as st
from search import Search
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

chrome_version = "76.0.3809.68"
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager(chrome_version).install()), options=options)		

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--headless")

driver = get_driver()


st.header("Downloading Data")
st.write("Given a search term, web-scrape Techport and SBIR databases. The first option manually uses Selenium to access the websites to receive an up-to-date csv file. The second option uses pre-scraped data to greatly improve efficiency when a user wants to query data.")
st.write("#### Option 1. Generate up-to-date data from all available sources")
st.warning('Will take longer to run with use of Selenium web driver.', icon="⚠️")
search_phrase_1 = st.text_input('Enter your search phrase', key="1")
if search_phrase_1:
	s = Search(search_phrase_1, get_driver())
	curr = time.time()
	with st.spinner("Please wait for web scraper..."):
		download_data_1_csv = s.scrape_data().to_csv().encode('utf-8')
		time_taken = time.time() - curr
	st.success('Success! Took ' + str(round(time_taken, 3)) + ' sec. Press below to download csv file of data.', icon="✅")
	st.download_button('Download CSV file of Techport projects.', data=download_data_1_csv, file_name='download_data_1.csv', mime='text/csv')
		
st.markdown("#### Option 2. Generate from stored data (can use [boolean format](https://www.scribbr.com/working-with-sources/boolean-operators/))")
st.warning("""Must follow a boolean format! No spaces and you can use 'AND', 'OR', and 'NOT' operations. An example is the following: "heliophysics AND (laser OR NOT earth)" """, icon="⚠️")
search_phrase_2 = st.text_input('Enter your search phrase')
if search_phrase_2:
	s = Search(search_phrase_2, get_driver())
	curr = time.time()
	with st.spinner("Please wait for data to generate..."):
		download_data_2_csv = s.get_data().to_csv().encode('utf-8')
		time_taken = time.time() - curr
	st.success('Success! Took ' + str(round(time_taken, 3)) + ' sec. Press below to download csv file of data.', icon="✅")
	st.download_button('Download CSV file of Techport projects.', data=download_data_2_csv, file_name='download_data_2.csv', mime='text/csv',)
	