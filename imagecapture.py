# Piyush Karkare
# First try of controlling  my DSLR (Canon 60D) with raspberry pi
# uses gphoto2 to control DSLR
# Feb-2022

# IMPORTS 
from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess, os.path
# ----------------------------------------------------------------------

# Kill gphoto process
def killgphoto2Process():
	p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
	out, err = p.communicate()
	#search of the gphoto2 process
	for line in out.splitlines():
		if b'gvfsd-gphoto2' in line:
			#kill this process
			pid = int(line.split(None,1)[0])
			os.kill(pid, signal.SIGKILL)
# ----------------------------------------------------------------------

# Set date and time for stamping  ** GLOBAL Variables **
shot_date = datetime.now().strftime("%Y-%m-%d")
picID = "PiShot"
folder_name = shot_date + picID
# Set save location 
save_location = "/media/pi/PIYUSH - SPLM Backup/dslr/Orchid/" + folder_name
# ----------------------------------------------------------------------

# ** GLOBAL COMMANDS **
clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]
# ----------------------------------------------------------------------


def createSaveFolder():
	try:
		os.makedirs(save_location)
	except:
		print(" ------ > changing to save location", save_location)
		os.chdir(save_location)
# ----------------------------------------------------------------------

def clear_screen():
    # It is for MacOS and Linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # It is for Windows platfrom
        _ = os.system('cls')	
# ----------------------------------------------------------------------

def captureImages():
	print ("******* TAKE PIC *********")
	gp(triggerCommand)
	sleep(4)
	gp(downloadCommand)
	print ("Downloaded image to: ", save_location)
# ----------------------------------------------------------------------
	
def renameFiles(ID):
	os.chdir(save_location)
	global shot_time
	print ("change Dir: ", save_location)
	for filename in os.listdir("."):
		# Time sstamp the file
		shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		if len(filename) < 13:
			if filename.endswith(".JPG"):
				os.rename(filename, (shot_time + ID + ".JPG"))
				print("JPG renamed:", shot_time)
			elif filename.endswith(".CR2"):
				os.rename(filename, (shot_time + ID + ".CR2"))
				print("RAW renamed")
# ----------------------------------------------------------------------

def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d:%02d" % (hour, min, sec)
# ----------------------------------------------------------------------

def MyTimer(min,sec):
	NumSec=min*60+sec
	# Count number of files in the save_location
	NumFiles = len([name for name in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, name))])
	for s in range(NumSec):	
		print ("Time remaining(h:m:s): ", convert(NumSec-s))
		print ("Last Shot          : " + shot_time + picID + ".JPG")
		print ("Total shots today  : ", NumFiles/2)
		sleep(1)	
		clear_screen()
# ----------------------------------------------------------------------

# Start the capture
killgphoto2Process()
while True:
	clear_screen()
	createSaveFolder()
	captureImages()
	renameFiles(picID)
	gp(clearCommand)
	MyTimer(20,0)
# ----------------------------------------------------------------------
