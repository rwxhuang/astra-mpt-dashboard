import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from itertools import combinations
from pypfopt import EfficientFrontier
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
    
    def get_assets(self, asset_name):
        return self.df[asset_name].unique()
    
    def get_regs(self, asset_name, time_variable):
        def lin_func(x, a, b):     
            return a * x + b
        def r_squared(y, y_pred):
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y_pred)) ** 2)

            if ss_tot != 0:
                return 1 - (ss_res / ss_tot)
            return 1

        assets = self.get_assets(asset_name)

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
    
    def set_custom_matrix(self, df):
        self.custom_matrix = {row.iloc[0]: (0, row.iloc[1], row.iloc[2]) for _, row in df.iterrows()}
    
    def generate_graphs(self, asset_name, regs, variables, custom_function, bounds, corr_projects_filename=None):

        def reg_func(name, a, x, b):
            if name == 'exp':
                return math.e ** (a * x + b)
            if name == 'poly':
                return a * x ** b
        
        matrix_names = ['optimistic', 'likely', 'pessimistic']

        # Get the current year
        # currentYear = datetime.now().year
        currentYear = 2023
        
        # Compute 'value' for each new instrument
        ## Create column for optimistic, likely, pessimistic

        for i in range(3):
            self.tech_projects_df['Year_' + matrix_names[i]] = self.tech_projects_df.apply(lambda row: math.ceil(row['Year'] + (row['Year'] - currentYear) * self.custom_matrix[row[asset_name]][i]), axis=1)
            self.tech_projects_df['deltaT_' + matrix_names[i]] = self.tech_projects_df['Year_' + matrix_names[i]] - 1960
            for var in variables:
                if var in self.tech_projects_df.columns and var in regs:
                    params = regs[var]
                    self.tech_projects_df['Projected_' + var + '_' + matrix_names[i] + 'Year'] = self.tech_projects_df.apply(lambda row: reg_func(params[row[asset_name]][0], params[row[asset_name]][1], row['deltaT_' + matrix_names[i]], params[row[asset_name]][2]), axis=1)
        ## Calculate values from custom function
        self.tech_projects_df['value1'] = self.tech_projects_df.apply(lambda row: custom_function(*(row[var] if var in self.tech_projects_df.columns else None for var in variables)), axis=1)
        self.tech_projects_df['value1_norm'] = self.tech_projects_df['value1'] / self.tech_projects_df.apply(lambda row: custom_function(*(row['Projected_' + var  + '_optimisticYear'] if 'Projected_' + var + '_optimisticYear' in self.tech_projects_df.columns else None for var in variables)), axis=1)
        self.tech_projects_df['value1_norm_likely'] = self.tech_projects_df['value1'] / self.tech_projects_df.apply(lambda row: custom_function(*(row['Projected_' + var + '_likelyYear'] if 'Projected_' + var + '_likelyYear' in self.tech_projects_df.columns else None for var in variables)), axis=1)
        self.tech_projects_df['value1_norm_pessimistic'] = self.tech_projects_df['value1'] / self.tech_projects_df.apply(lambda row: custom_function(*(row['Projected_' + var + '_pessimisticYear'] if 'Projected_' + var + '_pessimisticYear' in self.tech_projects_df.columns else None for var in variables)), axis=1)

        self.tech_projects_df['value1_norm_mean'] = (self.tech_projects_df['value1_norm'] + self.tech_projects_df['value1_norm_likely'] + self.tech_projects_df['value1_norm_pessimistic']) / 3
        self.tech_projects_df['value1_norm_var'] = (self.tech_projects_df['value1_norm'] ** 2 +  self.tech_projects_df['value1_norm_likely'] ** 2 + self.tech_projects_df['value1_norm_pessimistic'] ** 2 - self.tech_projects_df['value1_norm'] * self.tech_projects_df['value1_norm_likely'] - self.tech_projects_df['value1_norm'] * self.tech_projects_df['value1_norm_pessimistic'] - self.tech_projects_df['value1_norm_likely'] * self.tech_projects_df['value1_norm_pessimistic']) / 18

        # Output new csv file with calculated values
        self.tech_projects_df.to_csv('./data/tech_projects_out.csv', index=False)

        # TODO - Get the correlation matrices and covariance matrices
        ## Correlation coeffs
        corr_matrix = {}
        # if not corr_projects_filename:
        #     corr_coeffs = {}
        #     for asset_type_1, asset_type_2 in combinations(self.tech_projects_df[asset_name].unique(), 2):
        #         corr_coeffs[(asset_type_1, asset_type_2)] = np.array([[random.random(), random.random()], [random.random(), random.random()]])
        #     ## Correlation Matrix
        #     corr_matrix = {key: corr_coeffs[key][0][1] for key in corr_coeffs}
        #     for asset_type in self.tech_projects_df[asset_name].unique():
        #         corr_matrix[(asset_type, asset_type)] = 1
        # else: 
        assets = [arr[0] for arr in self.corr_df.values]
        for asset_type_1, asset_type_2 in combinations(self.tech_projects_df[asset_name].unique(), 2):
            index1 = assets.index(asset_type_1)
            index2 = assets.index(asset_type_2) + 1
            corr_matrix[(asset_type_1, asset_type_2)] = self.corr_df.values[index1][index2]
        for asset_type in self.tech_projects_df[asset_name].unique():
            corr_matrix[(asset_type, asset_type)] = 1

        ## Covariance matrix
        cov_matrix = []
        for i, row1 in self.tech_projects_df.iterrows():
            temp = []
            for j, row2 in self.tech_projects_df.iterrows():
                asset_type_1, asset_type_2 = row1[asset_name], row2[asset_name]
                if (asset_type_1, asset_type_2) in corr_matrix:
                    temp.append(corr_matrix[(asset_type_1, asset_type_2)] * math.sqrt(row1['value1_norm_var'] * row2['value1_norm_var'] ))
                elif (asset_type_2, asset_type_1) in corr_matrix:
                    temp.append(corr_matrix[(asset_type_2, asset_type_1)] * math.sqrt(row1['value1_norm_var'] * row2['value1_norm_var'] ))
            cov_matrix.append(temp)

        # Calculating efficient frontier
        ef = EfficientFrontier(self.tech_projects_df['value1_norm_mean'], np.array(cov_matrix), weight_bounds=bounds)
        _NUM_PORTS = 20
        res_weights = []
        res_risk_return = []
        vars = list(self.tech_projects_df['value1_norm_var'])
        if not ef._max_return_value:
            a = ef.deepcopy()
            max_return = a._max_return()
        else:
            max_return = ef._max_return_value
        for mean in np.linspace(min(self.tech_projects_df['value1_norm_mean']), float(max_return), num=20):
            weights = ef.efficient_return(mean)
            weights_arr = [weights[i] for i in range(len(weights))]
            std = sum([weights_arr[i] ** 2 * vars[i] for i in range(len(weights_arr))]) ** 0.5
            res_risk_return.append([std, mean])
            res_weights.append(np.array([weights_arr]).T)
        res_weights = np.concatenate(res_weights, axis=1)
        return res_weights, res_risk_return
    
    def get_tech_projects(self, tech_projects_filename):
        self.tech_projects_df = pd.read_excel("./data" + "/" + tech_projects_filename)
        self.tech_projects_df.columns = ['Name'] + list(self.tech_projects_df.columns[1:])

        return list(self.tech_projects_df['Name'])
    
    def set_tech_projects(self, df):
        self.tech_projects_df = df

    def set_correlation_matrix(self, df):
        self.corr_df = df