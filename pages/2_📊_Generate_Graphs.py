import streamlit as st
from search import Search
import plotly.express as px
from generate_graphs import Graph1A, Graph1B, Graph2A, Graph2B

st.set_page_config(layout="wide")

def stacked_bar_plot_g1(df):
    fig = px.bar(df, x='Year', y='Count', color='Taxonomy Level', orientation='v')
    fig.update_layout(
        hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        )
    )
    return fig

def stacked_bar_plot_g2(df):
    fig = px.bar(df, x='Year', y='Count', color='TRL Level', orientation='v')
    fig.update_layout(
        hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        )
    )
    return fig

st.header("Graph Generation")
st.write("Given a search term that must satisfy the boolean format, generate a set of useful graphs from bar charts to heatmaps.")
with st.form(key='graph_form'):
	search_phrase = st.text_input(label='Enter search phrase', value='heliophysics')
	submit_button = st.form_submit_button(label='Display graphs')
with st.spinner("Please wait for graphs to generate..."):
	s = Search(search_phrase, None)
	data = s.get_data()
col1, col2 = st.columns(2)
with col1:
	# Graph 1A - Number of Projects Started, Grouped by Taxonomy Level
	g1a = Graph1A(data)
	g1a_df = g1a.generate_graph()
	fig1a = stacked_bar_plot_g1(g1a_df)
	st.write('#### Graph 1A. Number of Projects Started, Grouped by Taxonomy Level')
	st.plotly_chart(fig1a, theme="streamlit", use_container_width=True)
	# Graph 2A - Number of Projects started by TRL_in level
	g2a = Graph2A(data)
	g2a_df = g2a.generate_graph()
	fig2a = stacked_bar_plot_g2(g2a_df)
	st.write('#### Graph 2A. Number of Projects Ongoing, Grouped by Taxonomy Level')
	st.plotly_chart(fig2a, theme="streamlit", use_container_width=True)
	with st.expander('About this Application', expanded=False):
		st.write('''
			- Data Source: [Techport](https://techport.nasa.gov/home).
			- :orange[**Graph Generation**]: Conveniently generate multiple visuals given a search term to produce graphs, heat maps, etc.
			''')
with col2:
	# Graph 1B - Number of Projects Ongoing, Grouped by Taxonomy Level
	g1b = Graph1B(data)
	g1b_df = g1b.generate_graph()
	fig1b = stacked_bar_plot_g1(g1b_df)
	st.write('#### Graph 1B. Number of Projects Ongoing, Grouped by Taxonomy Level')
	st.plotly_chart(fig1b, theme="streamlit", use_container_width=True)
	# Graph 2B - Number of Projects started by TRL_out level
	g2b = Graph2B(data)    
	g2b_df = g2b.generate_graph()
	fig2b = stacked_bar_plot_g2(g2b_df)
	st.write('#### Graph 2B. Number of Projects Ongoing, Grouped by Taxonomy Level')
	st.plotly_chart(fig2b, theme="streamlit", use_container_width=True)