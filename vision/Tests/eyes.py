import cv2
import time
import os
import sys
import random
from datetime import datetime

# images directory
images_dir = os.path.join(os.getcwd(), 'images')

# define video capture object
video = cv2.VideoCapture(1)

# last immage save time
from datetime import datetime

# Initialize last_image_save_time with the current time
last_image_save_time = datetime.now()

def is_time_difference_five_seconds(last_image_save_time):
    current_time = datetime.now()
    time_difference = current_time - last_image_save_time
    return time_difference.total_seconds() >= 2


# function to genration random name for the image
def random_name():
    # get the current time
    current_time = time.strftime("%Y%m%d-%H%M%S")

    # get a random number
    random_number = random.randint(0, 100000)

    # return the random name
    return current_time + str(random_number)


# function save an image given a frame
def save_image(frame):
    # get the current time
    current_time = time.strftime("%Y%m%d-%H%M%S")

    image_name = random_name()

    # save the image
    cv2.imwrite(os.path.join(images_dir, image_name + '.jpg'), frame)
    return 'complete'


def checker(frame):
    global last_image_save_time
    if is_time_difference_five_seconds(last_image_save_time):
        # save the image
        save_image(frame)
        last_image_save_time = datetime.now()
    else:
        pass


def capture():
    
    # start the video capture
    while True:
        ret, frame = video.read()

        # run the image checker
        checker(frame)

        # print
        print('running...')
        
        # display the frame
        cv2.imshow('ALFIE-Vision (preview)', frame)


        # press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

capture()

