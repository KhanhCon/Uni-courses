# class Vertex:
#     def __init__(self, n):
#         self.name = n


class Graph:
    vertices = {}
    edges = []
    edge_indices = {}

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = vertex
            for row in self.edges:
                row.append(0)
            self.edges.append([0] * (len(self.edges) + 1))
            self.edge_indices[vertex] = len(self.edge_indices)
            return True
        else:
            return False

    def add_edge(self, u, v, weight):
        if u in self.vertices and v in self.vertices:
            self.edges[self.edge_indices[u]][self.edge_indices[v]] = weight
            self.edges[self.edge_indices[v]][self.edge_indices[u]] = weight
            return True
        else:
            return False

    def get_weight(self, u, v):
       return self.edges[self.edge_indices[u]][self.edge_indices[v]]

    def print_graph(self):
        for v, i in sorted(self.edge_indices.items()):
            print v + ' '
            for j in range(len(self.edges)):
                print self.edges[i][j],
                print ' '
