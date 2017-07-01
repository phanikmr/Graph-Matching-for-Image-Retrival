import cv2
import numpy
import itertools
import os
from imgutils import imageview
from bresenham import bresenham

class GraphifyPattern(object):
    
    _pattern = None
    image = None
    bin_image = None
    nodes = None
    adjacency_matrix = None
    node_ids = None

    
    def __init__(self, pattern, *args, **kwargs):
        self._pattern = pattern        
        self.image = pattern.getPatternOnImage()
        self.bin_image = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        _,self.bin_image = cv2.threshold(self.bin_image,128,255,cv2.THRESH_BINARY_INV)
        self.node_ids = []
        self.nodes = self._pattern.points[:]
        points_size  = len(self._pattern.points)
        for i in xrange(0,points_size):
            self.node_ids.append(i)
        self.adjacency_matrix = numpy.zeros((points_size,points_size),bool)

        
    def printPointsDistances(self):
        combinations = list(itertools.combinations(self.node_ids,2))
        for item in combinations:
            #print item[0].distanceFromThisPoint(item[1])
            #self.connectedLinePresentArth(item[0],item[1])
            point1 = self.nodes[item[0]]
            point2 = self.nodes[item[1]]
            pts  = list(bresenham(point1.X,point1.Y,point2.X,point2.Y))
            if self.checkPixels(pts,int(0.1*(point1.distanceFromThisPoint(point2)))):
                self.drawPixels(pts)
                self.adjacency_matrix[item[0]][item[1]] = True
                self.adjacency_matrix[item[1]][item[0]] = True
        print self.adjacency_matrix
        os.system('temp.png')


    def getGraph(self):
        combinations = list(itertools.combinations(self.node_ids,2))
        for item in combinations:
            #print item[0].distanceFromThisPoint(item[1])
            #self.connectedLinePresentArth(item[0],item[1])
            point1 = self.nodes[item[0]]
            point2 = self.nodes[item[1]]
            pts  = list(bresenham(point1.X,point1.Y,point2.X,point2.Y))

            if self.checkPixels(pts,int(0.1*(point1.distanceFromThisPoint(point2)))):
                self.drawPixels(pts)
                self.adjacency_matrix[item[0]][item[1]] = True
                self.adjacency_matrix[item[1]][item[0]] = True
        return self.nodes,self.adjacency_matrix

    def getNodes(self):
        return self.nodes

    def getAdjacencyMatrix(self):
        return self.adjacency_matrix

    def connectedLinePresent(self,point1,point2):
        dx = float(point2.X - point1.X)
        dy = float(point2.Y - point1.Y)
        if dx == 0.0:
            derr = 0.0
        else:
            derr = abs(dy/dx)
        error = derr - 0.5
        Y = point1.Y
        for X in xrange(point1.X,point2.X):
            print str(self._pattern.image[X][Y]) + "pixel value"
            error += derr
            if error >= 0.5:
                Y += 1
                error = error - 1.0

    def connectedLinePresentArth(self,point1,point2):
        dx = float(point2.X - point1.X)
        dy = float(point2.Y - point1.Y)
        D = 2*dy - dx
        Y = point1.Y
        step = 1
        if dx == 0:
            if point1.Y > point2.Y:
                step = -1
            for Y in range(point1.Y,point2.Y,step):
                print str(self._pattern.image[point1.X][Y]) + "pixel value"
                self.image[point1.X][Y] = [0,255,255]
        else:
            if point1.X > point2.X:
                step = -1
            for X in range(point1.X , point2.X, step):
                try:
                    print str(self._pattern.image[X][Y]) + "pixel value"
                    self.image[point1.X][Y] = [0,255,255]
                except :

                    print X,Y
                    print self.image.shape
                if D>0:
                    Y = Y+1
                    D = D-dx
                D = D+dy

    def checkPixels(self,pixelsList,errorThres):
        missed_points = 0
        for pixel in pixelsList:
          if self.bin_image[pixel[0]][pixel[1]] != 255:           
              missed_points += 1
              if missed_points >errorThres:
                  #print "Missed Points : " + str(missed_points)
                  return False
        #print "Missed Points : " + str(missed_points)
        return True
          
    def drawPixels(self,PixelList):
        temp = self.image
        for pixel in PixelList:
            temp[pixel[0]][pixel[1]] = [155,0,125]
        #imageview.plotMatrix(temp)
        cv2.imwrite("temp.png",temp)
        #os.system("temp.png")