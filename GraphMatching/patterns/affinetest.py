from pattern import Pattern
import cv2
import numpy
from point import Point
from transformations import *

def mainAffine():
    #normal_pattern = Pattern.from_file("C://Users//palapathik//Source//Workspaces//Windows Services//Utility//R & D Team//Phani//Graph Matching//GraphMatching//Images//test//B.png")

    #transformed_pattern = Pattern.from_file("C://Users//palapathik//Source//Workspaces//Windows Services//Utility//R & D Team//Phani//Graph Matching//GraphMatching//Images//test//B_trans.png")

    #pts1 = []
    #for point in normal_pattern.points:
    #    pts1.append(point.getAsList())

    #pts2 = []
    #for point in transformed_pattern.points:
    #    pts2.append(point.getAsList())

    pts1 = numpy.float32([[49,0],[0,99],[99,99]])
    pts2 = numpy.float32([[0,0],[199,0],[99,199]])

    affine  = cv2.getAffineTransform(pts2,pts1)
    print affine

    a = Point(49,0)
    b = Point(0,99)
    p = Point(0,0)
    q = Point(199,0)

    [s,t,tx,ty] = getScaleRotationTranslation(p,q,a,b)
    print [s,t,tx,ty]
    affine = getAffineMatrix(s,t,tx,ty)
    print affine

    img1 = numpy.zeros((100,100),numpy.uint8)
    img2 = numpy.zeros((100,100),numpy.uint8)



    cv2.line(img1,(49,0),(0,99),255)
    cv2.line(img1,(0,99),(99,99),255)
    cv2.line(img1,(99,99),(49,0),255)

    

    cv2.line(img2,(0,0),(99,0),255)
    cv2.line(img2,(99,0),(49,99),255)
    cv2.line(img2,(49,99),(0,0),255)

    img = cv2.warpAffine(img2,affine,(500,500))

    for pts in pts2:
        print affine[0][0]*pts[0] + affine[0][1]*pts[1] + affine[0][2] , affine[1][0]*pts[0] + affine[1][1]*pts[1] + affine[1][2]



    img1 = cv2.dilate(img1,None)
    img2 = cv2.dilate(img2,None)
    img = cv2.dilate(img,None)

    #cv2.imshow("normal",img1)
    #cv2.imshow("transed",img2)
    #cv2.imshow("modified",img)
    #cv2.waitKey()
