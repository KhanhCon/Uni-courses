import random
import numpy as np

def get_node(edges):
    nodes = set()
    for edge in edges:
        nodes.add(edge[0])
        nodes.add(edge[1])
    return nodes

def random_walk(edges, tele_prob, iters):
    # Max iteration 10000
    nodes = get_node(edges)
    histogram = {}
    for node in nodes:
        histogram[node] = 0
    currentNode = 0  # 5 nodes
    for i in range(iters):
        histogram[currentNode] += 1.0

        prob = random.uniform(0, 1)
        if prob < tele_prob:
            # print("tele")
            currentNode = random.sample(nodes, 1)[0]
        else:
            # print("walk")
            links = []
            for edge in edges:
                if edge[0] == currentNode:
                    links.append(edge)
            if not links:
                # continue
                currentNode = random.sample(nodes,1)[0] # teleport when stuck
            else:
                currentNode = random.choice(links)[1]
    for node, freq in histogram.iteritems():
        histogram[node] = round(freq / iters, 2)
    return histogram

def transition_matrix(edges):
    # Function return initial matrix
    nodes = get_node(edges)
    matrix = np.zeros((len(nodes), len(nodes)))
    # matrix = {}

    for node in nodes:
        # matrix[node] = [0.0]*len(nodes)
        links = []
        for edge in edges:
            if node == edge[0]:
                links.append(edge[1])#

        for i in nodes:
            matrix[node][i] = round(1.0/len(links),2) if i in links else 0

    return matrix, nodes

def pagerank(edges, iters, tele_prob = 0):
    matrixP, nodes = transition_matrix(edges)
    vector = np.array([1.0/len(nodes)]*len(nodes))
    for i in range(iters):
        vector = vector.dot(matrixP) #Mulitply matrix and vector
    return vector


if __name__ == "__main__":
    edges = {(0, 1), (1, 2), (2, 0), (2, 2), (2, 3), (3, 3), (3, 4)}
    HI = random_walk(edges, 0.1, 45000)
    print(HI)
    print(pagerank(edges, 5000))

#Question 3: pagerank requirese less
#Question 4: No you cant increase score by putting more links