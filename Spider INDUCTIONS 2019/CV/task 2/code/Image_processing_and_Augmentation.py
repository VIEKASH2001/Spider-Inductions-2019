#Author Name : V K VIEKASH
#Domain: Signal Processing and Machine Learning
#Sub-Domain: Image Processing,task 2
#Functions: VideoInit,update,FrameToOpenglTexture,Aruco,VideoCapture,DrawGLScene,Cube,InitGL,keyPressed
#Global Variables: i,p,l,colors,surfaces,rate,threadQuit,cap,newframe,width,height,corners,ID,meanx,meany

import numpy as np
import cv2
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from threading import Thread
import cv2.aruco as aruco
from ObjLoader import *

threadQuit = 0#this is a flag which is used to say wether to stop the threading or not to the video threading function
i=0#no.of iterations passed 
p=0#A flag which says wether the Aruco has been previously detected or not
l=0#stores the no.of Aruco markers detected in the screen(used because ,just incase of any wrong detection, if the code detects more than 1 Aruco markers)
rate=32#thhis is the variable which is calculated out of probability of having the aruco on the screen after these many iterations
cap = cv2.VideoCapture(0)
_,newframe = cap.read()
width,height=700,700#dimensions of the window

#stores the colors for each face of the cube in R,G,B format
colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )
#store the surface connections for the 
surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )


def VideoInit(): 
    #Function Name: VideoInit
    #output: NONE
    #Input: NONE
    #Logic: initializes the threading operation which facilitates the Video capture
    #Example Call: VideoInit()
    
    VideoThread = Thread(target=update, args=())
    VideoThread.start()

def update():
    #Function Name:update() 
    #Output: NONE
    #Input: NONE
    #Logic: captures the frame and this function is initialized during the threading procedure
    #Example Call:update
    
    global newframe
    while(True):
        _,newframe = cap.read()
        if threadQuit == 1:
            break
    cap.release()
    cv2.destroyAllWindows()

def FrameToOpenglTexture():
    #Function Name: FrameToOpenglTexture
    #Output:NONE
    #Input:NONE
    #Logic: convert Captured frame to OpenGL texture format
    #Example Call: FrameToOpenglTexture()
    
    tx_image = cv2.flip(newframe, 0)#flips the image as the resulting image without flipping would be upside down and is stored in the variable tx-image
    tx_image = Image.fromarray(tx_image)#Creates an image memory from an object exporting the array interface
    #ix and iy holds the dimension of the frame
    ix = tx_image.size[0]
    iy = tx_image.size[1]
    tx_image = tx_image.tobytes('raw', 'BGRX', 0, -1)#Return image as a bytes object
    
    # create texture
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)#set texture parameters
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, tx_image)#texture creation

def Aruco():
    #Function Name: Aruco 
    #Output: ids(aruco ids that are detected is returned)
    #Input: NONE
    #Logic: Aruco detection function
    #Example Call:  Aruco()
    
    global corners#stores the corners of the detected Aruco marker
    gray = cv2.cvtColor(newframe, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
    parameters =  aruco.DetectorParameters_create()
    corners, ids,_= aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    return ids
    
def VideoCapture():
    #Function Name: VideoCapture
    #Output: NONE
    #Input: NONE
    #Logic:  positionS the video captured and displayS on the screen
    #Example Call: VideoCapture()
    
    glPushMatrix()
    glTranslatef(0.0,0.0,-6.0)
    glBegin(GL_QUADS)
    #glTedxCoord() set the current texture coordinates
    glTexCoord2f(0.0, 1.0); glVertex3f(-4.0, -3.0, 0.0)
    glTexCoord2f(1.0, 1.0); glVertex3f( 4.0, -3.0, 0.0)
    glTexCoord2f(1.0, 0.0); glVertex3f( 4.0,  3.0, 0.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(-4.0,  3.0, 0.0)
    glEnd()
    glPopMatrix()
    
def DrawGLScene():
    #Function Name: DrawGLScene
    #Output: NONE
    #Input: NONE
    #Logic: Invokes all the functions required to setup the cube and video frame. Also contains the Video stabilisation algorithm
    #Example Call: DrawGLScene()
    
    global i
    global p
    global ID
    global l
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    ID=Aruco()# this variable stores the aruco ID of the detected marker
    l=len(corners)
    FrameToOpenglTexture()
    VideoCapture()#opening the video screen in the display window
    #the below set of statements are for 2 puposes:
    # 1.To manage the case of multiple Arucos being detected instead of the single Aruco marker shown.
    # 2.Algorithm for video stabilisation
    #Video stabilisation algorithm:
    #           there are 3 nested if statements inside the below if statement. in the first statement i is incremented whenever no Aruco marker is detected
    #           then in the 2nd if statement I check wether i<= Rate, because if the Aruco is not detected for about the Rate number of iterations then the 
    #           chances of the Aruco Marker having left the screen is higher, Here i have chosen the Rate value out of Trail and error
    # for example: I counted the time taken for each iterations to happen in the program.It came out to be like 1 iteration = 1/64 seconds, So I gave a condition like this:
    #              If the no.of iterations aruco IDs is not detected is >Rate (means Rate/64 seconds) then it means that the aruco marker has completely left the screen(Assumption,HIgher Probability)
    #              And if it is less than Rate then it means that some iterations have been skipped detecting the marker so that need not be considered as the Aruco having left the screen(again here also Assumption,Higher Probability)
    #So to summarize my code will see to that if the number of skipped iterations is less than Rate then still the cube will be displayed But if it is >Rate  then the probability that it has left the screen is greater
                 
    if(l==1 or l== 0):
       if(ID!=250):#here the value 250 is the ID of the Aruco Marker that I used.
           i+=1
       if(ID!=250 and i<=rate and p!=0): #here p says wether the cube has already been detected once(this is because if the video capture has started and i is <=rate and ID=NONE then cube will be displayed without any aruco marker)
           Cube()
       if(ID==250):
           Cube()
           i=0#once the Aruco is detected the no.of iterations passed is reseted to 0
           p=1#flag value made 1
    if(l>1):#if more than one marker is detected then the list of IDs are checked and the cube is displayed only if 250 is detected
        for ids in ID:
            if(ids==250):
               Cube()
               break
    glutSwapBuffers()
    
def Cube():
    #Function Name: Cube
    #Output: NONE
    #Input: NONE
    #Logic: facilitates the cube positioning and cube formation 
    #Example Call: Cube()
    
    global i
    global p
    global l
    global meanx#stores the x coordinate of the midpoint of the aruco marker
    global meany#stores the y coordinate of the midpoint of the aruco marker
    #the below set of conditions are same as that in DrawGLScene()
    #these are for Aruco locationing and cube positioning first
    #I am using my own algorithm to calibrate the camera to position the cube on the aruco
    #first i calculate the midpoint of the aruco marker (meanx, meany)
    #then here i do a small calculation to calibrate the aruco and store it in x and y 
    if(l==1 or l== 0):
        if(ID==250):
            meanx=(corners[0][0][0][0]+corners[0][0][2][0])/2
            meany=(corners[0][0][0][1]+corners[0][0][2][1])/2
            x=(meanx*0.0068)-1.7
            y=(meany*0.0068)-1.7
            i=0
            p=1
        if(ID!=250 and i<=rate and p!=0):
            x=(meanx*0.0068)-1.7#I got the values 0.0068 and 1.7 by my own logic,by compparing the number of pixels present and number of pixels occupied by the cube
            y=(meany*0.0068)-1.7   
        if(ID!=250):
            i+=1
    if(l>1):#if more than one marker is detected then the correct set of corners have to be returned so the below operation is done to retun the corner coordinates of ID:250 alone
        for ids in ID:
            if(ids==250):
                meanx=(corners[0][0][0][0]+corners[0][0][2][0])/2
                meany=(corners[0][0][0][1]+corners[0][0][2][1])/2
                x=(meanx*0.007)-1.7
                y=(meany*0.007)-1.7
                break
    side=0.6#this variable stores the side of the cube displayed
    #stores the vertices
    vertices= (
    (x, -(y-side), 0),
    (x, -y, 0),
    (x-side, -y, 0),
    (x-side, -(y-side), 0),
    (x, -(y-side), side),
    (x, -y, side),
    (x-side, -(y-side), side),
    (x-side, -y, side)
    )
    
    glPushMatrix()
    glTranslatef(0.0,0.0,-6.0)
    
    #surfaces are formed
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
    glEnd()
    glPopMatrix()
    
def InitGL(Width,Height):
    #Function Name: InitGL 
    #Output: NONE
    #Input: width and height sre the function arguements. These are required to define the dimensions of the window
    #Logic: initializes the parameters for displaying the cube
    #Example Call: InitGL(Width, Height)
    
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)#specify the value used for depth buffer comparisons
    glEnable(GL_DEPTH_TEST)#enable or disable server-side GL capabilities
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_TEXTURE_2D)

def keyPressed():
    #Function Name: keyPressed
    #Output: NONE
    #Input: NONE
    #Logic:  stops the threading operation by changing the value of threadQuit to 1
    #Example Call: keyPressed()
    
    global threadQuit
    if key == chr(27) or key == "q":
        threadQuit = 1
        
#Window creation and initialization of functions
VideoInit()
glutInit()
glutInitDisplayMode(GLUT_RGBA|GLUT_DEPTH|GLUT_DOUBLE)
glutInitWindowSize(width,height)
glutInitWindowPosition(100,100)
glutCreateWindow(b'video window')
glutDisplayFunc(DrawGLScene)
glutIdleFunc(DrawGLScene)
glutKeyboardFunc(keyPressed)
InitGL(width,height)
glutMainLoop()
   


