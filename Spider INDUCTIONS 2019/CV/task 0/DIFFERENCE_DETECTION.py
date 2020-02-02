#Author Name : V K VIEKASH
#Domain: Signal Processing and Machine Learning,task 0
#Functions: NONE
#Global Variables: NONE

import serial
import time
import cv2
import numpy as np

ard=serial.Serial("COM10",9600)

#reading the images
img1=cv2.imread('test_image_2.jpg')
img2=cv2.imread('test_image_1.jpg')


#thresholding and reducing the noise of each images,i observed that noise reduction before difference produces lesser noise than noise reduction after finding difference.so i did this.
gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
ret, othresh1 = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(othresh1,kernel,iterations = 1)
dilation1 = cv2.dilate(erosion,kernel,iterations = 1)

gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
ret, othresh2 = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
erosion = cv2.erode(othresh2,kernel,iterations = 1)
dilation2 = cv2.dilate(erosion,kernel,iterations = 1)

#finding difference
diff=dilation1-dilation2

#resizing the difference to 512x512 dimensions, to get final image in 512X512 dimensions
r = 512.0 / diff.shape[1]
dim = (512, int(diff.shape[0] * r))
resized = cv2.resize(diff, dim, interpolation = cv2.INTER_AREA)
cv2.imshow('differences',resized)


eimg=img1#taking img1 as reference(eimg) to display the circled images

#resizing the eimg to 512x512
r = 512.0 / eimg.shape[1]
dim = (512, int(eimg.shape[0] * r))
rimg = cv2.resize(eimg, dim, interpolation = cv2.INTER_AREA)

#to enclose the differences with circle
_, contours,_ = cv2.findContours(resized , cv2.RETR_TREE , cv2.CHAIN_APPROX_NONE)
for cnt in contours:
      (x,y),radius = cv2.minEnclosingCircle(cnt)
      center = (int(x) , int(y))
      radius = int(radius)
      rimg = cv2.circle(rimg , center , radius , (0,225,0) , 5)
cv2.imshow('differences with circle enclosed',rimg)

#now, again im finding the difference after converting it into 5X5. This is because if i find the difference and then convert it into 5X5 then many unexpected
#values are there apart from 0s and 1s. So by first converting it into 5X5 and then finding the difference, i am able to give the result in 0s and 1s.
#the main purpose of me finding the difference before itself is to display the difference to the viewers as 5X5 image cannot be viewed properly because of its low resolution

#converting the images to 5x5 dimensions
dim=(5,5)
resized1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
resized2 = cv2.resize(img2, dim, interpolation = cv2.INTER_AREA)
diff1=resized1-resized2

#thresholdong the difference
gray = cv2.cvtColor(diff1, cv2.COLOR_BGR2GRAY)
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
thresh1=thresh1/255#to make the array full of only 0s and 1s
print(thresh1)#displays the numpy array which shows the positions where LEDs will be glowing 


#now i am considering the formed 5x5 numpy array as a binary number and then converting it into decimal number inorder to send it to arduino
n=1#power of 2 changes using this variable
num=0#the decimal number is stored in this variable
for t in np.nditer(thresh1):
       num+=(t*pow(2,25-n))
       n+=1
num=int(num)
#serial communication to arduino
ard.write(str.encode(str(num)))
ard.flush()
cv2.waitKey(0)

