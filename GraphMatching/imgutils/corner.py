import cv2
import numpy


def cornersOfImage(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    gray = numpy.float32(gray)
    dst=cv2.cornerHarris(gray,2,3,0.04)
   
    real_corners = dst.copy()

    print real_corners.dtype
    pts = []

               #print [i,j] , dst[i,j]
    #dst = cv2.dilate(dst,None)


    #print 0.01*dst.max()
    #cmp = 0.01*dst.max()
    #for i in xrange(0,dst.shape[0]):
    #    for j in xrange(dst.shape[1]):
    #        if dst[i,j] > cmp:
    #           pts.append([i,j])
   
    image[dst>0.05*dst.max()]=[0,0,255]
    output = numpy.zeros(image.shape,dtype = numpy.uint8)
    output[real_corners>0.05*real_corners.max()]=255
    cv2.imwrite("pt1.png",output)
    print dst.dtype
    print pts
    print len(pts)
    cv2.imwrite("corners.png",image)
    cv2.imshow("pts dialted",output)
    cv2.imshow("",image)
    cv2.waitKey()


if __name__ == "__main__":
    pass