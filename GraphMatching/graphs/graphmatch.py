import cv2
import numpy
import itertools
from Queue import *

from graph import Graph

class GraphMatch(object):
    
    model_graph = None
    query_graph = None
    model_visited = None
    query_visited = None

    def __init__(self, ModelGraph, QueryGraph):
        self.model_graph = ModelGraph
        self.query_graph = QueryGraph
        self.model_visited = numpy.zeros(ModelGraph.nodes_count,bool)
        #self.query_visited = numpy.zeros(QueryGraph.nodes_count,bool)

    
    def checkIsoMorphism(self,graph1,graph2):

        if graph1.nodes_count != graph2.nodes_count :
            return False
        adj1 = graph1.adjacency_matrix
        adj2 = graph2.adjacency_matrix
        P = numpy.eye(adj1.shape[0],dtype=bool)
        permutations = []
        for i in xrange(0,adj1.shape[0]):
            permutations.append(i)
        permutations = list(itertools.permutations(permutations,adj1.shape[0]))
        curr_perm = numpy.zeros(adj1.shape,bool)
        perm_count = 0
        for perm in permutations:
            perm_count += 1
            print perm_count
            for i in xrange(0,len(perm)):
                curr_perm[i] = P[perm[i]]
            curr_perm_inv = numpy.linalg.inv(curr_perm)
            curr_perm_inv = curr_perm_inv.astype(bool)
            temp = numpy.matmul(curr_perm , adj1)
            temp = numpy.matmul(temp , curr_perm_inv)
            if self.checkMatricesForEqulaity(temp,adj2):
                return True
        return False


    def checkMatricesForEqulaity(self,mat1,mat2):
        if mat1.shape != mat2.shape:
            return False
        a=numpy.equal(mat1,mat2)
        ans = numpy.count_nonzero(a)
        return ans >= ((mat1.shape[0] * mat1.shape[0])-mat1.shape[0])

    def getNextUnconnectedGraph(self,startNode):
        q = Queue()
        curr_graph_nodes = []
        curr_graph_nodes.append(startNode)
        q.put(startNode)    
        self.model_visited[startNode] = True 
        while not q.empty():
            curr_node_ind = q.get()
            
            for i in xrange(0,self.model_graph.nodes_count):
                if not self.model_visited[i]:
                    if self.model_graph.adjacency_matrix[curr_node_ind][i]:
                        self.model_visited[i] = True
                        q.put(i)
                        curr_graph_nodes.append(i)
        curr_graph_node_count = len(curr_graph_nodes)
        adj_mat = numpy.zeros((curr_graph_node_count,curr_graph_node_count),bool)
        nodes = []
        for i in xrange(0,curr_graph_node_count):
            for j in xrange(0,curr_graph_node_count):
                adj_mat[i][j] = self.model_graph.adjacency_matrix[curr_graph_nodes[i]][curr_graph_nodes[j]]
            nodes.append(self.model_graph.nodes[curr_graph_nodes[i]])

        return nodes,adj_mat
                


    def findMatch(self):
        
        for i in xrange(0,self.model_graph.nodes_count):
            if not self.model_visited[i]:
                curr_graph_indices,adj_mat = self.getNextUnconnectedGraph(i)
                curr_graph = Graph(curr_graph_indices,adj_mat)
                if self.checkIsoMorphism(curr_graph,self.query_graph):
                    return curr_graph
                



if __name__ == "__main__":
    #graph = Graph([0,1,2,3,4,5],[[False,True,True,False,False,False],[True,False,False,True,False,False],[True,False,False,True,False,False],[False,True,True,False,False,False],[False,False,False,False,False,True],[False,False,False,False,True,False]])
    graph2 = Graph([0,1,2],[[False,True,True],[True,False,True],[True,True,False]])
    match = GraphMatch(graph2,graph2)
    print match.findMatch()