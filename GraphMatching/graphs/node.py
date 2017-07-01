import copy

class Node(object):

    index = int
    shape = str
    extent = float
    solidity = float
    pr1 = float
    pr2 = float
    ps = float
    parent = None
    children = None
    close_sibilings = None
    location = None    
    
    def __init__(self,Index, Shape, PointsCount, Extent, Solidity, Pr1, Pr2, Ps, Location, Parent=None, Children=[], Close_Sibilings=[]):
        self.index = Index        
        self.shape = Shape
        self.pts_count = PointsCount
        self.extent = Extent
        self.solidity = Solidity
        self.children = Children
        self.close_sibilings = Close_Sibilings
        self.parent = Parent
        self.location = Location
        self.pr1 = Pr1
        self.pr2 = Pr2
        self.ps = Ps

    def updateParent(self,Parent):
        self.parent = Parent
    
    def updateChildren(self,Children):
        self.children = Children

    def updateClose_Sibilings(self,Close_Sibilings):
        self.close_sibilings = Close_Sibilings
    
    def updateLocation(self,Location):
        self.location = Location
    
    def addChild(self,Child):
        self.children.append(Child)

    def addClose_Sibiling(self,Close_Sibiling):
        self.close_sibilings.append(Close_Sibiling)

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        ind = "index : " + str(self.index) + "\n"
        shp = "shape : " + self.shape + "\n"
        pts = "Points Count : " + str(self.pts_count) + "\n"
        prt = "parent : " + str(self.parent) + "\n"
        chd = "children : " + str(self.children) + "\n"
        ccs = "close sibilings : " + str(self.close_sibilings) + "\n"
        ext = "extent : " + str(self.extent) + "\n"
        sol = "solidity : " + str(self.solidity) + "\n"        
        PR1 = "PR1 : " + str(self.pr1) + "\n"
        PR2 = "PR2 : " + str(self.pr2) + "\n"
        PS = "PS : " + str(self.ps) + "\n"
        #loc = "location  : " + str(self.location) + "\n"
        return ind+shp+pts+prt+chd+ccs+ext+sol+PR1+PR2+PS
   
if __name__ == "__main__":
    pass