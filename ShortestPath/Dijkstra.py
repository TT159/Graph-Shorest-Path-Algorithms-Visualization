import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

class Dijkstra:
    def __init__(self, nodes, edges) -> None:
        self.nodes = nodes
        self.edges = edges

    def shortest_path(self, start_node):
        num_node = len(self.nodes)
        path = [None] * num_node
        distance = [None] * num_node  # initialize the min distance as None
        edge_weight = defaultdict(lambda: None)
        node_neighbors = defaultdict(set)
        # initialize, u is from point, v is to point, w is weight
        for (u, v, w) in self.edges:
            edge_weight[(u, v)] = w
            node_neighbors[u].add(v)
        distance[start_node] = 0

        for neighbor in node_neighbors[start_node]:
            path[neighbor] = start_node
            distance[neighbor] = edge_weight[(start_node, neighbor)]
        not_visit = [_ for _ in range(num_node) if _ != start_node] # the unvisited nodes

        while len(not_visit):
            min_w_node = not_visit[0]  # min_w_node, the node with the min distance to start point
            for i in not_visit:
                if distance[i] == None:
                    continue
                elif distance[i] < distance[min_w_node]:
                    min_w_node = i
            not_visit.remove(min_w_node)

            # update minimum distance and path
            for i in not_visit:
                if edge_weight[(min_w_node, i)] == None:
                    continue
                elif distance[i] == None or distance[min_w_node]+edge_weight[(min_w_node, i)] < distance[i]:
                    distance[i] = distance[min_w_node]+edge_weight[(min_w_node, i)]
                    path[i] = min_w_node
        return path, distance

def get_nodes_edges(path, end_node):
    # Get all nodes and all edges of the shortest path from path
    nodes, edges = [], []
    v = end_node
    nodes.append(v)
    while path[end_node] != None:
        u = path[end_node]
        nodes.append(u)
        edges.append((u, v))
        end_node = u
        v = u
    return nodes[::-1], edges[::-1]

def draw(DG, color_nodes, color_edges):
    # Draw a graph and color the nodes and edges on the shortest path as red
    edges = list(DG.edges)
    # number_of_nodes(): built-in function
    num_nodes = DG.number_of_nodes()  # # of nodes
    num_edges = DG.number_of_edges()  # # of edges
    node_color = ['pink'] * num_nodes   # initialize node color
    edge_color = ['pink'] * num_edges  # initialize edge color

    # color nodes
    for i in color_nodes:
        node_color[i] = 'green'
    # color edges
    for i in range(num_edges):
        u, v = edges[i][0], edges[i][1]
        if (u, v) in set(color_edges):
            edge_color[i] = 'green'
            
    pos = nx.circular_layout(DG)
    plt.title('Dijkstra: Shortest Path')
    nx.draw(DG, pos, with_labels=True, node_color=node_color, edge_color=edge_color)
    edge_labels = nx.get_edge_attributes(DG, 'weight')
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=edge_labels)
    plt.savefig('Dijkstra Result.png', format='PNG')
    plt.show()


# main():
# initialize the nodes and edges
# nodes = [0, 1, 2, 3, 4, 5, 6]  # node 6 is an isolated node
nodes = [0, 1, 2, 3, 4, 5]
edges = [(0, 1, 1), (0, 2, 12), (1, 2, 9), (1, 3, 3), (2, 4, 5), (2, 3, 4), (3, 4, 13), (3, 5, 15), (4, 5, 4)]
start_node, end_node = 0, 5  # select two specific vertices

# construct the network graph
DG = nx.DiGraph()
DG.add_nodes_from(nodes)
DG.add_weighted_edges_from(edges)

# plot the original network graph
plt.figure(1)
# plt.subplot(1, 2, 1)
pos = nx.circular_layout(DG)
plt.title('Original Network Graph')
nx.draw(DG, pos, with_labels=True, node_color='pink', edge_color='pink')
# store the weights
edge_labels = nx.get_edge_attributes(DG, 'weight')
nx.draw_networkx_edge_labels(DG, pos, edge_labels=edge_labels)
plt.savefig('Origin Network.png', format='PNG')
plt.show()

# applying dijkstra
print('Following are the paths:')
path, distance = Dijkstra(nodes, edges).shortest_path(start_node)
for i in range(len(nodes)):
    if start_node != nodes[i]:
        print('{}->{}: {} | {}'.format(start_node, nodes[i], get_nodes_edges(path, nodes[i]), distance[nodes[i]]))
pass_nodes, pass_edges = get_nodes_edges(path, end_node)

# plot the result network graph
plt.figure(2)
draw(DG, pass_nodes, pass_edges)

