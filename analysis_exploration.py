from common import get_plots_path, get_raw_data_path
from matplotlib.colors import BoundaryNorm
import matplotlib.pyplot as plt
from analysis import read_data
import networkx as nx
import seaborn as sns
import numpy as np
import csv
import sys


def visualize_graph(file_name):
    matrix = np.loadtxt(file_name, delimiter=",")
    G = nx.DiGraph(matrix)

    cmap = plt.get_cmap("PiYG")
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = cmap.from_list("Custom cmap", cmaplist, cmap.N)
    bounds = [-1, -0.75, -0.5, -0.25, -.0001, .0001, 0.25, 0.5, 0.75, 1]
    norm = BoundaryNorm(bounds, cmap.N)

    weights = nx.get_edge_attributes(G, "weight")
    color_map = [cmap(norm(weights[edge])) for edge in G.edges()]

    plt.figure(figsize=(8,8))
    pos = nx.circular_layout(G)
    nx.draw(G, pos=pos, with_labels=True, node_size=1000, edge_color=color_map, node_color="lightgrey")

    plt.savefig(f"{file_name[:-4]}_graph.png")
    plt.close()


def visualize_matrix(file_name):
    matrix = np.loadtxt(file_name, delimiter=",")

    cmap = plt.get_cmap("PiYG")
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = cmap.from_list("Custom cmap", cmaplist, cmap.N)
    bounds = [-1, -0.75, -0.5, -0.25, -.0001, .0001, 0.25, 0.5, 0.75, 1]
    norm = BoundaryNorm(bounds, cmap.N)

    plt.imshow(matrix, cmap=cmap, interpolation="none", norm=norm)
    plt.colorbar(ticks=[-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
    plt.xlabel("in")
    plt.ylabel("out")
    plt.title(file_name, fontsize=15)
    plt.savefig(f"{file_name[:-4]}.png")
    plt.close()


def sample_matrices(df, config_num, replicate):
    cmap = plt.get_cmap("PiYG")
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = cmap.from_list("Custom cmap", cmaplist, cmap.N)
    cm_bounds = [-1, -0.75, -0.5, -0.25, -.0001, .0001, 0.25, 0.5, 0.75, 1]
    norm = BoundaryNorm(cm_bounds, cmap.N)

    df_filter = df.loc[(df["config_num"] == config_num) & (df["replicate"] == replicate)]
    matrices = df_filter["matrix"].sample(n=20)

    figure, axis = plt.subplots(5, 4, figsize=(12,12))
    row = 0
    col = 0
    for matrix in matrices:
        axis[row][col].imshow(matrix, cmap=cmap, interpolation='none', norm=norm)
        row += 1
        if row % 5 == 0:
            col += 1
            row = 0
    figure.tight_layout()
    plt.savefig(f"{get_plots_path()}{exp_name}/sample_{config_num}_{replicate}.png")
    plt.close()


def write_matrix(interactions, output_name):
    with open(output_name, "w") as f:
        wr = csv.writer(f)
        wr.writerows(interactions)


def get_highest_scoring_matrices(df, n, param_names):
    df_best = df.nlargest(n, "score")
    for index, row in df_best.iterrows():
        write_matrix(row["matrix"], f"chemical-ecology/matrix_{index}.dat")
        print(f"Matrix {index}")
        print(f"\tscore {row['score']}")
        for param in param_names:
            try:
                print(f"\t{param} {row[param]}")
            except:
                continue
        print(f"./chemical-ecology " +
              f"-DIFFUSION {row['diffusion']} -SEEDING_PROB {row['seeding']} -PROB_CLEAR {row['clear']} " +
              f"-INTERACTION_SOURCE matrix_{index}.dat -SEED {row['replicate']} -N_TYPES {row['ntypes']} " +
              f"-WORLD_WIDTH 10 -WORLD_HEIGHT 10")
        print()


def individual_scatter(df, x, y, hue, exp_name):
    plt.figure()
    sns.scatterplot(x=x, y=y, data=df, hue=hue)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.savefig(f"{get_plots_path()}{exp_name}/zcatter_{x}_{y}_{hue}.png")
    plt.close()


def main(exp_name):
    df, param_names, constraints = read_data(exp_name)
    # sample_matrices(df, "1", "1")
    # get_highest_scoring_matrices(df, 1, param_names)
    # visualize_matrix("chemical-ecology/matrix_3372.dat")
    # visualize_graph("chemical-ecology/matrix_3372.dat")
    individual_scatter(df, "num_of_mod", "score", "pos_int_pro", exp_name)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        exp_name = sys.argv[1]
        main(exp_name)
    else:
        print("Please provide an experiment name.")