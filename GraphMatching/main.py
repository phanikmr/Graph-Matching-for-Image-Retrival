import cv2
import numpy
import os
import tkFileDialog
import Tkinter
import Tkconstants
import time
import subprocess

from imgutils import imageview
from imgutils.imageselector import ImageSelector
from imgutils.shapetest import ShapeTest
from imgutils.stokewidth import StokeWidthTransform
from graphs.tree import Tree
from graphs.matcher import Matcher
from graphs.contours import filterContours
from graphs.contours import isContoursIntersect
from patterns.pattern import Pattern
from patterns.patternmatching import PatternMatching
from imgutils import shapetest
from imgutils.corner import cornersOfImage
from patterns.affinetest import mainAffine
from patterns.graphifypattern import GraphifyPattern
from graphs.graph import Graph
from graphs.graphmatch import GraphMatch

def matchTest():
     run_count = 0
     while True:          
            filename = getImageFile("Images//models","Select Model Image")
            #filename = "Images//models//model3.png"
            image1 = cv2.imread(filename,cv2.IMREAD_ANYCOLOR)
            if len(image1.shape) < 3:
                bin_img = image1.copy()
            else:
                bin_img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            _,bin_img = cv2.threshold(bin_img,100,255,cv2.THRESH_BINARY_INV)
            kernel = numpy.ones((3,3),numpy.uint8)
            bin_img = cv2.morphologyEx(bin_img,cv2.MORPH_CLOSE,kernel)  
            total_area = bin_img.shape[0] * bin_img.shape[1]
            filter_area = 0.0002 * total_area
            model_size = bin_img.shape 
            _, contours, hierarchy = cv2.findContours(bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours,hierarchy = filterContours(contours,hierarchy,filter_area)
            model_graph = Tree.from_contours(contours, hierarchy,image1.shape)


            filename = getImageFile("Images//queries","Select Query Image")            
            #filename = "Images//queries//4.png"
            image2 = cv2.imread(filename,cv2.IMREAD_ANYCOLOR)
            if len(image2.shape) < 3:
                bin_img = image2.copy()
            else:
                bin_img = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)      
            _,bin_img = cv2.threshold(bin_img,100,255,cv2.THRESH_BINARY_INV)   
            bin_img = cv2.morphologyEx(bin_img,cv2.MORPH_CLOSE,kernel) 
            query_size = bin_img.shape   
            _, contours, hierarchy = cv2.findContours(bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours,hierarchy = filterContours(contours,hierarchy,filter_area)
            
            
            query_graph = Tree.from_contours(contours, hierarchy,image2.shape)
            

            _ = subprocess.call("cls", shell=True)
            
            match = Matcher(model_graph,query_graph)

            curr_time = time.time()
            matched_nodes = match.findMatch()
            #matched_graph = match.findStrictMatch()
            curr_time = time.time() - curr_time
            

            ##print matched_graph
            #print query_graph
            #print model_graph
            print matched_nodes

            print curr_time
            if matched_nodes is not None:
                imageview.drawNodeContours(model_graph,matched_nodes,image1)
                #imageview.drawGraphContours(matched_graph,image1)
                cv2.imwrite("result.png",image1)
                os.system("result.png")
            run_count = run_count + 1
            print run_count
    

def contourTest():
    filename = getImageFile()
    image = cv2.imread(filename)
    gray_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    _,cnt_img = cv2.threshold(gray_img,128,255,cv2.THRESH_BINARY_INV)
    kernel = numpy.ones((3,3),numpy.uint8)
    cnt_img = cv2.morphologyEx(cnt_img,cv2.MORPH_CLOSE,kernel)
    _,contours,hierarchy = cv2.findContours(cnt_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    areas = []
    for contour in contours:
        areas.append( cv2.contourArea(contour))
    total_area = cnt_img.shape[0] * cnt_img.shape[1]
    selected_area = 0.0002 * total_area
    print total_area,selected_area
    contours,hierarchy = filterContours(contours,hierarchy,selected_area)
    print len(contours)
    imageview.drawContours(contours,image)
    cv2.imwrite("result.png",image)
    os.system("result.png")

    
        

def graphTest():
    filename = getImageFile()
    image = cv2.imread(filename)
    gray_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    _,cnt_img = cv2.threshold(gray_img,128,255,cv2.THRESH_BINARY_INV)
    kernel = numpy.ones((3,3),numpy.uint8)
    cnt_img = cv2.morphologyEx(cnt_img,cv2.MORPH_CLOSE,kernel)
    _,contours,hierarchy = cv2.findContours(cnt_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours,hierarchy = filterContours(contours, hierarchy, 2000)
    imageview.drawContours(contours,image)
    graph = Tree.from_contours(contours,hierarchy,image.shape)
    print graph
    selector = None

    def on_press_callback(event):
        (x,y) = (event.xdata,event.ydata)
        temp = image.copy()
        for node_index in graph.level_nodes[2]:
            node = graph.graph_nodes[node_index]
            flag = cv2.pointPolygonTest(node.location,(x,y),False)
            print flag
            if flag == 1:
                children = [node_index]
                for child in children:
                    children.extend(graph.graph_nodes[child].children)
                imageview.drawNodeContours(graph,children,temp)   
                selector.updateImage(temp)  
                print Tree.from_graph(graph,children)                                                    
                break           
    selector = ImageSelector(image,on_press_callback)
    selector.showImage()
    

    

def getImageFile(Initialdir="Images//", Title="Select image"):
    root = Tkinter.Tk()
    root.resizable(width=True, height=True)
    root.filename = tkFileDialog.askopenfilename(initialdir = Initialdir,title = Title,filetypes = (("png files","*.png"),("all files","*.*")))
    filename = root.filename
    root.destroy()
    return filename

def getFolder(Initialdir="Images//", Title="Select Image Folder"):
    root = Tkinter.Tk()
    root.resizable(width=True, height=True)
    root.filename = tkFileDialog.askdirectory(initialdir = Initialdir,title = Title)
    foldername = root.filename 
    root.destroy()
    return foldername

def getGraph(image,minarea):
    gray_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    _,cnt_img = cv2.threshold(gray_img,128,255,cv2.THRESH_BINARY_INV)
    kernel = numpy.ones((3,3),numpy.uint8)
    cnt_img = cv2.morphologyEx(cnt_img,cv2.MORPH_CLOSE,kernel)
    _,contours,hierarchy = cv2.findContours(cnt_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #contours,hierarchy = filterContours(contours, hierarchy, minarea)
    return Tree.from_contours(contours,hierarchy,image.shape)


class GroupMatching(object):

    graph_list = None
    image_list = None
    files_count = 0
    index = 0
    imageSelector = None
    selected_graph = None
    folder = ""

    def __init__(self,FolderPath):

        self.graph_list = []
        self.image_list = []
        self.folder = FolderPath
        for file in os.listdir(FolderPath):
            if file.endswith(".png"):
                self.files_count = self.files_count + 1
                self.image_list.append(file)

                image = cv2.imread(self.folder + os.sep + file)
                self.graph_list.append(getGraph(image,2000))
        image = cv2.imread(self.folder + os.sep + self.image_list[0])
        self.imageSelector = ImageSelector(image,self.onReleaseCallback,self.pressKeyCallback)
        self.imageSelector.showImage()


    def pressKeyCallback(self,event):
        if event.key == "right":
            if self.index < self.files_count - 1:
                self.index += 1
                image = cv2.imread(self.folder + os.sep + self.image_list[self.index])
                self.imageSelector.updateImage(image)
                self.selected_graph = None
        elif event.key == "left":
            if self.index > 0:
                self.index -= 1
                image = cv2.imread(self.folder + os.sep + self.image_list[self.index])
                self.imageSelector.updateImage(image)
                self.selected_graph = None
        elif event.key == "enter" and self.selected_graph is not None:
           for i in xrange(0,self.files_count):
               graph = self.graph_list[i]
               matcher = Matcher(graph,self.selected_graph)
               temp = matcher.findStrictMatch()
               if temp is not None:
                   image = cv2.imread(self.folder + os.sep + self.image_list[i])
                   imageview.drawNodeContours(graph,temp,image)
                   cv2.imwrite(str(i) + ".png",image)
                   os.system(str(i) + ".png")

    def onReleaseCallback(self,event):  
        (x,y) = (event.xdata,event.ydata)
        if x is not None:
            graph = self.graph_list[self.index]
            if len(graph.level_nodes) < 3:
                return
            for node_index in graph.level_nodes[2]:
                node = graph.graph_nodes[node_index]
                flag = cv2.pointPolygonTest(node.location,(x,y),False)
                if flag == 1:
                    children = [node_index]
                    for child in children:
                        children.extend(graph.graph_nodes[child].children)
                    temp = cv2.imread(self.folder + os.sep + self.image_list[self.index])
                    imageview.drawNodeContours(graph,children,temp)                       
                    self.imageSelector.updateImage(temp)  
                    self.selected_graph = Tree.from_graph(self.graph_list[self.index],children)     
                    break 




def shapeTest():
    image = cv2.imread("Images/test/rectangle.png")
    image_ = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    _,im1 = cv2.threshold(image_,128,255,cv2.THRESH_BINARY)

    _,contour1,_ = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    st = ShapeTest()
    print st.detect(contour1[0])
    


if __name__ == "__main__":
    #contourTest()
    matchTest()
    #contourTest()
    #graphTest()
    #GroupMatching(getFolder())
    #shapeTest()
    #file = getImageFile()
    #image = cv2.imread(file)
    #print getGraph(image,0)
    #pattern1 = Pattern.from_file("Images/test/alphabets.png")
    #pattern1.showPatternOnImage()
   # pattern1.showPatternOnImage()
   ## file = getImageFile()
    #pattern2 = Pattern.from_file("Images/test/A.png")
    #pattern2.showPatternOnImage()
    #w,h = pattern2.size

    #res =
    #cv2.matchTemplate(pattern1.points_image,pattern2.points_image,cv2.TM_CCOEFF)
    #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #top_left = max_loc
    #bottom_right = (top_left[0] + w, top_left[1] + h)

    #cv2.rectangle(pattern1.image,top_left, bottom_right, 0, 2)
    #cv2.imwrite("template.png",pattern1.image)
    #cv2.imshow("",pattern1.image)
    #cv2.waitKey()
   # pattern2.showPatternOnImage()
   # #temp_pat1 = [[0,0],[0,1],[1,0],[1,1]]
   # #temp_pat2 = [[2,2],[2,3],[3,2],[3,3]]
    #pm = PatternMatching.from_patterns(pattern1,pattern2)
    #pm.matchPatternV1()
    #mainAffine()

    ### Canny Test ###
    #file = getImageFile()

    ### Graph Matching Test ###

    #file = "Images/test/AL.png"
    #image = cv2.imread(file,cv2.IMREAD_ANYCOLOR)
    #file = "Images/test/A.png"
    #image2 = cv2.imread(file,cv2.IMREAD_ANYCOLOR)
    
    #query_pattern = Pattern.from_image(image2)
    #query_graph_pattern = GraphifyPattern(query_pattern)
    #node1,adj_mat1 = query_graph_pattern.getGraph()
    #query_graph = Graph(node1,adj_mat1)
    ##gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ##edge = cv2.Canny(gray,100,200)
    ##imageview.plotMatrix(edge)
    ##StokeWidthTransform(gray)
    #pattern = Pattern.from_image(image)
    #graphifyPattern = GraphifyPattern(pattern)
    ##graphifyPattern.printPointsDistances()
    #nodes,adj_mat = graphifyPattern.getGraph()
    #graph = Graph(nodes,adj_mat)
    #matcher = GraphMatch(graph,query_graph) 
    #t0 = time.time()
    #result_graph = matcher.findMatch()
    #print time.time() - t0
    #print result_graph.nodes,result_graph.adjacency_matrix
    #imageview.drawGraphOnImage(result_graph,image)
    #imageview.plotMatrix(image)



    #file = "Images/test/A.png"
    #image = cv2.imread(file,cv2.IMREAD_ANYCOLOR)
    #pattern = Pattern.from_image(image)
    #img = pattern.getPatternOnImage()
    #imageview.plotMatrix(img)



    ### Canny Contours Test ###
    #file =  "Images/test/letters_capital.png"
    #image = cv2.imread(file,cv2.IMREAD_ANYCOLOR)
    #gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #edge = cv2.Canny(gray,100,200);
    #_,contours, hierarchy = cv2.findContours(edge,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #approx_cnts = []
    #for contour  in contours:
    #    peri = cv2.arcLength(contour, True)
    #    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    #    approx_cnts.append(approx)
    #print approx_cnts
    #pattern = Pattern.from_contours(approx_cnts,image)
    #out_img = pattern.getPatternOnImage()
    #print len(pattern.points)
    #cv2.imwrite("res.png",out_img)
    #os.system("res.png")