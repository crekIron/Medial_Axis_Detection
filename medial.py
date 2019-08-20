import cv2
import numpy as np 
import math

def findDfromOrigin(m,x1,y1):
    c = y1 - m*x1
    a = m
    b = -1
    d = abs((a * 0 + b * 0 + c)) / (math.sqrt(a * a + b * b))
    return d

def medial_line(img, linesP, vote):
    track=[]
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            # print(str(l[0])+" "+str(l[1])+" "+str(l[2])+" "+str(l[3]))
            if l[2]-l[0]==0:
                alpha=np.deg2rad(-90)
                d=l[2]
            else: 
                m = (l[3]-l[1])/(l[2]-l[0])
                alpha = np.arctan(m)
                d = findDfromOrigin(m, l[0], l[1])
            maxy=0
            miny=0
            if l[3]>l[1]:
                maxy = l[3]
                miny = l[1]
            else:
                maxy = l[1]
                miny = l[3]
            
            maxx=0
            minx=0
            if l[2]>l[0]:
                maxx = l[2]
                minx = l[0]
            else:
                maxx = l[0]
                minx = l[2]

            # print(str(d) + " " + str(np.rad2deg(alpha)))
            
            if track is None:
                track.append([alpha, d, 1, maxy, miny, maxx, minx])
                print(str(d) + " " + str(np.rad2deg(alpha)))
                continue

            check=0
            rn = 100
            for t in track:
                if ((t[0]-np.deg2rad(10))<=alpha<=(t[0]+np.deg2rad(10))) and ((t[1]-rn)<=d<=(t[1]+rn)):
                    t[0]=(t[2]*t[0]+alpha)/(t[2]+1)
                    t[1]=(t[2]*t[1]+d)/(t[2]+1)
                    t[2]=t[2]+1
                    if t[3]<maxy: 
                        t[3]=maxy
                    if t[4]>miny: 
                        t[4]=miny
                    break
                check=check+1
            if check==len(track):
                track.append([alpha, d, 1, maxy, miny, maxx, minx])
                print(str(d) + " " + str(np.rad2deg(alpha)))
            
    totalvotes=0
    for t in track:
        totalvotes=totalvotes+t[2]
    
    for t in track:
        if t[2]/totalvotes>0.5:
            if np.sin(t[0])==0:
                y1=(t[3]+t[4])/2
                y2=y1
                x1=t[5]
                x2=t[6]
            else:
                y1=t[3]
                y2=t[4]
                cos = 0
                if np.sin(t[0])>0:
                    cos = -1*np.cos(t[0])
                else:
                    cos = np.cos(t[0])

                x1=(t[1]-y1*cos)/abs(np.sin(t[0]))
                x2=(t[1]-y2*cos)/abs(np.sin(t[0]))
            print(str(x1)+" "+str(y1)+" "+str(x2)+" "+str(y2)+" "+"vote:" + str(t[2]))
            cv2.line(img,(int(x1),y1),(int(x2),y2),(255,0, 0), 3, cv2.LINE_AA)
            
            # print(str(np.rad2deg(t[0]))+" "+str(t[1])+" "+ "vote:" + str(t[2]))
    return img