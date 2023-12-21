import cv2
import time
import os
import sys
import random
from datetime import datetime

# images directory


from datetime import datetime
import os
import cv2
import time
import random
from datetime import datetime

# image directory
images_dir = os.path.join(os.getcwd(), 'images')


class Vision:
    def __init__(self, camera_port=0):
        self.last_image_save_time = datetime.now()
        self.current_time = datetime.now()
        self.video = cv2.VideoCapture(camera_port)

    def is_time_difference_five_seconds(self):
        current_time = datetime.now()
        time_difference = current_time - self.last_image_save_time
        return time_difference.total_seconds() >= 5

    def random_name(self):
        current_time = time.strftime("%Y%m%d-%H%M%S")
        random_number = random.randint(0, 100000)
        return current_time + str(random_number)

    def save_image(self, frame, passed_time):
        image_name = ''
        time_difference = passed_time - self.current_time
        seconds = time_difference.total_seconds()

        if seconds >= 2:
            print(seconds)
            self.current_time = datetime.now()
            image_name = self.random_name()
            print('saving image... {image_name}')
            os.system('clear')

        print(fr'continuing.... {datetime.now().strftime("%H:%M:%S")}, Passed Seconds: {seconds}')
        cv2.imwrite(os.path.join(images_dir, image_name + '.jpg'), frame)

    def checker(self, frame):
        if self.is_time_difference_five_seconds():
            self.save_image(frame, datetime.now())
            self.last_image_save_time = datetime.now()

    def capture(self):
        while True:
            ret, frame = self.video.read()
            self.save_image(frame, datetime.now())
            print('running...')
            cv2.imshow('ALFIE-Vision (preview)', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

vision = Vision()
while True:
    vision.capture()