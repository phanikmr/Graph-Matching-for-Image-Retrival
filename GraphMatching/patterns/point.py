import math
import copy
import numpy

class Point(object):
    
    X = int
    Y = int

    def __init__(self, x,y):
        self.X = x
        self.Y = y

    def distanceFromThisPoint(self,point):
        return distanceBetweenTwoPoints(self,point)
     
    def angleWithThisPoint(self,point):
        return angleBetweenTwoPoints(self,point)

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        return str((self.X,self.Y))

    def __eq__(self,point):
        return self.X == point.X and self.Y == point.Y
    
    def __ne__(self,point):
        return self.X != point.X and self.Y != point.Y

    def __add__(self,point):
        return Point(self.X+point.X,self.Y+point.Y)

    def __sub__(self,point):
        return Point(self.X-point.X,self.Y-point.Y)

    def __mul__(self,scale):
        return Point(float(self.X*scale), float(self.Y*scale))

    def __div__(self,scale):
        return Point(float(self.X/scale), float(self.Y/scale))

    def __getitem__(self,key):
        if key == 0:
            return self.X
        else:
            return self.Y
    
    def getAsList(self):
        return [self.X,self.Y]

    def getPointAsYXList(self):
        return [self.Y, self.X]


    # test addition

    

def distanceBetweenTwoPoints(point1,point2):
    return math.sqrt(math.pow(point1.X - point2.X,2) + math.pow(point1.Y - point2.Y,2))

def angleBetweenTwoPoints(point1,point2):
    return numpy.arctan2(point2.Y-point1.Y,point2.X-point1.X)

def printListOfPoints(points,listName=""):
    print listName
    print "#################################"
    for point in points:
        print point
    print "#################################"

if __name__ == "__main__":
    #print distanceBetweenTwoPoints(Point(1,1),Point(2,2))
    print angleBetweenTwoPoints(Point(0,0),Point(1,0))
    point = Point(10,5)
    print point[0],point[1]

