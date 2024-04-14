colors = ["#E6B0AA", "#D7BDE2", "#D4E6F1", "#D1F2EB", "#A9DFBF", 
            "#F9E79F", "#F5CBA7", "#DC7633", "#E5E7E9", "#AEB6BF", 
            "#C0392B", "#9B59B6", "#3498DB", "#48C9B0", "#F1C40F",
            "#BA4A00", "#2E4053", "#641E16", "#512E5F", "#1B4F72",
            "#0B5345", "#186A3B", "#7E5109", "#7B7D7D", "#16A085", "#FCF3CF"]
import pandas as pd

class Graph:
    def __init__(self, df):
        self.df = df[1:]
        self.df['TX_truncated'] = self.df['Technology Area'].str[:2]

class Graph1A(Graph):
    def generate_graph(self):
        counts_per_year_per_taxonomy = self.df.groupby([self.df['Start Year'], 'TX_truncated']).size()
        res_df = pd.DataFrame(columns=['Year', 'Taxonomy Level', 'Count'])
        for group in counts_per_year_per_taxonomy.index:
            res_df = res_df._append({'Year': group[0], 'Taxonomy Level': group[1], 'Count': counts_per_year_per_taxonomy[group]}, ignore_index=True)
        return res_df
class Graph1B(Graph):
    def generate_graph(self):
        counts_per_year_per_taxonomy = self.df[self.df['End Year'] >= 2023].groupby([self.df['End Year'], 'TX_truncated']).size()
        res_df = pd.DataFrame(columns=['Year', 'Taxonomy Level', 'Count'])
        for group in counts_per_year_per_taxonomy.index:
            res_df = res_df._append({'Year': group[0], 'Taxonomy Level': group[1], 'Count': counts_per_year_per_taxonomy[group]}, ignore_index=True)
        return res_df

class Graph2A(Graph):
    def generate_graph(self):
        counts_per_year_per_taxonomy = self.df.groupby([self.df['Start Year'], 'Start TRL']).size()
        res_df = pd.DataFrame(columns=['Year', 'TRL Level', 'Count'])
        for group in counts_per_year_per_taxonomy.index:
            res_df = res_df._append({'Year': group[0], 'TRL Level': group[1], 'Count': int(counts_per_year_per_taxonomy[group])}, ignore_index=True)
        return res_df

class Graph2B(Graph):
    def generate_graph(self):
        counts_per_year_per_taxonomy = self.df.groupby([self.df['Start Year'], 'Estimated End TRL']).size()
        res_df = pd.DataFrame(columns=['Year', 'Estimated End TRL', 'Count'])
        for group in counts_per_year_per_taxonomy.index:
            res_df = res_df._append({'Year': group[0], 'TRL Level': group[1], 'Count': int(counts_per_year_per_taxonomy[group])}, ignore_index=True)
        return res_df
        