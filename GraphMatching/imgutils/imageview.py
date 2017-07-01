import sys
import cv2
import random
from matplotlib import pyplot

def plotMatrix(matrix, title=""):
    figure = pyplot.figure()
    ax = figure.add_subplot(111)
    ax.imshow(matrix)
    pyplot.title = title
    pyplot.show()


def imShow(matrix, title=""):
    cv2.imshow(title,matrix)
    cv2.waitKey(0)

def imagesShow(*images):
    i=1
    for image in images:
        cv2.imshow(str(i),image)
        i=i+1
    cv2.waitKey(0)

def printImagePixels(matrix):
    row = matrix.shape[0]
    col = matrix.shape[1]
    for i in range(row):
        for j in range(col):
            sys.stdout.write("%3d " %matrix[i,j])
        sys.stdout.write("\n")


def drawCircles(circles, image):
    for circle in circles:
        center = circle[0]
        radius = circle[1]
        cv2.circle(image,tuple(center),radius,(0,255,255),4)
        cv2.rectangle(image,(center[0] - 5, center[1] - 5), (center[0] + 5, center[1] + 5), (0, 128, 255), -1)

def showContours(contours, image):
    img = image.copy()
    for contour in contours:
        cv2.drawContours(img,[contour],-1, (random.randint(0,255),random.randint(0,255),random.randint(0,255)),1)
    plotMatrix(img)

def drawContours(contours, image):    
    for contour in contours:
        cv2.drawContours(image,[contour],-1, (random.randint(0,255),random.randint(0,255),random.randint(0,255)),5)

def drawGraphContours(graph, image):
    for i in xrange(0,graph.node_count):
        node = graph.graph_nodes[i]
        cv2.drawContours(image,[node.location],-1,(0,255,0),5)

def drawNodeContours(graph,nodes,image):
    for i in nodes:
        node = graph.graph_nodes[i]
        cv2.drawContours(image,[node.location],-1,(0,255,0),5)

def drawGraphOnImage(graph,image):
    points = graph.nodes
    for point in points:
        cv2.circle(image,(point.Y,point.X),5,(125,45,78),-1) 
       