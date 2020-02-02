#Author Name : V K VIEKASH
#Domain: Signal Processing and Machine Learning
#Sub-Domain: Image Processing,task 1
#Functions: NONE
#Global Variables: NONE

#implementing the required packages
import cv2
import numpy as np

img=cv2.imread("test_image_2.jpeg")#feed the test image in here

#finding the contours present in the image
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV +cv2.THRESH_OTSU)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(thresh,kernel,iterations = 1)
dilation = cv2.dilate(erosion,kernel,iterations = 1)
contours,_= cv2.findContours(dilation , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnt = cv2.drawContours(img, contours, -1,(0,255,0), 3)

coordinates_list=[0]#this is the list which will store the coordinates of the list 
length=len(contours)#stores the number of contours totaly formed
i=0#this is a variable which will be incremented in each iteration of the below while loop to know when it has to break out of the loop
j=0#this variable will count the number of errors and is also used to display the count of the error when the corrected image is displayed
check=0#this is a variable which holds value greater than zero if error exists else zero if no error

#in each iteration of this loop, aruco ID of each aruco marker will be detected
while(1):
    #in order to seperate out each aruco marker out of the given image i am going to crop the specific aruco marker on which error detection is done in each iteration
    
    o=0#this variable gives the number of iterations that have taken place while finding the corner coordinates of the image
    cp=len(contours[i])#gives the total number of contour points for the considered aruco marker
    coordinates_list[0]=contours[i][0]
    #cx and cy temproarily stores the x and y coordinate of the contour points
    cx=coordinates_list[0][0][0]
    cy=coordinates_list[0][0][1]
    #(x1,y1)is the coordinate of the near end and (x2,y2) is the coordinate of the farther end
    x1=coordinates_list[0][0][0]
    y1=coordinates_list[0][0][1]
    #cmin and cmax holds the minimum and maximum sum of x and y coordinate of the temproary coordinates
    cmin=cx+cy
    cmax=cx+cy

    #this loop will find the corner coordinates, which are to the near end and to the farther end in order to select the ROI
    while(1):
        coordinates_list[0]=contours[i][o]
        cx=coordinates_list[0][0][0]
        cy=coordinates_list[0][0][1]
        csum=cx+cy
        if(csum<cmin):
            cmin=csum
            x1=coordinates_list[0][0][0]
            y1=coordinates_list[0][0][1]
        if(csum>cmax):
            cmax=csum
            x2=coordinates_list[0][0][0]
            y2=coordinates_list[0][0][1]
        o+=1
        #checking wether all iterations are over
        if(o==cp):
            break
        
    roi = img[y1:y2, x1:x2]#the cropped aruco marker is stored in this variable
    dim=(7,7)#this variable stores the dimensions to which the aruco marker image is resized    
    resized = cv2.resize(roi, dim, interpolation = cv2.INTER_AREA)
    
    #the resized image is converted into a binary numpy array
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    array=thresh/255
  
    index_list=[1,2,3,4,5]#gives values for the variable index in the error detection loop
    error_list=[0,0,0]#list to collect data abour error in each parity

    #this loop does error detection using hamming algorithm
    for index in index_list:#variable index holds the index of the numpy array
        sum1=array[index][2]+array[index][4]+array[index][5]
        if(sum1%2==0):
                error_list[2]=0#as it is not an error
        else:
                error_list[2]=1#as it is an error   
        sum2=array[index][2]+array[index][1]
        if(sum2%2==0):
                error_list[1]=1#as it is an error
        else:
                error_list[1]=0#as it is not an error
        sum3=array[index][4]+array[index][3]   
        if(sum3%2==0):
            error_list[0]=0#as it is not an error
        else:
            error_list[0]=1#as it is an error

    edec=(error_list[0]*4)+(error_list[1]*2)+(error_list[2]*1)#this variable acts as a flag to say wether error is there or not
    
    
    binum=[0,0,0,0,0,0,0,0,0,0]#this is a list which will contain the 10 bit binary number of the aruco ID when converted
    p=0#this variable serves as the index of the list binum

    #this loop will just seperate out the data bits from the aruco markers and will store it in the list binum 
    for index in index_list:#variable index holds the index of the numpy array
        binum[p]=array[index][2]
        binum[p+1]=array[index][4]
        p+=2
        
    dec=0#this variable will store the decimal value of the aruco ID
    k=0#power of 2 changes using this variable while doing binary to decimal conversion
    
    #this loop will convert the binary form of aruco ID to decimal form    
    for index in binum:#variable index holds the index of the numpy array
        dec+=index*pow(2,9-k)
        k+=1
        
    #to create the statement to be displayed on top of the aruco marker based on its validity
    if(edec==0):#if no error
        text='ARUCO ID: '+ str(int(dec)) #this variable holds the text that is going to be displayed in the generated aruco marker
        cv2.putText(cnt,text,(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255))#to display text which says the ID of the aruco marker
    else:#if error exists
        check+=1
        
    #resizing the final image containing the detected aruco markers to display it
    u = 700.0 / cnt.shape[1]#this operation is carried out inorder not to disturb the propotions of the original image while resizing it
    dim = (700, int(cnt.shape[0] * u))#this variable stores the dimensions to which the aruco marker image is resized    
    fin = cv2.resize(cnt, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow("DETECTED_ARUCO_MARKERS",fin)#displays the detected aruco marker
    i+=1
    cv2.waitKey(5)
    #checking wether all iterations are over
    if(i==length):
        break
    
#to print the error status    
if(check>0):#if error exists
    print("error found in aruco markers that aren't name tagged")
else:#if no error
    print("all the aruco markers are error free")
