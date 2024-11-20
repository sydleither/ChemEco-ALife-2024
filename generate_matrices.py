from random import random


def stochastic_block_model(num_nodes, communities, edge_probabilities):
    adj = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
    for edge1 in range(num_nodes):
        for edge2 in range(num_nodes):
            community1 = communities[edge1]
            community2 = communities[edge2]
            edge_prob = edge_probabilities[community1][community2]
            if random() < edge_prob:
                adj[edge1][edge2] = 1
    return adj



adj = stochastic_block_model(9, {0:0, 1:0, 2:0, 3:1, 4:1, 5:1, 6:2, 7:2, 8:2}, [[0.9, 0.1, 0.1], [0.1, 0.9, 0.1], [0.1, 0.1, 0.9]])
for row in adj:
    print(row)