import cv2
import numpy
import imageview

def shapeTest(image):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    scale = input("Enter Scale: ")
    scaled_image = cv2.resize(image,(0,0),fx=scale,fy=scale)    
    angle = input("Enter angle: ")
    M = cv2.getRotationMatrix2D(center,angle,1.0)
    rotated_image = cv2.warpAffine(image,M,(w,h))
    M = cv2.getRotationMatrix2D(center,angle,scale)
    scro_image = cv2.warpAffine(image,M,(w,h))


    image_ = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    scaled_image_ = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)
    rotated_image_ = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)
    scro_image_ = cv2.cvtColor(scro_image, cv2.COLOR_BGR2GRAY)
    
    _,im1 = cv2.threshold(image_,128,255,cv2.THRESH_BINARY)
    _,im2 = cv2.threshold(scaled_image_,128,255,cv2.THRESH_BINARY)
    _,im3 = cv2.threshold(rotated_image_,128,255,cv2.THRESH_BINARY)
    _,im4 = cv2.threshold(scro_image_,128,255,cv2.THRESH_BINARY)


    
    _,contour1,_ = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    _,contour2,_ = cv2.findContours(im2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    _,contour3,_ = cv2.findContours(im3,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    _,contour4,_ = cv2.findContours(im4,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    peri1 = cv2.arcLength(contour1[0],True)
    peri2 = cv2.arcLength(contour2[0],True)
    peri3 = cv2.arcLength(contour3[0],True)
    peri4 = cv2.arcLength(contour4[0],True)

    epsilon = 0.03

    approx1 = cv2.approxPolyDP(contour1[0], epsilon * peri1, True)
    approx2 = cv2.approxPolyDP(contour2[0], epsilon * peri2, True)
    approx3 = cv2.approxPolyDP(contour3[0], epsilon * peri3, True)
    approx4 = cv2.approxPolyDP(contour4[0], epsilon * peri4, True)


    print len(approx1),len(approx2),len(approx3),len(approx4)

    imageview.drawContours([approx1],image)
    imageview.drawContours([approx2],scaled_image)
    imageview.drawContours([approx3],rotated_image)
    imageview.drawContours([approx4],scro_image)

    imageview.imagesShow(image,scaled_image,rotated_image,scro_image)

def shapeDetect(Contour,epsilon=0.03):
    peri = cv2.arcLength(Contour,True)
    approx = cv2.approxPolyDP(Contour,epsilon*peri,True)
    pts_count = len(approx)
    if pts_count == 3:
        return "triangle",pts_count
    elif pts_count == 4:
        return "rectangle",pts_count
    elif pts_count == 5:
        return "pentagon", pts_count
    elif pts_count == 6:
        return "hexagon", pts_count
    elif pts_count == 2:
        return "line", pts_count
    elif pts_count == 1:
        return "point", pts_count
    else:
        return "ploygon", pts_count    
    

class ShapeTest(object):

    shapes = {"triangle":None,"rectangle":None,"circle":None}
    

    def __init__(self, *args):
        self.tri_pts = numpy.array([[0,50],[99,0],[99,99]],int)
        self.rect_pts = numpy.array([[25,0],[25,99],[75,99],[75,0]],int)
        #self.pent_pts = numpy.array([[0,49],[24,99],[99,84],[99,14],[24,0]],int)
        self.cirl_pts = numpy.array([[49,0],[90,24],[99,49],[91,74],[49,99],[9,74],[0,49],[9,24]],int)

    def initvals(self):
        self.shapes["triangle"]=None
        self.shapes["rectangle"]=None
        #self.shapes["pentagon"]=None
        self.shapes["circle"]=None

    def detect(self,contour):
        self.initvals()

        self.shapes["triangle"] = cv2.matchShapes(self.tri_pts,contour,1,0)
        self.shapes["rectangle"] = cv2.matchShapes(self.rect_pts,contour,1,0)
        #self.shapes["pentagon"] = cv2.matchShapes(self.pent_pts,contour,1,0)
        self.shapes["circle"] = cv2.matchShapes(self.cirl_pts,contour,1,0)

        min_val = min(self.shapes.itervalues())
        print self.shapes
        return [k for k, v in self.shapes.iteritems() if v == min_val]


if __name__ == "__main__":
    shapetest = ShapeTest()

