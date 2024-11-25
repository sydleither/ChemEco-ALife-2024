import json
import sys

import numpy as np

from graph_generation_utils import (assign_weights, is_network_valid, random_graph, 
                                    stochastic_block_model, symmetric_edges)
from common import get_data_path, write_matrix


def process_topology(exp_matrices_dir, matrix_name, topology_matrix, edge_weights, matrix_names):
    if not is_network_valid(topology_matrix):
        print(f"Too many connected components for matrix {matrix_name}")
        return
    weighted_graph = np.array(topology_matrix) * np.array(edge_weights)
    write_matrix(weighted_graph, f"{exp_matrices_dir}/{matrix_name}")
    matrix_names.append(matrix_name)


def create_run_script(data_dir, exp_name, matrix_names, local=False):
    if local:
        preamble = f"python3 run_experiment.py {exp_name} "
    else:
        preamble = f"sbatch run_experiment.sb {exp_name} "
    with open(f"{data_dir}/run.sh", "w") as f:
        for matrix_name in matrix_names:
            f.write(preamble+matrix_name+"\n")


def test():
    exp_dir = get_data_path("test")
    exp_matrices_dir = get_data_path("test", "matrices")
    ew_reps = 10
    top_reps = 10
    num_nodes = 9
    communities = {0:0, 1:0, 2:0, 3:1, 4:1, 5:1, 6:2, 7:2, 8:2}
    edge_probabilities = symmetric_edges(3, 0.9, 0.2)
    connectance = np.mean([x for y in edge_probabilities for x in y])
    edge_params = symmetric_edges(3, (0.5, 0.25), (-0.5, 0.25))

    matrix_names = []
    for i in range(ew_reps):
        edge_weights = assign_weights(num_nodes, communities, edge_params)
        write_matrix(edge_weights, f"{exp_matrices_dir}/ew_{i}")
        for j in range(top_reps):
            sbm_topology = stochastic_block_model(num_nodes, communities, edge_probabilities)
            process_topology(exp_matrices_dir, f"sbm_{i}_{j}", sbm_topology, edge_weights, matrix_names)
            random_topology = random_graph(num_nodes, connectance)
            process_topology(exp_matrices_dir, f"random_{i}_{j}", random_topology, edge_weights, matrix_names)

    #TODO future experiments will have multiple edge_probabilities, etc
    #so params should be written for each condition, not just once per experiment
    #could read in this dict and pass in directly to funcs rather than defining afterwards
    exp_params = {
        "ew_reps": ew_reps,
        "top_reps": top_reps,
        "num_nodes": num_nodes,
        "communities": communities,
        "edge_probabilities": edge_probabilities,
        "connectance": connectance,
        "edge_params": edge_params
    }
    with open(f"{exp_dir}/params.json", "w") as f:
        json.dump(exp_params, f, indent=4)
    create_run_script(exp_dir, "test", matrix_names, local=True)


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