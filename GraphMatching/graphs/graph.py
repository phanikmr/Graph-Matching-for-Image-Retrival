import cv2
import numpy


class Graph(object):
    
    nodes = None
    adjacency_matrix = None
    nodes_count = 0

    def __init__(self,Nodes,AdjacencyMatrix):
        self.nodes = Nodes
        self.adjacency_matrix = AdjacencyMatrix
        self.nodes_count = len(Nodes)




