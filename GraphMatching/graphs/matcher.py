from node import Node
from tree import Tree
from imgutils.imageview import *
from PIL import Image
import msvcrt 
import numpy
import cv2
import os
import operator

class Matcher(object):

    model_graph = None
    query_graph = None
    matched_nodes = None
    scores = None

    
    def __init__(self, Model_Graph, Query_Graph):
       
        self.model_graph = Model_Graph
        self.query_graph = Query_Graph
        self.scores = {}
        

    def matchNode(self,node1,node2):               
        
        a = node1.shape == node2.shape
        b = abs(node1.extent - node2.extent) < 0.1
        c = abs(node1.solidity - node2.solidity) < 0.1
        d = True
        #d = node1.pts_count == node2.pts_count
        #d = abs(node1.pc - node2.pc) < 1.0
        e = abs(node1.pr1 - node2.pr1) < 0.3
        f = abs(node1.pr2 - node2.pr2) < 0.3
        g = abs(node1.ps - node2.ps) < 1.0
        h = cv2.matchShapes(node1.location,node2.location,1,0)


        print node1.index,node2.index
        print node1.shape,node2.shape,a
        print abs(node1.extent - node2.extent),b
        print abs(node1.solidity - node2.solidity),c
        print node1.pts_count,node2.pts_count,d
        print abs(node1.pr1 -  node2.pr1),e
        print abs(node1.pr2 - node2.pr2),f
        print abs(node1.ps - node2.ps),g
        print h                
        print a,b,c,e,f,g,h<0.6
        print a and b and c and d and e and f and g and (h<0.6) 
        ##print matchContours(node1.location,node2.location, self.model_image_size, self.query_image_size) 
        #print "" 
        
        #im1 = numpy.zeros(self.model_image_size,'uint8')
        #im2 = numpy.zeros(self.query_image_size,'uint8') 
        #cv2.drawContours(im1,[node1.location],0,255,-1)
        #cv2.drawContours(im2,[node2.location],0,255,-1)
        #cv2.imwrite("temp1.png",im1)
        #cv2.imwrite("temp2.png",im2)
        #images = map(Image.open, ["temp1.png","temp2.png"])
        #widths, heights = zip(*(i.size for i in images))

        #total_width = sum(widths)
        #max_height = max(heights)

        #new_im = Image.new('RGB', (total_width, max_height))

        #x_offset = 0
        #for im in images:
        #  new_im.paste(im, (x_offset,0))
        #  x_offset += im.size[0]

        #new_im.save('test.png')
        #os.system("test.png")
        ans = a and b and c and d and e and f and g and (h<0.6)
        if ans:
            score = abs(node1.extent-node2.extent) + abs(node1.solidity-node2.solidity) + abs(node1.pr1-node2.pr1) + abs(node1.pr2-node2.pr2) + abs(node1.ps-node2.ps) + h
            self.scores[node1.index] = score
        return ans


    def matchOnlyNode(self,node1,node2):
        a = node1.shape == node2.shape
        b = abs(node1.extent - node2.extent) < 0.1
        c = abs(node1.solidity - node2.solidity) < 0.1
        d = True
        #d = node1.pts_count == node2.pts_count
        #d = abs(node1.pc - node2.pc) < 1.0
        e = abs(node1.pr1 - node2.pr1) < 0.3
        f = abs(node1.pr2 - node2.pr2) < 0.3
        g = abs(node1.ps - node2.ps) < 1.0
        h = cv2.matchShapes(node1.location,node2.location,1,0)

        ans = a and b and c and d and e and f and g and (h<0.6)
        if ans:
            score = abs(node1.extent-node2.extent) + abs(node1.solidity-node2.solidity) + abs(node1.pr1-node2.pr1) + abs(node1.pr2-node2.pr2) + abs(node1.ps-node2.ps) + h
            self.scores[node1.index] = score
        return ans

    def matchSibilings(self,sibilings1,sibilings2):
        if len(sibilings1) != len(sibilings2):
            return False
        ch1 = sibilings1[:]
        ch2 = sibilings2[:]
        while len(ch1) != 0:
            child1 = ch1[0]
            temp = False
            for child2 in ch2:
                if self.matchOnlyNode(self.model_graph.graph_nodes[child1],self.query_graph.graph_nodes[child2]):
                    temp = True
                    break
            if not temp:
                return False
            else:
                ch1.remove(child1)
                ch2.remove(child2)
        return True


    def matchSemiIsoMorphism(self, children1, children2):
        if len(children1) != len(children2):
            return False
        ch1 = children1[:]
        ch2 = children2[:]
        while len(ch1) != 0:
            child1 = ch1[0]
            temp = False
            for child2 in ch2:
                if self.matchNode(self.model_graph.graph_nodes[child1],self.query_graph.graph_nodes[child2]):
                    temp = True
                    break
            if not temp:
                return False
            else:
                ch1.remove(child1)
                ch2.remove(child2)
        return True

    def matchSemiHomoMorphismV1(self,QueryLevel,ModelLevel):
        if len(ModelLevel) < len(QueryLevel):
            return False
        query_level = QueryLevel[:]
        model_level = ModelLevel[:]
        while len(query_level) != 0:
            node1 = query_level[0]
            temp = False
            for node2 in model_level:
                if self.matchNode(self.model_graph.graph_nodes[node2],self.query_graph.graph_nodes[node1]):
                    temp = True
                    self.matched_nodes.append(node2)
                    break
            if not temp:
                return False
            else:
                query_level.remove(node1)
                model_level.remove(node2)
        return True   


    def matchSemiHomoMorphismV2(self,QueryLevel,ModelLevel):
        if len(ModelLevel) < len(QueryLevel):
            return False
        map = {}
        for query_node in QueryLevel:
            match_count = 0
            for model_node in ModelLevel:                
                if self.matchNode(self.model_graph.graph_nodes[model_node],self.query_graph.graph_nodes[query_node]):
                    map[model_node] = model_node
                    match_count = match_count + 1
            if match_count < 1:
                return False
        self.matched_nodes.append(map)
        return True
                               

    # Returns complete list of matched nodes
    def findStrictMatch(self):
        self.scores = {}
        matched_root = None
        for i in xrange(0,self.model_graph.level_count):
            current_level_nodes = self.model_graph.level_nodes[i]
            #Level Search to match root Nodes
            for node in current_level_nodes:
                if self.matchNode(self.model_graph.graph_nodes[node], self.query_graph.graph_nodes[0]):
                    matched_root = node
                    children1 = []
                    children2 = []
                    failed = False
                    #Match children here
                    for current_level in xrange(1,self.query_graph.level_count):
                        children2 = self.query_graph.level_nodes[current_level]
                        if current_level == 1:
                            children1 = self.model_graph.graph_nodes[node].children
                        else:    
                            temp = []
                            for child in children1:
                                temp.extend(self.model_graph.graph_nodes[child].children)
                                children1 = temp
                        if not self.matchSemiIsoMorphism(children1, children2):
                            failed = True
                            break
                    if not failed:
                        #result_graph = self.query_graph.copy()
                        #for i in xrange(0 , self.query_graph.node_count):
                        #    result_graph.graph_nodes[i].location = self.model_graph.graph_nodes[i+matched_root].location
                        result_nodes = []
                        for i in xrange(0,self.query_graph.node_count):
                           result_nodes.append(matched_root+i)
                        print "scores : " + str(self.scores)
                        return result_nodes         
        return None

    # Returns List of Matched Nodes in Model Graph
    def findPartialMatchV1(self):
        for i in range(self.model_graph.level_count-1,0,-1):
            matched_height = 0
            self.matched_nodes = []
            current_model_level  = self.model_graph.level_nodes[i]            
            matched_model_level = i-1            
            matched_query_level = self.query_graph.level_count-2
            current_query_level = self.query_graph.level_nodes[self.query_graph.level_count-1]
            
            while self.matchSemiHomoMorphismV1(current_query_level,current_model_level) and matched_model_level>=0 and matched_query_level>=0:                
                current_model_level = self.model_graph.level_nodes[matched_model_level]
                current_query_level = self.query_graph.level_nodes[matched_query_level]
                matched_height = matched_height+1 
                matched_model_level = matched_model_level-1
                matched_query_level = matched_query_level-1

            if matched_height >=  self.query_graph.level_count-1:               
                return self.matched_nodes
        return None



    # Returns List of Matched Nodes in Model Graph
    def findPartialMatchV2(self):
        for i in range(self.model_graph.level_count-1,0,-1):
            self.matched_nodes = []
            current_model_level  = self.model_graph.level_nodes[i]            
            matched_model_level = i-1            
            matched_query_level = self.query_graph.level_count-2
            current_query_level = self.query_graph.level_nodes[self.query_graph.level_count-1]
            
            while self.matchSemiHomoMorphismV2(current_query_level,current_model_level) and matched_model_level>=0 and matched_query_level>=0 and len(self.matched_nodes)<=self.query_graph.level_count-2 :              
                current_model_level = self.model_graph.level_nodes[matched_model_level]
                current_query_level = self.query_graph.level_nodes[matched_query_level]
                matched_model_level = matched_model_level-1
                matched_query_level = matched_query_level-1


            if len(self.matched_nodes) ==  self.query_graph.level_count-1 and len(self.matched_nodes) != 0:
                nodes = self.matched_nodes[len(self.matched_nodes)-1]
                nodes = nodes.keys()
                for node_id in nodes:
                    node = self.model_graph.graph_nodes[node_id]
                    child_nodes = node.children 
                    nodes.extend(child_nodes)  
                print "scores : " + str(self.scores)
                return nodes
        return None

    # Returns List of Matched Nodes in Model Graph
    def findMatch(self):
        matched_nodes = self.findStrictMatch()
        if matched_nodes is not None: 
            return matched_nodes 
        self.scores = {}
        matched_nodes = self.findPartialMatchV2()
        sorted_vals = sorted(self.scores.items(), key=operator.itemgetter(1), reverse = True)   
        print sorted_vals 
        nodes_count = self.query_graph.node_count
        temp = []     
        while nodes_count>1 and len(sorted_vals)>0:
            item = sorted_vals.pop()
            temp.append(item[0])
            nodes_count -= 1
        print "sorted nodes: "+str(temp)
        print "matched nodes: "+str(matched_nodes)
        return temp
        

def waitTORead(*args):
    for arg in args:
        print arg
    msvcrt.getch()