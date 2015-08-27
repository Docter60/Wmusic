###########################################################
# Program created by Brian Boellner
###########################################################

import os
import subprocess
from random import randrange
from signal import SIGTERM
from commands import getoutput
from time import sleep

from speech import say

###########################################################
# Variable declarations

disFlag = False
count = False
batteryCheck = False
mac = None
path = os.path.dirname(os.path.abspath('__file__'))


###########################################################
# musicPath() sets where music is pulled from.


def musicPath():
    path = raw_input('Path to music folder (leave blank for default): ')
    while True:
        if path == '':
            path = os.path.dirname(os.path.abspath('__file__'))
            break
        elif (os.path.isdir(path)):
            print('Pulling music from ' + path)
            break
        else:
            print('Path not found.')


###########################################################
# The code below tries to see if necessary programs and modules
#   are installed.

try:
    import cwiid
except ImportError:
    say('Seaweed is not installed, install python-seaweed')
    raise SystemExit
try:
    subprocess.call(["mpg123", "--version"])
except OSError:
    say('mpg123 is not installed, install mpg123')


###########################################################
# getRandomFile() gets a file name from the Music folder


def getRandomFile(path):
    files = os.listdir(path)
    index = randrange(0, len(files))
    return files[index]


###########################################################
#
def connAttempt():
    global mac, wm, disFlag, batteryCheck
    try:
        wm = cwiid.Wiimote()
        wm.led = 1
        wm.rpt_mode = cwiid.RPT_BTN
        scanZero = subprocess.check_output(["hcitool", "con"])
        scanZero = scanZero[15:]
        nextCon = scanZero.find('\n')
        macColon = scanZero.find(':')
        possibleMac = scanZero[macColon - 2:macColon + 15]
        if 'Nintendo' in subprocess.check_output(["hcitool", "info", possibleMac]):
            mac = possibleMac
            disFlag = False
            batteryCheck = False
        else:
            scanZero = scanZero[nextCon:]

    except RuntimeError:
        pass


###########################################################
# connectToWiimote() connects to a Wiimote when no Wiimote
#   is connected to this program.


def connectToWiimote():
    global mac, wm, disFlag, batteryCheck
    while (mac == None):
        connAttempt()
    if mac in subprocess.check_output(["hcitool", "con"]):
        wmInfo = str(wm.state)
        batteryLife = int(wmInfo[wmInfo.index('\'battery\': ') + 11:wmInfo.index('}')])
        if batteryLife <= 15 and batteryCheck == False:
            say('Batteries are low')
            batteryCheck = True
    elif disFlag == False:
        say('Wiimote disconnected.')
        disFlag == True
        connAttempt()
    elif disFlag == True:
        connAttempt()


###########################################################
# Shuffle() checks to see if omxplayer is already running.
#   if so, omxplayer is killed.  Omxplayer is executed after checking.


def shuffle():
    global music
    x = getRandomFile(path + '/music')
    tasks = getoutput('ps -A')
    if 'omxplayer.bin' in tasks:
        # kill omxplayer
        os.killpg(music.pid, SIGTERM)
    # start any music file
    say(x[: - 4])
    music = subprocess.Popen(["omxplayer", "-o", "local", path + '/music/' + x],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             preexec_fn=os.setsid)


###########################################################
# Action() handles the Wiimote's buttons and current omxplayer.


def Action():
    global wm, music, count
    tasks = getoutput('ps -A')
    if wm.state['buttons'] & cwiid.BTN_B:
        # shuffle music
        shuffle()
        count = True
    elif wm.state['buttons'] & cwiid.BTN_DOWN and 'omxplayer.bin' in tasks:
        # stop music
        os.killpg(music.pid, SIGTERM)
        count = False
    elif wm.state['buttons'] & cwiid.BTN_A and 'omxplayer.bin' in tasks:
        # pause/play music
        music.stdin.write("p")
        music.stdout.flush()
        sleep(0.2)
    elif wm.state['buttons'] & cwiid.BTN_PLUS:
        # code to increase volume?
        music.stdin.write("+")
        music.stdout.flush()
        sleep(0.15)
    elif wm.state['buttons'] & cwiid.BTN_MINUS:
        # code to decrease volume?
        music.stdin.write("-")
        music.stdout.flush()
        sleep(0.15)
    elif wm.state['buttons'] & cwiid.BTN_HOME:
        # close program
        if 'omxplayer.bin' in tasks:
            os.killpg(music.pid, SIGTERM)
            count = False
        raise SystemExit
    if count:
        if music.poll() != None:
            # auto shuffle music
            shuffle()


###########################################################
# Main Loop

say('Press one and two on the wiimote now.')
while True:
    connectToWiimote()
    Action()
