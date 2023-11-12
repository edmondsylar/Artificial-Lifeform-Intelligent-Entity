from data import *
from rich.console import Console

console = Console()

# function logs completed tasks
def _complete_task(task):
    complete_tasks.append(task)
    console.log(f'Completed Task: \n {tasks}')


def _build_memory(db, player, content):
    
    _build = {
        "role" : f"{player}", 
        "content" : f"{content}"
    }
    db.append(_build)