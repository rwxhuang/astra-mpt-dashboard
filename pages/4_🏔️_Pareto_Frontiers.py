import streamlit as st

st.error('Implementation still in progress!', icon="🚨")

with st.sidebar:
    st.title('🏔️ Pareto Frontiers')
    st.text("Dataset Information:")
    step1 = st.container(border=True)
    dataset = step1.file_uploader('Select Dataset')