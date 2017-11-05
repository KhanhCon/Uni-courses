# class Vertex:
#     def __init__(self, n):
#         self.name = n
import collections


class Graph:
    # vertices = {}
    # edges = []
    # edge_indices = {}

    def __init__(self):
        self.vertices = {}
        self.edges = []
        self.edge_indices = {}

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


class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def addList(self, listOfKeys):
        for key in listOfKeys:
            if key not in self.map:
                end = self.end
                curr = end[1]
                curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key


    def peek(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)


if __name__ == '__main__':
    s = OrderedSet('abracadaba')
    t = OrderedSet('simsalabim')
    print(s | t)
    print(s & t)
    print(s - t)