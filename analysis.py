import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from common import get_configs_path, get_non_property_column_names, get_plots_path, get_processed_data_path
from save_properties import abbreviate_property_name

sns.set_palette(sns.color_palette(["#ef7c8e", "#4c956c", "#d68c45"]))

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


def score_heatmap(df, exp_name, constraints):
    if len(constraints) != 2:
        return
    constraint0_targets = sorted(df[constraints[0]].unique())
    constraint1_targets = sorted(df[constraints[1]].unique())
    constraint_means = []
    for target1 in constraint1_targets:
        constraint_means_row = []
        for target0 in constraint0_targets:
            constraint_means_row.append(df.loc[(df[constraints[0]] == target0) & (df[constraints[1]] == target1)]["score"].mean())
        constraint_means.append(constraint_means_row)
    df_t = pd.DataFrame(constraint_means, index=constraint0_targets, columns=constraint1_targets)
    figure = plt.figure()
    ax = sns.heatmap(df_t, center=0, vmin=min(df["score"]), vmax=max(df["score"]), cmap="coolwarm")
    ax.set(xlabel=constraints[0], ylabel=constraints[1], title="Mean Score")
    figure.tight_layout()
    plt.savefig(f"{get_plots_path()}{exp_name}/heatmap_mean_score.png")
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
        sns.heatmap(df_t, center=0, vmin=min(df["score"]), vmax=max(df["score"]), cmap="coolwarm")

    def create_heatmaps_facet(df, exp_name, figure, title=None, facet=""):
        figure.map_dataframe(build_heatmap, sorted(df[constraints[0]].unique()), sorted(df[constraints[1]].unique()))
        figure.set_axis_labels(constraints[0], constraints[1])
        figure.tight_layout()
        if title:
            figure.fig.suptitle(title)
        figure.savefig(f"{get_plots_path()}{exp_name}/histogram_score_facet{facet}.png")

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
    sns.heatmap(corr, center=0, vmin=-1, vmax=1, cmap="coolwarm")
    figure.tight_layout()
    plt.savefig(f"{get_plots_path()}{exp_name}/correlation_param.png")
    plt.close()


def plot_score_correlated_properties(df, param_names, exp_name):
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
        max_p = max(df[p])
        min_p = min(df[p])
        max_score = max(df["score"])
        min_score = min(df["score"])
        num_configs = len(configs)
        fig_col_cnt = 2 if num_configs <= 4 else 4
        fig_row_cnt = int(np.ceil(num_configs/fig_col_cnt))
        figure, axis = plt.subplots(fig_row_cnt, fig_col_cnt, figsize=(5*fig_row_cnt, 3*fig_col_cnt), squeeze=False)
        fig_row = 0
        fig_col = 0
        for i in configs:
            df_group = df.loc[df["config_num"] == i]
            axis[fig_row][fig_col].scatter(df_group[p], df_group["score"])
            axis[fig_row][fig_col].set_title(f"Config {i}, r = {round(correlations[i][p], 2)}")
            axis[fig_row][fig_col].set_xlim(min_p, max_p)
            axis[fig_row][fig_col].set_ylim(min_score, max_score)
            fig_col += 1
            if fig_col % fig_row_cnt == 0:
                fig_row += 1
                fig_col = 0
        figure.tight_layout(rect=[0, 0.03, 1, 0.95])
        figure.suptitle(f"{exp_name} scatter plots")
        figure.supylabel("Score")
        figure.supxlabel(p)
        plt.savefig(f"{get_plots_path()}{exp_name}/score_{p}.png")
        plt.close()


"""
Main functions
"""
def read_data(exp_name):
    file_path = get_processed_data_path()
    df = pd.read_pickle(f"{file_path}{exp_name}.pkl")
    param_names = list(set(df.columns) - set(get_non_property_column_names()))
    df = df.reset_index()
    df["adaptive"] = np.where(df["score"] > 2, True, False)

    config_num = df["config_num"].unique()[0]
    config = json.load(open(f"{get_configs_path()}{exp_name}/{config_num}.json"))
    constraints = [abbreviate_property_name(p) for p in config["eval_funcs"].keys() if p != "weak_components"]
    for constraint in constraints:
        df[constraint] = df[constraint].round(1)

    return df, param_names, constraints


def main(exp_name, config_level_analysis=False):
    df, param_names, constraints = read_data(exp_name)

    path = f"{get_plots_path()}{exp_name}"
    if not os.path.exists(path):
        os.makedirs(path)

    score_correlation(df, param_names, exp_name, "config_num")
    plot_score_correlated_properties(df, param_names, exp_name)
    score_histograms(df, exp_name, constraints)
    score_heatmaps(df, exp_name, constraints)

    if exp_name == "uniform":
        param_correlation_heatmap(df, param_names, exp_name)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        exp_name = sys.argv[1]
        main(exp_name)
    else:
        print("Please provide an experiment name.")