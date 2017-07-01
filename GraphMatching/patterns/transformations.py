import cv2
import numpy
from point import Point


def affineTransformPoint(point,affineMatrix):
    tx = affineMatrix[0][0] * point.X + affineMatrix[0][1] * point.Y + affineMatrix[0][2]
    ty = affineMatrix[1][0] * point.X + affineMatrix[1][1] * point.Y + affineMatrix[1][2]
    return Point(int(tx),int(ty))

def affineTransformPointsList(PointsList, affineMatrix):
    points = []
    for point in PointsList:
        points.append(affineTransformPoint(point,affineMatrix))
    return points

def getAffineMatrixOfPointsList(SrcPts,DstPts):
    srcpts = SrcPts[:3]
    dstpts = DstPts[:3]
    for i in xrange(0,3):
        temp = srcpts.pop()
        temp = temp.getAsList()
        srcpts = [temp] + srcpts
        temp = dstpts.pop()
        temp = temp.getAsList()
        dstpts = [temp] + dstpts
    srcpts = numpy.float32(srcpts)
    dstpts = numpy.float32(dstpts)
    return cv2.getAffineTransform(srcpts,dstpts)


def getAffineMatrix(scale,theta,tx,ty):
    theta = numpy.pi * theta/180.0
    M = numpy.zeros((2,3),float)
    M[0][0] = scale * numpy.cos(theta)
    M[0][1] = scale * numpy.sin(theta)
    M[0][2] = tx
    M[1][0] = -scale * numpy.sin(theta)
    M[1][1] = scale * numpy.cos(theta)
    M[1][2] = ty
    return M

def getScaleRotationTranslation(PointA,PointB,PointP,PointQ):
    AB = PointA.distanceFromThisPoint(PointB)
    PQ = PointP.distanceFromThisPoint(PointQ)
    scale = PQ/AB
    diff1 = (PointB-PointA)/AB
    diff2 = (PointQ-PointP)/PQ
    rad = -180/numpy.pi * (numpy.arctan2(diff2.Y,diff2.X) + numpy.arctan2(diff1.Y,diff1.X))
    M = getAffineMatrix(scale,rad,0,0)

    trans_pt = affineTransformPoint(PointA,M)
    tx = PointP.X - trans_pt.X
    ty = PointP.Y - trans_pt.Y
    return [scale,rad,tx,ty]




if __name__ == "__main__":
    #print getAffineMatrixOfPointsList([Point(68,45),Point(68,41),Point(68,11),"Some Dumb"],[Point(68,45),Point(68,41),Point(68,11),"Some Dumb"])
    a = Point(68,45)
    b = Point(68,41)
    p = Point(68,45)
    q = Point(68,41)
    print getScaleRotationTranslation(a,b,p,q)