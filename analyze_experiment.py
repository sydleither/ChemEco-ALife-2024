import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common import get_data_path

sns.set_palette(sns.color_palette(["#ef7c8e", "#4c956c", "#d68c45"]))


def graph_generation_pointplot(df, save_dir):
    fig, ax = plt.subplots()
    sns.pointplot(data=df, x="graph_type", y="score", hue="ew_rep", ax=ax)
    fig.patch.set_alpha(0.0)
    fig.tight_layout()
    fig.savefig(f"{save_dir}/pointplot_graph_generation_types.png", bbox_inches="tight")
    plt.close()


def graph_generation_bars(df, save_dir, y_axis="score"):
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="ew_rep", y=y_axis, hue="graph_type", ax=ax)
    fig.patch.set_alpha(0.0)
    fig.tight_layout()
    fig.savefig(f"{save_dir}/bars_graph_generation_{y_axis}.png", bbox_inches="tight")
    plt.close()


def graph_generation_paired(df, save_dir, gg_type1, gg_type2, values="score"):
    df = pd.pivot(df, index="replicate", columns="graph_type", values=values)    
    df = df.reset_index()
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x=gg_type1, y=gg_type2, ax=ax)
    fig.suptitle(values)
    fig.patch.set_alpha(0.0)
    fig.tight_layout()
    fig.savefig(f"{save_dir}/correlation_{gg_type1}_{gg_type2}_{values}.png", bbox_inches="tight")
    plt.close()


def main(exp_name):
    exp_dir = get_data_path(exp_name)
    save_dir = get_data_path(exp_name, "plots")
    df = pd.read_csv(f"{exp_dir}/results.csv")
    graph_generation_bars(df, save_dir, "score")
    graph_generation_bars(df, save_dir, "num_communities")
    graph_generation_pointplot(df, save_dir)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Please provide an experiment name.")