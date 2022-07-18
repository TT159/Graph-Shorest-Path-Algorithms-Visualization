import dgl
import numpy as np
import networkx as nx
import scipy.sparse as sp
import matplotlib.pyplot as plt

# INF = int(float('inf'))
INF = 20220504  # graph_mat[i][j]=INF to represent i can't reach j

class FloydWarshall:
    def __init__(self, graph_mat) -> None:
        self.graph_mat = graph_mat  # adjacency matrix

    def shortest_path(self):
        m, n = len(self.graph_mat), len(self.graph_mat[0])
        # print("len m:", m, 'len n:', n)
        distance_mat = self.graph_mat.copy()
        # print("shortest path function matrix:")
        # print(distance_mat)
        path = [[None] * n for _ in range(m)]
        for k in range(m):
            # print('******** k=', k)
            for i in range(m):
                for j in range(n):
                    if distance_mat[i][k]+distance_mat[k][j] < distance_mat[i][j]:
                        distance_mat[i][j] = distance_mat[i][k]+distance_mat[k][j]
                        path[i][j] = k
                        # print("(",i,j,")",distance_mat[i][j])
                        # print('k:',path[i][j])
                    # else:
                    #     print("no",k,"(", i, j, ")", distance_mat[i][j])
        return distance_mat, path

# recursive to get the shortest path
def get_nodes_edges(paths, i, j):
        if i == j:
            return [i], []
        else:
            if paths[i][j] == None:
                return [j], [(i, j)]
            else:
                left_nodes, left_edges = get_nodes_edges(paths, i, paths[i][j])
                right_nodes, right_edges = get_nodes_edges(paths, paths[i][j], j)
        return left_nodes+right_nodes, left_edges+right_edges


def draw(sp_mat, color_nodes, color_edges):
    # to construct the network graph with dgl.from_scipy(); by default it's directed graph
    G = dgl.from_scipy(sp_mat, eweight_name='w')
    # print(type(G))
    # change into undirected graph
    nx_multi_G = dgl.to_networkx(G, edge_attrs='w').to_undirected()
    UG = nx.Graph(nx_multi_G)
    # print(UG.edges(data=True))
    edge_labels = nx.get_edge_attributes(UG, 'w')
    edge_labels = {(key[0], key[1]): edge_labels[key].item() for key in edge_labels}
    edges = list(UG.edges)
    num_nodes = UG.number_of_nodes()
    num_edges = UG.number_of_edges()
    node_color = ['pink'] * num_nodes
    edge_color = ['pink'] * num_edges

    # color the nodes & edges in the shortest path as green
    for i in color_nodes:
        node_color[i] = 'green'
    for i in range(num_edges):
        u, v = edges[i][0], edges[i][1]
        if (u, v) in set(color_edges) or (v, u) in set(color_edges):
            edge_color[i] = 'green'

    pos = nx.circular_layout(UG)
    plt.title('FloydWarshall: Shortest Path')
    nx.draw(UG, pos, with_labels=True, node_color=node_color, edge_color=edge_color)
    nx.draw_networkx_edge_labels(UG, pos, edge_labels=edge_labels)
    plt.savefig('FloydWarshall Result.png', format='PNG')
    plt.show()


# main():
# initialize the table
row = np.array([0, 0, 1, 1, 2, 2, 3, 3, 4])
col = np.array([1, 2, 2, 3, 4, 3, 4, 5, 5])
data = np.array([1, 12, 9, 3, 5, 4, 13, 15, 4])
start_node, end_node = 0, 5  # start point, end point
count_node = 6
# print(count_node)

# to construct the graph matrix; sp_mat : sparse matrix
sp_mat = sp.coo_matrix((data, (row, col)), shape=(count_node, count_node))
graph_mat = sp_mat.toarray()
# print("Following is the original table:")
# print(graph_mat)
# undirected graph
for i in range(len(graph_mat)):
    for j in range(i):
        if graph_mat[i][j] == 0 and graph_mat[j][i] == 0:
            graph_mat[i][j] = graph_mat[j][i] = INF
        else:
            graph_mat[i][j] += graph_mat[j][i]
            graph_mat[j][i] = graph_mat[i][j]
# print(graph_mat)

# Applying floyd-warshall algorithm to get the distance matrix
distance_mat, paths = FloydWarshall(graph_mat).shortest_path()
# print("Following is the distance matrix:")
# print(distance_mat)
# print(paths)

# print the paths
print('Following are the paths:')
for i in range(count_node):
    for j in range(i+1, count_node):
        print('{}->{}: {} | {}'.format(i, j, get_nodes_edges(paths, i, j), distance_mat[i][j]))
pass_nodes, pass_edges = get_nodes_edges(paths, start_node, end_node)

# plot the result network graph
plt.figure(1)
draw(sp_mat, pass_nodes, pass_edges)

