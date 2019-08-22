import cv2
import numpy as np 
import medial
def houghline_transform(edges,img):
    lines = cv2.HoughLines(edges,1,np.pi/180,90)
    if lines is not None:
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
    
    return img

def houghlineP_transform(edges, img):
    linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 20)
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(img, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
    return img


def houghmedial(edges, img, history, hist_th, th):
    linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 20)
    img, ans= medial.medial_line(img,linesP,history, hist_th, th)
    return img, ans