import tkinter as tk
import customtkinter as ctk
import threading
import subprocess

# impor the interact function from the speech2text file
from functions.speech2text import _interact


def _run_graphical_user_input():
    # system settings.
    ctk.set_appearance_mode("dark")
    # ctk.set_default_color_theme("black")

    # out app frame.
    app = ctk.CTk()
    app.geometry("720x75")
    app.title("Artificial Lifeform Intelligent Entity | p-typed Research (Preview)")

    # add the main UI elements.
    # title = ctk.CTkLabel(app,text="")
    # title.pack(side="left",padx=10,pady=10)

    speech_engine = "system"

    query = tk.StringVar()

    query_holder = ctk.CTkEntry(app, width=600, height=35, font=("Arial", 14.5), textvariable=query)
    query_holder.pack(side="left",padx=10,pady=10)

    # print entered text after user clicks enter.
    def print_text(event):
        request = query.get()
        print(request)

        # call the _interact function in a new thread
        threading.Thread(target=_interact, args=(request,)).start()
        query_holder.delete(0, 'end')



    def _run_graphical_user_input():
        # bind the enter key to the print_text function.
        query_holder.bind("<Return>", print_text)
        # run the app mainloop.
        app.mainloop()

def _use_command_line():
    
    while True:
        user_text = input("Enter your text input On the new Line: \n")

        if user_text == "exit":
            break
        # call the _interact function in a new thread
        threading.Thread(target=_interact, args=(user_text,)).start()
    
    # close the command line interface.
    # exit()
    # subprocess.run("exit")

    
# run the use command line function.
_use_command_line()
