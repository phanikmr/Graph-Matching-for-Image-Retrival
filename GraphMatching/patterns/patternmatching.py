import cv2
import numpy
import math
from point import Point, distanceBetweenTwoPoints, printListOfPoints
from pattern import Pattern
from transformations import affineTransformPointsList,getAffineMatrixOfPointsList

class PatternMatching(object):

    pattern_points = None
    query_points = None
    modelPattern = None
    queryPattern = None

    def __init__(self, *args, **kwargs):
        self.pattern_points = args[0]
        self.query_points = args[1]
        if len(args) > 2:
            self.modelPattern = args[2]
            self.queryPattern = args[3]

    @classmethod
    def from_patterns(cls,modelPattern,queryPattern):
        return cls(modelPattern.points,queryPattern.points,modelPattern,queryPattern)

    @classmethod
    def from_patternpts(cls,modelPatternPoints,queryPatternPoints):
        return cls(modelPatternPoints,queryPatternPoints)


    def euclideanDistance(self,point1,point2):
        return math.sqrt(math.pow(point1[0] - point2[0],2) + math.pow(point1[1] - point2[1],2)) 

    def matchPatternV1(self):
        image = numpy.zeros(self.modelPattern.size,numpy.uint8)
        reference_point1 = self.query_points[0]
        for i in xrange(1,len(self.query_points)):
            reference_point2 = self.query_points[i]
            reference_angle = numpy.arctan2(reference_point2.Y - reference_point1.Y , reference_point2.X - reference_point1.X)
            reference_dist = distanceBetweenTwoPoints(reference_point1,reference_point2)
            # test with pattern
            for j in xrange(0,len(self.pattern_points)):
                target_point1 = self.pattern_points[j]
                target_found = False
                for k in xrange(0,len(self.pattern_points)):
                    target_point2 = self.pattern_points[k]
                    if j == k or target_point1 is None or target_point2 is None:
                        continue                    
                    target_dist = distanceBetweenTwoPoints(target_point1,target_point2)
                    target_angle = numpy.arctan2(target_point2.Y - target_point1.Y,target_point2.X - target_point1.X)
                    if abs(target_dist - reference_dist) == 0 and (target_angle - reference_angle) == 0:                
                        target_found = True
                        break
                if target_found:
                    self.pattern_points[j] = None
                    self.pattern_points[k] = None                   
                    print reference_point1,target_point1,reference_angle,target_angle
                    image[target_point1.X,target_point1.Y] = 255
                    image[target_point2.X,target_point2.Y] = 255
                    #cv2.circle(self.modelPattern.image,(target_point1.X,target_point1.Y),5,(255,0,0),2)
                    break
            reference_point1 = reference_point2
        image = cv2.dilate(image,None)
        self.modelPattern.image[image > 0] = [0,0,255]
        cv2.imwrite("reult.png",self.modelPattern.image)
        cv2.imshow("",self.modelPattern.image)
        cv2.waitKey()

    def matchPatternV2(self):
        pt_count = len(self.query_points)
        image = numpy.zeros(self.modelPattern.size,numpy.uint8)
        points_selected = []

        for j in xrange(0,len(self.pattern_points)):
            points_selected.append(False)

        #affine_matrix =
        #getAffineMatrixOfPointsList(self.query_points,self.pattern_points)
        #transformed_pts =
        #affineTransformPointsList(self.query_points,affine_matrix)
        #self.queryPattern =
        #Pattern.from_pattern(self.queryPattern,transformed_pts)
        #self.queryPattern.showPattern()


        for i in xrange(0,len(self.query_points)):
            count = 0
            querypt_distances = self.queryPattern.distance_matrix[i]
            for j in xrange(0,len(self.pattern_points)):
                if points_selected[j]:
                    continue
                point_found = False        
                for k in xrange(0,len(querypt_distances)):
                    modelpt_distances = numpy.absolute(numpy.array(self.modelPattern.distance_matrix[j],int) - querypt_distances[k])
                    modelpt_distances.sort()
                    current_dist = modelpt_distances[0]
                    if abs(current_dist) <= 0:
                        count+=1
                        modelpt_distances[0] = self.modelPattern.size[0] + self.modelPattern.size[1]
                        if count >= pt_count:
                            point = self.pattern_points[j]
                            points_selected[j] = True
                            print point
                            image[point.X][point.Y] = 255
                            point_found = True
                            break
                    else:
                        break
                if point_found:
                   break
        image = cv2.dilate(image,None)
        self.modelPattern.image[image > 0] = [0,0,255]
        cv2.imwrite("result.png",self.modelPattern.image)
        cv2.imshow("",self.modelPattern.image)
        cv2.waitKey()         
            

    def matchPatternV3(self):
        image = self.modelPattern.getPatternOnImage()
        print image.shape
        print self.modelPattern.size

        referencePoint1 = self.query_points[0]
        referencePoint2 = self.query_points[1]
        referencePoint3 = self.query_points[2]
        for i in xrange(0,len(self.pattern_points)):
            for j in xrange(0,len(self.pattern_points)):
                for k in xrange(0,len(self.pattern_points)):
                    targetPoint1 = self.pattern_points[i]
                    targetPoint2 = self.pattern_points[j]
                    targetPoint3 = self.pattern_points[k]
                    M = getAffineMatrixOfPointsList([targetPoint1,targetPoint2,targetPoint3],[referencePoint1,referencePoint2,referencePoint3])
                    trans_pattern_points = affineTransformPointsList(self.query_points,M)


                    printListOfPoints(trans_pattern_points,"transformed")
        printListOfPoints(self.pattern_points,"pattern_point")
                    #printListOfPoints(self.query_points,"Query Points")
                    
                    
                    #for point in trans_pattern_points:
                    #    print point
                    #    if point.X<self.modelPattern.size[0] and point.Y<self.modelPattern.size[1] and point.X>=0 and point.Y>=0:
                    #        print point, image[point.X][point.Y]
                    #    else:
                    #        break                                          