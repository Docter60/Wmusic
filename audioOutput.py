import subprocess

def audioOutput():
    outputList = subprocess.check_output(["pactl", "list", "sinks"])
