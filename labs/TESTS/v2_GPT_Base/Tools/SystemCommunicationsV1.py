# import win10toast 
from win10toast import ToastNotifier 
import threading
import time

# create an object to ToastNotifier class 

def sendSystemNotification():
    # sleep for 5 seconds.
    time.sleep(5)

    n = ToastNotifier() 
    n.show_toast(
        "GEEKSFORGEEKS", 
        "You got notification", 
        duration = 10, 
        icon_path ="https://media.geeksforgeeks.org/wp-content/uploads/geeks.ico",
        threaded=True
        ) 


# while True:
#     input("Enter to send another tnotification in 5 seconds")
#     threading.Thread(target=sendSystemNotification).start()