import cv2
import numpy as np 

def hough_transform(edges,img):
    lines = cv2.HoughLines(edges,1,np.pi/180,90)
    if lines is not None:
        print("oh yeah!!")
        for line in lines:
            for rho,theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))

                cv2.line(img,(x1,y1),(x2,y2),(255,0, 0),2)
    
    else:
        print("wtf")
    # cv2.imshow('frame', img)
    return img