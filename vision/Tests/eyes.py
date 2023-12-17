import cv2
import time
import os

# images directory
images_dir = os.path.join(os.getcwd(), 'images')

# define video capture object
video = cv2.VideoCapture(1)

def capture():
    
    # start the video capture
    while True:
        ret, frame = video.read()
        print (ret, frame)

        # display the frame
        cv2.imshow('ALFIE-Vision (preview)', frame)


        # press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

capture()

