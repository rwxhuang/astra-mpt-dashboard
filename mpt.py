import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matlab.engine
import random
from datetime import datetime
from itertools import combinations
import math

# # Change python version to 3.10
# UNCOMMENT TO DOWNGRADE PYTHON VERSION MANUALLY
import os
# os.system("pyenv install 3.10")
# os.system("pyenv global 3.10")
# os.system('eval "$(pyenv init --path)"')

class MPT:
    def __init__(self, file_name):
        self.df = pd.read_excel("./data" + "/" + file_name)
    
    def get_cols(self):
        return list(self.df.select_dtypes(include=['number']).columns)
    
    def get_instrument_options_cols(self):
        return list(self.df.select_dtypes(exclude=['number']).columns)
    
    def get_regs(self, asset_name, time_variable):
        def lin_func(x, a, b):     
            return a * x + b
        def r_squared(y, y_pred):
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y_pred)) ** 2)

            if ss_tot != 0:
                return 1 - (ss_res / ss_tot)
            return 1

        assets = self.df[asset_name].unique()

        num_cols = self.get_cols()

        num_cols.remove(time_variable)
        res = {col_name: [] for col_name in num_cols}
        for col_name in num_cols:
            asset_res = {}
            for asset in assets:
                if type(asset) != str:
                    continue
                ## Mean version
                df_inst = self.df.query(asset_name + ' == "' + asset + '"')[[col_name, time_variable, asset_name]]
                if len(df_inst) < 20:
                    continue
                df_inst = df_inst[df_inst[col_name].notna()][df_inst[time_variable].notna()]
                df_inst = df_inst.groupby([time_variable, asset_name])[col_name].mean()
                df_inst = df_inst.reset_index()
                df_inst['Time'] = df_inst[time_variable] - 1960 if np.mean(df_inst[time_variable]) > 1960 else df_inst[time_variable]
                df_inst['log_var'] = np.log(df_inst[col_name])
                if len(df_inst) <= 1:
                    continue
                params_mean, _ = curve_fit(lin_func, df_inst['Time'], df_inst['log_var'])
                r_squared_mean = r_squared(df_inst['log_var'], lin_func(df_inst['Time'], *params_mean))
                ## Min version
                df_inst = self.df.query(asset_name + ' == "' + asset + '"')[[col_name, time_variable, asset_name]]
                if len(df_inst) < 20:
                    continue
                df_inst = df_inst[df_inst[col_name].notna()][df_inst[time_variable].notna()]
                df_inst = df_inst.groupby([time_variable, asset_name])[col_name].min()
                df_inst = df_inst.reset_index()
                df_inst['Time'] = df_inst[time_variable] - 1960 if np.mean(df_inst[time_variable]) > 1960 else df_inst[time_variable]
                df_inst['log_var'] = np.log(df_inst[col_name])
                if len(df_inst) <= 1:
                    continue
                params_min, _ = curve_fit(lin_func, df_inst['Time'], df_inst['log_var'])
                r_squared_min = r_squared(df_inst['log_var'], lin_func(df_inst['Time'], *params_min))
                asset_res[asset] = ('exp', params_mean[0], params_mean[1]) if r_squared_mean > r_squared_min else ('exp', params_min[0], params_min[1])
            res[col_name] = asset_res
        return res
    
    def generate_graphs(self, custom_matrix_filename, tech_projects_filename, asset_name, regs, variables, custom_function, corr_projects_filename=None):

        def reg_func(name, a, x, b):
            if name == 'exp':
                return math.e ** (a * x + b)
            if name == 'poly':
                return a * x ** b
        custom_matrix_df = pd.read_excel("./data" + "/" + custom_matrix_filename)
        custom_matrix = {row.iloc[0]: (row.iloc[1], row.iloc[2], row.iloc[3]) for _, row in custom_matrix_df.iterrows()}
        matrix_names = ['optimistic', 'likely', 'pessimistic']
        tech_projs_df = pd.read_excel("./data" + "/" + tech_projects_filename)
        tech_projs_df.columns = ['Name'] + list(tech_projs_df.columns[1:])

        # Get the current year
        # currentYear = datetime.now().year
        currentYear = 2023
        
        # Compute 'value' for each new instrument
        ## Create column for optimistic, likely, pessimistic

        for i in range(3):
            tech_projs_df['Year_' + matrix_names[i]] = tech_projs_df.apply(lambda row: math.ceil(row['Year'] + (row['Year'] - currentYear) * custom_matrix[row[asset_name]][i]), axis=1)
            tech_projs_df['deltaT_' + matrix_names[i]] = tech_projs_df['Year_' + matrix_names[i]] - 1960
            for var in variables:
                if var in tech_projs_df.columns and var in regs:
                    params = regs[var]
                    tech_projs_df['Projected_' + var + '_' + matrix_names[i] + 'Year'] = tech_projs_df.apply(lambda row: reg_func(params[row[asset_name]][0], params[row[asset_name]][1], row['deltaT_' + matrix_names[i]], params[row[asset_name]][2]), axis=1)
        ## Calculate values from custom function
        tech_projs_df['value1'] = tech_projs_df.apply(lambda row: custom_function(*(row[var] if var in tech_projs_df.columns else None for var in variables)), axis=1)
        tech_projs_df['value1_norm'] = tech_projs_df['value1'] / tech_projs_df.apply(lambda row: custom_function(*(row['Projected_' + var  + '_optimisticYear'] if 'Projected_' + var + '_optimisticYear' in tech_projs_df.columns else None for var in variables)), axis=1)
        tech_projs_df['value1_norm_likely'] = tech_projs_df['value1'] / tech_projs_df.apply(lambda row: custom_function(*(row['Projected_' + var + '_likelyYear'] if 'Projected_' + var + '_likelyYear' in tech_projs_df.columns else None for var in variables)), axis=1)
        tech_projs_df['value1_norm_pessimistic'] = tech_projs_df['value1'] / tech_projs_df.apply(lambda row: custom_function(*(row['Projected_' + var + '_pessimisticYear'] if 'Projected_' + var + '_pessimisticYear' in tech_projs_df.columns else None for var in variables)), axis=1)

        tech_projs_df['value1_norm_mean'] = (tech_projs_df['value1_norm'] + tech_projs_df['value1_norm_likely'] + tech_projs_df['value1_norm_pessimistic']) / 3
        tech_projs_df['value1_norm_var'] = (tech_projs_df['value1_norm'] ** 2 +  tech_projs_df['value1_norm_likely'] ** 2 + tech_projs_df['value1_norm_pessimistic'] ** 2 - tech_projs_df['value1_norm'] * tech_projs_df['value1_norm_likely'] - tech_projs_df['value1_norm'] * tech_projs_df['value1_norm_pessimistic'] - tech_projs_df['value1_norm_likely'] * tech_projs_df['value1_norm_pessimistic']) / 18

        # Output new csv file with calculated values
        tech_projs_df.to_csv('./data/tech_projects_out.csv', index=False)

        # GRAPH 1/2 - Expected return VS Standard Deviation
        plt.scatter(tech_projs_df['value1_norm_var'] ** 0.5, tech_projs_df['value1_norm_mean'], color='blue', marker='o')

        for i, txt in enumerate(tech_projs_df.iloc[:,0]):
            plt.annotate(txt, ((tech_projs_df['value1_norm_var'] ** 0.5)[i], tech_projs_df['value1_norm_mean'][i]))
        plt.xlabel('Standard Deviation')
        plt.ylabel('Expected Return')
        plt.savefig('./out/mpt_graph_1_2.png')

        # TODO - Get the correlation matrices and covariance matrices
        ## Correlation coeffs
        corr_matrix = {}
        if not corr_projects_filename:
            corr_coeffs = {}
            for asset_type_1, asset_type_2 in combinations(tech_projs_df[asset_name].unique(), 2):
                corr_coeffs[(asset_type_1, asset_type_2)] = np.array([[random.random(), random.random()], [random.random(), random.random()]])
            ## Correlation Matrix
            corr_matrix = {key: corr_coeffs[key][0][1] for key in corr_coeffs}
            for asset_type in tech_projs_df[asset_name].unique():
                corr_matrix[(asset_type, asset_type)] = 1
        else:
            corr_df = pd.read_excel("./data" + "/" + corr_projects_filename)
            assets = [arr[0] for arr in corr_df.values]
            for asset_type_1, asset_type_2 in combinations(tech_projs_df[asset_name].unique(), 2):
                index1 = assets.index(asset_type_1)
                index2 = assets.index(asset_type_2) + 1
                corr_matrix[(asset_type_1, asset_type_2)] = corr_df.values[index1][index2]
            for asset_type in tech_projs_df[asset_name].unique():
                corr_matrix[(asset_type, asset_type)] = 1

        ## Covariance matrix
        cov_matrix = []
        for i, row1 in tech_projs_df.iterrows():
            temp = []
            for j, row2 in tech_projs_df.iterrows():
                asset_type_1, asset_type_2 = row1[asset_name], row2[asset_name]
                if (asset_type_1, asset_type_2) in corr_matrix:
                    temp.append(corr_matrix[(asset_type_1, asset_type_2)] * math.sqrt(row1['value1_norm_var'] * row2['value1_norm_var'] ))
                elif (asset_type_2, asset_type_1) in corr_matrix:
                    temp.append(corr_matrix[(asset_type_2, asset_type_1)] * math.sqrt(row1['value1_norm_var'] * row2['value1_norm_var'] ))
            cov_matrix.append(temp)

        with open("./data/cov_matrix.txt", "w") as txt_file:
            for line in cov_matrix:
                txt_file.write("".join(str(line)[1:-1]) + "\n")

        eng = matlab.engine.start_matlab()
        eng.myScript(nargout=0)
    
    def get_tech_projects(self, tech_projects_filename):
        tech_projs_df = pd.read_excel("./data" + "/" + tech_projects_filename)
        tech_projs_df.columns = ['Name'] + list(tech_projs_df.columns[1:])

        return list(tech_projs_df['Name'])
        