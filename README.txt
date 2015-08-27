
Requirements:
- Wiimote
- Bluetooth enabled device/dongle
- OS: Linux
- At least Python 2.7
- python-cwiid installation
- mpg123 installation

Description:
	This program will let the user play music through control of a Wiimote. Music is output
through the 3.5 mm audio jack on the system.  Place all desired music files to be shuffled in the
Music folder in the same directory of this program.  Controls are listed below:

A = Pause/Play current song
B = Skip and Shuffle
Down = Stop current song
Plus = Increase Volume 3 dB
Minus = Decrease Volume 3 dB
Home = Exit Program
1+2 = Connect

If batteries are below 15%, it will tell you batteries are low once you connect.

Note: If a raspberry pi is used, increasing volume will result in music clipping because a
Raspberry Pi can only output so much amplification due to only intaking 5 V at 2 A,
therefore external amplification must be applied to change volume.

Program made by Brian Boellner
Cwiid made by abtrakraft
mpg123 open source

To do:
-Option for audio output (info pactl)
-Fix volume problems (info amixer)
-Option automatic at startup
-Option terminal/offline version
-Cleanup
-Long term...Research Java version?
-Make 2.0 both online and offline