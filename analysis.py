import json
import os
import sys
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
import seaborn as sns

from common import abbreviate_property_name, get_configs_path, get_non_property_column_names, get_plots_path, get_processed_data_path

sns.set_palette(sns.color_palette(["#ef7c8e", "#4c956c", "#d68c45"]))
warnings.filterwarnings('ignore')

"""
Data Exploration Plots
"""
def score_histograms(df, exp_name, constraints):
    def create_histograms_facet(df, exp_name, figure, title=None, facet=""): 
        figure.map_dataframe(sns.histplot, x="score", stat="proportion", binwidth=50)
        figure.set_axis_labels("Score", "Proportion")
        figure.set(ylim=(0, 0.5), xlim=(min(df["score"]), max(df["score"])))
        figure.tight_layout()
        if title:
            figure.fig.suptitle(title)
        figure.savefig(f"{get_plots_path()}{exp_name}/histogram_score_facet{facet}.png")

    if len(constraints) == 1:
        figure = sns.FacetGrid(df, col=constraints[0])
        create_histograms_facet(df, exp_name, figure, title=None, facet="")
    elif len(constraints) == 2:
        figure = sns.FacetGrid(df, col=constraints[0], row=constraints[1])
        create_histograms_facet(df, exp_name, figure, title=None, facet="")
    elif len(constraints) == 3:
        for i,facet_target in enumerate(df[constraints[2]].unique()):
            df_facet = df.loc[df[constraints[2]] == facet_target]
            figure = sns.FacetGrid(df_facet, col=constraints[0], row=constraints[1])
            create_histograms_facet(df, exp_name, figure, title=f"{constraints[2]} = {facet_target}", facet=i)


def score_correlation(df, param_names, exp_name, grouping):
    figure, axis = plt.subplots(1, 1, figsize=(8,4))
    for i in df[grouping].unique():
        df_group = df.loc[df[grouping] == i]
        scores = df_group["score"].values
        correlations = [np.corrcoef(df_group[param].values, scores)[0,1] for param in param_names]
        axis.scatter(correlations, range(len(param_names)), label=i)
    axis.yaxis.set_ticks(list(range(len(param_names))), param_names)
    figure.tight_layout(rect=[0, 0.03, 1, 0.95])
    figure.suptitle(f"{exp_name} correlation between parameters and score")
    figure.supxlabel("Correlation with score")
    plt.grid(axis="y")
    plt.savefig(f"{get_plots_path()}{exp_name}/correlation_score.png")
    plt.close()


def score_heatmaps(df, exp_name, constraints):
    def build_heatmap(*args, **kwargs):
        df = kwargs.pop("data")
        constraint0_targets = args[0]
        constraint1_targets = args[1]
        constraint_means = []
        for target1 in constraint1_targets:
            constraint_means_row = []
            for target0 in constraint0_targets:
                constraint_means_row.append(df.loc[(df[constraints[0]] == target0) & (df[constraints[1]] == target1)]["score"].mean())
            constraint_means.append(constraint_means_row)
        df_t = pd.DataFrame(constraint_means, index=constraint0_targets, columns=constraint1_targets)
        sns.heatmap(df_t, center=0, vmin=min(df["score"]), vmax=max(df["score"]), cmap="PiYG", square=True)

    def create_heatmaps_facet(df, exp_name, figure, title=None, facet=""):
        figure.map_dataframe(build_heatmap, sorted(df[constraints[0]].unique()), sorted(df[constraints[1]].unique()))
        figure.set_axis_labels(constraints[0], constraints[1])
        figure.tight_layout()
        if title:
            figure.fig.suptitle(title)
        figure.savefig(f"{get_plots_path()}{exp_name}/heatmap_score_facet{facet}.png")

    if len(constraints) == 2:
        figure = sns.FacetGrid(df)
        create_heatmaps_facet(df, exp_name, figure, title=None, facet="")
    elif len(constraints) == 3:
        figure = sns.FacetGrid(df, col=constraints[2])
        create_heatmaps_facet(df, exp_name, figure, title=None, facet="")
    elif len(constraints) == 4:
        for i,facet_target in enumerate(df[constraints[3]].unique()):
            df_facet = df.loc[df[constraints[3]] == facet_target]
            figure = sns.FacetGrid(df_facet, col=constraints[2], row=constraints[3])
            create_heatmaps_facet(df, exp_name, figure, title=f"{constraints[2]} = {facet_target}", facet=i)


"""
Other Functions
"""
def param_correlation_heatmap(df, param_names, exp_name):
    figure = plt.figure()
    df_params = df[param_names]
    corr = df_params.corr()
    sns.heatmap(corr, center=0, vmin=-1, vmax=1, cmap="PiYG")
    figure.tight_layout()
    plt.savefig(f"{get_plots_path()}{exp_name}/correlation_param.png")
    plt.close()


def plot_score_correlated_properties(df, param_names, exp_name, constraints):
    def create_scatter_facet(df, param, exp_name, figure, title=None, facet=""): 
        figure.map_dataframe(sns.scatterplot, x=param, y="score")
        figure.set_axis_labels(param, "score")
        figure.set(xlim=(min(df[param]), max(df[param])), ylim=(min(df["score"]), max(df["score"])))
        figure.tight_layout()
        if title:
            figure.fig.suptitle(title)
        figure.savefig(f"{get_plots_path()}{exp_name}/score_{param}_facet{facet}.png")

    configs = sorted(df["config_num"].unique())
    num_params = len(param_names)
    highly_correlated = set()
    correlations = dict()
    for i in configs:
        df_group = df.loc[df["config_num"] == i]
        scores = df_group["score"].values
        correlations[i] = {param:np.corrcoef(df_group[param].values, scores)[0,1] for param in param_names}
        for j in range(num_params):
            param = param_names[j]
            correlation = correlations[i][param]
            if abs(correlation) > 0.2:
                highly_correlated.add(param)

    for p in highly_correlated:
        if len(constraints) == 1:
            figure = sns.FacetGrid(df, col=constraints[0])
            create_scatter_facet(df, p, exp_name, figure, title=None, facet="")
        elif len(constraints) == 2:
            figure = sns.FacetGrid(df, col=constraints[0], row=constraints[1])
            create_scatter_facet(df, p, exp_name, figure, title=None, facet="")
        elif len(constraints) == 3:
            for i,facet_target in enumerate(df[constraints[2]].unique()):
                df_facet = df.loc[df[constraints[2]] == facet_target]
                figure = sns.FacetGrid(df_facet, col=constraints[0], row=constraints[1])
                create_scatter_facet(df, p, exp_name, figure, title=f"{constraints[2]} = {facet_target}", facet=i)


"""
Main functions
"""
def read_data(exp_name):
    file_path = get_processed_data_path()
    df = pd.read_pickle(f"{file_path}{exp_name}.pkl")
    param_names = list(set(df.columns) - set(get_non_property_column_names()))
    df = df.reset_index()

    config_num = df["config_num"].unique()[0] #assumes all configs for one exp name hold the same constraints
    config = json.load(open(f"{get_configs_path()}{exp_name}/{config_num}.json"))
    constraints = []
    for constraint in [p for p in config["eval_funcs"].keys() if p != "weak_components"]:
        constraint_abbrv = abbreviate_property_name(constraint)
        if is_numeric_dtype(df[constraint_abbrv]):
            df[constraint_abbrv] = df[constraint_abbrv].round(1)
        constraints.append(constraint_abbrv)

    return df, param_names, constraints


def main(exp_name):
    df, param_names, constraints = read_data(exp_name)
    numeric_param_names = [x for x in param_names if is_numeric_dtype(df[x])]

    path = f"{get_plots_path()}{exp_name}"
    if not os.path.exists(path):
        os.makedirs(path)

    score_correlation(df, numeric_param_names, exp_name, "config_num")
    plot_score_correlated_properties(df, numeric_param_names, exp_name, constraints)
    score_histograms(df, exp_name, constraints)
    score_heatmaps(df, exp_name, constraints)

    if exp_name == "uniform":
        param_correlation_heatmap(df, numeric_param_names, exp_name)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        exp_name = sys.argv[1]
        print(exp_name)
        main(exp_name)
    else:
        print("Please provide an experiment name.")