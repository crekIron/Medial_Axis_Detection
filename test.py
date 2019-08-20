import cv2
import numpy as np 
import grad
import line

src = cv2.imread("mask/frame146.jpg")
edges = grad.CannyThreshold(100, src)

####detect lines
img_with_lines=line.houghline_transform(edges, src)
src=cv2.imread("mask/frame146.jpg")
img_with_medial=line.houghlineP_transform(edges,src)



cv2.imwrite("mask/img_with_lines.jpg", img_with_lines)
cv2.imwrite("mask/img_with_medial.jpg", img_with_medial)
