import cv2
import numpy as np 
import math

def max(a , b):
    if a>b:
        return a
    return b
def min(a ,b):
    if a>b:
        return b
    return a

def maxth(a , b, th):
    if(a-b>=th or b-a>=th):
        return a
    if a>b:
        return a
    return b
def minth(a ,b, th):
    if(a-b>=th or b-a>=th):
        return a
    if a>b:
        return b
    return a


def findDfromOrigin(m,x1,y1):
    c = y1 - m*x1
    a = m
    b = -1
    d = abs((a * 0 + b * 0 + c)) / (math.sqrt(a * a + b * b))
    return d

def medial_line(img, linesP, historys, hist_th, th):
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

            maxy=max(l[3],l[1])
            miny=min(l[3],l[1])
            maxx=max(l[2],l[0])
            minx=min(l[2],l[0])

            # print(str(d) + " " + str(np.rad2deg(alpha)))
            
            if track is None:
                track.append([alpha, d, 1, maxy, miny, maxx, minx])
                print(str(d) + " " + str(np.rad2deg(alpha)))
                continue

            check=0
            dth = th[1]
            alphath = np.deg2rad(th[0])
            for t in track:
                if ((t[0]-alphath)<=alpha<=(t[0]+alphath)) and ((t[1]-dth)<=d<=(t[1]+dth)):
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
    
    
    ans=[[0,0,0,0,0,0]]
    print(len(ans))
    newlinehascame = False
    for t in track:
        if t[2]/totalvotes>0.3:
            newlinehascame = True
            for history in historys:
                if len(history)!=0:
                    if ((history[0]-np.deg2rad(hist_th[0]))<=t[0]<=(history[0]+np.deg2rad(hist_th[0]))) and ((history[1]-hist_th[1])<=t[1]<=(history[1]+hist_th[1])):
                        t[0]=(t[0]+history[0])/2
                        t[1]=(t[1]+history[1])/2
                        t[3]=maxth(t[3],history[2],20)
                        t[4]=minth(t[4],history[3],20)
                        t[5]=maxth(t[5],history[4],20)
                        t[6]=minth(t[6],history[5],20)
                        break

            # ans=[t[0], t[1], t[3], t[4], t[5], t[6]]
            ans.append([t[0], t[1], t[3], t[4], t[5], t[6]])
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
            cv2.line(img,(int(x1),int(y1)),(int(x2),int(y2)),(255,0, 0), 3, cv2.LINE_AA)
            # print(str(np.rad2deg(t[0]))+" "+str(t[1])+" "+ "vote:" + str(t[2]))
    if newlinehascame==False and len(historys)!=0:
        for history in historys:
            t=[0, 0, 0, 0, 0, 0, 0]
            t[0]=history[0]
            t[1]=history[1]
            t[2]=1
            t[3]=history[2]
            t[4]=history[3]
            t[5]=history[4]
            t[6]=history[5]

            ans.append([t[0], t[1], t[3], t[4], t[5], t[6]])
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
            cv2.line(img,(int(x1),int(y1)),(int(x2),int(y2)),(255,0, 0), 3, cv2.LINE_AA)
    ans.pop(0)
    return img, ans