import cv2
import time
import os

def capture_images(interval=1.5, folder="images"):
    # Create the images directory if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Open the default camera
    cap = cv2.VideoCapture(0)

    # Initialize the image counter
    i = 0

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Save the resulting frame
            cv2.imwrite(os.path.join(folder, f'image{i}.jpg'), frame)

            # Increment the image counter
            i += 1

            # Wait for the specified interval
            time.sleep(interval)
    finally:
        # When everything is done, release the capture
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_images()