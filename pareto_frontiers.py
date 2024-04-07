import pandas as pd
import numpy as np
import math


class ParetoFrontiers:
    def __init__(self, file_name):
        read_file = pd.read_excel("./data" + "/" + file_name)
        self.df = pd.DataFrame(read_file)

    def get_cols(self):
        return list(self.df.columns.values)

    def get_instruments(self):
        return list(set(self.df["Instrument_Type"]))

    def get_scatter(
        self, x_axis, y_axis, log_x, log_y, query_string="", custom_string=""
    ):
        res_df = self.df.copy()
        
        if query_string != "":
            res_df = res_df.query(query_string)
        res_df = res_df[[x_axis, y_axis]].dropna()
        if log_x:
            res_df[x_axis] = res_df[x_axis].apply(lambda x: np.log(x) if x > 0 else 0)
        if log_y:
            res_df[y_axis] = res_df[y_axis].apply(lambda y: np.log(y) if y > 0 else 0)
        res_df = res_df.round(3)
        if custom_string:
            res_df = res_df.groupby(eval(custom_string))
            return [df for _, df in res_df]
        return [res_df]

    def generate_frontier(self, scatter_dfs, x_pareto_max, y_pareto_max):
        def get_pareto_coors(coors):
            pareto_coors = {}
            if not x_pareto_max and not y_pareto_max:
                for coor in coors:
                    if (coor[1] < pareto_coors.get(coor[0], (float("inf"), float("inf")))[1]):
                        pareto_coors[coor[0]] = (coor[0], coor[1])
            elif not x_pareto_max and y_pareto_max:
                for coor in coors:
                    if (coor[0] < pareto_coors.get(coor[1], (float("inf"), float("inf")))[0]):
                        pareto_coors[coor[1]] = (coor[0], coor[1])
            return list(pareto_coors.values())

        def filter_pareto_coors(coors):
            score_arr = []
            for i, coor1 in enumerate(coors):
                scores = []
                for j, coor2 in enumerate(coors):
                    score = 0
                    if i == j:
                        scores.append(1)
                        continue
                    if x_pareto_max:
                        if coor1[0] > coor2[0]:
                            score += 1
                        else:
                            score -= 1
                    else:
                        if coor1[0] < coor2[0]:
                            score += 1
                        else:
                            score -= 1
                    if y_pareto_max:
                        if coor1[1] > coor2[1]:
                            score += 1
                        else:
                            score -= 1
                    else:
                        if coor1[1] < coor2[1]:
                            score += 1
                        else:
                            score -= 1
                    scores.append(1 if score >= 0 else 0)
                score_arr.append(scores)
            res = []
            for i, row in enumerate(score_arr):
                if sum(row) == len(coors):
                    res.append(coors[i])
            res.sort()
            return res

        frontiers = []
        for df in scatter_dfs:
            coors = [tuple(row) for _, row in df.iterrows()]
            axis_names = df.columns.tolist()
            pareto_coors = get_pareto_coors(coors)
            final_pareto_coors = filter_pareto_coors(pareto_coors)
            pareto_coors_df = pd.DataFrame(columns=axis_names)
            for coor in final_pareto_coors:
                pareto_coors_df = pareto_coors_df._append({axis_names[0]: coor[0], axis_names[1]: coor[1]}, ignore_index=True)
            frontiers.append(pareto_coors_df)
        return frontiers

