import random
import numpy as np

#This function takes a set of edges then return all the nodes
def get_node(edges):
    nodes = set()
    #Get the nodes from the edges then put them in a set to remove duplicate
    for edge in edges:
        nodes.add(edge[0])
        nodes.add(edge[1])
    return nodes

def random_walk(edges,iters, tele_prob):
    nodes = get_node(edges)
    histogram = {}
    for node in nodes:
        histogram[node] = 0
    currentNode = 0 #Set current node to 0 (first node)
    for i in range(iters):
        histogram[currentNode] += 1.0 #add 1.0 to current node's score
        prob = random.uniform(0, 1)
        if prob < tele_prob: # Perform teleport
            currentNode = random.sample(nodes, 1)[0]
        else:
            links = [] # All the out-links a node contains
            for edge in edges:
                if edge[0] == currentNode:
                    links.append(edge)
            if not links: #If a node has no out-links then perform teleport
                currentNode = random.sample(nodes,1)[0] # teleport when stuck
            else:
                # Jump to a one of the node that current node links to
                currentNode = random.choice(links)[1]

    #Compute a histogram with nodes's score
    for node, freq in histogram.iteritems():
        histogram[node] = round(freq / iters, 2)
    return histogram

#This function takes a set of edges then return a transition matrix
def transition_matrix(edges):

    nodes = get_node(edges) # Get a set of nodes
    matrix = np.zeros((len(nodes), len(nodes))) #Initialise a zeros matrix

    for node in nodes:
        links = [] #out-links of a node
        for edge in edges:
            if node == edge[0]:
                links.append(edge[1])

        for i in nodes:
            matrix[node][i] = round(1.0/len(links),2) if i in links else 0

    return matrix, nodes


def pagerank(edges, iters, tele_prob):
    #Transition matrix
    matrixP, nodes = transition_matrix(edges)
    Q = np.ones_like(matrixP) / len(nodes) #Matrix with values 1/n
    matrixPnew = (1.0-tele_prob)*matrixP + tele_prob*Q # New P matrix with teleport probability
    vector = np.array([1.0/len(nodes)]*len(nodes)) # an arbitrary probability vector (1/Ns where N is the number of all states)
    for i in range(iters):
        vector = vector.dot(matrixPnew) #Mulitply matrix and vector
    return vector


if __name__ == "__main__":
    edges = {(0, 2 ), (1,1),  (1, 2), (2, 0), (2, 2), (2, 3), (3, 3), (3,4)}

    iter = 50000
    print(random_walk(edges, iter, 0.1))
    print(random_walk(edges, iter, 0.1) == random_walk(edges, iter + 5000, 0.1))

    p1 = pagerank(edges, 4000, 0.1)
    p2 = pagerank(edges, 5000, 0.1)
    print(p1)
    print(p2)
    print(p1==p2)

    #In crease outlinks from node 1.
    edges_increase_out = {(0, 2 ), (1,1),  (1, 2), (1,3), (1,4), (2, 0), (2, 2), (2, 3), (3, 3), (3,4)}

    print("Increase outlinks from node 1: %s" %random_walk(edges_increase_out, 80000, 0.1))


    #Question 3: As we can see above, Pagerank requires significantly less iterration than randomwalk
    # in order to reach steady state ( 50000 for randomwalk compares to 4000 for page rank)

    #Question 4: No you cant influence score of your own page by chaning the number of out-links it contains.
    # The score for node 1 stays the same when we put more out-links into it. (0.07)