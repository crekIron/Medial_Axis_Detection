# Program To Read video 
# and Extract Frames 
import cv2 
import numpy as np
import grad 
import line
# Path to video file 
cv2.namedWindow("frame", cv2.WINDOW_NORMAL) 
vidObj = cv2.VideoCapture("videos/9.mp4") 
width = int(vidObj.get(3))
height = int(vidObj.get(4))

video = cv2.VideoWriter('result_9.avi',cv2.CAP_FFMPEG,cv2.VideoWriter.fourcc('M','J','P','G'),20,(width,height),isColor = True)
# fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
fgbg = cv2.bgsegm.createBackgroundSubtractorCNT(minPixelStability = 10, useHistory = True, maxPixelStability = 10*30, isParallel = True)
# fgbg = cv2.createBackgroundSubtractorMOG2()


kernel1 = np.ones((3,3),np.uint8)
kernel2 = np.ones((5,5),np.uint8)
count = 0
history = []
hist_th = [5,100]
th = [5,100]
checkh=0
while count<vidObj.get(cv2.CAP_PROP_FRAME_COUNT): 
    ret, frame = vidObj.read() 
    print("##################frame: "+str(count+1)+" ##################")
    fgmask = fgbg.apply(frame)
    
    #### morphological techiques
    # fgmask = cv2.erode(fgmask,kernel1,iterations = 1) #erosion
    fgmask = cv2.erode(fgmask,kernel2,iterations = 1)
    # opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    
    ####detect edges
    # gradient = grad.getgrads(fgmask)
    edges = grad.CannyThreshold(100, fgmask)

    ####detect lines
    # img_with_lines=line.houghlineP_transform(edges, frame)
    historyb=history
    img_with_medial, history=line.houghmedial(edges, frame, history, hist_th, th)
    if history==historyb:
        checkh=checkh+1
    else:
        chekh=0
    if checkh==15:
        history=[]
    print(history)
    cv2.imshow('frame', img_with_medial)
    video.write(img_with_medial)
    # cv2.imwrite("mask/frame%d.jpg" % count, fgmask)
    count=count+1
    ####ending loop formalities
    k = cv2.waitKey(20) & 0xff
    if k == 27:
        break


cv2.destroyAllWindows()