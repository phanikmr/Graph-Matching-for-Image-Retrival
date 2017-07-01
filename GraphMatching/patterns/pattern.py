import cv2
import numpy
import copy
import itertools

from point import Point,distanceBetweenTwoPoints,angleBetweenTwoPoints
from imgutils.bwmorph_thin import bwmorph_thin
from imgutils.imageview import drawContours

class Pattern(object):
    points = None
    size = None
    image = None
    points_image = None
    distance_matrix = None
    orientation_matrix = None

    def __init__(self, *args, **kwargs):
        self.points = args[0]
        self.size = args[1]
        self.image = args[2]
        self.points_image = args[3]
        self.distance_matrix = []
        self.orientation_matrix = []
        self.initDistancesAndOrientations()
        
        
        
    @classmethod
    def from_file(cls,imageFile):
        image = cv2.imread(imageFile, cv2.IMREAD_ANYCOLOR)
        return cls.from_image(image)

    @classmethod
    def from_pattern(cls,OldPattern,TransformedPatternPts):
        OldPattern = OldPattern.copy()
        return cls(TransformedPatternPts,OldPattern.size,OldPattern.image,OldPattern.points_image)


    @classmethod
    def from_image(cls,image):
        if len(image.shape) > 2:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image.copy()
        gray_image = numpy.float32(gray_image)
        corners = cv2.cornerHarris(gray_image,2,3,0.04)
        thres = 0.05 * corners.max()
        shape = gray_image.shape
        pts = []
        #for i in xrange(0,shape[0]):
        #    for j in xrange(0,shape[1]):
        #        if corners[i,j] > thres:
        #            pts.append(Point(i,j))
        points_img = numpy.zeros(shape,numpy.uint8)
        points_img[corners > thres] = 255
        _, contours, hierarchy = cv2.findContours(points_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #a = len(contours)
        #a = numpy.count_nonzero(points_img)
        #temp = numpy.nonzero(points_img > 0)       
        ##points_img = cv2.dilate(points_img,None)
        #a = numpy.count_nonzero(points_img)
        #_, contours, hierarchy = cv2.findContours(points_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #a = len(contours)
       
        for i in xrange(0,len(contours)):
            M=cv2.moments(contours[i])
            point = []
            if M['m00'] == 0.0:
                pts.append(Point(contours[i][0][0][1],contours[i][0][0][0]))
                point.append(contours[i][0][0][1])
                point.append(contours[i][0][0][0])
            else:            
                pts.append(Point(int(M['m01']/M['m00']),int(M['m10']/M['m00'])))   
                point.append(int(M['m01']/M['m00']))
                point.append(int(M['m10']/M['m00']))
            #for pt in contours[i]:
            #    print pt[0], gray_image[pt[0][1]][pt[0][0]] ,point, gray_image[point[0]][point[1]]
            #print ""  
        return cls(pts,shape,image,points_img)

    @classmethod
    def from_contours(cls,contours,image):
        pts = []        
        shape = (image.shape[0],image.shape[1])
        points_img = numpy.zeros(shape,numpy.uint8)
        for contour in contours:          
            for point in contour:
                pts.append(Point(point[0][1],point[0][0]))
                
        indices = range(len(pts))
        point_combinations = list(itertools.combinations(indices,2))
        for point_combination in point_combinations:
            curr_ind_x = indices[point_combination[0]]
            curr_ind_y = indices[point_combination[1]]
            dist = pts[curr_ind_x].distanceFromThisPoint(pts[curr_ind_y])
            if dist <= 10:                
                indices[curr_ind_y] = curr_ind_x
        approx_pts = numpy.zeros(len(pts),object)           
        for ind in indices:
            approx_pts[ind] = pts[ind]
            point = pts[ind]
            points_img[point.X][point.Y] = 255
        approx_pts = filter(None,approx_pts)
        return cls(approx_pts,shape,image,points_img)
                

    def initDistancesAndOrientations(self):
        for point in self.points:
            current_distances = []
            current_orientations = []
            for pt in self.points:
                current_distances.append(int(distanceBetweenTwoPoints(point,pt)))
                current_orientations.append(angleBetweenTwoPoints(point,pt))
            self.distance_matrix.append(current_distances)
            self.orientation_matrix.append(current_orientations)


    def showPattern(self):
        temp_image = numpy.zeros(self.size, dtype=numpy.uint8)
        for point in self.points:
            temp_image[point.X,point.Y] = 255
        cv2.imshow("",temp_image)
        cv2.waitKey(0)

    def getPattern(self):
        temp_image = numpy.zeros(self.size, dtype=numpy.uint8)
        for point in self.points:
            temp_image[point.X,point.Y] = 255
        return temp_image

    def showPatternOnImage(self):
        temp_image = numpy.zeros(self.size, dtype=numpy.uint8)
        for point in self.points:
            temp_image[point.X,point.Y] = 255
            #print point
        temp_image = cv2.dilate(temp_image,None)
        Image = self.image.copy()
        Image[temp_image > 0] = [0,0,255]     
        cv2.imshow("",self.image)
        cv2.waitKey(0)

    def getPatternOnImage(self):
        temp_image = numpy.zeros(self.size, dtype=numpy.uint8)
        ind = 0
        for point in self.points:
            temp_image[point.X,point.Y] = 255
            
        temp_image = cv2.dilate(temp_image,None)
        Image = self.image.copy() 
        Image[temp_image>0] = [0,0,255]    

        for point in self.points:
            cv2.putText(Image,str(ind),(point.Y,point.X),cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,200,200), 1)
            ind += 1
        return Image    

    def copy(self):
        return copy.deepcopy(self)