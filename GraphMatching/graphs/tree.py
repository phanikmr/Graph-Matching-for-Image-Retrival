from node import Node
import copy
import cv2
import math
from imgutils.shapetest import shapeDetect
from imgutils.shapedetector import ShapeDetector
from contours import isContoursIntersect

class Tree(object):
      
    root_node = None
    node_count = None
    graph_nodes = None
    level_nodes = None
    level_count = None
    image_size = None

    CONTOUR_MODE = 0
    SUBGRAPH_MODE = 1


    def __init__(self, mode,*args):
        self.graph_nodes = []
        self.level_nodes = []
        if mode == Tree.CONTOUR_MODE:
            self.initiliseFromContours(args[0],args[1],args[2])
        elif mode == Tree.SUBGRAPH_MODE:
            self.initiliseFromGraph(args[0],args[1])



    @classmethod
    def from_graph(cls,graph,nodes):
        return cls(cls.SUBGRAPH_MODE,graph,nodes)



    @classmethod
    def from_contours(cls,contours,hierarchy,ImageSize):
        return cls(cls.CONTOUR_MODE,contours,hierarchy,ImageSize)



    def initiliseFromGraph(self,graph,nodes):
        self.node_count = len(nodes)
        nodes.sort()
        start_index = nodes[0]
        # Copying nodes 
        for nodex_index in nodes:
            temp_node = graph.graph_nodes[nodex_index].copy()
            temp_node.index = temp_node.index-start_index
            temp_node.parent = temp_node.parent - start_index
            children = temp_node.children
            for j in xrange(0,len(children)):
                children[j] = children[j] - start_index
            self.graph_nodes.append(temp_node)
        # Adding Levels
        self.level_nodes.append([0])
        current_level = 0
        while current_level<len(self.level_nodes):
            current_level_nodes = self.level_nodes[current_level]
            temp_nodes = []
            for current_node in current_level_nodes:
                temp_nodes.extend(self.graph_nodes[current_node].children)                               
            if len(temp_nodes) == 0:
                break    
            self.level_nodes.append(temp_nodes)
            current_level = current_level + 1
        self.level_count = len(self.level_nodes)
        # Updating Sibilings 


    
    def initiliseFromContours(self,contours,hierarchy,ImageSize):       
        self.node_count = len(contours)
        self.image_size = ImageSize
        if self.node_count == 0:
            raise("null contours passed")

        for i in xrange(0,self.node_count):
            area = cv2.contourArea(contours[i])
            x,y,w,h = cv2.boundingRect(contours[i])
            rect_area = w*h

            hull = cv2.convexHull(contours[i])
            hull_area = cv2.contourArea(hull)
            if hull_area==0:
                hull_area = 1
            peri = cv2.arcLength(contours[i],True)
            rect_peri = 2*(w+h)
            hull_peri = cv2.arcLength(hull,True)

            extent = float(area)/rect_area
            solidity = float(area)/hull_area
            pc = float(math.pow(hull_peri,2)) / hull_area
            pr1 = float(hull_area)/rect_area
            pr2 = float(hull_peri)/rect_peri
            ps = float(peri)/hull_peri


            # ShapeDetection Changed


            sd = shapeDetect(contours[i])
            shape_obj = ShapeDetector()
            temp_node = Node(i,shape_obj.detect(contours[i]),sd[1],extent,solidity,pr1,pr2,ps,contours[i])
            self.graph_nodes.append(temp_node) 
        self.graphify(contours,hierarchy)
        self.root_node = self.graph_nodes[0]
        self.level_count = len(self.level_nodes)
    

    def graphify(self,contours,hierarchy):    
        for i in xrange(0,self.node_count):
        # Adding Parent
            self.graph_nodes[i].updateParent(hierarchy[0][i][3])
        # Adding Children
            curr_child = hierarchy[0][i][2]
            chd_list = []
            while curr_child != -1:
                chd_list.append(curr_child)                
                curr_child = hierarchy[0][curr_child][0]
            self.graph_nodes[i].updateChildren(chd_list)
        # Adding Levels
        self.level_nodes.append([0])
        current_level = 0
        while current_level<len(self.level_nodes):
            current_level_nodes = self.level_nodes[current_level]
            temp_nodes = []
            for current_node in current_level_nodes:
                temp_nodes.extend(self.graph_nodes[current_node].children)                               
            if len(temp_nodes) == 0:
                break   
            self.level_nodes.append(temp_nodes)
            current_level = current_level + 1

        # Adding Sibilings
        for level in self.level_nodes:
            checkListNodes = copy.deepcopy(level)
            for check_node in level:
                checkListNodes.remove(check_node)
                check_node_loc = self.graph_nodes[check_node].location
                temp = []
                for node in checkListNodes:
                    if isContoursIntersect(check_node_loc,self.graph_nodes[node].location,self.image_size, 20.0):
                        temp.append(node)
                self.graph_nodes[check_node].close_sibilings = temp
                checkListNodes.append(check_node)

                
    def __str__(self):
        string = ""
        for i in xrange(0,self.node_count):
            string += self.graph_nodes[i].__str__() + "\n\n"
        return string + "\n Levels: " + str(self.level_nodes) + "\n\n"

    def copy(self):
        return copy.deepcopy(self)        