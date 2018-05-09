#!/usr/bin/python
# -------------------------------------------------------------------
# mod_openopc	
# -------------------------------------------------------------------
# ... integrating the Python OpenOPC project to run HMI
#     over Linux, BSD, any Unix, and now Shitty Windows
#     in an unfettered manner.
# -------------------------------------------------------------------
# Win32 Bootup Helper 
# -- (insert me into 'STARTUP' folder if desired.
# -------------------------------------------------------------------
# --------------------- DEBUGGER ------------------------------------
# --------------------- -- PDB --------------------------------------
import pdb			# the python debugger, because noone
				#    is perfect.  enable its use by
				#    placing the following tag where
				#    you would like to begin line by
				#    line hashing...
				#
#pdb.set_trace()		# uncomment to debug entire program
# --------------------- HARDCODED VARIABLES -------------------------
# --------------------- -- COMMON VARS ------------------------------
import mod_openopc_common
mod_openopc_SOCKET_FIRSTBOOT_WAIT = mod_openopc_common.OPC_GATEWAY_MONITOR_FIRSTBOOT_WAIT
mod_openopc_Win32_BOOTUP_ALC_WAIT = mod_openopc_SOCKET_FIRSTBOOT_WAIT * 2
mod_openopc_GARBAGE_0 = mod_openopc_common.GARBAGE_0
mod_openopc_GARBAGE_1 = mod_openopc_common.GARBAGE_1
mod_openopc_GARBAGE_2 = mod_openopc_common.GARBAGE_2
# --------------------- -- GARBAGE COLLECTION -----------------------
import gc
gc.set_threshold(mod_openopc_GARBAGE_0,mod_openopc_GARBAGE_1,mod_openopc_GARBAGE_2)
gc.enable()
# --------------------- LOAD LIBRARIES ------------------------------
# --------------------- -- STANDARD ---------------------------------
import sys
import os
import array
import time
import subprocess
# --------------------- -- BASE PATH DETERMINATION ------------------
PYTHON_EXECUTABLE = sys.executable
MOD_OPENOPC_EXECUTABLE = os.path.join(sys.path[0], "mod_openopc.py")
# --------------------- -- CORE -------------------------------------
import mod_openopc_library
# --------------------- -- MODE DETERMINATION -----------------------
try:
	if sys.argv[1] == 'RUN':
		YOURCOMMAND1 = sys.argv[1]
	else:
		YOURCOMMAND1 = "HELP"
except:
	YOURCOMMAND1 = "HELP"
print "mod_openopc Win32 Bootup Helper is executing..."
print "-- " + YOURCOMMAND1
print "------------------------------------------------------------"
print "------------------------------------------------------------"
print ""
# --------------------- -- THREAD ID -------------------------------
try:
	import setproctitle
except:
	pass
def name_that_thread():
	# DECLARE GLOBAL VARS
	global THREADNAME
	try:
		setproctitle.setproctitle(THREADNAME)
		print "-- THREAD RENAMED... " + THREADNAME
		print "------------------------------------------------------------"
		print ""
	except:
		print "-- SKIPPING THREAD RENAME via SETPROCTITLE"
		print "-- -- CANNOT ACCESS setproctitle.setproctitle()"
		print "------------------------------------------------------------"
		print ""
# -------------------------------------------------------------------
#
# --------------------- MODE EXECUTION ------------------------------
CLEAN_EXIT = "YES"
# --------------------- -- GATEWAY_DAEMON_ONLY ----------------------
if YOURCOMMAND1 == 'RUN':
	print "STARTING ROUTINE - RUN"
	print "------------------------------------------------------------"
	print ""
	# NAME THREAD
	THREADNAME = "mod_openopc_" + YOURCOMMAND1
	name_that_thread()
	# PREPARE THE COMMANDS
	CMD_GD = PYTHON_EXECUTABLE + " " + MOD_OPENOPC_EXECUTABLE + " " + "GATEWAY_DAEMON"
	CMD_ALC = PYTHON_EXECUTABLE + " " + MOD_OPENOPC_EXECUTABLE + " " + "AUTO_LAUNCH CONFIRM"
	# FIRE THEM OFF
	print "-- GATEWAY_DAEMON"
	print "-- Attempting Launch with command..."
	print CMD_GD
	CMD_GD_PROC_MONITOR = subprocess.Popen(CMD_GD)
	print "-- -- ... OK."
	time.sleep(mod_openopc_Win32_BOOTUP_ALC_WAIT)
	print ""
	print "-- AUTO_LAUNCH CONFIRM"
	print "-- Attempting Launch with command..."
	print CMD_ALC
	CMD_ALC_PROC_MONITOR = subprocess.Popen(CMD_ALC)
	print "-- -- ... OK."
	print ""
else:
	pass
# 
# --------------------- -- HELP -------------------------------------
if YOURCOMMAND1 == 'HELP':
	print ""
	print "STARTING ROUTINE - HELP"
	print ""
	print "Welcome to mod_openopc(2) - Win32 Bootup Helper."
	print "------------------------------------------------"
	print ""
	print "BASIC USAGE..."
	print "--------------"
	print ""
	print "/path/to/python /opt/mod_openopc_2/prog/win32_bootup.py [ARGS]"
	print ""
	print "ARGUMENTS..."
	print "------------"
	print ""
	print "win32_bootup.py RUN"
	print "-- -- gracefully launches the GATEWAY_DAEMON and then executes an"
	print "-- -- AUTO_LAUNCH CONFIRM command in a separate thread."
	print "-- -- this makes it a little easier for those limited by the use of"
	print "-- -- a Windows OS to fire up the backend."
	print "win32_bootup.py HELP (or -h , --help, help)"
	print "-- -- brings you back to this help file any"
	print "-- -- time you need a quick reference."
	print ""
	print "NOTICE -- THIS WINDOW WILL STAY VISIBLE FOR 90 SECONDS"
	print "OR UNTIL YOU CLOSE IT."
	time.sleep(90)		
else:
	pass
# 
# --------------------- CLEAN EXIT ----------------------------------
if CLEAN_EXIT == 'YES':
	exit()
else:
	print ""
	print "THIS WINDOW WILL STAY OPEN SO YOU MAY OBSERVE THE"
	print "PROBLEM! - manually close when you wish."

