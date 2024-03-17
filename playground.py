import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import random
from datetime import datetime
from itertools import combinations
import math

df = pd.read_excel("./data" + "/" + 'InstrumentData_Clean_Julia_Milton.xlsx')

def get_regs(asset_name, time_variable):
        def lin_func(x, a, b):     
            return a * x + b
        def r_squared(y, y_pred):
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y_pred)) ** 2)

            if ss_tot != 0:
                return 1 - (ss_res / ss_tot)
            return 1

        assets = df[asset_name].unique()

        num_cols = get_cols()

        num_cols.remove(time_variable)
        res = {col_name: [] for col_name in num_cols}
        for col_name in num_cols:
            asset_res = {}
            for asset in assets:
                if type(asset) != str:
                    continue
                ## Mean version
                df_inst = df.query(asset_name + ' == "' + asset + '"')[[col_name, time_variable, asset_name]]
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
                df_inst = df.query(asset_name + ' == "' + asset + '"')[[col_name, time_variable, asset_name]]
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