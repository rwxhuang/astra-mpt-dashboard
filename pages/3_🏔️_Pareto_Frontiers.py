import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from pareto_frontiers import ParetoFrontiers

COLORS = ['#361c64', '#17804f', '#a8ba7a', '#0407f2', '#2a685b', '#1e8cbe', '#977ecb', '#f0f87a', '#d2f29c', '#b39ffe', '#b3bb70', '#30f1c0', '#fa1921', '#9d62d8', '#4f4b4d', '#6ec697', '#de4520', '#b58819', '#1d57fc', '#f8df0a', '#f03d50', '#1e531d', '#c3d413', '#5f4cd0', '#de678e', '#13467a', '#612181', '#934673', '#a16c29', '#f2aaa1']
st.set_page_config(layout="centered")

st.header("Pareto Frontiers")
st.write("#### We calculate efficient frontiers in the 2-dimensional case from NASA technology projects.")

def generate_scatter(scatter_dataset, frontier_dataset, x_axis, y_axis, log_x, log_y):
    fig = make_subplots()
    for i in range(len(scatter_dataset)):
        scatter_df = scatter_dataset[i]
        scatter_df.insert(loc=len(scatter_df.columns), column='color', value=COLORS[i % 30])
        frontier_df = frontier_dataset[i]
        frontier_df.insert(loc=len(frontier_df.columns), column='color', value=COLORS[i % 30])
        fig.add_trace(go.Scatter(x=scatter_df[x_axis], y=scatter_df[y_axis], mode='markers', name='Scatter Plot Group ' + str(i), marker=dict(color=len(scatter_df) * [COLORS[i % 30]])))
        fig.add_trace(go.Scatter(x=frontier_df[x_axis], y=frontier_df[y_axis], mode='markers+lines', name='Scatter Plot Group ' + str(i), marker=dict(color=len(frontier_df) * [COLORS[i % 30]]), line=dict(color=COLORS[i % 30])))
    fig.update_layout(
        xaxis_title="" if not log_x else "log: " + x_axis,
        yaxis_title="" if not log_y else "log: " + y_axis,
        legend_title=dict(
            font = dict(size = 16),
            )
        ,legend=dict(
            orientation="h",
            font = dict(size = 14),
            entrywidth=200,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ), hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        )
    )
    return fig

with st.sidebar:
    st.title('🏔️ Pareto Frontiers')
    st.text("Dataset Information:")
    step1 = st.container(border=True)
    dataset = step1.file_uploader('Select Dataset')

    step2 = st.container(border=True)
    step2.text("Pareto Frontier Specifications:")
    pf = ParetoFrontiers(dataset.name if dataset else "InstrumentData_Clean_Julia_Milton.xlsx")
    column_names = pf.get_cols()
    instruments = pf.get_instruments()
    x_axis = step2.selectbox('Select the x-axis.', column_names, index=9 if len(column_names) > 9 else 0)
    x_max = False
    log_x = step2.toggle('Take logarithm of x-axis', True)
    y_axis = step2.selectbox('Select the y-axis.', column_names, index=16 if len(column_names) > 16 else 0)
    y_max = step2.toggle('Maximize y-axis', False)
    log_y = step2.toggle('Take logarithm of y-axis', True)

    with st.expander('Optional custom modifications', expanded=False):
        query_string = st.text_input('Custom Python pandas query string', value='Instrument_Type == "Imager" and Resolution_m < 100000')
        custom_string = st.text_input('Custom Python pandas Python task where self.df is the dataframe', value="pd.cut(self.df['Year_From'], [1964, 1979, 1994, 2010, 2026], right=True)")
    
    scatter_dataset = pf.get_scatter(
                    x_axis,
                    y_axis,
                    log_x=log_x,
                    log_y=log_y,
                    query_string=query_string,
                    custom_string=custom_string,
                )
    frontier_dataset = pf.generate_frontier(
                    scatter_dataset,
                    x_pareto_max=x_max,
                    y_pareto_max=y_max,
                )
fig = generate_scatter(scatter_dataset, frontier_dataset, x_axis, y_axis, log_x, log_y)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with st.expander('About this Application', expanded=False):
    st.write('''
        - Paper: [Earth Observation Technologies for Climate Change Adaptation and Monitoring: Future Projection from Decadal Trends](https://drive.google.com/file/d/1wrI86MDXatQ-N5V_CIMb3dpss4kq0MxX/view?usp=drive_link).
        - :orange[**Pareto Frontiers**]: Calculating the most efficient solutions in multi-objective optimization
        ''')