# the Ochestration Unit is the main class of the ACE project which is going to control the whole process and movement of data between the layers.

# this unit is going to handle all interactions with the layers, even between the bus and the layers.

import time
import os
from dotenv import load_dotenv

# load enironment variables.
load_dotenv()

key = os.getenv("")

class OrchestrationUnit:
    def __init__(self):

        self.idle_timer = None # this timer will keep waiting 

        pass

    def _ExternalUserRquest(self):
        pass


    def _InternalSystemThoughts(self):
        # thoughts


        pass


    def get_southbound_message(self):

        
        pass



    def get_northbound_messages(self):

        pass
        