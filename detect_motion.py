import cv2
import numpy as np

def detect_motion(video):
    cap = cv2.VideoCapture(video)
    
    oldx = None
    oldy = None
    oldxw = None
    oldyh = None

    while(cap.isOpened()):
        _, frame = cap.read()
        high = np.uint8([255,255,255])
        low = np.uint8([0,90,90])
        mask = cv2.inRange(frame,low,high)
        contours, _ = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
        if(len(contours)>0):
            c=max(contours, key=cv2.contourArea)
            M=cv2.moments(c)
            if(M['m00']!=0):
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.circle(mask,(cx,cy),5,(255,255,255),-1)
        
        cv2.drawContours(mask, c, -1, (0, 255, 0), 1)
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(mask, (x, y), (x+w, y+h), (255, 255, 0), 1)
        # print(w, h, cx, cy, sep=' ')
        
        if(oldx==None):
            oldx = cx
            oldy = cy
            oldw = w
            oldh = h

        else:
            if(cx-oldx>1):
                print("left")
            elif(oldx-cx>1):
                print("right")
            elif(cy-oldy>1):
                print("up")
            elif(oldy-cy>1):
                print("down")
            else:
                print("forward")

            oldx = cx
            oldy = cy
            oldw = w
            oldh = h
            

        cv2.imshow("mask", mask)
        cv2.imshow("frame", frame)

        if(cv2.waitKey(30)) & 0XFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


detect_motion("front_4.mp4")
#detect_motion("front_3.mp4")
#detect_motion("front_2.mp4")
#detect_motion("front_1.mp4")