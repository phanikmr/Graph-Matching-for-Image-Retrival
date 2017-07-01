import cv2
import numpy as np
import math
import operator

def Canny_edge(img):
    edges = cv2.Canny(img,100,200)
    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=-1)
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=-1)
    theta = np.arctan2(sobely, sobelx)
    return (edges, sobelx, sobely, theta)

def StokeWidthTransform(im):
        
        im_grey = im
        #disp_image(im_grey)

        ## Canny edge detection
        edges, sobelx, sobely, theta = Canny_edge(im_grey)
        #disp_image(edges);disp_image(sobelx);disp_image(sobely)

        ##SWT

        #start = time.time()
        swt = np.empty(theta.shape)
        swt[:] = np.Infinity
        rays = []

        ##StrokeWidthDirection
        normal_g_x = 1 * sobelx
        normal_g_y = 1 * sobely
        grad_mag = np.sqrt( normal_g_x * normal_g_x + normal_g_y * normal_g_y )
        with np.errstate(invalid = 'ignore'):
            grad_x = normal_g_x/grad_mag; grad_y = normal_g_y/grad_mag

        #disp_image(grad_x);disp_image(grad_y);disp_image(grad_mag)
        

        for x in xrange(edges.shape[1]):
            for y in xrange(edges.shape[0]):
                if edges[y,x] != 0:
                    x_p = normal_g_x[y,x];y_p = normal_g_y[y,x]
                    mag_p = grad_mag[y,x]
                    grad_x_p = grad_x[y,x];grad_y_p = grad_y[y,x]
                    ray = []; ray.append((x,y))
                    prev_x = x; prev_y = y; i = 0;
                    #print x,y
                    while True:
                        i += 1;
                        cur_x = math.floor(x + grad_x_p * i)
                        cur_y = math.floor(y + grad_y_p * i)
                        #print cur_x,cur_y
                        if np.isnan(cur_x) or np.isnan(cur_y):
                            break
                        cur_x = int(cur_x);cur_y = int(cur_y) 

                        ## Index out of raneg
                        if cur_x < 0 or cur_y < 0:
                            break
                        if cur_x > edges.shape[1] -1 or cur_y > edges.shape[0] - 1:
                            break

                        if cur_x != prev_x or cur_y != prev_y:
                            try:
                                if edges[cur_y, cur_x] != 0:
                                    ray.append((cur_x, cur_y))
                                    try:
                                        if math.acos(grad_x_p * -grad_x[cur_y, cur_x] + 
                                                        grad_y_p * -grad_y[cur_y, cur_x]) < np.pi/2.0:
                                            thickness = math.sqrt( (cur_x - x) * (cur_x - x) + (cur_y - y) * (cur_y - y) )
                                            for (r_x, r_y) in ray:
                                                swt[r_y, r_x] = min(thickness, swt[r_y, r_x])
                                            rays.append(ray)
                                            break
                                    except ValueError:
                                        pass
                                ray.append((cur_x, cur_y))
                            except IndexError:
                                break
                            
                            prev_x = cur_x
                            prev_y = cur_y

        for ray in rays:
            median = np.median([swt[y, x] for (x, y) in ray])
            for (x, y) in ray:
                swt[y, x] = min(median, swt[y, x])

        #print time.time() - start

        #print im_grey.shape[::-1]
        range = 0.2*im_grey.shape[1]
        
        swt_new = np.zeros_like(swt)
        for i in xrange(swt_new.shape[0]):
            for j in xrange(swt_new.shape[1]):
                if swt[i][j] < range:
                    swt_new[i][j] = swt[i][j]
                    swt_new[i][j] = int(swt_new[i][j])
        #return swt_new
        swt = swt_new.astype(int)
        if np.count_nonzero(swt) != 0:
            dict_thick = {}

            for i in xrange(np.max(swt) + 1):
                dict_thick[i] = 0


            for i in xrange(swt.shape[0]):
                for j in xrange(swt.shape[1]):
                    if swt[i][j] != 0:
                        dict_thick[swt[i][j]] += 1

            sorted_thick = sorted(dict_thick.items(), key=operator.itemgetter(1))
            print sorted_thick