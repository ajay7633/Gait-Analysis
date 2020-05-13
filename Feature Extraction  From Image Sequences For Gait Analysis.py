#!/usr/bin/env python
# coding: utf-8

# In[1]:


## LOADINGDATA SETS FROM THE PATH. THE USER IMPUTS IMAGE NUMBER IN FOLDER
## IMAGE PROCESSING TECHINIQUESAPPLIED TO LOADED IMAGE
#
# LOAD ALL REQUIRED LIBRARIES
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import scipy.io
import os
import re
from stack import stackImages        # STACKING MULTIPLE IMAGES
from read_file import read_image     # READ INPUT IMAGE FUNCTION
from contours import getContours     # CONTOURS FUNCTION
from contours import empty
from Contour import getContour

_nsre = re.compile('([0-9]+)')
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]   

#
# lOADING IMAGES
#
path = "./Sample Images"
def loadImages(path):
    
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.png')]

#
# OUTPUT THE TOTAL IMAGES CURRENTLY IN FOLDER 
# SORTED EACH IMAGE
#
filenames = loadImages(path)
filenames.sort(key=natural_sort_key)
images = []
for file in filenames:
    images.append(cv2.imread(file,cv2.IMREAD_UNCHANGED))
print("Loaded " + str(len(images)))



T =True
while(T):
    try:
        i = int(input("what is image do you want to load: "))
        img = images[i]
        T =False 
    except:
        print(" Unable to find the image you are looking for")

        
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow("Walk_Data_Original",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 3)
# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)  #1 or 2
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.08*dist_transform.max(),255,0)
# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)
imgContour1 = img.copy()
imgContour2 = img.copy()


# In[2]:


# FUNCTIONS TO DETERMINE THE CONTOUR
# ONE OF FUNCTIONS DETERMINE THE INNER /OUTER TYPE CONTOUR
def empty(a):
    pass
def getContours(threshold,imgContour):
    
    # OTHER POSSIBLE OPTIONS
    #contours,_ = cv2.findContours(threshold,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
    #contours,_ = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
    
    contours,_ = cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) 

    # POINTS IN IMAGE
    axis_x =[]
    axis_y =[]
    for cnt in contours:
        
        # OTHER POSSIBLE OPTIONS
        #areaMin = cv2.getTrackbarPos("Min_Area","Parameters")
        #areaMax = cv2.getTrackbarPos("Max_Area","Parameters")
        
        area =cv2.contourArea(cnt)

        if area > 1000:
            cv2.drawContours(imgContour,cnt,-1,(255,0,255),2)
            
            # CONTOUR APPROXIMATION
            
            peri =cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.1*peri,True)        
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            
            #DISPLAYING TEXT ON IMAGE CONTOUR

            cv2.putText(imgContour,"X: "+ str(int(x)),(x + w + 20 ,y +20 ),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
            cv2.putText(imgContour,"Y: "+ str(int(y)),(x + w + 20 ,y +40 ),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
            cv2.putText(imgContour,"W: "+ str(int(w)),(x + w + 20 ,y +60 ),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
            cv2.putText(imgContour,"H: "+ str(int(h)),(x + w + 20 ,y +80 ),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
            
            axis_x.append(x)
            axis_y.append(y)
    return axis_x,axis_y



def getContour(threshold,imgContour):
    
    # OTHER POSSIBLE OPTIONS
    #contours,_ = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #contours,_ = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    #contours,_ = cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #contours,_ = cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    
    contours,_ = cv2.findContours(threshold,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
    i =1
    m =0
    
    for cnt in contours:
        # OTHER POSSIBLE OPTIONS
        #areaMin = cv2.getTrackbarPos("Min_Area","Parameters")
        #areaMax = cv2.getTrackbarPos("Max_Area","Parameters")
        
        area =cv2.contourArea(cnt)
        
        if area > 1000:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            x,y,w,h = cv2.boundingRect(box)
            cv2.drawContours(imgContour,[box],0,(255,0,255),1)
            if(i % 2 != 0):
                cv2.putText(imgContour,"OuterBox",(x + w + 20,y + m),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
            else:
                cv2.putText(imgContour,"InnerBox",(x + w + 20,y + m),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
            cv2.putText(imgContour,"X: "+ str(int(x)),(x + w + 20 ,y +20 +m),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
            cv2.putText(imgContour,"Y: "+ str(int(y)),(x + w + 20 ,y +40 +m),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
            cv2.putText(imgContour,"W: "+ str(int(w)),(x + w + 20 ,y +60 +m),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
            cv2.putText(imgContour,"H: "+ str(int(h)),(x + w + 20 ,y +80 +m),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
            m =m +100
            if(i % 2 != 0):
                print("Box Outer")
            else:
                print("Box inner")
                m=0
            print("Values =" + "X: "+ str(int(x)) + ","+"Y: "+ str(int(y))+","+"W: "+ str(int(w))+","+"H: "+ str(int(h)))
            i=i+1
     


# In[3]:


X,Y = getContours(unknown,imgContour1)
getContour(unknown,imgContour2)

cv2.imshow("imgContour1",imgContour1)
cv2.imshow("imgContour2",imgContour2)
cv2.imshow("Image Boundary",unknown)
plott = imgContour1.copy()
cv2.waitKey(0)
cv2.destroyAllWindows()
print(imgContour1.shape)


# In[4]:


# CALCULATING THE VELOCITY USING FUNCTION
# DONE BY TAKING THE VALUES (X0,Y0) (X2,Y2) to CALCULATE VELOCITY
def velocity(x1, y1, x2, y2,Constant1,Constant2): 
    return abs((float)((x2-x1)*Constant1)/((y2-y1)*Constant2))

Constant1 = 100/496
Constant2 = 10/369
try:
    velocity = velocity(X[0],Y[0],X[2],Y[2],Constant1,Constant2)
    step_length = ((X[2] - X[1]) * Constant1) 
    stride_length = ((X[2] - X[0]) * Constant1)
    
    cv2.line(plott,(X[0],Y[0]),(X[2],Y[2]),(0,0,255),1)
    cv2.putText(plott,"Velocity(m/s): "+ str(round(velocity/39.3701,2)),(50 ,250),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1)
    cv2.putText(plott,"step_length(m): "+ str(round(step_length/39.3701,2)),(50 ,300),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1)
    cv2.putText(plott,"stride_length(m): "+ str(round(stride_length/39.3701,2)),(50 ,350),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1)
    cv2.imshow("Calculating the slope",plott)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except:
    print('Cannot calculate the value of velocity,steplength,stride left')

    
#PRINTING VELOCITY ,STRIDE LENGTH, STEP LENGTH    
print('Velocity :' ,round(velocity/39.3701,2))
print('Stride Length :',round(step_length/39.3701,2))
print('Step Length :',round(stride_length/39.3701,2))


# In[ ]:




