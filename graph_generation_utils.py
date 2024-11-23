from random import random

import networkx as nx
import numpy as np


def symmetric_edges(num_vals, internal, external):
    edge_probs = []
    for i in range(num_vals):
        edge_probs.append([])
        for j in range(num_vals):
            if i == j:
                edge_probs[i].append(internal)
            else:
                edge_probs[i].append(external)
    return edge_probs


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


def is_network_valid(matrix):
    nx_obj = nx.DiGraph(np.array(matrix))
    strong_components = len(list(nx.weakly_connected_components(nx_obj)))
    return strong_components == 1