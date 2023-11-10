import argparse
import subprocess
import os

def open_new_terminal_with_command(command):
    # For Windows
    if os.name == 'nt':
        subprocess.Popen(['start', 'cmd', '/k', command], shell=True)
    # For Unix-like OS (Linux, macOS)
    else:
        subprocess.Popen(['gnome-terminal', '-e', command])

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Open a new terminal and run a command.')
parser.add_argument('command', help='The command to run in the new terminal.')
args = parser.parse_args()

# Open a new terminal with the command
open_new_terminal_with_command(args.command)