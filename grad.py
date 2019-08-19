import cv2 
import numpy as np

def getgrads(gray):
    scale = 1
    delta = 0
    ddepth = cv2.CV_16S
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # Gradient-X
    grad_x = cv2.Scharr(gray,ddepth, 1, 0, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    # grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    # Gradient-Y
    grad_y = cv2.Scharr(gray,ddepth, 0, 1, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    # grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    
    
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    
    
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    
    return grad

def CannyThreshold(val, img_blur):
    ratio = 3
    kernel_size = 3
    low_threshold = val
    src = img_blur
    img_blur = cv2.GaussianBlur(img_blur, (3, 3), 0)
    detected_edges = cv2.Canny(img_blur, low_threshold, low_threshold*ratio, kernel_size)
    mask = detected_edges != 0
    dst = src * (mask[:,:].astype(src.dtype))
    return detected_edges