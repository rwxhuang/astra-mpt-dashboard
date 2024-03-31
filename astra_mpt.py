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
            df = df._append({'Portfolio Number': i, 'Project Name': proj_name, 'Proportion': round(float(matrix[j][i]), 3)}, ignore_index=True)
    return df

def portfolio_plot(df):
    fig = px.bar(df, x='Portfolio Number', y='Proportion', color='Project Name')
    fig.update_layout(
        hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        )
    )
    return fig
def get_all_pie_charts(df, later_portfolios):
    _NUM_ROWS = 10
    _NUM_COLS = 2
    _RNG = range(20) if later_portfolios else range(10)

    def pie_chart(chart_num):
        pie = go.Pie(values=df.query('`Portfolio Number` == ' + str(chart_num))['Proportion'], labels=df.query('`Portfolio Number` == ' + str(chart_num))['Project Name'])
        return pie
    specs = [[{'type' : 'domain'} for _ in range (_NUM_COLS)] for _ in range(_NUM_ROWS)]
    fig = make_subplots(rows=_NUM_ROWS, cols=_NUM_COLS, specs=specs, subplot_titles=["Portfolio #" + str(i+1) for i in _RNG])
    row = 0
    for i in _RNG:
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
            x=1,
            traceorder='normal'
        )
        )
    return fig


def create_portfolio_df(proj_names, matrix):
    df = pd.DataFrame(matrix)
    df.insert(0, 'Projects (down)/ Portfolio # (right)', proj_names)
    return df.to_csv().encode('utf-8')

def scatter_plot(matrix):
    df = pd.DataFrame(columns=['Mean Return of Portfolio Returns', 'Risk of Portfolio (std dev.)', 'text_label'])
    tech_projs_df = pd.read_csv('./data/tech_projects_out.csv')
    for i in range(len(matrix)):
        df = df._append({'Risk of Portfolio (std dev.)': round(float(matrix[i][0]), 3), 'Mean Return of Portfolio Returns': round(float(matrix[i][1]), 3), 'text_label': 'Portfolio ' + str(i)}, ignore_index=True)
    trace1 = go.Scatter(x=df['Risk of Portfolio (std dev.)'], y=df['Mean Return of Portfolio Returns'], mode='lines+markers', name='Portfolio (#) Return Risk', text=df['text_label'])
    trace2 = go.Scatter(x=list(round(np.sqrt(tech_projs_df['value1_norm_var']), 3)), y=list(round(tech_projs_df['value1_norm_mean'], 3)), mode='markers', name='Technology Project Return/Risk', text=tech_projs_df['Name'])
    fig = make_subplots()
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.update_traces(line={'width': 5},
                      marker=dict(size=8,
                              line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(
        xaxis_title="Risk of Portfolio (std dev.)",
        yaxis_title="Mean Return of Portfolios",
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
    tech_proj_file = step3.file_uploader('Upload Technology Projects to Invest in:')
    tech_projects_df =  pd.read_excel(tech_proj_file) if tech_proj_file else pd.read_excel("./data" + "/" + "Technology_Projects.xlsx")
    tech_projects_df.columns = ['Name'] + list(tech_projects_df.columns[1:])
    step3.write("Tech projects: ")
    edited_tech_projects_df = step3.data_editor(tech_projects_df, num_rows="dynamic")
    m.set_tech_projects(edited_tech_projects_df.copy())
    tech_proj_names = list(edited_tech_projects_df['Name'])

    with st.expander('Optional custom modifications', expanded=False):
        # Setting minimum and maximum investment percentages
        min_max_df = pd.DataFrame(
            [{"project": tech_project, "min_invest_fraction": 0.0, "max_invest_fraction": 1.0} for tech_project in tech_proj_names]
        )
        st.write("Modify bounds for investment percentages [0.0-1.0]:")
        edited_min_max_df = st.data_editor(min_max_df, num_rows="fixed", column_config={
            "min_invest_fraction": st.column_config.NumberColumn(
                min_value=0.0,
                max_value=1.0
            ),
            "max_invest_fraction": st.column_config.NumberColumn(
                min_value=0.0,
                max_value=1.0
            )
        })
        bounds = [(edited_min_max_df["min_invest_fraction"][i], edited_min_max_df["max_invest_fraction"][i]) for i in range(len(tech_proj_names))]
        # Setting matrix completion factors (likely, pessimistic)
        completion_factors_df = pd.DataFrame(
            [{"project_type": project_type, "likely_factor": 1.1, "pessimistic_factor": 1.2} for project_type in m.get_assets(selected_tech_proj_var)]
        )
        ## Hardcoding values to match the paper
        row_index_1 = completion_factors_df.index[completion_factors_df['project_type'] == 'Radiometer']
        completion_factors_df.loc[row_index_1] = ['Radiometer', 1.2, 1.4]
        row_index_2 = completion_factors_df.index[completion_factors_df['project_type'] == 'Sounder']
        completion_factors_df.loc[row_index_2] = ['Sounder', 1.3, 1.5]

        st.write("Modify likely and pessimism factors for project types:")
        edited_completion_factors_df = st.data_editor(completion_factors_df, num_rows="fixed")
        m.set_custom_matrix(edited_completion_factors_df)

        # Setting correlation matrix
        corr_cont = st.container(border=True)
        corr_matrix_file = corr_cont.file_uploader('Upload Custom Correlation Matrix') 
        corr_matrix_df =  pd.read_excel(corr_matrix_file) if corr_matrix_file else pd.read_excel("./data" + "/" + "Custom_Correlation_Matrix.xlsx")
        corr_cont.write("Correlation coefficients: ")
        edited_corr_matrix_df = corr_cont.data_editor(corr_matrix_df, num_rows="fixed")
        m.set_correlation_matrix(edited_corr_matrix_df.copy())

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
    pwgt, risk_ret = m.generate_graphs(selected_tech_proj_var, regs, num_columns, custom_function, bounds)
    bar.progress(95)
    time.sleep(1)
    bar.empty()
    st.toast("Completed generating graphs")

col = st.columns((0.65, 0.35), gap='large')
with col[0]:
    st.title('Recommended Portfolios')
    # pwgt_matrix = txt_to_matrix('./out/pwgt1.txt')
    pwgt_df = create_pwgt_df(tech_proj_names, pwgt)
    pwgt_stacked_bar_fig = portfolio_plot(pwgt_df)
    st.markdown("#### Risk and Return for 20 Calculated Portfolios")
    fig = scatter_plot(risk_ret)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown("#### Portfolio Weights for each Portfolio #")
    st.plotly_chart(pwgt_stacked_bar_fig, use_container_width=True)

    st.markdown("#### Download Portfolio Calculations")
    st.write("Download csv file for the calculated portfolio investments:")
    st.download_button('Download CSV file of portfolios', data=create_portfolio_df(tech_proj_names, pwgt), file_name='portfolio_investments.csv', mime='text/csv',)
with col[1]:
    with st.expander('About this Application', expanded=False):
        st.write('''
            - Paper: [Application of Markowitz Portfolio Theory for Space Technologies](https://drive.google.com/file/d/1o7cFdl9_NCfGeJULHbUtofH8E9j1vR3K/view?usp=sharing).
            - :orange[**Markowitz Portfolio Theory**]: Building a portfolio of investments while maximizing expected return 
            - :orange[**Contributors to Project**]: Roderick Huang, Afreen Siddiqi, Julian Milton, Olivier de Weck
            ''')
    st.markdown("#### Pie Charts for Calculated Portfolios")
    on = st.toggle("Toggle to view all 20 portfolio pie charts")
    pie_charts = get_all_pie_charts(pwgt_df, later_portfolios=on)
    st.plotly_chart(pie_charts, use_container_width=True, use_container_height=True)
