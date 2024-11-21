import json
import sys

import numpy as np

from graph_generation_utils import assign_weights, random_graph, stochastic_block_model
from common import get_data_path, write_matrix


def test():
    exp_dir = get_data_path("test")
    exp_matrices_dir = get_data_path("test", "matrices")
    replicates = 5
    num_nodes = 9
    communities = {0:0, 1:0, 2:0, 3:1, 4:1, 5:1, 6:2, 7:2, 8:2}
    edge_probabilities = [[0.9, 0.1, 0.1], [0.1, 0.9, 0.1], [0.1, 0.1, 0.9]]
    connectance = np.mean([x for y in edge_probabilities for x in y])
    edge_params = [[(1, 0.5), (0, 0.5), (0, 0.5)], [(0, 0.5), (1, 0.5), (0, 0.5)], [(0, 0.5), (0, 0.5), (1, 0.5)]]
    for i in range(replicates):
        edge_weights = assign_weights(num_nodes, communities, edge_params)
        sbm_topology = stochastic_block_model(num_nodes, communities, edge_probabilities)
        sbm_network = np.array(sbm_topology) * np.array(edge_weights)
        random_topology = random_graph(num_nodes, connectance)
        random_network = np.array(random_topology) * np.array(edge_weights)
        write_matrix(edge_weights, f"{exp_matrices_dir}/ew_{i}")
        write_matrix(sbm_network, f"{exp_matrices_dir}/sbm_{i}")
        write_matrix(random_network, f"{exp_matrices_dir}/random_{i}")
    #TODO future experiments will have multiple edge_probabilities, etc
    #so params should be written for each condition, not just once per experiment
    #could read in this dict and pass in directly to funcs rather than defining afterwards
    exp_params = {
        "replicates": replicates,
        "num_nodes": num_nodes,
        "communities": communities,
        "edge_probabilities": edge_probabilities,
        "connectance": connectance,
        "edge_params": edge_params
    }
    with open(f"{exp_dir}/params.json", "w") as f:
        json.dump(exp_params, f, indent=4)


def main(exp_name):
    if exp_name == "test":
        test()
    else:
        print("Invalid experiment name provided.")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Please provide an experiment name to generate files for.")