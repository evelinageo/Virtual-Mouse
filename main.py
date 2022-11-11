#needed for the camera
import cv2
#needed to detect the hand
import mediapipe as mp
#needed to move the mouse
import pyautogui

#ask cv to capture video
cap=cv2.VideoCapture(0)
hand_detector= mp.solutions.hands.Hands()
drawing_utils=mp.solutions.drawing_utils
screen_width,screen_height=pyautogui.size()
#define index_y
index_y=0
while True:
    _,frame = cap.read()
    #flip the camera, 1 means flip on the y axis
    frame=cv2.flip(frame,1)
    #get the width and height of the frame camera
    frame_height, frame_width, _=frame.shape
    #convert color of the frame, using cv2
    color_frame= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output=hand_detector.process(color_frame)
    hands=output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame,hand)
            landmarks=hand.landmark
            #passing all the landmarks of the hand
            for id,landmark in enumerate(landmarks):
                #find the pixels, the position of hand
                x=int(landmark.x*frame_width)
                y=int(landmark.y*frame_height)
                #print(x,y)
                #seperate the index finger, the tip of the index is number 8
                if id==8:
                    cv2.circle(img=frame,center=(x,y), radius=10, color=(0,255,255))
                    #find how much bigger the screen is compared to the frame and multiply
                    #with x value
                    index_x=screen_width/frame_width*x
                    index_y=screen_height/frame_height*y
                    # move the mouse wherever you want
                    pyautogui.moveTo(index_x, index_y)
                #number 4 is the tip of the thumb
                if id==4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    #print('outside',abs(index_y-thumb_y))
                    #if the distance between the index and the thumb is really small
                    if abs(index_y-thumb_y)<50:
                        pyautogui.click()
                        pyautogui.sleep(1)
                        #print('click')


    #show image
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
