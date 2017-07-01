import numpy
import cv2
import mahotas
import copy
from scipy.spatial import distance
from imgutils.imageview import *

def filterContours(Contours, Hierarchy, Area):
    contours = []
    hierarchy = None
    valid_contours = []
    
    for i in xrange(0,len(Contours)):
        if cv2.contourArea(Contours[i]) > Area:
            valid_contours.append(i)
    for valid_contour in valid_contours:
        first_child = Hierarchy[0][valid_contour][2]        
        if first_child not in valid_contours and first_child!= -1:
            first_child = Hierarchy[0][first_child][0]
            while first_child not in valid_contours:
                first_child = Hierarchy[0][first_child][0]
                if first_child == -1:
                    break
            Hierarchy[0][valid_contour][2] = first_child
        next_cnt = Hierarchy[0][valid_contour][0]
        if next_cnt not in valid_contours and next_cnt != -1:
            next_cnt = Hierarchy[0][next_cnt][0]
            while next_cnt not in valid_contours:
                next_cnt = Hierarchy[0][next_cnt][0]
                if next_cnt == -1:
                    break
            Hierarchy[0][valid_contour][0] = next_cnt            
    hierarchy = numpy.ones((1,len(valid_contours),4),int)
    for i in xrange(0,len(valid_contours)):
        hierarchy[0][i] = Hierarchy[0][valid_contours[i]]
        contours.append(Contours[valid_contours[i]])
    for i in xrange(0,len(valid_contours)):
        for j in xrange(0,4):
            if hierarchy[0][i][j] >= 0:
                try:
                    hierarchy[0][i][j] = valid_contours.index(hierarchy[0][i][j])
                except ValueError:
                    hierarchy[0][i][j] = -1    
    return contours,hierarchy

def centroid(Contour):
    M = cv2.moments(Contour)
    cen_x = int(M['m10']/M['m00'])
    cen_y = int(M['m01']/M['m00'])
    return (cen_x, cen_y)

def radius(Contour):
    area = cv2.contourArea(Contour)
    radius = numpy.sqrt(4*area/numpy.pi)/2
    return radius

def zernikeMoments(Image,Radius,Centroid):
    return mahotas.features.zernike_moments(Image,Radius,cm=Centroid)

def euclideanDistance(Vec1,Vec2):
    return cv2.norm(Vec1,Vec2,cv2.NORM_L2)

def extent(Contour):
    area = cv2.contourArea(Contour)
    x,y,w,h = cv2.boundingRect(contour)
    rect_area = w*h 
    extnt = float(area)/rect_area
    return extnt

def solidity(Contour):
    area = cv2.contourArea(Contour)
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    soldty = float(area) / hull_area
    return soldty

def matchContours(Contour1,Contour2,Size1,Size2):
    image1 = numpy.zeros(Size1,dtype=numpy.uint8)
    image2 = numpy.zeros(Size2,dtype=numpy.uint8)
    radius1 = radius(Contour1)
    radius2 = radius(Contour2)
    centroid1 = centroid(Contour1)   
    centroid2 = centroid(Contour2)
    print centroid1
    print Size1[0]/2, Size1[1]/2
    print centroid2
    print Size2[0]/2, Size2[1]/2 
    cnt1 = copy.deepcopy(Contour1)
    cnt2 = copy.deepcopy(Contour2)
    diff_x1 = Size1[0]/2 - centroid1[0]
    diff_y1 = Size1[1]/2 - centroid1[1]
    diff_x2 = Size2[0]/2 - centroid2[0]
    diff_y2 = Size2[1]/2 - centroid2[1]
    print len(cnt1)
    print len(cnt2)
    print diff_x1,diff_y1,diff_x2,diff_y2
    for x in xrange(0,len(cnt1)):
        print cnt1[x]
        cnt1[x][0][0] = cnt1[x][0][0] + diff_x1   
        cnt1[x][0][1] = cnt1[x][0][1] + diff_y1
        print cnt1[x],Contour1[x]
    for x in xrange(0,len(cnt2)):
        print cnt2[x]
        cnt2[x][0][0] = cnt2[x][0][0] + diff_x2
        cnt2[x][0][1] = cnt2[x][0][1] + diff_y2
        print cnt2[x],Contour2[x]
    cv2.drawContours(image1,[cnt1],0,255,-1)
    cv2.drawContours(image2,[cnt2],0,255,-1)
    cv2.drawContours(image1,[Contour1],0,255,-1)
    cv2.drawContours(image2,[Contour2],0,255,-1)
    imagesShow(image1,image2)
    ZM1 = zernikeMoments(image1,radius1,centroid1)
    ZM2 = zernikeMoments(image2,radius2,centroid2)
    return distance.euclidean(ZM1,ZM2)


def isContoursIntersect(Contour1,Contour2,image_size,threshold_dist):
    image = numpy.zeros(image_size,'uint8')
    
    rect1 = cv2.boundingRect(Contour1)
    rect2 = cv2.boundingRect(Contour2)
    Rect1 = []
    Rect2 = []
    Rect1.append( (rect1[0],rect1[1]))
    Rect1.append( (rect1[0],rect1[1]+rect1[3]))
    Rect1.append( (rect1[0]+rect1[2],rect1[1]+rect1[3]))
    Rect1.append( (rect1[0]+rect1[2],rect1[1]))
    Rect2.append( (rect2[0],rect2[1]))
    Rect2.append( (rect2[0],rect2[1]+rect2[3]))
    Rect2.append( (rect2[0]+rect2[2],rect2[1]+rect2[3]))
    Rect2.append( (rect2[0]+rect2[2],rect2[1]))
    r_ind1 = 0
    r_ind2 = 0
    dist = image_size[0]+image_size[1]
    for i in xrange(0,4):
        for j in xrange(0,4):
            curr_dist = cv2.norm(Rect1[i],Rect2[j])
            if dist>curr_dist:
                dist = curr_dist           
    return dist<=threshold_dist