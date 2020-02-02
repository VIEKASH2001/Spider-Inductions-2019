#Author Name : V K VIEKASH
#Domain: Signal Processing and Machine Learning
#Sub-Domain: Image Processing,task 1
#Functions: NONE
#Global Variables: NONE

#implementing the required packages
import cv2
import numpy as np

array=np.zeros((9,9),np.uint8)#creating a 9x9 numpy array
ID=input("enter the aruco ID: ")#this variable stores the value of the aruco ID to be generated
intID=int(ID)#this variable stores the integer value of the aruco ID

if(intID>=0 and intID<1024): #checking the validity of the entered aruco ID
    
    binum=[0,0,0,0,0,0,0,0,0,0]#this is a list which will contain the 10 bit binary number of the aruco ID when converted
    k=9#this variable serves as the index of the list binum
    
    #decimal to binary conversion of aruco ID
    for r in binum:#variable r is just a dummy variable in here, which i have used to just facilitate each iterations
        j=intID%2
        binum[k]=j
        k-=1
        intID/=2
        intID=int(intID)
        
    index_list=[2,3,4,5,6]#this variable is a list containing the index in which the aruco markers are going to be generated in the 9x9 matrix
    p=0#this variable holds the index of list binum in each iteration

    #this loop if to fill the data bits, data 1 and data 2 with the generated binary number
    for index in index_list:#variable index holds the index of the numpy array
        array[index][3]=binum[p]
        array[index][5]=binum[p+1]
        p+=2

    #this loop will create the parity bits and will fill in the 3 parity bits parity 1,parity 2 and parity 3 using the Hamming Algorithm
    for index in index_list:#variable index holds the index of the numpy array
        num=array[index][3]+array[index][5]
        if(num%2==0):
            array[index][6]=0
        else:
            array[index][6]=1

        if(array[index][3]%2==0):
            array[index][2]=1
        else:
            array[index][2]=0

        if(array[index][5]%2==0):
            array[index][4]=0
        else:
            array[index][4]=1

    index_list=[0,1,2,3,4,5,6,7,8]##this variable is a list containing the index in which white borders are going to be created
    
    #this loop is for creating white border around the aruco marker        
    for index in index_list:#variable index holds the index of the numpy array
        array[0][index]=1
        array[8][index]=1    
        array[index][0]=1
        array[index][8]=1
        
    print("the matrix of the created aruco marker is: ")    
    print(array)#prints the matrix of the formed aruco marker
    
    array*=255#this is done to change all the 1s in the array to 255 so that while being displayed they are displayed as white color

    #resizing the formed numpy array to display it
    side=int((9*400)/7)#this variable stores the side length of the image to be formed pn resixing. I have chosen int((9*400)/7) as my side length inorder to get the dimension of the marker generated to be 400x400 (excluding the white border)
    dim=(side,side)#variable dim stores the dimension of the image formed on resizing
    resized = cv2.resize(array, dim, interpolation = cv2.INTER_AREA)
    
    text='ARUCO ID: '+ID#this variable holds the text that is going to be displayed in the generated aruco marker
    cv2.putText(resized,text,(130,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0))#to display text which says the ID of the aruco marker
    cv2.imshow("GENERATED_ARUCO_MARKER",resized)#displays the generated aruco marker

else:
    print("invalid aruco ID")#if the aruco ID entered is invalid this statement is displayed
