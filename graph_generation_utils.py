from random import random

import numpy as np


def random_graph(num_nodes, connectance):
    adj = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
    for edge1 in range(num_nodes):
        for edge2 in range(num_nodes):
            if edge1 == edge2:
                continue
            if random() < connectance:
                adj[edge1][edge2] = 1
    return adj


def stochastic_block_model(num_nodes, communities, edge_probabilities):
    adj = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
    for edge1 in range(num_nodes):
        for edge2 in range(num_nodes):
            if edge1 == edge2:
                continue
            community1 = communities[edge1]
            community2 = communities[edge2]
            edge_prob = edge_probabilities[community1][community2]
            if random() < edge_prob:
                adj[edge1][edge2] = 1
    return adj


def assign_weights(num_nodes, communities, edge_params):
    adj = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
    for edge1 in range(num_nodes):
        for edge2 in range(num_nodes):
            community1 = communities[edge1]
            community2 = communities[edge2]
            mean, var = edge_params[community1][community2]
            edge_weight = np.random.normal(mean, var)
            edge_weight = max(min(edge_weight, 1), -1)
            adj[edge1][edge2] = edge_weight
    return adj