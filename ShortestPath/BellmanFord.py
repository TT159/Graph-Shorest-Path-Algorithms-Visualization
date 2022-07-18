import networkx as nx
import matplotlib.pyplot as plt

class Bellman_ford:
    def __init__(self, nodes, edges, start_node) -> None:
        self.nodes = nodes
        self.edges = edges
        self.start_node = start_node

    def shortest_path(self):
        num_node = len(self.nodes)
        num_edge = len(self.edges)
        distance, path = [None] * num_node, [None] * num_node
        distance[self.start_node] = 0
        times, flag = 0, True

        # to create slack function
        def slack(edge, distance, path):
            u, v, w = edge[0], edge[1], edge[2]
            if distance[u] == None:
                return False
            elif distance[v] == None or distance[u]+w < distance[v]:
                distance[v] = distance[u]+w
                path[v] = u
                return True
            return False

        while flag and times < num_node-1:
            flag = False
            for i in range(num_edge):
                if slack(self.edges[i], distance, path) and not flag:
                    flag = True
            times += 1

        # to check whether there is a negative circle
        for i in range(num_edge):
            u, v, w = self.edges[i][0], self.edges[i][1], self.edges[i][2]
            if distance[u]+w < distance[v]:
                return False, distance, path
        return True, distance, path

def get_nodes_edges(path, end_node):
    # get nodes and edges from  path
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
    edges = list(DG.edges) # all edges
    num_nodes = DG.number_of_nodes()    # # of nodes
    num_edges = DG.number_of_edges()    # # of edges
    node_color = ['pink'] * num_nodes  # initialize color for nodes
    edge_color = ['pink'] * num_edges  # initialize color for edges

    # nodes and edges in the shortest path colored as green
    for i in color_nodes:
        node_color[i] = 'green'
    for i in range(num_edges):
        u, v = edges[i][0], edges[i][1]
        if (u, v) in set(color_edges):
            edge_color[i] = 'green'
            
    pos = nx.circular_layout(DG)
    plt.title('BellmanFord: Shortest Path')
    nx.draw(DG, pos, with_labels=True, node_color=node_color, edge_color=edge_color)  # draw the graph
    edge_labels = nx.get_edge_attributes(DG, 'weight')
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=edge_labels)  # draw the weights
    plt.savefig('BellmanFord Result.png', format='PNG')
    plt.show()


# An example not contains a negative weighted loop
nodes = [0, 1, 2, 3, 4, 5]
edges = [(0, 1, 1), (0, 2, 12), (1, 2, 9), (1, 3, 3), (2, 4, 5), (2, 3, 4), (3, 4, 13), (3, 5, 15), (4, 5, 4)]
start_node, end_node = 0, 5
# The example contains a negative weighted loop
# nodes = [0, 1, 2]
# edges = [(0, 1, 1), (1, 2, 2), (2, 0, -4)]

flag, distance, path = Bellman_ford(nodes, edges, start_node).shortest_path()
if flag:
    print("Following are the paths:")
    for i in range(len(nodes)):
        if start_node != nodes[i]:
            print('{}->{} {} | {}'.format(start_node, nodes[i], get_nodes_edges(path, nodes[i]), distance[i]))
else:
    print('The graph contains a negative weighted loop')

pass_nodes, pass_edges = get_nodes_edges(path, end_node)
DG = nx.DiGraph()
DG.add_nodes_from(nodes)
DG.add_weighted_edges_from(edges)

# plot the result graph
draw(DG, pass_nodes, pass_edges)
