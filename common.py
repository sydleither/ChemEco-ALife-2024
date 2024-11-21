import csv
import os

from matplotlib.colors import BoundaryNorm
import matplotlib.pyplot as plt


def get_data_path(exp_name, sub_dir="."):
    data_path = f"output/{exp_name}/{sub_dir}"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return data_path


def get_edge_colorscheme():
    cmap = plt.get_cmap("PiYG")
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = cmap.from_list("Custom cmap", cmaplist, cmap.N)
    bounds = [-1, -0.75, -0.5, -0.25, -.0001, .0001, 0.25, 0.5, 0.75, 1]
    norm = BoundaryNorm(bounds, cmap.N)
    return cmap, norm


def write_matrix(interactions, output_name):
    with open(output_name, "w") as f:
        wr = csv.writer(f)
        wr.writerows(interactions)