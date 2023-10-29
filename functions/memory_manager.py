import os
import time

_tempMemory = []

def build_memory(owner, output):
    global _tempMemory
    _tempMemory.append({
        "owner": owner,
        "output": output
    })
    
    