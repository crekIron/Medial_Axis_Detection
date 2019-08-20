# Program To Read video 
# and Extract Frames 
import cv2 
import numpy as np
import grad 
import line
# Path to video file 
vidObj = cv2.VideoCapture("videos/1.mp4") 
 
# fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
fgbg = cv2.bgsegm.createBackgroundSubtractorCNT(minPixelStability = 10, useHistory = True, maxPixelStability = 10*60, isParallel = True)
# fgbg = cv2.createBackgroundSubtractorMOG2()


kernel1 = np.ones((3,3),np.uint8)
kernel2 = np.ones((5,5),np.uint8)
count = 0
while True: 
    ret, frame = vidObj.read() 

    fgmask = fgbg.apply(frame)
    
    #### morphological techiques
    fgmask = cv2.erode(fgmask,kernel1,iterations = 1) #erosion
    fgmask = cv2.erode(fgmask,kernel2,iterations = 1)
    # opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    
    ####detect edges
    # gradient = grad.getgrads(fgmask)
    edges = grad.CannyThreshold(100, fgmask)

    ####detect lines
    # img_with_lines=line.houghlineP_transform(edges, frame)
    img_with_medial=line.houghmedial(edges, frame)
    
    cv2.imshow('frame', img_with_medial)
    # cv2.imwrite("mask/frame%d.jpg" % count, fgmask)
    # count=count+1
    ####ending loop formalities
    k = cv2.waitKey(20) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()