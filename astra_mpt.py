import streamlit as st
import mpt
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="ASTRA MPT Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded")

def txt_to_matrix(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        for line in file:
            row = line.strip().split(',')
            matrix.append(row)
    return matrix

def create_pwgt_df(proj_names, matrix):
    df = pd.DataFrame(columns=['Portfolio Number', 'Project Name', 'Proportion'])
    for i in range(len(matrix[0])):
        for j, proj_name in enumerate(proj_names):
            df = df._append({'Portfolio Number': i, 'Project Name': proj_name, 'Proportion': matrix[j][i]}, ignore_index=True)
    return df

def portfolio_plot(df):
    fig = px.bar(df, x='Portfolio Number', y='Proportion', color='Project Name')
    return fig
def get_all_pie_charts(df):
    _NUM_ROWS = 10
    _NUM_COLS = 2
    def pie_chart(chart_num):
        part_df = df[df['Portfolio Number'] == chart_num]
        pie = go.Pie(values=part_df.query('Proportion != "0"')['Proportion'], labels=part_df.query('Proportion != "0"')['Project Name'])
        return pie
    specs = [[{'type' : 'domain'} for _ in range (_NUM_COLS)] for _ in range(_NUM_ROWS)]
    fig = make_subplots(rows=_NUM_ROWS, cols=_NUM_COLS, specs=specs, subplot_titles=["Portfolio #" + str(i+1) for i in range(10)])
    row = 0
    for i in range(10):
        if i % _NUM_COLS == 0:
            row+=1
        fig.add_trace(pie_chart(i), row=row, col= i % _NUM_COLS + 1)

    fig.update_traces(textposition='inside')
    fig.update_layout(height=2400, 
                      legend_title="Legend",
        font=dict(
            size=12
        ),legend=dict(
            orientation="h",
            entrywidth=60,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
        )
    return fig


def create_portfolio_df(proj_names, matrix):
    df = pd.DataFrame(matrix)
    df.insert(0, 'Projects (down)/ Portfolio # (right)', proj_names)
    return df.to_csv().encode('utf-8')

def scatter_plot():
    df = pd.DataFrame(columns=['Mean of Portfolio Returns', 'Standard Deviation of Portfolio Returns'])
    tech_projs_df = pd.read_csv('./data/tech_projects_out.csv')
    matrix = txt_to_matrix('./out/risk_return.txt')
    for i in range(len(matrix)):
        df = df._append({'Mean of Portfolio Returns': matrix[i][0], 'Standard Deviation of Portfolio Returns': matrix[i][1]}, ignore_index=True)
    trace1 = go.Scatter(x=df['Mean of Portfolio Returns'], y=df['Standard Deviation of Portfolio Returns'], mode='lines+markers', name='Portfolio (#) Return Risk')
    trace2 = go.Scatter(x=list(np.sqrt(tech_projs_df['value1_norm_var'])), y=list(tech_projs_df['value1_norm_mean']), mode='markers', name='Technology Project Return/Risk')
    fig = make_subplots()
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.update_traces(line={'width': 5},
                      marker=dict(size=8,
                              line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(
        xaxis_title="Mean of Portfolio Returns",
        yaxis_title="Standard Deviation of Portfolio Returns",
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
        )
    )
    return fig



with st.sidebar:
    st.title('🚀 ASTRA MPT Dashboard')
    st.text("Dataset Information:")
    step1 = st.container(border=True)
    dataset = step1.file_uploader('Select Dataset')

    m = mpt.MPT(dataset.name if dataset else "InstrumentData_Clean_Julia_Milton.xlsx")
    word_columns = m.get_instrument_options_cols()
    num_columns = m.get_cols()

    selected_tech_proj_var = step1.selectbox('Select a technology project variable from the dataset.', word_columns, index=7)
    selected_time_variable = step1.selectbox('Select a time numerical variable from the dataset.', num_columns, index=1)
    step1.write("Available numerical variables:")
    step1.code('\n'.join(num_columns))
    custom_function_name = step1.text_input('Custom Formula using numerical variables above', value='(1 / Resolution_m) / Mass_kg')

    st.text("Technology Projects Information:")
    step3 = st.container(border=True)
    tech_projects = step3.file_uploader('Upload Technology Projects')
    min_invest_frac = step3.slider("Select minimum investment percentage", 0, 100, value=0) / 100
    max_invest_frac = step3.slider("Select maximum investment percentage", 0, 100, value=100) / 100
    m.update_invest_fracs(min_invest_frac, max_invest_frac)
    custom_matrix = step3.file_uploader('Upload Custom Matrix Completion Factors')

    st.text("Optional Custom Modifications:")
    step4 = st.container(border=True)
    step4.file_uploader('Upload Custom Regression Constants')
    corr_matrix_file = step4.file_uploader('Upload Custom Correlation Matrix')

# try:
bar = st.progress(10)
with st.spinner(text='In progress'):
    regs = m.get_regs(selected_tech_proj_var, selected_time_variable)
    regs['Mass_kg'] = {'Imager': ('exp', 0.03, 2.90142159), 'Radiometer': ('exp', 0.02, 3.2906), "SyntheticApertureRadar": ('exp', 0.03, 5.2169), "Sounder": ('exp', 0.04, 2.90142159)}
    regs['Resolution_m'] = {'Imager': ('exp', -0.14, 7.21376830812), 'Radiometer': ('exp', -0.03, 10.8462644), "SyntheticApertureRadar": ('exp', -0.16, 9.5217878), "Sounder": ('poly', 1.01 * 10 ** 6, -1.54)}
bar.progress(40)
with st.spinner(text='Building custom function'):
    def build_custom_function(variables, func):
        return eval('lambda ' + str(variables).replace("'", '')[1:-1] + ": " + func)
    custom_function = build_custom_function(num_columns, custom_function_name)
bar.progress(80)
with st.spinner(text='Generating graphs'):
    custom_matrix_file = custom_matrix.name if custom_matrix else "Custom_Matrix_ASTRA.xlsx"
    tech_projects_file = tech_projects.name if tech_projects else "Technology_Projects.xlsx"
    corr_matrix_file = corr_matrix_file.name if corr_matrix_file else "Custom_Correlation_Matrix.xlsx"
    m.generate_graphs(custom_matrix_file, tech_projects_file, selected_tech_proj_var, regs, num_columns, custom_function, corr_projects_filename=corr_matrix_file)
    bar.progress(95)
    time.sleep(1)
    bar.empty()
    st.toast("Completed generating graphs")

col = st.columns((0.65, 0.35), gap='large')
with col[0]:
    st.title('Recommended Portfolios')
    tech_proj_names = m.get_tech_projects(tech_projects_file)
    pwgt_matrix = txt_to_matrix('./out/pwgt1.txt')
    pwgt_df = create_pwgt_df(tech_proj_names, pwgt_matrix)
    pwgt_stacked_bar_fig = portfolio_plot(pwgt_df)
    st.markdown("#### Risk and Return for 20 Calculated Portfolios")
    fig = scatter_plot()
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown("#### Portfolio Weights for each Portfolio #")
    st.plotly_chart(pwgt_stacked_bar_fig, use_container_width=True)
    st.markdown("#### Download Portfolio Calculations")

    st.write("Download csv file for the calculated portfolio investments:")
    st.download_button('Download CSV file of portfolios', data=create_portfolio_df(tech_proj_names, pwgt_matrix), file_name='portfolio_investments.csv', mime='text/csv',)
with col[1]:
    with st.expander('About this Application', expanded=False):
        st.write('''
            - Paper: [Application of Markowitz Portfolio Theory for Space Technologies](https://drive.google.com/file/d/1o7cFdl9_NCfGeJULHbUtofH8E9j1vR3K/view?usp=sharing).
            - :orange[**Markowitz Portfolio Theory**]: Building a portfolio of investments while maximizing expected return 
            - :orange[**Contributors to Project**]: Roderick Huang, Afreen Siddiqi, Julian Milton, Olivier de Weck
            ''')
    st.markdown("#### Pie Charts for First 10 Calculated Portfolios")
    pie_charts = get_all_pie_charts(pwgt_df)
    st.plotly_chart(pie_charts, use_container_width=True, use_container_height=True)
# except:
    # st.error('Invalid input. Please try something else.', icon="🚨")