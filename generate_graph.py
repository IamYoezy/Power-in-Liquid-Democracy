import networkx as nx
import numpy as np

#Generate four types of networks.
#Input parameters for underlying networks.
#Return the [0,1] matrix of the corresponding underlying network.

def draw_smallworld(n,k,p):#generate small world network
    G=nx.generators.random_graphs.watts_strogatz_graph(n,k,p)#Generate small world network, which contains n nodes, each node connects to k nearest nodes and connects to other nodes with probability p.
    A=np.zeros((n,n))
    for i in range(n):
        for j in range(i,n):
            if j in G[i]:
                A[i][j]=1
    return A,G #G is the dict network, A is the matrix network
        
def draw_regular(d,n): #generate regular network
    G=nx.generators.random_graphs.random_regular_graph(d,n)#Generate regular network, which contains n nodes and each each node has degree of d.
    A=np.zeros((n,n))
    for i in range(n):
        for j in range(i,n):
            if j in G[i]:
                A[i][j]=1
    return A,G

def draw_random(n,p):#generate random network
    G=nx.generators.random_graphs.gnp_random_graph(n,p)#Generate random network with n nodes and each node connect to other nodes with probability of p.
    A=np.zeros((n,n))
    for i in range(n):
        for j in range(i,n):
            if j in G[i]:
                A[i][j]=1
    return A,G

def draw_scale_free(n): 
    G=nx.scale_free_graph(n)#Generate scale free network with n nodes.
    A=np.zeros((n,n))
    for i in range(n):
        for j in range(i,n):
            if j in G[i]:
                A[i][j]=1
    return A,G

def draw_complete(n):
    G=nx.complete_graph(n)#Generate complete network with n nodes.
    A=np.ones((n,n))
    return A,G

def neighbor_of(G,D,i): #return the list of i's neioghbors in G, except for those delegating to i.
    neighbor=[]
    for j in G[i]:
        if j in D[i]:
            continue
        else:
            neighbor.append(j)
    neighbor.append(i)
    return neighbor
