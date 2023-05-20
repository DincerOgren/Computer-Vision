import cv2 as cv
import time
import numpy as np
import threading


frameWidth=640
frameHeigth=480



cap = cv.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeigth)

def TimerStatus(given):
    return given

def countdown(lockSecs=5):
    global my_timer 
    global stop_timer
    stop_timer=True
    my_timer=lockSecs
    while True:
        if not TimerStatus(stop_timer):
            pass
        elif TimerStatus(stop_timer):
            time.sleep(1)
            tempTimer=my_timer
            continue
    # while True:   

        if stop_timer:
            continue
        print('Kilitleme işlemine son '+str(int(tempTimer))+' saniye.')
        tempTimer-=1
        time.sleep(1)
        if tempTimer<=0:
            if stop_timer==False:
                print('Kilitleme işlemi başarılı')
            else:
                print('Cisim kayboldu')
            break


    
countdown_thread=threading.Thread(target=countdown)
countdown_thread.start()

def nothing(x):
    pass

timerStart=False

cv.namedWindow("Trackbars")
cv.resizeWindow("Trackbars",480,250)
cv.createTrackbar("L-H","Trackbars",45,180,nothing)
cv.createTrackbar("L-S","Trackbars",118,255,nothing)
cv.createTrackbar("L-V","Trackbars",119,255,nothing)
cv.createTrackbar("H-H","Trackbars",180,180,nothing)
cv.createTrackbar("H-S","Trackbars",255,255,nothing)
cv.createTrackbar("H-V","Trackbars",245,255,nothing)

font=cv.FONT_HERSHEY_COMPLEX

while True:
    _,revframe=cap.read()
    frame=cv.flip(revframe,1)
   

    capWidth = int(frame.shape[1])
    capHeight = int(frame.shape[0])
    
    startX=int(0.25*capWidth)
    startY=int(0.10*capHeight)

    endX=int(capWidth-startX) 
    endY=int(capHeight-startY)

    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    l_h=cv.getTrackbarPos("L-H","Trackbars")
    l_s=cv.getTrackbarPos("L-S","Trackbars")
    l_v=cv.getTrackbarPos("L-V","Trackbars")
    h_h=cv.getTrackbarPos("H-H","Trackbars")
    h_s=cv.getTrackbarPos("H-S","Trackbars")
    h_v=cv.getTrackbarPos("H-V","Trackbars")



    blueLower=np.array([l_h,l_s,l_v])
    blueUpper=np.array([h_h,h_s,h_v])
    blueMask=cv.inRange(hsv,blueLower,blueUpper)
    kernel=(5,5)
    blueMask=cv.erode(blueMask,kernel)

    #contours detection
    contours,hierarchy=cv.findContours(blueMask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    aimSquare=cv.rectangle(frame,(startX,startY),(endX,endY),(255,0,0),3)
    
    for cnt in contours:
        area=cv.contourArea(cnt)
        approx=cv.approxPolyDP(cnt,0.01*cv.arcLength(cnt,True),True)
        x=approx.ravel()[0]
        y=approx.ravel()[1]

        if area>500:
            cv.drawContours(frame, [cnt],0,(0,0,0),4) 

            x_,y_,w,h=cv.boundingRect(approx)
            w_=int(w*10/100)
            h_=int(h*10/100)
            w+=w_
            h+=h_
            lockSquare=cv.rectangle(frame,(x_-w_,y_-h_),(x_+w,y_+h),(0,0,0),5)
            
            lockSquareStartX=x_-w_
            lockSquareStartY=y_-h_
            lockSquareEndX=x_+w
            lockSquareEndY=y_+h
            # if not countdown_thread.is_alive():
            try:
                countdown_thread.start()
                
               
            except RuntimeError: #occurs if thread is dead
                if not countdown_thread.is_alive():
                    countdown_thread = threading.Thread(target=countdown) #create new instance if thread is dead
                    countdown_thread.start() #start thread
                if (startX<=lockSquareStartX and lockSquareEndX<=endX) and (lockSquareStartY>=startY and lockSquareEndY<=endY):  
                    stop_timer=False
                    TimerStatus(stop_timer)    
                # start_time = time.time()
                # while (time.time() - start_time) < 3:
                #     print('Kilitleme işlemine son '+str(int(10-(time.time()-start_time)))+' saniye.')
                # print('Kilitleme işlemi başarılı')
                else:
                    TimerStatus(stop_timer)
                    stop_timer=True
                # countdown_thread.
            if len(approx)== 4:
                cv.putText(frame,"Rectangle",(x,y),font,1,(0,0,0))
            if 10<len(approx<20):
                cv.putText(frame,"Circle",(x,y),font,1,(0,0,0))

            # print(len(approx))
    
    # print(countdown_thread.is_alive(),stop_timer)
            

    cv.imshow("Frame",frame)
    cv.imshow("Mask",blueMask)

    key = cv.waitKey(1)
    if key ==27:
        break

cap.release()
cv.destroyAllWindows()