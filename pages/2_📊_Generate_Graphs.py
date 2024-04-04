import streamlit as st

st.error('Implementation still in progress!', icon="🚨")
st.header("Graph Generation")
st.write("Given a search term that must satisfy the boolean format, generate a set of useful graphs from bar charts to heatmaps.")
with st.form(key='graph_form'):
	search_phrase = st.text_input(label='Enter search phrase')
	submit_button = st.form_submit_button(label='Download data')