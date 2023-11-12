import cv2
from deepface import DeepFace
import threading
import pathlib
import time

# set the counter to 0
counter = 0

face_match = False
# reference image
# ref_img = cv2.imread("edmond.jpg")

# get the faces folder in the same directory using the pathlib module
faces_folder = pathlib.Path("faces/")
# edmond = pathlib.Path("edmond2.jpg")

# Systsm Variables
current_time = time.time()
Current_User = "Edmond"
Current_user_role = "Admin"
System_status = "Active"
system_envrionment = "debug"

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# function create a random filename.
def random_filename():
    return str(time.time()).replace(".", "") 


# take a picture.
def capture_frame(cap):
    filename = random_filename()

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(f"faces/{filename}.jpg", frame) 

def check_face(param):
    faces_folder = pathlib.Path("faces/")
    # print the passed parameter
    print(param)

    global face_match
    for img_path in faces_folder.glob("*.jpg"):
        try:
            if DeepFace.verify(img1_path=str(param), img2_path=str(img_path))['verified']:
                face_match = True
                return
        except ValueError:
            pass
    face_match = False
    # If face is not detected, capture a frame
    capture_frame(cap)


while True:
    ret, frame = cap.read()
    if ret:
        # show the system status
        cv2.putText(frame, "System Status: " + System_status, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        # show the current user
        cv2.putText(frame, "Current User: " + Current_User, (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        # show the current user role
        cv2.putText(frame, "Current User Role: " + Current_user_role, (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        # show the system environment
        cv2.putText(frame, "System Environment: " + system_envrionment, (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        # show the current time
        cv2.putText(frame, "Current Time: " + str(time.time()), (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)


        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
        counter += 1

        if face_match:
            cv2.putText(frame, "MATCH", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO MATCH", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("ALFIE Vision (Preview)", frame)


    key = cv2.waitKey(1)
    if key == ord("q"):
        break