#!/usr/bin/python
# -------------------------------------------------------------------
# mod_openopc	
# -------------------------------------------------------------------
# ... integrating the Python OpenOPC project to run HMI
#     over Linux, BSD, any Unix, and now Shitty Windows
#     in an unfettered manner.
# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------
#
# --------------------- COPYRIGHT -----------------------------------
# THE FOLLOWING -37- LINES MAY NOT BE REMOVED, BUT MAY BE APPENDED
#   WITH ADDITIONAL CONTRIBUTOR INFORMATION.
print ""
print "------------------------------------------------------------"
print "------------------------------------------------------------"
print "mod_openopc(_2)"
print "Copyright (C) 2008-2013."  
print "V. Spinelli for Sorrento Lactalis American Group"
print "... http://www.lactalis.us/"
print "Copyright (C) 2013-2014."
print "V. Spinelli for SpinelliCreations"
print "... http://www.spinellicreations.com/"
print "Copyright (C) 2014."
print "V. Spinelli for Harper International, Corp."
print "... http://www.harperintl.com"
print "Copyright (C) 2016."
print "V. Spinelli & J. Trembley for RS Automation, LLC"
print "... http://www.rsautomation.net"
print "------------------------------------------------------------"
print "This program comes with ABSOLUTELY NO WARRANTY;"
print "As this program is based on [and has dependancies]"
print "the content of GPL and LGPL works, GPL is preserved."
print ""
print "This is open software, released under GNU GPL v3,"
print "and you are welcome to redistribute it, with this"
print "tag in tact."
print ""
print "A copy of the GPL should be included with this work."
print "If you did not receive a copy, see..."
print "http://www.gnu.org/licenses/gpl-3.0.txt"
print "------------------------------------------------------------"
print "-- The only people who have anything to fear from"
print "-- free software are those whose products are worth"
print "-- even less. - David Emery"
print "------------------------------------------------------------"
print "version number = 3.3-2 (build #66)"
print "------------------------------------------------------------"
print "------------------------------------------------------------"
print ""
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
mod_openopc_SOCKET = mod_openopc_common.OPC_GATEWAY_MONITOR_PORT
mod_openopc_SOCKET_FIRSTBOOT_WAIT = mod_openopc_common.OPC_GATEWAY_MONITOR_FIRSTBOOT_WAIT
mod_openopc_SOCKET_RESTART_WAIT = mod_openopc_common.OPC_GATEWAY_MONITOR_RESTART_WAIT 
OPENOPCGATEWAYSERVICENAME = mod_openopc_common.OPC_SERVICE_NAME
OPENOPCGATEWAYSOCKET = mod_openopc_common.OPC_GATEWAY_PORT
GATEWAY_COMM_CMD_INVALID = mod_openopc_common.GATEWAY_COMM_CMD_INVALID
GATEWAY_COMM_CMD_INVALID_TO_SEND = mod_openopc_common.GATEWAY_COMM_CMD_INVALID_TO_SEND
GATEWAY_COMM_CMD_GATEWAY_RESET = mod_openopc_common.GATEWAY_COMM_CMD_GATEWAY_RESET
GATEWAY_COMM_CMD_GATEWAY_RESET_TO_SEND = mod_openopc_common.GATEWAY_COMM_CMD_GATEWAY_RESET_TO_SEND
GATEWAY_COMM_CMD_CONFIRM = mod_openopc_common.GATEWAY_COMM_CMD_CONFIRM
GATEWAY_COMM_CMD_CONFIRM_TO_SEND = mod_openopc_common.GATEWAY_COMM_CMD_CONFIRM_TO_SEND
GATEWAY_COMM_CMD_PROCEED_WITH_JOBS = mod_openopc_common.GATEWAY_COMM_CMD_PROCEED_WITH_JOBS
GATEWAY_COMM_CMD_PROCEED_WITH_JOBS_TO_SEND = mod_openopc_common.GATEWAY_COMM_CMD_PROCEED_WITH_JOBS_TO_SEND
GATEWAY_COMM_CMD_GATEWAY_RESET_WITH_OPC_SERVER = mod_openopc_common.GATEWAY_COMM_CMD_GATEWAY_RESET_WITH_OPC_SERVER
GATEWAY_COMM_CMD_GATEWAY_RESET_WITH_OPC_SERVER_TO_SEND = str(GATEWAY_COMM_CMD_GATEWAY_RESET_WITH_OPC_SERVER)
mod_openopc_GARBAGE_0 = mod_openopc_common.GARBAGE_0
mod_openopc_GARBAGE_1 = mod_openopc_common.GARBAGE_1
mod_openopc_GARBAGE_2 = mod_openopc_common.GARBAGE_2
# --------------------- -- GARBAGE COLLECTION -----------------------
import gc
gc.set_threshold(mod_openopc_GARBAGE_0,mod_openopc_GARBAGE_1,mod_openopc_GARBAGE_2)
gc.enable()
# --------------------- -- INIT VARS --------------------------------
CLEAN_EXIT = "YES"
OK_GATEWAY_DAEMON = 0
# --------------------- LOAD LIBRARIES ------------------------------
# --------------------- -- STANDARD ---------------------------------
import sys
import array
import ConfigParser
config = ConfigParser.ConfigParser()
import time
from datetime import datetime
import timeit
import shutil
import os
import subprocess
import socket
import random
# --------------------- -- BASE PATH DETERMINATION ------------------
PYTHON_EXECUTABLE = sys.executable
MOD_OPENOPC_EXECUTABLE = os.path.join(sys.path[0], "mod_openopc.py")
MOD_OPENOPC_GATEWAY_EXECUTABLE = os.path.join(sys.path[0], "mod_openopc_gateway.py")
# --------------------- -- CORE -------------------------------------
import mod_openopc_library
# --------------------- -- MODE DETERMINATION -----------------------
try:
	if sys.argv[1] == 'HELP':
		MOD_OPENOPC_MODE = "HELP"
		YOURCOMMAND1 = "HELP"
	else:
		if sys.argv[1] == 'GATEWAY_DAEMON':
			MOD_OPENOPC_MODE = "GATEWAY_DAEMON_ONLY"
			YOURCOMMAND1 = sys.argv[1]
			OK_GATEWAY_DAEMON = 1
		else:
			try:
				import MySQLdb
				MOD_OPENOPC_MODE = "ALL"
				YOURCOMMAND1 = "ALL_PENDING"
			except:
				MOD_OPENOPC_MODE = "HELP"
				YOURCOMMAND1 = "HELP"
except:
	MOD_OPENOPC_MODE = "HELP"
	YOURCOMMAND1 = "HELP"
print "mod_openopc is operating in the following MODE..."
print "-- " + MOD_OPENOPC_MODE
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
# --------------------- BASIC DATESTAMP TO USE ----------------------
def stamp_date():
	global datestamp
	datestamp = datetime.now()
	datestamp = datestamp.strftime("%Y_%m%d_%H:%M:%S")
	return datestamp
# -------------------------------------------------------------------
#
# --------------------- ERROR HANDLING ------------------------------
# --------------------- -- HEADER -----------------------------------
def mod_openopc_error_all_header():
	print ""
	print "ERROR!"
# --------------------- -- FOOTER -----------------------------------
def mod_openopc_error_all_footer():
	print ""
	print "This window will automatically close (or the routine will"
	print "quit) in 30 seconds." 
	time.sleep(30)
# --------------------- -- LACKING ARGUMENTS ------------------------
def mod_openopc_error_command():
	global YOURCOMMAND1
	mod_openopc_error_all_header()
	print ""
	print "You've chosen to run the..."
	print YOURCOMMAND1
	print "...routine, however, you have not supplied us with all"
	print "of the required arguments to do so.  Please run HELP"
	print "to learn more."
	mod_openopc_error_all_footer()
# --------------------- -- SOCKET -----------------------------------
def mod_openopc_error_socket():
	mod_openopc_error_all_header()
	print ""
	print "Unable to maintain network socket connection."
	print "Your subroutine is now effectively halted, and"
	print "no action will be taken in response to attempted"
	print "communication."
	print "This will cause you problems, and must be resolved"
	print "before attempting to restart the subroutine."
	print "Check firewall permissions, as we're binding to"
	print "all interfaces... typically, if a port is blocked"
	print "it will simply not receive / send data - not fault"
	print "this subroutine, so you may have more serious"
	print "backend machine issues."
	print "We haven't settled on a permanent socket format"
	print "as of yet, so open up tcp and upd for your"
	print "desired port, as it may vary depending on which"
	print "version / subversion of mod_openopc you've got."
	mod_openopc_error_all_footer()
# -------------------------------------------------------------------
#
# --------------------- MODE EXECUTION ------------------------------
# --------------------- -- GATEWAY_DAEMON_ONLY ----------------------
if YOURCOMMAND1 == 'GATEWAY_DAEMON':
	print "STARTING ROUTINE - GATEWAY_DAEMON"
	print "------------------------------------------------------------"
	print ""
	if OK_GATEWAY_DAEMON == 1:
		# NAME THREAD
		THREADNAME = "mod_openopc_" + YOURCOMMAND1
		name_that_thread()
		# MASH VARS AS NEEDED
		print "-- YOUR mod_openopc GATEWAY SERVICE ID IS: " + OPENOPCGATEWAYSERVICENAME
		print ""
		GW_MONITOR_HANDSHAKE = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		GW_MONITOR_HANDSHAKE.bind(("", mod_openopc_SOCKET))
		GW_MONITOR_HANDSHAKE_FAULT = "NO"
		# FIRE UP FOR FIRST TIME AT BOOT
		print "-- First Boot..."
		print "-- -- Waiting " + str(mod_openopc_SOCKET_FIRSTBOOT_WAIT) + " seconds to"
		print "-- -- ensure your backend OPC Servers have time to startup."
		print ""
		time.sleep(mod_openopc_SOCKET_FIRSTBOOT_WAIT)
		AUTO_LAUNCH_COMMAND = PYTHON_EXECUTABLE + " " + MOD_OPENOPC_GATEWAY_EXECUTABLE
		print "-- Attempting Launch with command..."
		print AUTO_LAUNCH_COMMAND
		AUTO_LAUNCH_PROCESS = "mod_openopc_GATEWAY_DAEMON"
		AUTO_LAUNCH_PROCESS_MONITOR = subprocess.Popen(AUTO_LAUNCH_COMMAND)
		print "-- -- ... Gateway should be up now."
		print ""
		# RUN PERSISTENT
		try:
			while GW_MONITOR_HANDSHAKE_FAULT == "NO":
				#
				stamp_date()
				print ""
				print "-- NOTICE - " + datestamp + " MONITORING ALL INTERFACES, PORT NUMBER: " + str(mod_openopc_SOCKET)
				print ""
				GW_MONITOR_HANDSHAKE.listen(1)
				try:
					# ACCEPT THE CLIENT CONNECTION
					GW_MONITOR_HANDSHAKE_CONNECTION, GW_MONITOR_HANDSHAKE_ADDY = GW_MONITOR_HANDSHAKE.accept()
					GW_MONITOR_HANDSHAKE_DATA = GW_MONITOR_HANDSHAKE_CONNECTION.recv(4096)
					stamp_date()
					GW_MONITOR_HANDSHAKE_ADDY = str(GW_MONITOR_HANDSHAKE_ADDY)
					print "-- -- RECEIVED MESSAGE at " + datestamp + " FROM CLIENT AT " + GW_MONITOR_HANDSHAKE_ADDY
					print "-- -- -- MESSAGE IS: " + str(GW_MONITOR_HANDSHAKE_DATA)
					print "-- -- -- CHECKING AGAINST: " + GATEWAY_COMM_CMD_GATEWAY_RESET_TO_SEND + " OR " + GATEWAY_COMM_CMD_GATEWAY_RESET_WITH_OPC_SERVER_TO_SEND
					print ""
					# CHECK FOR VALID REQUEST OR BAD DATA / RANDOM JUNK FROM UNKNOWN CLIENT
					DROPPED = 0
					GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_STOP_CMD = "none"
					GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_START_CMD = "none"
					try:
						DROPPED_SEARCH = (int(str(GW_MONITOR_HANDSHAKE_DATA).count(str(GATEWAY_COMM_CMD_GATEWAY_RESET_TO_SEND)))) + (int(str(GW_MONITOR_HANDSHAKE_DATA).count(str(GATEWAY_COMM_CMD_GATEWAY_RESET_WITH_OPC_SERVER_TO_SEND))))
						if DROPPED_SEARCH > 0:
							print "-- -- -- CHECK OK"
							print ""
							DROPPED_SEARCH_2 = int(str(GW_MONITOR_HANDSHAKE_DATA).count(str(GATEWAY_COMM_CMD_GATEWAY_RESET_WITH_OPC_SERVER_TO_SEND)))
							if DROPPED_SEARCH_2 > 0:
								GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_STOP_CMD = str(GW_MONITOR_HANDSHAKE_DATA).split('XXX')
								GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_STOP_CMD = GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_STOP_CMD[1]
								GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_STOP_CMD = GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_STOP_CMD.split('YYY')
								GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_STOP_CMD = GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_STOP_CMD[0]
								GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_START_CMD = str(GW_MONITOR_HANDSHAKE_DATA).split('YYY')
								GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_START_CMD = GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_START_CMD[1]
								GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_START_CMD = GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_START_CMD.split('ZZZ')
								GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_START_CMD = GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_START_CMD[0]
							else:
								pass
						else:
							print "-- -- -- CHECK FAILED"
							print "-- -- -- DISCARDING!"
							print ""
							DROPPED = 1
					except:
						print "-- -- -- FAILED TO PARSE"
						print "-- -- -- DISCARDING!"
						print ""
						DROPPED = 1
					if DROPPED == 0:
						GW_MONITOR_HANDSHAKE_CONNECTION.send(GATEWAY_COMM_CMD_CONFIRM_TO_SEND)
						GW_MONITOR_HANDSHAKE_DATA = GW_MONITOR_HANDSHAKE_CONNECTION.recv(4096)
						if GW_MONITOR_HANDSHAKE_DATA != '':
							# CALL FOR RESET
							# -- STOP GATEWAY
							print "-- -- -- Stopping Gateway."
							AUTO_LAUNCH_PROCESS_MONITOR.terminate()
							AUTO_LAUNCH_PROCESS_PERSISTENCE = AUTO_LAUNCH_PROCESS_MONITOR.poll()
							if AUTO_LAUNCH_PROCESS_PERSISTENCE:
								AUTO_LAUNCH_PROCESS_MONITOR.wait()
							else:
								pass
							AUTO_LAUNCH_PROCESS_MONITOR = "x"
							print "-- -- -- -- SUCCESS."
							print ""
							# -- WAIT
							time.sleep(3)
							# CHECK IF CLIENT WANTS US TO RECYCLE THE OPC SERVER AS WELL
							if (GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_STOP_CMD != 'none') and (GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_START_CMD != 'none'):
								# -- STOP OPC SERVER VIA USER SUPPLIED COMMAND
								try:
									print "-- -- -- Stopping OPC Server."
									print "-- -- -- -- CMD is... " + str(GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_STOP_CMD)
									GATEWAY_RESET_FORK_OPC_SERVER_COMPLETE = 0
									GATEWAY_RESET_FORK_OPC_SERVER_TIME = 0
									GATEWAY_RESET_FORK_OPC_SERVER = subprocess.Popen(GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_STOP_CMD)
									while GATEWAY_RESET_FORK_OPC_SERVER_COMPLETE == 0:
										GATEWAY_RESET_FORK_OPC_SERVER_RETURNCODE = GATEWAY_RESET_FORK_OPC_SERVER.poll()
										if GATEWAY_RESET_FORK_OPC_SERVER_RETURNCODE != None:
											GATEWAY_RESET_FORK_OPC_SERVER = "x"
											GATEWAY_RESET_FORK_OPC_SERVER_COMPLETE = 1
										else:
											pass
										time.sleep(3)
										GATEWAY_RESET_FORK_OPC_SERVER_TIME = GATEWAY_RESET_FORK_OPC_SERVER_TIME + 3
										if GATEWAY_RESET_FORK_OPC_SERVER_TIME > 300:
											GATEWAY_RESET_FORK_OPC_SERVER.terminate()
											GATEWAY_RESET_FORK_OPC_SERVER.wait()
											GATEWAY_RESET_FORK_OPC_SERVER = "x"
											GATEWAY_RESET_FORK_OPC_SERVER_COMPLETE = 1
											print "-- -- -- -- Stop FAILED - KILLED STOP CMD."
										else:
											pass
									print "-- -- -- -- Stopped OK."	
								except:
									pass
								# -- WAIT
								time.sleep(3)
								# -- START OPC SERVER VIA USER SUPPLIED COMMAND
								try:
									print "-- -- -- Starting OPC Server."	
									print "-- -- -- -- CMD is... " + str(GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_START_CMD)
									GATEWAY_RESET_FORK_OPC_SERVER_COMPLETE = 0
									GATEWAY_RESET_FORK_OPC_SERVER_TIME = 0
									GATEWAY_RESET_FORK_OPC_SERVER = subprocess.Popen(GW_MONITOR_HANDSHAKE_DATA_OPC_SERVER_START_CMD)
									while GATEWAY_RESET_FORK_OPC_SERVER_COMPLETE == 0:
										GATEWAY_RESET_FORK_OPC_SERVER_RETURNCODE = GATEWAY_RESET_FORK_OPC_SERVER.poll()
										if GATEWAY_RESET_FORK_OPC_SERVER_RETURNCODE != None:
											GATEWAY_RESET_FORK_OPC_SERVER = "x"
											GATEWAY_RESET_FORK_OPC_SERVER_COMPLETE = 1
										else:
											pass
										time.sleep(3)
										GATEWAY_RESET_FORK_OPC_SERVER_TIME = GATEWAY_RESET_FORK_OPC_SERVER_TIME + 3
										if GATEWAY_RESET_FORK_OPC_SERVER_TIME > 300:
											GATEWAY_RESET_FORK_OPC_SERVER.terminate()
											GATEWAY_RESET_FORK_OPC_SERVER.wait()
											GATEWAY_RESET_FORK_OPC_SERVER = "x"
											GATEWAY_RESET_FORK_OPC_SERVER_COMPLETE = 1
											print "-- -- -- -- Start FAILED - KILLED START CMD."
										else:
											pass
									print "-- -- -- -- Started OK."	
								except:
									pass
							else:
								pass
							# -- START GATEWAY
							print "-- -- -- Starting Gateway."
							AUTO_LAUNCH_PROCESS_MONITOR = subprocess.Popen(AUTO_LAUNCH_COMMAND)
							print "-- -- -- -- SUCCESS."
							print ""
							# -- WAIT
							time.sleep(mod_openopc_SOCKET_RESTART_WAIT)
						else:
							print "-- -- -- CLIENT IS ASKING US TO RECYCLE WITHOUT CONFIRMATION."
							print "-- -- -- -- THAT DOESN'T JIVE."
							print "-- -- -- -- TELLING CLIENT TO JUST GO AHEAD AND PROCEED..."
							print "-- -- -- -- NOT EXECUTING ANY RESET."
							print ""
						# SEND THE OK-TO-RESUME-OPC-JOBS INSTRUCTION BACK TO CLIENT
						GW_MONITOR_HANDSHAKE_CONNECTION.send(GATEWAY_COMM_CMD_PROCEED_WITH_JOBS_TO_SEND)
					else:
						# DENY RESET AND COMPLAIN TO CLIENT
						print "-- -- -- CLIENT SENT US AN INVALID MESSAGE."
						print "-- -- -- -- NO ACTION TAKEN - CLIENT REJECTED."
						print ""
						GW_MONITOR_HANDSHAKE_CONNECTION.send(GATEWAY_COMM_CMD_INVALID_TO_SEND)
				except:
					stamp_date()
					print "-- -- RECEIVED GARBAGE DATA FROM UNKNOWN CLIENT, IGNORING! at " + datestamp
					print ""
				# CLOSE THE CLIENT CONNECTION
				GW_MONITOR_HANDSHAKE_CONNECTION.close()
		except:
			GW_MONITOR_HANDSHAKE_FAULT = "YES"
			CLEAN_EXIT = "NO"
			try:
				GW_MONITOR_HANDSHAKE_CONNECTION.close()
			except:
				pass
			mod_openopc_error_socket()
	else:
		mod_openopc_error_command()
else:
	pass
# -------------------------------------------------------------------
#
# --------------------- MODE EXECUTION ------------------------------
# --------------------- -- ALL (OTHER MODES) ------------------------
if MOD_OPENOPC_MODE == 'ALL':
	# IMPORT GLOBAL OPTIONS
	# -- WHAT IS CURRENT WORKING DIRECTORY
	global_presetpath = sys.path[0]
	# -- HARD CODE REFERENCE TO OPTIONS FOLDER AND THE GLOBAL OPTIONS FILE
	# -- -- TO DO SO, REMOVE '/prog' FROM THE PATH DECLARATION
	global_hardcodedroot = global_presetpath[:-5]
	global_presetpath = os.path.join(global_hardcodedroot, 'options', 'options.opt')
	global_presetpath = os.path.normpath(global_presetpath)
	# -- AGNOSTIC PRESET FILE
	# -- -- PRE-DETERMINE PRESET FILE BASED UPON mod_openopc BUILTIN SNIFFER
	# -- -- THIS SHOULD WORK FOR ALL OS.
	global_presetfile = open(global_presetpath,"r")
	try:
		# SNIFFED PROGRAM FOLDERS
		PROGPATH = global_hardcodedroot
		PROGPATH_OPTIONS = "options"
		PROGPATH_OPTIONS = os.path.join(PROGPATH, PROGPATH_OPTIONS)
		PROGPATH_OPC = "server_configs"
		PROGPATH_OPC = os.path.join(PROGPATH_OPTIONS, PROGPATH_OPC)
		PROGPATH_SQL = "sql_configs"
		PROGPATH_SQL = os.path.join(PROGPATH_OPTIONS, PROGPATH_SQL)
		PROGPATH_PRE = "presets"
		PROGPATH_PRE = os.path.join(PROGPATH_OPTIONS, PROGPATH_PRE)
		PROGPATH_PROG = "prog"
		PROGPATH_PROG = os.path.join(PROGPATH, PROGPATH_PROG)
		PROGPATH_RESET = "gwreset"
		PROGPATH_RESET = os.path.join(PROGPATH, PROGPATH_RESET)
		PROGPATH_GWCOMM = "gwcomm"
		PROGPATH_GWCOMM = os.path.join(PROGPATH, PROGPATH_GWCOMM)
		TEMPDIR = "temp"
		TEMPDIR = os.path.join(PROGPATH, TEMPDIR)
		# ADD SECTIONS FROM FILE
		config.add_section("global_runtime")
		config.add_section("global_throttle")
		config.add_section("global_network")
		config.add_section("global_openopc")
		config.add_section("auto_launch")
		config.add_section("gateway_reset")
		# READ FROM THE FILE
		config.readfp(global_presetfile)
		# ASSIGN VARS BASED ON THE FILE
		MINIMALRESPONSE = config.get("global_runtime","MINIMALRESPONSE")
		if MINIMALRESPONSE == 'YES':
			VERBOSE = "NO"
		else:
			VERBOSE = "YES"
		# -- THROTTLING AND LOAD HANDLING
		GROUPBUILD_TIMEOUT_OVERRIDE = config.get("global_throttle","GROUPBUILD_TIMEOUT_OVERRIDE")
		GROUPBUILD_TIMEOUT_OVERRIDE = float(GROUPBUILD_TIMEOUT_OVERRIDE)
		# -- NETWORK CONNECTIONS
		MYIP = config.get("global_network","MYIP")
		MYDEFAULTGATEWAY = config.get("global_network","MYDEFAULTGATEWAY")
		# -- OPENOPC CONNECTION
		OPENOPC_TIE_IN = config.get("global_openopc","OPENOPC_TIE_IN")
		# -- AUTO LAUNCHER
		AUTO_LAUNCH = config.get("auto_launch","AUTO_LAUNCH")
		AUTO_LAUNCH = AUTO_LAUNCH.split('|')
		# -- SERVER RESET
		GATEWAY_LIST_TO_RESET = config.get("gateway_reset","GATEWAY_LIST_TO_RESET")
		GATEWAY_LIST_TO_RESET = GATEWAY_LIST_TO_RESET.split('|')
		#
		OK_GLOBAL_OPTS = '1'
		global_presetfile.close()
	except:
		OK_GLOBAL_OPTS = '0'
		global_presetfile.close()
	#
	# ERROR DEFINITION WITHIN ALL (OTHER) MODE
	# -- ERROR AUTO LAUNCHER HAS FAILED OR FAULTED
	def mod_openopc_error_autolaunch():
		mod_openopc_error_all_header()
		print ""
		print "We were unable to connect to execute the request."
		print "Perhaps you have mistyped the names of your presets in the"
		print "global options file?  Or perhaps you've malformed the AUTO_LAUNCH"
		print "variable string?"
		print "... elsewise, something is seriously fragged, or you may be using"
		print "an older version of Python which does not support all of the"
		print "functions necessary for this task."
		mod_openopc_error_all_footer()
	# -- ERROR CANNOT CONNECT TO SQL DATABASE
	def mod_openopc_error_sql():
		mod_openopc_error_all_header()
		print ""
		print "We were unable to connect to your selected MySQL database."
		print "Perhaps you have setup incorrect options in..."
		print "-- options/sql_configs/[sqlserver].sql"
		print "Or your SQL server may be down, either way, you must correct"
		print "this before you can proceed."
		mod_openopc_error_all_footer()
	# -- ERROR CANNOT PROPERLY CLOSE SQL DATABASE
	def mod_openopc_error_sql_close():
		# DECLARE GLOBAL VARS
		global sql_connect, sql_cursor
		mod_openopc_error_all_header()
		print ""
		print "Failed to close MySQL connection gracefully."
		sql_connect = ''
		sql_cursor = ''
		# RETURN ARGS
		return sql_connect, sql_cursor
	# -- ERROR OPTIONS FILES NOT PROPERLY IMPORTED OR BAD
	def mod_openopc_error_options():
		mod_openopc_error_all_header()
		print ""
		print "Something is wrong with the syntax or entries within one of"
		print "your options files or preset files..."
		print "-- options/presets/[preset].pre"
		print "-- options/server_configs/[opcserver].opc"
		print "-- options/sql_configs/[sqlserver].sql"
		print "Please correct this before trying to run this routine again."
		mod_openopc_error_all_footer()
	# -- ERROR IN GLOBAL OPTIONS FILE OR MAYBE BAD PERMISSIONS
	def mod_openopc_error_global_options():
		mod_openopc_error_all_header()
		print ""
		print "Your GLOBAL OPTIONS file is not loading properly.  Either"
		print "the syntax is bad or the text of your option arguments are."
		print "Please read the README file and refer to the default options"
		print "file under..."
		print "-- options/default_options.opt"
		mod_openopc_error_all_footer()
	#
	# COMMAND LINE ARGUMENTS
	if OK_GLOBAL_OPTS == '1':
	# -- NOTE, COMMAND ARGUMENTS ASSUME THIS PROGRAM (ITSELF)
	#    TO BE ARGUMENT ZERO
		# VARS
		OK_READ = 0
		OK_READ_ONE_SHOT = 0
		OK_WRITE = 0
		OK_WRITE_ONE_SHOT = 0
		OK_MAINT_DB = 0
		OK_TEST_FOR_ECHO = 0
		OK_WRITE_DAEMON = 0
		OK_READ_DAEMON = 0
		OK_BRIDGE = 0
		OK_SPACE_BRIDGE = 0
		OK_GATEWAY_RESET = 0
		OK_GATEWAY_RESET_DAEMON = 0
		OK_AUTO_LAUNCH = 0
		OK_SERVER_SEEK = 0
		try:
			YOURCOMMAND1 = sys.argv[1]
			if YOURCOMMAND1 == '-h':
				YOURCOMMAND1 = "HELP"
			else:
				if YOURCOMMAND1 == '--help':
					YOURCOMMAND1 = "HELP"
				else:
					YOURCOMMAND1 = YOURCOMMAND1
		except:
			YOURCOMMAND1 = "HELP"
		try:
			YOURCOMMAND2 = sys.argv[2]
		except:
			YOURCOMMAND2 = "null"
		try:
			YOUROPTION1 = sys.argv[2]
			OK_READ = OK_READ + 1
			OK_READ_ONE_SHOT = OK_READ_ONE_SHOT + 1
			OK_WRITE = OK_WRITE + 1
			OK_WRITE_ONE_SHOT = OK_WRITE_ONE_SHOT + 1
			OK_TEST_FOR_ECHO = OK_TEST_FOR_ECHO + 1
			OK_WRITE_DAEMON = OK_WRITE_DAEMON + 1
			OK_READ_DAEMON = OK_READ_DAEMON + 1
			OK_BRIDGE = OK_BRIDGE + 1
			OK_MAINT_DB = OK_MAINT_DB + 1
			OK_SPACE_BRIDGE = OK_SPACE_BRIDGE + 1
			OK_GATEWAY_RESET = OK_GATEWAY_RESET + 1
			OK_GATEWAY_RESET_DAEMON = OK_GATEWAY_RESET_DAEMON + 1
			OK_AUTO_LAUNCH = OK_AUTO_LAUNCH + 1
			OK_SERVER_SEEK = OK_SERVER_SEEK + 1
		except:
			YOUROPTION1 = "null"
			OK_READ = OK_READ - 1
			OK_READ_ONE_SHOT = OK_READ_ONE_SHOT - 1
			OK_WRITE = OK_WRITE - 1
			OK_WRITE_ONE_SHOT = OK_WRITE_ONE_SHOT - 1
			OK_TEST_FOR_ECHO = OK_TEST_FOR_ECHO - 1
			OK_WRITE_DAEMON = OK_WRITE_DAEMON - 1
			OK_READ_DAEMON = OK_READ_DAEMON - 1
			OK_BRIDGE = OK_BRIDGE - 1
			OK_MAINT_DB = OK_MAINT_DB - 1
			OK_SPACE_BRIDGE = OK_SPACE_BRIDGE - 1
			OK_GATEWAY_RESET = OK_GATEWAY_RESET - 1
			OK_GATEWAY_RESET_DAEMON = OK_GATEWAY_RESET_DAEMON - 1
			OK_AUTO_LAUNCH = OK_AUTO_LAUNCH - 1
			OK_SERVER_SEEK = OK_SERVER_SEEK - 1
		try:
			YOUROPTION2 = sys.argv[3]
			OK_READ = OK_READ + 1
			OK_READ_ONE_SHOT = OK_READ_ONE_SHOT + 1
			OK_WRITE = OK_WRITE + 1
			OK_WRITE_ONE_SHOT = OK_WRITE_ONE_SHOT + 1
			OK_BRIDGE = OK_BRIDGE + 1
			OK_SPACE_BRIDGE = OK_SPACE_BRIDGE + 1
			OK_GATEWAY_RESET = OK_GATEWAY_RESET + 1
			OK_GATEWAY_RESET_DAEMON = OK_GATEWAY_RESET_DAEMON + 1
		except:
			YOUROPTION2 = "null"
			OK_READ = OK_READ - 1
			OK_READ_ONE_SHOT = OK_READ_ONE_SHOT - 1
			OK_WRITE = OK_WRITE - 1
			OK_WRITE_ONE_SHOT = OK_WRITE_ONE_SHOT - 1
			OK_BRIDGE = OK_BRIDGE - 1
			OK_SPACE_BRIDGE = OK_SPACE_BRIDGE - 1
			OK_GATEWAY_RESET = OK_GATEWAY_RESET - 1
			OK_GATEWAY_RESET_DAEMON = OK_GATEWAY_RESET_DAEMON - 1
		try:
			YOUROPTION3 = sys.argv[4]
			OK_WRITE_ONE_SHOT = OK_WRITE_ONE_SHOT + 1
			OK_GATEWAY_RESET_DAEMON = OK_GATEWAY_RESET_DAEMON + 1
			if OK_BRIDGE == 2:
				OK_BRIDGE = OK_BRIDGE + 1
		except:
			YOUROPTION3 = "null"
			OK_WRITE_ONE_SHOT = OK_WRITE_ONE_SHOT - 1
			OK_GATEWAY_RESET_DAEMON = OK_GATEWAY_RESET_DAEMON - 1
		try:
			YOUROPTION4 = sys.argv[5]
			OK_WRITE_ONE_SHOT = OK_WRITE_ONE_SHOT + 1
		except:
			YOUROPTION4 = "null"
			OK_WRITE_ONE_SHOT = OK_WRITE_ONE_SHOT - 1
		try:
			YOUROPTION5 = sys.argv[6]
		except:
			YOUROPTION5 = "null"
		#
		# PULL IN SPECIFIED (NON GLOBAL) PRESETS
		def pull_in_preset():
			# DECLARE GLOBAL VARS
			global GROUP_SOURCE, VERBOSE, COMMENTENABLE, YOURCOMMAND1, YOURLEAFERS2, YOURGROUP, YOURBRIDGELENGTH, YOURSQLCOLUMNCOUNT, YOUROPTION1, YOUROPTION2, YOUROPTION3, YOUROPTION4, YOUROPCSERVER, YOURSQLSERVER, YOURSQLTABLE, YOURSQLCOMMENTTABLE, YOURSQLFILLERCOUNT, YOURSQLCOLUMNDATESTAMP, YOURSQLCOLUMNLEAFNAME, YOURDAEMON, YOURLEAFERS, YOURBRIDGE, YOURSPACEBRIDGE, YOURFORGEDMACHINENAMES, YOURGATEWAY
			if YOURCOMMAND1 != 'TEST_FOR_ECHO':
				if YOURCOMMAND1 != 'SERVER_SEEK':
					if YOURCOMMAND1 != 'MAINT_DB':
						if YOURCOMMAND1 != 'WRITE_ONE_SHOT':
							# PULL IN NORMALLY
							if YOURCOMMAND1 == 'WRITE':
								pre_presetfile = os.path.join(PROGPATH_PRE, YOUROPTION1) + ".wrt"
							else:
								if YOURCOMMAND1 == 'WRITE_DAEMON':
									pre_presetfile = os.path.join(PROGPATH_PRE, YOUROPTION1) + ".wdm"
								else:
									if YOURCOMMAND1 == 'READ_DAEMON':
										pre_presetfile = os.path.join(PROGPATH_PRE, YOUROPTION1) + ".rdm"
									else:
										if YOURCOMMAND1 == 'BRIDGE':					
											pre_presetfile = os.path.join(PROGPATH_PRE, YOUROPTION1) + ".brg"
										else:
											if YOURCOMMAND1 == 'SPACE_BRIDGE':
												pre_presetfile = os.path.join(PROGPATH_PRE, YOUROPTION1) + ".sbrg"
											else:
												pre_presetfile = os.path.join(PROGPATH_PRE, YOUROPTION1) + ".pre"
							if VERBOSE == 'NO':
								print ""
								print "NOTICE! -- YOUR PRE_PRESETFILE IS..."
								print pre_presetfile
							pre_presetfile = open(pre_presetfile,"r")
							if VERBOSE == 'NO': 
								print "-- opened."
							config.add_section("your_server")
							if VERBOSE == 'NO':
								print "-- -- added section 'your_server'."
							if YOURCOMMAND1 == 'WRITE':
								config.add_section("your_write")
								if VERBOSE == 'NO':
									print "-- -- added section 'your_write'."
							else:
								if YOURCOMMAND1 == 'WRITE_DAEMON':
									config.add_section("your_daemon")
									if VERBOSE == 'NO':
										print "-- -- added section 'your_daemon'."
								else:
									if YOURCOMMAND1 == 'READ_DAEMON':
										config.add_section("your_daemon")
										if VERBOSE == 'NO':
											print "-- -- added section 'your_daemon'."
									else:
										if YOURCOMMAND1 == 'BRIDGE':
											config.add_section("your_bridge")
											if VERBOSE == 'NO':
												print "-- -- added section 'your_bridge'."
										else:
											if YOURCOMMAND1 == 'SPACE_BRIDGE':
												config.add_section("your_bridge")
												if VERBOSE == 'NO':
													print "-- -- added section 'your_bridge'."
											else:
												config.add_section("your_read")
												if VERBOSE == 'NO':
													print "-- -- added section 'your_read'."
							# -- READ FROM THE RUN PRESET FILE
							config.readfp(pre_presetfile)
							if VERBOSE == 'NO':
								print "-- reading."
							# -- ASSIGN VARS BASED ON THE RUN PRESET FILE
							YOUROPCSERVER = config.get("your_server","YOUROPCSERVER")
							YOURSQLSERVER = config.get("your_server","YOURSQLSERVER")
							if VERBOSE == 'NO':
								print "-- -- read section 'your_server'."
							if YOURCOMMAND1 == 'WRITE':
								YOURLEAFERS = config.get("your_write","YOURLEAFERS")
								if VERBOSE == 'NO':
									print "-- -- read section 'your_write'."
								# RETURN THE VARS
								return YOUROPCSERVER, YOURSQLSERVER, YOURLEAFERS
							else:
								if YOURCOMMAND1 == 'WRITE_DAEMON':
									YOURDAEMON = config.get("your_daemon","YOURDAEMON")
									YOURDAEMON = os.path.join(PROGPATH_GWCOMM, YOURDAEMON)
									if VERBOSE == 'NO':
										print "-- -- read section 'your_daemon'."
									# RETURN THE VARS
									return YOUROPCSERVER, YOURSQLSERVER, YOURDAEMON
								else:
									if YOURCOMMAND1 == 'READ_DAEMON':
										YOURDAEMON = config.get("your_daemon","YOURDAEMON")
										YOURDAEMON = os.path.join(PROGPATH_GWCOMM, YOURDAEMON)
										if VERBOSE == 'NO':
											print "-- -- read section 'your_daemon'."
										# RETURN THE VARS
										return YOUROPCSERVER, YOURSQLSERVER, YOURDAEMON
									else:
										if YOURCOMMAND1 == 'BRIDGE':
											GROUP_SOURCE = config.get("your_server","DATA_SOURCE")
											YOURLEAFERS = config.get("your_bridge","YOURLEAFERS")
											YOURLEAFERS2 = config.get("your_bridge","YOURLEAFERS2")
											YOURBRIDGELENGTH = config.get("your_bridge","YOURBRIDGELENGTH")
											if VERBOSE == 'NO':
												print "-- -- read section 'your_bridge'."
											# RETURN THE VARS
											return GROUP_SOURCE, YOUROPCSERVER, YOURSQLSERVER, YOURLEAFERS, YOURLEAFERS2, YOURBRIDGELENGTH
										else:
											if YOURCOMMAND1 == 'SPACE_BRIDGE':
												YOURSPACEBRIDGE = config.get("your_server","YOURSPACEBRIDGE")
												GROUP_SOURCE = config.get("your_server","DATA_SOURCE")
												YOURLEAFERS = config.get("your_bridge","YOURLEAFERS")
												YOURLEAFERS2 = config.get("your_bridge","YOURLEAFERS2")
												YOURBRIDGELENGTH = config.get("your_bridge","YOURBRIDGELENGTH")
												if VERBOSE == 'NO':
													print "-- -- read section 'your_bridge'."
												# RETURN THE VARS
												return GROUP_SOURCE, YOUROPCSERVER, YOURSQLSERVER, YOURLEAFERS, YOURLEAFERS2, YOURBRIDGELENGTH, YOURSPACEBRIDGE
											else:
												YOURSQLTABLE = config.get("your_server","YOURSQLTABLE")
												COMMENTENABLE = config.get("your_server","COMMENTENABLE")
												GROUP_SOURCE = config.get("your_server","DATA_SOURCE")
												YOURSQLCOMMENTTABLE = config.get("your_server","YOURSQLCOMMENTTABLE")
												YOURSQLFILLERCOUNT = config.get("your_server","YOURSQLFILLERCOUNT")
												YOURSQLCOLUMNCOUNT = config.get("your_server","YOURSQLCOLUMNCOUNT")
												YOURLEAFERS = config.get("your_read","YOURLEAFERS")
												# FOR READ - ONLY
												if (YOURCOMMAND1 == 'READ'):
													try:
														YOURFORGEDMACHINENAMES = config.get("your_read","YOURFORGEDMACHINENAMES")
													except:
														# this exception allows compatability with legacy
														# READ preset files written before March 2014.
														YOURFORGEDMACHINENAMES = "NONE"
													# FOR READ - UPDATE ONLY
													if (YOUROPTION3 == 'UPDATE'):
														YOURSQLCOLUMNDATESTAMP = config.get("your_server","YOURSQLCOLUMNDATESTAMP")
														YOURSQLCOLUMNLEAFNAME = config.get("your_server","YOURSQLCOLUMNLEAFNAME")
													else:
														pass
												else:
													pass
												if VERBOSE == 'NO':
													print "-- -- read section 'your_read'."
												# RETURN THE VARS
												if (YOURCOMMAND1 == 'READ'):
													if (YOUROPTION3 == 'UPDATE'):
														return GROUP_SOURCE, COMMENTENABLE, YOURSQLCOMMENTTABLE, YOUROPCSERVER, YOURSQLCOLUMNCOUNT, YOURSQLSERVER, YOURSQLTABLE, YOURSQLFILLERCOUNT, YOURLEAFERS, YOURSQLCOLUMNDATESTAMP, YOURSQLCOLUMNLEAFNAME, YOURFORGEDMACHINENAMES
													else:
														return GROUP_SOURCE, COMMENTENABLE, YOURSQLCOMMENTTABLE, YOUROPCSERVER, YOURSQLCOLUMNCOUNT, YOURSQLSERVER, YOURSQLTABLE, YOURSQLFILLERCOUNT, YOURLEAFERS, YOURFORGEDMACHINENAMES
												else:
													return GROUP_SOURCE, COMMENTENABLE, YOURSQLCOMMENTTABLE, YOUROPCSERVER, YOURSQLCOLUMNCOUNT, YOURSQLSERVER, YOURSQLTABLE, YOURSQLFILLERCOUNT, YOURLEAFERS
							if VERBOSE == 'NO':
								print "-- variables imported successfully."
						else:
							# IF YOURCOMMAND1 IS WRITE_ONE_SHOT USE CLI ARGS TO SUBSTITUTE
							if VERBOSE == 'NO':
								print ""
								print "NOTICE! -- USING CLI ARGUMENT OVERRIDES..." 
								print "-- -- YOUR LEAVES ARE..."
							YOURLEAFERS = YOUROPTION1
							if VERBOSE == 'NO':
								print YOURLEAFERS
								print "-- -- YOUR OPC SERVER IS..."
							YOUROPCSERVER = YOUROPTION3
							if VERBOSE == 'NO':
								print YOUROPCSERVER
								print "-- -- YOUR SQL SERVER IS..."
							YOURSQLSERVER = YOUROPTION4
							if VERBOSE == 'NO':
								print YOURSQLSERVER
							# RETURN THE VARS
							return YOUROPCSERVER, YOURSQLSERVER, YOURLEAFERS
							if VERBOSE == 'NO':
								print "-- variables imported successfully."
						pre_presetfile.close()
					else:
						# IF YOURCOMMAND1 IS MAINT_DB	
						if VERBOSE == 'NO':
							print ""
							print "NOTICE! -- USING CLI ARGUMENT OVERRIDES..."
							print "-- YOUR WORKING SQL SERVER IS..." 
						YOURSQLSERVER = YOUROPTION1
						# RETURN THE VARS
						return YOURSQLSERVER
				else:
					# IF YOUR COMMAND IS SERVER_SEEK
					print ""
					print "NOTICE! -- USING CLI ARGUMENT OVERRIDES..."
					print "-- YOUR GATEWAY THROUGH WHICH TO SEEK IS..."
					YOURGATEWAY = YOUROPTION1
					print YOURGATEWAY
					# RETURN THE VARS
					return YOURGATEWAY
			else:
				# IF YOURCOMMAND1 IS TEST_FOR_ECHO
				print ""
				print "NOTICE! -- USING CLI ARGUMENT OVERRIDES..."
				print "-- YOUR TESTED OPC SERVER IS..." 
				YOUROPCSERVER = YOUROPTION1
				print YOUROPCSERVER
				# RETURN THE VARS
				return YOUROPCSERVER
		# OPC SERVER OPTIONS
		def pull_in_opc():
			# DECLARE GLOBAL VARS
			global VERBOSE, YOUROPCSERVER, OPC_DEVICENAME_START_TRIM, OPC_DEVICENAME_END_TRIM, SERVER_RESTART_WITH_GATEWAY, SERVER_START_CMD_LINE_INPUT, SERVER_STOP_CMD_LINE_INPUT, IP_OF_GATEWAY_FOR_SERVER, OPC_SERVER_NAME, OPC_SERVER_TEST, OPC_MINIMUM_SCAN_INTERVAL
			# PULL OPC SERVER OPTIONS
			opc_presetfile = os.path.join(PROGPATH_OPC, YOUROPCSERVER) + ".opc"
			if VERBOSE == 'NO':
				print ""
				print "NOTICE! -- YOUR OPC_PRESETFILE IS..."
				print opc_presetfile
			opc_presetfile = open(opc_presetfile,"r")
			if VERBOSE == 'NO':
				print "-- opened."
			config.add_section("opc_server_configs")
			if VERBOSE == 'NO':
				print "-- -- added section 'opc_server_configs'."
			# -- READ FROM THE OPC SERVER OPTIONS FILE
			config.readfp(opc_presetfile)
			if VERBOSE == 'NO':
				print "-- reading."
			# -- ASSIGN VARS BASED ON THE OPC SERVER OPTIONS FILE
			IP_OF_GATEWAY_FOR_SERVER = config.get("opc_server_configs","IP_OF_GATEWAY_FOR_SERVER")
			OPC_SERVER_NAME = config.get("opc_server_configs","SERVER_NAME")
			OPC_SERVER_TEST = config.get("opc_server_configs","SERVER_TEST")
			OPC_MINIMUM_SCAN_INTERVAL = config.get("opc_server_configs","MINIMUM_SCAN_INTERVAL")
			OPC_DEVICENAME_START_TRIM = config.get("opc_server_configs","OPC_DEVICENAME_START_TRIM")
			OPC_DEVICENAME_END_TRIM = config.get("opc_server_configs","OPC_DEVICENAME_END_TRIM")
			SERVER_STOP_CMD_LINE_INPUT = config.get("opc_server_configs","SERVER_STOP_CMD_LINE_INPUT")
			SERVER_START_CMD_LINE_INPUT = config.get("opc_server_configs","SERVER_START_CMD_LINE_INPUT")
			SERVER_RESTART_WITH_GATEWAY = config.get("opc_server_configs","SERVER_RESTART_WITH_GATEWAY")
			if VERBOSE == 'NO':
				print "-- -- read section 'opc_server_configs'."
			OPC_MINIMUM_SCAN_INTERVAL = int(OPC_MINIMUM_SCAN_INTERVAL)
			OPC_DEVICENAME_START_TRIM = int(OPC_DEVICENAME_START_TRIM)
			OPC_DEVICENAME_END_TRIM = int(OPC_DEVICENAME_END_TRIM)
			if VERBOSE == 'NO':
				print "-- -- manipulated vars as needed."
			# RETURN THE VARS
			return SERVER_RESTART_WITH_GATEWAY, SERVER_START_CMD_LINE_INPUT, SERVER_STOP_CMD_LINE_INPUT, IP_OF_GATEWAY_FOR_SERVER, OPC_DEVICENAME_START_TRIM, OPC_DEVICENAME_END_TRIM, OPC_SERVER_NAME, OPC_SERVER_TEST, OPC_MINIMUM_SCAN_INTERVAL
			if VERBOSE == 'NO':
				print "-- variables imported successfully."
			opc_presetfile.close()
		# RESET STATE CALLS TO TEST
		# -- READ DAEMON AND WRITE DAEMON TYPE SUBROUTINES
		def pull_in_reset_CHECK_READ_AND_WRITE_DAEMON_TYPE_ROUTINES():
			global RESET_STATE, YOURDAEMON
			if RESET_STATE == "RERUN":
				RESET_STATE = "RUN"
				time.sleep(5)
				print ""
				print "NOTICE! -- WAITING for EVENT INPUT..."
				print YOURDAEMON
			pull_in_reset()
			if RESET_STATE == "RERUN":
				RESET_STATE = "RUN"
				time.sleep(5)
				print ""
				print "NOTICE! -- WAITING for EVENT INPUT..."
				print YOURDAEMON
			return RESET_STATE
		# -- READ AND BRIDGE TYPE SUBROUTINES
		def pull_in_reset_CHECK_READ_AND_BRIDGE_TYPE_ROUTINES():
			global RESET_STATE, voodoo_again
			# THIS FUNCTION WAS CALLED FOR A REASON, EITHER INITIAL CHECK
			# OR CYCLICAL WAIT TIME CHECK, LET US HANDLE BOTH CASES
			voodoo_again_short_nap = voodoo_again
			voodoo_again_short_nap_pending = voodoo_again_short_nap
			if RESET_STATE == 'RUN':
				voodoo2 = timeit.Timer('pull_in_reset()', 'from __main__ import pull_in_reset')
				witching_time2 = int(round(voodoo2.timeit(number=1), 0))
				if witching_time2 < 0:
					witching_time2 = 0
				voodoo_again_short_nap_pending = voodoo_again_short_nap_pending - witching_time2
			if RESET_STATE == "RERUN":
				voodoo2 = timeit.Timer('mod_openopc_group()', 'from __main__ import mod_openopc_group')
				RESET_STATE = "RUN"
				witching_time2 = int(round(voodoo2.timeit(number=1), 0))
				if witching_time2 < 0:
					witching_time2 = 0
				voodoo_again_short_nap_pending = voodoo_again_short_nap_pending - witching_time2
			while voodoo_again_short_nap > 5:
				print "voodoo - " + str(voodoo_again_short_nap)
				if RESET_STATE == 'RUN':
					voodoo2 = timeit.Timer('pull_in_reset()', 'from __main__ import pull_in_reset')
					witching_time2 = int(round(voodoo2.timeit(number=1), 0))
					if witching_time2 < 0:
						witching_time2 = 0
					voodoo_again_short_nap_pending = voodoo_again_short_nap_pending - witching_time2
				if RESET_STATE == "RERUN":
					voodoo2 = timeit.Timer('mod_openopc_group()', 'from __main__ import mod_openopc_group')
					RESET_STATE = "RUN"
					witching_time2 = int(round(voodoo2.timeit(number=1), 0))
					if witching_time2 < 0:
						witching_time2 = 0
					voodoo_again_short_nap_pending = voodoo_again_short_nap_pending - witching_time2
				time.sleep(5)
				voodoo_again_short_nap_pending = voodoo_again_short_nap_pending - 5
				voodoo_again_short_nap = voodoo_again_short_nap_pending
			if voodoo_again_short_nap > 0:
				print "voodoo - " + str(voodoo_again_short_nap)
				time.sleep(voodoo_again_short_nap)
			return RESET_STATE
		# RESET STATE TEST
		def pull_in_reset():
			global reset_statefile_added, THREADNAME, PROGPATH_RESET, IP_OF_GATEWAY_FOR_SERVER, RESET_STATE	
			# PULL IN RESET OPTIONS
			reset_statefile = os.path.join(PROGPATH_RESET, IP_OF_GATEWAY_FOR_SERVER) + ".state"
			try:
				reset_statefile = open(reset_statefile,"r")
				if reset_statefile_added != 1:
					config.add_section("reset_state")
					reset_statefile_added = 1
				config.readfp(reset_statefile)
				# -- ASSIGN VARS BASED ON THE RESET STATE OPTIONS FILE
				RESET_STATE = config.get("reset_state","RESET_STATE")
			except:
				RESET_STATE = "RUN"
			try:
				reset_statefile.close()
			except:
				pass
			if RESET_STATE != "RUN":
				try:	
					opc.remove(THREADNAME)
					print ""
					print "THREAD KILLED"
				except:		
					print ""
					print "THREAD DEAD OR DID NOT EXIST"
				try:
					opc.close()
				except:
					pass
				print ""
				print "SCHEDULED RESET IN PROGRESS..."
				# CHECK IF THE SERVER IS BACK UP
				RESET_STATE_CHECK = "GATEWAY_RESETTING"
				while RESET_STATE_CHECK != 'RUN':
					# RE-READ THE STATE FILE
					try:
						reset_statefile = os.path.join(PROGPATH_RESET, IP_OF_GATEWAY_FOR_SERVER) + ".state"
						reset_statefile = open(reset_statefile,"r")
						if reset_statefile_added != 1:
							config.add_section("reset_state")
							reset_statefile_added = 1
						config.readfp(reset_statefile)
						# -- ASSIGN VARS BASED ON THE RESET STATE OPTIONS FILE
						RESET_STATE_CHECK_PENDING = config.get("reset_state","RESET_STATE")
						reset_statefile.close()
						RESET_STATE_CHECK = RESET_STATE_CHECK_PENDING
					except:
						pass
					if RESET_STATE_CHECK != 'RUN':
						time.sleep(5)
				try:
					print ""
					print "RECONNECTING..."
					# ANTI-RECONNECT-CHATTER DELAY
					time_to_sleep = random.randrange(5,15)
					time.sleep(time_to_sleep)
					fire_up_gw()
					fire_up_opc()
					print "-- connected successfully."
					RESET_STATE = "RERUN"
				except:
					print ""
					print "FAILED to RECONNECT."
					RESET_STATE = "DOWN"
			# RETURN THE VARS
			return reset_statefile_added, RESET_STATE
		# SQL SERVER OPTIONS
		def pull_in_sql():
			# DECLARE GLOBAL VARS
			global VERBOSE, SQL_MAINTTABLES, COMMITTRANSACTIONS, COMMENTENABLE, SQL_COMMENT_TABLE, YOURSQLCOMMENTTABLE, YOURCOMMAND1, YOURSQLSERVER, YOURSQLTABLE, SQL_IP, SQL_DB, SQL_TABLE, SQL_TABLE_FLATFILE_CHECK, SQL_FAULT, SQL_FAULTTABLE, SQL_USER, SQL_PASS, SQL_RETENTION, SQL_RETENTIONFIELD
			# PULL SQL SERVER OPTIONS
			sql_presetfile = os.path.join(PROGPATH_SQL, YOURSQLSERVER) + ".sql"
			if VERBOSE == 'NO':
				print ""
				print "NOTICE! -- YOUR SQL_PRESETFILE IS..."
				print sql_presetfile
			sql_presetfile = open(sql_presetfile,"r")
			if VERBOSE == 'NO':
				print "-- opened."
			config.add_section("sql_server_configs")
			if VERBOSE == 'NO':
				print "-- -- adding section 'sql_server_configs'."
			# -- READ FROM THE SQL SERVER OPTIONS FILE
			config.readfp(sql_presetfile)
			if VERBOSE == 'NO':
				print "-- reading."
			# -- ASSIGN VARS BASED ON THE SQL SERVER OPTIONS FILE
			SQL_DB = config.get("sql_server_configs","MYSQLDB")
			if YOURCOMMAND1 != 'MAINT_DB':
				if YOURCOMMAND1 != 'WRITE_ONE_SHOT':
					if YOURCOMMAND1 != 'WRITE':
							if YOURCOMMAND1 != 'WRITE_DAEMON':
								if YOURCOMMAND1 != 'READ_DAEMON':
									if YOURCOMMAND1 != 'BRIDGE':
										if YOURCOMMAND1 != 'SPACE_BRIDGE':
											SQL_TABLE = YOURSQLTABLE
											SQL_TABLE_FLATFILE_CHECK = SQL_TABLE[-4:]
											if VERBOSE == "YES":
												print ""
												print "FLATFILE CHECK RESULT 1... " + SQL_TABLE_FLATFILE_CHECK
											if SQL_TABLE_FLATFILE_CHECK == '.log':
												SQL_TABLE_FLATFILE_CHECK = int(1)
											else:
												SQL_TABLE_FLATFILE_CHECK = int(0)
											if VERBOSE == "YES":
												print ""
												print "FLATFILE CHECK RESULT 2... " + str(SQL_TABLE_FLATFILE_CHECK)
											if COMMENTENABLE == "yes":
												SQL_COMMENT_TABLE = YOURSQLCOMMENTTABLE
											else:
												SQL_COMMENT_TABLE = 'NULL'
										else:
											SQL_TABLE = 'NULL'
											SQL_COMMENT_TABLE = 'NULL'
											SQL_TABLE_FLATFILE_CHECK = int(0)
									else:
										SQL_TABLE = 'NULL'
										SQL_COMMENT_TABLE = 'NULL'
										SQL_TABLE_FLATFILE_CHECK = int(0)
								else:
									SQL_TABLE = 'NULL'
									SQL_COMMENT_TABLE = 'NULL'
									SQL_TABLE_FLATFILE_CHECK = int(0)
							else:
								SQL_TABLE = 'NULL'
								SQL_COMMENT_TABLE = 'NULL'
								SQL_TABLE_FLATFILE_CHECK = int(0)
					else:
						SQL_TABLE = 'NULL'
						SQL_COMMENT_TABLE = 'NULL'
						SQL_TABLE_FLATFILE_CHECK = int(0)
				else:
					SQL_TABLE = 'NULL'
					SQL_COMMENT_TABLE = 'NULL'
					SQL_TABLE_FLATFILE_CHECK = int(0)
			else:
				SQL_TABLE = 'NULL'
				SQL_COMMENT_TABLE = 'NULL'
				SQL_TABLE_FLATFILE_CHECK = int(0)
			SQL_IP = config.get("sql_server_configs","MYSQLIP")
			SQL_FAULT = config.get("sql_server_configs","MYSQLFAULT")
			SQL_FAULTTABLE = config.get("sql_server_configs","FAULTTABLENAME")
			SQL_USER = config.get("sql_server_configs","MYSQLUSER")
			SQL_PASS = config.get("sql_server_configs","MYSQLPASS")
			COMMITTRANSACTIONS = config.get("sql_server_configs","COMMITTRANSACTIONS")
			SQL_RETENTION = config.get("sql_server_configs","MYSQLRETENTION")
			SQL_RETENTIONFIELD = config.get("sql_server_configs","FIELDRETENTION")
			SQL_MAINTTABLES = config.get("sql_server_configs","MYSQLMAINTTABLES")
			SQL_MAINTTABLES = SQL_MAINTTABLES.split('|')
			if VERBOSE == 'NO':
				print "-- -- read section 'sql_server_configs'."
			# RETURN THE VARS
			return SQL_MAINTTABLES, SQL_DB, SQL_IP, SQL_TABLE, SQL_TABLE_FLATFILE_CHECK, SQL_COMMENT_TABLE, SQL_FAULT, SQL_FAULTTABLE, SQL_USER, SQL_PASS, SQL_RETENTION, SQL_RETENTIONFIELD
			if VERBOSE == 'NO':
				print "-- variables imported successfully."
			sql_presetfile.close()
		#
		# FIRE UP CONNECTIONS
		# -- SQL CONNECT
		def fire_up_sql():
			# DECLARE GLOBAL VARS
			global SQL_USER, SQL_PASS, SQL_DB, SQL_FAULT, SQL_FAULTTABLE, sql_connect, sql_cursor, sql_connect_FAULT, sql_cursor_FAULT, SQL_IP
			sql_connect = MySQLdb.connect (host=SQL_IP, user=SQL_USER, passwd=SQL_PASS, db=SQL_DB)
			sql_cursor = sql_connect.cursor ()
			sql_connect_FAULT = MySQLdb.connect (host=SQL_IP, user=SQL_USER, passwd=SQL_PASS, db=SQL_FAULT)
			sql_cursor_FAULT = sql_connect_FAULT.cursor ()
			# RETURN ARGS
			return sql_connect, sql_cursor, sql_connect_FAULT, sql_cursor_FAULT
		# -- SQL REFRESH
		# -- -- DEPRECATES AND REPLACES SQL KEEPALIVE INSTRUCTIONS
		def fire_up_sql_refresh():
			# DECLARE GLOBAL VARS
			global sql_connect, sql_cursor, sql_connect_FAULT, sql_cursor_FAULT
			# BREAK CURRENT SQL CONNECTION
			try:
				# GRACEFULLY
				sql_cursor.close ()
				sql_connect.close ()
				sql_cursor_FAULT.close ()
				sql_connect_FAULT.close ()
			except:
				# HARD IF GRACEFUL FAILS
				sql_connect = ''
				sql_cursor = ''
				sql_connect_FAULT = ''
				sql_cursor_FAULT = ''
			# REESTABLISH CONNECTION
			sql_refreshed = 0
			sql_refresh_attempt_count = 0
			while (sql_refreshed == 0) and (sql_refresh_attempt_count < 3):
				try:
					fire_up_sql()
					sql_refreshed = 1
				except:
					sql_refresh_attempt_count = sql_refresh_attempt_count + 1
			if sql_refreshed != 1:
				exit()
			else:
				pass
			# RETURN ARGS
			return sql_connect, sql_cursor, sql_connect_FAULT, sql_cursor_FAULT
		# -- OPC GW CONNECT
		def fire_up_gw():
			# DECLARE GLOBAL VARS
			global OPENOPC_TIE_IN, IP_OF_GATEWAY_FOR_SERVER, opc
			# THIS IS ABSOLUTELY CRITICAL.  DIRECT CONNECT WIN32 HOSTS MAY USE
			# THE 'DIRECT' OPTION (WITH VARYING LEVELS OF SUCCESS)
			# GATEWAY or PROXY CONNECT UNIX, LINUX, BSD, OR OTHER HOSTS SHOULD
			# MAKE USE OF THE 'GATEWAY' OPTION.  IF YOU GET THIS WRONG, NOTHING
			# WILL JIVE.  THIS PARAMETER IS SET IN THE GLOBAL OPTIONS FILE.
			# SEE THE README DOCUMENTATION FOR HELP.
			print ""
			print "CONNECTING TO GATEWAY..."
			if OPENOPC_TIE_IN == 'DIRECT':
				# IF DIRECT CONNECT
				opc = mod_openopc_library.client()
				print "-- connection to GATEWAY succcessful!"
			else:
				# IF GATEWAY CONNECT
				opc = mod_openopc_library.open_client(host=IP_OF_GATEWAY_FOR_SERVER, port=OPENOPCGATEWAYSOCKET)
				print "-- connection to GATEWAY succcessful!"	
			# RETURN ARGS
			return opc
		# -- OPC SERVER CONNECT
		def fire_up_opc():
			# DECLARE GLOBAL VARS
			global OPC_SERVER_NAME, opc
			print ""
			print "YOUR OPC SERVER IS..."
			print OPC_SERVER_NAME
			opc.connect(OPC_SERVER_NAME)
			print "-- connection to OPC SERVER successful!"
			print ""
			# WAIT A MOMENT PREVENTS NON VALUE READS
			time.sleep(5)
		#
		# SQL DB QUERY FUNCTIONS
		# -- EXECUTE QUERY
		def execute_sql_query(log_fault = 'no'):
			# DECLARE GLOBAL VARS
			global sql_query, sql_connect, sql_cursor, sql_connect_FAULT, sql_cursor_FAULT, COMMITTRANSACTIONS
			# EXECUTE
			sql_query = str(sql_query)
			if log_fault == 'yes':
				sql_cursor_FAULT.execute (sql_query)
				# COMMIT QUERY TO DB
				# -- PATCH FOR InnoDB ENGINE (and future MyISAM Engine)
				if COMMITTRANSACTIONS == "YES":
					try:
						# PUNCH THE CHANGE IN
						sql_connect_FAULT.commit()
					except:
						# REVERT
						sql_connect_FAULT.rollback()
			else:
				sql_cursor.execute (sql_query)
				# COMMIT QUERY TO DB
				# -- PATCH FOR InnoDB ENGINE (and future MyISAM Engine)
				if COMMITTRANSACTIONS == "YES":
					try:
						# PUNCH THE CHANGE IN
						sql_connect.commit()
					except:
						# REVERT
						sql_connect.rollback()
			return sql_query, sql_cursor, sql_connect, sql_cursor_FAULT, sql_connect_FAULT
		#
		# MOD OPENOPC NATIVE FUNCTIONS
		# -- READ
		# -- -- GROUP BASED, VERY EFFICIENT
		def mod_openopc_read():
			# DECLARE GLOBAL VARS
			global GROUP_SOURCE, COMMENTENABLE, OPC_DEVICENAME_START_TRIM, OPC_DEVICENAME_END_TRIM, SQL_COMMENT_TABLE, YOURSQLCOLUMNCOUNT, THREADNAME, time, mod_openopc_fault_unk, datestamp, YOURSQLFILLERCOUNT, YOURLEAFERS, opc, sql_query, sql_cursor, SQL_TABLE, SQL_TABLE_FLATFILE_CHECK, YOUROPTION3, save_value_ack_ok_PROOF, YOURSQLCOLUMNLEAFNAME, YOURSQLCOLUMNDATESTAMP, YOURFORGEDMACHINENAMES
			# GENERATE A DATESTAMP
			stamp_date()
			datestamp = datestamp
			#
			# DEFINE DELINEATION
			splitter = str(',')
			linesplitter = str(';')
			# RESET THE VALUE HOLDING TAG
			value_y = ''
			value_final = ''
			save_value = '1'
			#
			# PARSE OUT LEAF LINES (SETS)
			leaflines = YOURLEAFERS.count('|')
			leaflinearray = YOURLEAFERS.split('|')
			forgednames = YOURFORGEDMACHINENAMES.split('|')
			#
			# RESET COUNTERS
			leaf_int = 0
			leaf_i = 1
			#
			leafline_int = 0
			leafline_i = 1
			#
			# DEAL WITH ANY FILLER COLUMNS YOU MAY BE USING
			YOURSQLFILLERCOUNT_USE = int(YOURSQLFILLERCOUNT)
			if YOURSQLFILLERCOUNT_USE == 0:
				end_of_row_filler = '';
			else:
				filler_cnt = 0
				end_of_row_filler = ''
				# DEAL WITH COMMENT COLUMNS AS THEY'RE INCLUDED IN THE
				# FILLER COLUMN COUNT
				if COMMENTENABLE == "yes":
					YOURSQLFILLERCOUNT_USE = YOURSQLFILLERCOUNT_USE - 1
				while filler_cnt < YOURSQLFILLERCOUNT_USE:
					end_of_row_filler = end_of_row_filler + splitter + "NULL"
					filler_cnt = filler_cnt + 1
			# SOURCE THE READ
			try:
				updated_group = opc.read(group=THREADNAME, source=GROUP_SOURCE)
				group_test = updated_group[0]
				print ""
				print "GROUP ALREADY EXISTS"	
			except:
				opc.remove(THREADNAME)
				print ""
				print "NEW GROUP, SO LET'S BUILD IT..."
				mod_openopc_group()
				time.sleep(5)
				updated_group = opc.read(group=THREADNAME, source=GROUP_SOURCE)
			# WE NEED TO BE ABLE TO GET OUT OF THIS LOOP IF WE FAULT
			# DUE TO THE WAY WE ARE HANDLING GROUPS WE CANNOT STAY IN IT
			get_out_now = 0
			save_value_ack_ok_PROOF = 0
			#
			while leaf_int<leaflines:
				save_value = 1
				# WE WANT TO FORCE A GOOD READ
				good_read = 0
				while good_read == 0:
					if get_out_now == 0:
						try:
							# DECLARE WHAT SET OF LEAVES WE ARE ON
							leafarray = leaflinearray[leaf_int]
							if (YOURFORGEDMACHINENAMES == 'NONE'):
								leaf_sql_name_forged = "NONE"
							else:
								leaf_sql_name_forged = str(forgednames[leaf_int])
							leafarray = str(leafarray)
							# LEAVES IN LINE
							leafendofline = leafarray.count('&')
							leafendofline = leafendofline - 1
							leafarray = leafarray.split('&')
							leaf = leafarray[leafline_int]
							leaf = str(leaf)
							# WHAT TAG ARE WE ON WHERE TAGS EQUATE TO LEAVES
							tag_int = int(leaf_int) * int(YOURSQLCOLUMNCOUNT)
							tag_int = tag_int + leafline_int
							tag = updated_group[tag_int]
							# NOTE THE FOLLOWING IS A WAY TO CHOP AND PARSE OUR
							# TAGS, WHERE A TAG IS A COMBINATION OF THE 'XXX'
							# START PLACEHOLDER, 'DEVICE' YOUR TALKING TO, 'YYY'
							# END PLACEHOLDER, AND THE 'TAG' ITSELF.
							# EXAMPLE1... XXXDEVICEYYYTAG 
							# EXAMPLE2... XXX[MYPLC1]YYYN7:10 (RSLinx)
							# EXAMPLE3... XXXCHANNEL1.MYPLC1YYYN7:10 (Kepware)
							leaf_sql_name = leaf.split('YYY')
							leaf_sql_name = leaf_sql_name[0]
							leaf_sql_name = str(leaf_sql_name)
							# THIS TRIM WILL GET RID OF OUR 'XXX' START
							leaf_sql_name = leaf_sql_name[3:]
							# WE DO NOT NEED TO TRIM THE 'YYY' FROM THE
							#   END BECAUSE THE 'SPLIT' ABOVE DOES THIS
							#   FOR US.
							# THIS TRIM WILL GET RID OF ANY EXTRA CHARS
							#   DEFINED IN THE OPC SERVER CONFIG FILE
							#   FROM START AND END
							if int(OPC_DEVICENAME_START_TRIM) > 0:
								leaf_sql_name = leaf_sql_name[OPC_DEVICENAME_START_TRIM:]
							else:
								pass
							if int(OPC_DEVICENAME_END_TRIM) > 0:
								leaf_sql_name = leaf_sql_name[:-OPC_DEVICENAME_END_TRIM]
							else:
								pass
							# ALLOW FORGING OF THE MACHINE NAME (leaf_sql_name)
							if (leaf_sql_name_forged == 'NONE'):
								pass
							else:
								leaf_sql_name = leaf_sql_name_forged
							# NEW STYLE READ LONG FORM WITH ATTRIBUTES
							value_leaf = tag[1]
							quality_leaf = tag[2]
							quality_leaf = str(quality_leaf)
							# CHECK IF LEAF WE PULLED IS A NUMBER OR A ASCII STRING
							# ---- quality options are... 'Good', 'Bad', and 'OK'
							if quality_leaf != "Bad":
								try:
									if VERBOSE == "YES":
										print "Numeric value incoming..."
									value_leaf = str(round(value_leaf,4))
								except:
									if VERBOSE == "YES":
										print "ASCII string incoming..."
								if VERBOSE == "YES":
									print value_leaf
								good_read = 1
							else:
								print ""
								print "-- -- YOUR TARGET DEVICE IS DOWN OR NOT RESPONDING!"
								print "-- -- DEVICE is..."
								print leaf_sql_name
								save_value = 0
								good_read = 1
						except:
							print leaf_sql_name 
							print "cannot be accessed... skipping."
							save_value = 0
							# GET OUT OF THIS LOOP NOW
							get_out_now = 1
							mod_openopc_fault_unk()
				if get_out_now != 1:
					if leafline_int == leafendofline:
						if save_value == 1:
							if SQL_TABLE_FLATFILE_CHECK == 0:
								value_y = value_y + "\'" + value_leaf + "\'"
								value_final = "\'" + datestamp + "\'" + splitter + "\'" + leaf_sql_name + "\'" + splitter + value_y
							else:
								value_y = value_y + value_leaf
								value_final = datestamp + splitter + leaf_sql_name + splitter + value_y
							if COMMENTENABLE == "yes":
								comment_query = "SELECT * FROM " + SQL_COMMENT_TABLE + " WHERE MACHINE LIKE \'" + leaf_sql_name + "\'"
								comment_query = str(comment_query)
								if VERBOSE == "YES":
	                                                        	print "Comment string incoming..."
	                                                        	print comment_query
								sql_cursor.execute (comment_query)
								value_comment = sql_cursor.fetchone()
								value_comment = value_comment[1]
								value_comment = str(value_comment)
								if VERBOSE == "YES":
		                                                        print value_comment
								if SQL_TABLE_FLATFILE_CHECK == 0:
									value_comment = "\'" + value_comment + "\'"
									value_final = value_final + splitter + value_comment + end_of_row_filler
								else:
									value_final = value_final + splitter + value_comment + linesplitter
							else:
								if SQL_TABLE_FLATFILE_CHECK == 0:
									value_final = value_final + end_of_row_filler
								else:
									value_final = value_final + linesplitter
							if YOUROPTION3 != 'ACK':
								# STANDARD ADD MODE, MAY OR MAY NOT UPDATE
								save_value_ack_ok = 1
							else:
								# ADD MODE W/ ACK
								# -- ADD NEW DATA ONLY BASED ON STATUS OF FINAL LEAFER (DATA TAG)
								# -- -- 0 = OLD DATA, DISCARD
								# -- -- 1 = NEW DATA, ADD
								try:
									# ENSURE VALUE BEING TESTED IS A NUMBER, AND DROP ANY DECIMAL PLACES
									value_leaf_ack_test = int(float(value_leaf))
								except:
									value_leaf_ack_test = 0
								if VERBOSE == "YES":
									print ""
									print "VALUE LEAF ACK TEST = " + str(value_leaf_ack_test)
								if value_leaf_ack_test == 1:
									if VERBOSE == "YES":
										print ""
										print "NEW DATA... ADDING"
									save_value_ack_ok = 1
								else:
									if VERBOSE == "YES":
										print ""
										print "OLD DATA... DISCARDING"
									save_value_ack_ok = 0
							if save_value_ack_ok == 1:
								save_value_ack_ok_PROOF = 1
								# PUSH THE ROW INTO THE DATABASE
								# -- psuedo_query_example = INSERT INTO SQL_TABLE VALUES(value_final)
								if SQL_TABLE_FLATFILE_CHECK == 0:
									sql_query = "INSERT INTO " + SQL_TABLE + " VALUES(" + value_final + ")"
								else:
									# FLATFILE VALIDATION
									YMD_STAMP = datetime.now()
									YMD_STAMP = YMD_STAMP.strftime("%Y_%m%d")
									FLATFILE_DATED = SQL_TABLE[:-4]
									FLATFILE_DATED = FLATFILE_DATED + "_" + YMD_STAMP + ".log"
									if os.path.isfile(FLATFILE_DATED):
										if VERBOSE == "YES":
											print ""
											print "FLATFILE EXISTS... " + FLATFILE_DATED
										pass
									else:
										if VERBOSE == "YES":
											print ""
											print "CREATING FLATFILE... " + FLATFILE_DATED
										FLATFILE_WORK = file(FLATFILE_DATED,'wt')
										os.chmod(FLATFILE_DATED, 0777)
								print ""
								print "NOTICE! -- EXPORTING RESULTS - FOR..." + leaf_sql_name
								if SQL_TABLE_FLATFILE_CHECK == 0:
									if VERBOSE == "YES":
										print "WE ARE USING THE FOLLOWING QUERY STRING..."
										print sql_query
									execute_sql_query()
								else:
									# FLATFILE PUSH DATA
									FLATFILE_WORK = open(FLATFILE_DATED,'at')
									FLATFILE_CONTENT = value_final + "\n"
									if VERBOSE == "YES":
										print "WE ARE APPENDING THE FOLLOWING DATA..."
										print FLATFILE_CONTENT
									FLATFILE_WORK.write(FLATFILE_CONTENT)
									FLATFILE_WORK.close()
								if YOUROPTION3 != 'UPDATE':
									# ADD MODE ACTIVE
									# -- ALLOW OLD RECORDS TO PERSIST
									pass
								else:
									if SQL_TABLE_FLATFILE_CHECK == 0:
										# UPDATE MODE ACTIVE
										# -- UPDATE MOST RECENT RECORD
										# -- psuedo_query_example = INSERT INTO SQL_TABLE VALUES(value_final)
										sql_query = "DELETE FROM " + SQL_TABLE + " WHERE ( (" + YOURSQLCOLUMNLEAFNAME + " = '" + leaf_sql_name + "') AND (" + YOURSQLCOLUMNDATESTAMP + " < '" + datestamp + "') )"
										print ""
										print "NOTICE! -- DELETING OLD RECORDS FROM YOUR SQL TABLE - FOR..." + leaf_sql_name
										if VERBOSE == "YES":
											print "WE ARE USING THE FOLLOWING QUERY STRING..."
											print sql_query
										execute_sql_query()
									else:
										print ""
										print "BAD CLI OPTION! -- LOGGING TO FLATFILE DOES NOT SUPPORT UPDATING EXISTING RECORDS."
										print "... bypassing update request."
								# END PUSH THE ROW INTO THE DATABASE
							else:
								pass
							leafline_int = 0
							leaf_int = leaf_int + leaf_i
							value_y = ''
							value_final = ''
						else:
							leafline_int = 0
							leaf_int = leaf_int + leaf_i
							value_y = ''
							value_final = ''
					else:
						if save_value == 1:
							if SQL_TABLE_FLATFILE_CHECK == 0:
								value_y = value_y + "\'" + value_leaf + "\'" + splitter
							else:
								value_y = value_y + value_leaf + splitter
							leafline_int = leafline_int + leafline_i
						else:
							leafline_int = 0
							leaf_int = leaf_int + leaf_i
							value_y = ''
							value_final = ''
				else:
					leaf_int = leaf_lines
			return save_value_ack_ok_PROOF
		# -- SPACE BRIDGE
		def mod_openopc_space_bridge():
			# DECLARE GLOBAL VARS
			global GROUP_SOURCE, OPC_DEVICENAME_START_TRIM, OPC_DEVICENAME_END_TRIM, YOURLEAFERS2, THREADNAME, time, YOURBRIDGELENGTH, mod_openopc_fault_unk, datestamp, YOURLEAFERS, YOURSPACEBRIDGE, opc
			# GENERATE A DATESTAMP
			stamp_date()
			datestamp = datestamp
			#
			# RESET THE VALUE HOLDING TAG
			save_value = '1'
			#
			# PARSE OUT LEAF LINES (SETS)
			leaflines = YOURLEAFERS2.count('|')
			leaflinearray = YOURLEAFERS2.split('|')
			#
			# RESET COUNTERS
			leaf_int = 0
			leaf_i = 1
			#
			leafline_int = 0
			leafline_i = 1
			#
			# SOURCE THE READ
			try:
				updated_group = opc.read(group=THREADNAME, source=GROUP_SOURCE)
				group_test = updated_group[0]
				print ""
				print "GROUP ALREADY EXISTS"	
			except:
				opc.remove(THREADNAME)
				print ""
				print "NEW GROUP, SO LET'S BUILD IT..."
				mod_openopc_group()
				time.sleep(5)
				updated_group = opc.read(group=THREADNAME, source=GROUP_SOURCE)
			# WE NEED TO BE ABLE TO GET OUT OF THIS LOOP IF WE FAULT
			# DUE TO THE WAY WE ARE HANDLING GROUPS WE CANNOT STAY IN IT
			get_out_now = 0
			#
			# RESET THE BRIDGE VALUE ARRAY
			bridge_value = []
			target_value = []
			# CYCLE THROUGH LEAFERS
			while leaf_int<leaflines:
				save_value = 1
				# WE WANT TO FORCE A GOOD READ
				good_bridge = 0
				while good_bridge == 0:
					if get_out_now == 0:
						# DECLARE WHAT SET OF LEAVES WE ARE ON
						leafarray = leaflinearray[leaf_int]	
						leafarray = str(leafarray)
						# LEAVES IN LINE
						leafendofline = leafarray.count('&')
						leafendofline = leafendofline - 1
						leafarray = leafarray.split('&')
						leaf = leafarray[leafline_int]
						leaf = str(leaf)
						# NOTE THE FOLLOWING IS A WAY TO 
						#   REMOVE THE START AND END XXX YYY FLAGS FROM
						#   THE VARIABLE WHICH WILL BUILD OUR WRITE ARRAY
						#   -- REMOVED!
						#   -- -- THE SPACE BRIDGE REQUIRES THAT THESE
						#   -- -- TAGS REMAIN IN PLACE FOR EXPORT TO THE
						#   -- -- DECLARED WRITE DAEMON
						#leaf_opc_write_friendly = leaf.replace('XXX', '')
						#leaf_opc_write_friendly = leaf_opc_write_friendly.replace('YYY', '')
						#    -- REPLACED WITH...
						leaf_opc_write_friendly = leaf
						# WHAT TAG ARE WE ON WHERE TAGS EQUATE TO LEAVES
						tag_int = int(leaf_int) * int(YOURBRIDGELENGTH)
						tag_int = tag_int + leafline_int
						tag = updated_group[tag_int]
						# NOTE THE FOLLOWING IS A WAY TO CHOP AND PARSE OUR
						# TAGS, WHERE A TAG IS A COMBINATION OF THE 'XXX'
						# START PLACEHOLDER, 'DEVICE' YOUR TALKING TO, 'YYY'
						# END PLACEHOLDER, AND THE 'TAG' ITSELF.
						# EXAMPLE1... XXXDEVICEYYYTAG 
						# EXAMPLE2... XXX[MYPLC1]YYYN7:10 (RSLinx)
						# EXAMPLE3... XXXCHANNEL1.MYPLC1YYYN7:10 (Kepware)
						leaf_sql_name = leaf.split('YYY')
						leaf_sql_name = leaf_sql_name[0]
						leaf_sql_name = str(leaf_sql_name)
						# THIS TRIM WILL GET RID OF OUR 'XXX' START
						leaf_sql_name = leaf_sql_name[3:]
						# WE DO NOT NEED TO TRIM THE 'YYY' FROM THE
						#   END BECAUSE THE 'SPLIT' ABOVE DOES THIS
						#   FOR US.
						# THIS TRIM WILL GET RID OF ANY EXTRA CHARS
						#   DEFINED IN THE OPC SERVER CONFIG FILE
						#   FROM START AND END
						if int(OPC_DEVICENAME_START_TRIM) > 0:
							leaf_sql_name = leaf_sql_name[OPC_DEVICENAME_START_TRIM:]
						else:
							pass
						if int(OPC_DEVICENAME_END_TRIM) > 0:
							leaf_sql_name = leaf_sql_name[:-OPC_DEVICENAME_END_TRIM]
						else:
							pass
						try:
							# NEW STYLE READ LONG FORM WITH ATTRIBUTES
							value_leaf = tag[1]
							quality_leaf = tag[2]
							quality_leaf = str(quality_leaf)
							# CHECK IF LEAF WE PULLED IS A NUMBER OR A ASCII STRING
							# ---- quality options are... 'Good', 'Bad', and 'OK'
							if quality_leaf != "Bad":
								try:
									if VERBOSE == "YES":
										print "Numeric value incoming..."
									value_leaf = str(round(value_leaf,4))
								except:
									if VERBOSE == "YES":
										print "ASCII string incoming..."
								if VERBOSE == "YES":
									print value_leaf
								bridge_value.append(value_leaf)
								target_value.append(leaf_opc_write_friendly)
								good_bridge = 1
							else:
								# WE SHOULD BE ABLE TO TELL THE USER WHICH DEVICE IS DOWN
								# EVEN IF IT IS A SOURCE DEVICE FROM A DIFFERENT ARRAY.
								# BUT, WE CAN'T, AND WE DON'T HAVE TIME TO FIX IT RIGHT NOW.
								# SO WE'LL TELL THE USER WHAT WE DO KNOW, AND FIX THE NOTIFICATION
								# SOMEDAY.
								# THE BRIDGE STILL WORKS, THIS IS JUST A PROBLEM WITH FEEDBACK.
								print ""
								print "-- -- YOUR SOURCE DEVICE IS DOWN OR NOT RESPONDING!"
								print "-- -- WE CAN'T TELL YOU WHICH SOURCE IT IS, BUT WE"
								print "-- -- CAN TELL YOU THAT IT WOULD HAVE BEEN BRIDGED"
								print "-- -- OVER TO DEVICE WITH NAME..."
								print leaf_sql_name
								save_value = 0
								good_bridge = 1
						except:
							print leaf_sql_name 
							print "cannot be accessed... skipping."
							save_value = 0
							# GET OUT OF THIS LOOP NOW
							get_out_now = 1
							mod_openopc_fault_unk()
				if get_out_now != 1:
					if leafline_int == leafendofline:
						if save_value == 1:
							leafline_int = 0
							leaf_int = leaf_int + leaf_i
						else:
							leafline_int = 0
							leaf_int = leaf_int + leaf_i
					else:
						if save_value == 1:
							leafline_int = leafline_int + leafline_i
						else:
							leafline_int = leafline_int + leafline_i
							leaf_int = leaf_int + leaf_i
				else:
					leaf_int = leaf_lines
			# BUILD THE BRIDGE VALUE FOR EXPORT TO THE TARGET
			bridge_to_write  = ''
			for identity, leaf in enumerate(target_value):
				x_target_value = str(target_value[identity])
				y_bridge_value = str(bridge_value[identity])
				xy_value = x_target_value + "&" + y_bridge_value + "&|"
				bridge_to_write = bridge_to_write + xy_value
			# NOW WRITE THE ENTIRE BRIDGE TO THE TARGET
			# ONLY WRITE IF NOT EMPTY SET...
			if save_value == 1:
				print "Exporting data to mod_openopc WRITE_DAEMON..."
				if VERBOSE == "YES":
					print bridge_to_write
				# IF INPUT IS NOT BAD THEN PUSH IT TO mod_openopc
				datestamp = datetime.now()
				datestamp = datestamp.strftime("%Y_%m%d_%H-%M-%S")
				FLATFILE = os.path.join(TEMPDIR, THREADNAME)
				# ADD RANDOM NUMBER TO PREVENT ANY POTENTIAL FILE LOCK
				FLATFILE = FLATFILE + "_" + datestamp + "_" + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + ".temp"
				print "-- built export file..."
				print FLATFILE
				FLATFILE_WORK = file(FLATFILE,'wt')
				FLATFILE_WORK = open(FLATFILE,'w')
				FLATFILE_CONTENT = "# START WRITE_DAEMON EVENT FILE FROM mod_openopc SPACE BRIDGE.\n"
				FLATFILE_CONTENT = FLATFILE_CONTENT + "[your_write_type]\n"
				FLATFILE_CONTENT = FLATFILE_CONTENT + "YOURWRITETYPE:DECLARED\n"
				FLATFILE_CONTENT = FLATFILE_CONTENT + "# -- WRITE DECLARED VALUES TO OPC TARGET\n"
				FLATFILE_CONTENT = FLATFILE_CONTENT + "[your_leafers]\n"
				FLATFILE_CONTENT = FLATFILE_CONTENT + "YOURLEAFERS:"
				FLATFILE_CONTENT = FLATFILE_CONTENT + bridge_to_write + "\n"
				FLATFILE_CONTENT = FLATFILE_CONTENT + "YOURWRITEPRESET:NONE\n"
				FLATFILE_CONTENT = FLATFILE_CONTENT + "# -- NAME OF PRESET FILE TO WRITE\n"
				FLATFILE_CONTENT = FLATFILE_CONTENT + "# END OF FILE\n"
				FLATFILE_WORK.write(FLATFILE_CONTENT)
				FLATFILE_WORK.close()
				# MOVE THE TEMP FILE TO THE DAEMON IMPORT DIRECTORY
				EXPORT = os.path.join(PROGPATH_GWCOMM, YOURSPACEBRIDGE)
				EXPORT = os.path.join(EXPORT, THREADNAME)
				EXPORT = EXPORT + "_" + datestamp + "_" + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + ".event"
				shutil.move(FLATFILE,EXPORT)
				print ""
				print "EXPORT COMPLETED..."
				print "-- handed the file off to mod_openopc..."
			else:
				print "We didn't have any data to perform a write with."
				print "-- patch for empty set writes, ignore, wait, recycle."
				print "-- if this was a legitimate fault (comm error, whatever),"
				print "-- then the 'BAD' tag from OPC comm would drop this"
				print "-- routine for full recycle."
				print "-- We'll just wait 5 seconds... and try again, but this"
				print "-- is usually an indication of a failure to communicate"
				print "-- with the SOURCE device."
				time.sleep(5)
			# END ONLY WRITE IF NOT EMPTY SET...
		# -- BRIDGE
		def mod_openopc_bridge():
			# DECLARE GLOBAL VARS
			global GROUP_SOURCE, OPC_DEVICENAME_START_TRIM, OPC_DEVICENAME_END_TRIM, YOURLEAFERS2, THREADNAME, time, YOURBRIDGELENGTH, mod_openopc_fault_unk, datestamp, YOURLEAFERS, opc
			# GENERATE A DATESTAMP
			stamp_date()
			datestamp = datestamp
			#
			# RESET THE VALUE HOLDING TAG
			save_value = '1'
			#
			# PARSE OUT LEAF LINES (SETS)
			leaflines = YOURLEAFERS2.count('|')
			leaflinearray = YOURLEAFERS2.split('|')
			#
			# RESET COUNTERS
			leaf_int = 0
			leaf_i = 1
			#
			leafline_int = 0
			leafline_i = 1
			#
			# SOURCE THE READ
			try:
				updated_group = opc.read(group=THREADNAME, source=GROUP_SOURCE)
				group_test = updated_group[0]
				print ""
				print "GROUP ALREADY EXISTS"	
			except:
				opc.remove(THREADNAME)
				print ""
				print "NEW GROUP, SO LET'S BUILD IT..."
				mod_openopc_group()
				time.sleep(5)
				updated_group = opc.read(group=THREADNAME, source=GROUP_SOURCE)
			# WE NEED TO BE ABLE TO GET OUT OF THIS LOOP IF WE FAULT
			# DUE TO THE WAY WE ARE HANDLING GROUPS WE CANNOT STAY IN IT
			get_out_now = 0
			#
			# RESET THE BRIDGE VALUE ARRAY
			bridge_value = []
			target_value = []
			# CYCLE THROUGH LEAFERS
			while leaf_int<leaflines:
				save_value = 1
				# WE WANT TO FORCE A GOOD READ
				good_bridge = 0
				while good_bridge == 0:
					if get_out_now == 0:
						# DECLARE WHAT SET OF LEAVES WE ARE ON
						leafarray = leaflinearray[leaf_int]	
						leafarray = str(leafarray)
						# LEAVES IN LINE
						leafendofline = leafarray.count('&')
						leafendofline = leafendofline - 1
						leafarray = leafarray.split('&')
						leaf = leafarray[leafline_int]
						leaf = str(leaf)
						# NOTE THE FOLLOWING IS A WAY TO 
						#   REMOVE THE START AND END XXX YYY FLAGS FROM
						#   THE VARIABLE WHICH WILL BUILD OUR WRITE ARRAY
						leaf_opc_write_friendly = leaf.replace('XXX', '')
						leaf_opc_write_friendly = leaf_opc_write_friendly.replace('YYY', '')
						# WHAT TAG ARE WE ON WHERE TAGS EQUATE TO LEAVES
						tag_int = int(leaf_int) * int(YOURBRIDGELENGTH)
						tag_int = tag_int + leafline_int
						tag = updated_group[tag_int]
						# NOTE THE FOLLOWING IS A WAY TO CHOP AND PARSE OUR
						# TAGS, WHERE A TAG IS A COMBINATION OF THE 'XXX'
						# START PLACEHOLDER, 'DEVICE' YOUR TALKING TO, 'YYY'
						# END PLACEHOLDER, AND THE 'TAG' ITSELF.
						# EXAMPLE1... XXXDEVICEYYYTAG 
						# EXAMPLE2... XXX[MYPLC1]YYYN7:10 (RSLinx)
						# EXAMPLE3... XXXCHANNEL1.MYPLC1YYYN7:10 (Kepware)
						leaf_sql_name = leaf.split('YYY')
						leaf_sql_name = leaf_sql_name[0]
						leaf_sql_name = str(leaf_sql_name)
						# THIS TRIM WILL GET RID OF OUR 'XXX' START
						leaf_sql_name = leaf_sql_name[3:]
						# WE DO NOT NEED TO TRIM THE 'YYY' FROM THE
						#   END BECAUSE THE 'SPLIT' ABOVE DOES THIS
						#   FOR US.
						# THIS TRIM WILL GET RID OF ANY EXTRA CHARS
						#   DEFINED IN THE OPC SERVER CONFIG FILE
						#   FROM START AND END
						if int(OPC_DEVICENAME_START_TRIM) > 0:
							leaf_sql_name = leaf_sql_name[OPC_DEVICENAME_START_TRIM:]
						else:
							pass
						if int(OPC_DEVICENAME_END_TRIM) > 0:
							leaf_sql_name = leaf_sql_name[:-OPC_DEVICENAME_END_TRIM]
						else:
							pass
						leaf_sql_name = str(leaf_sql_name)
						try:
							# NEW STYLE READ LONG FORM WITH ATTRIBUTES
							value_leaf = tag[1]
							quality_leaf = tag[2]
							quality_leaf = str(quality_leaf)
							# CHECK IF LEAF WE PULLED IS A NUMBER OR A ASCII STRING
							# ---- quality options are... 'Good', 'Bad', and 'OK'
							if quality_leaf != "Bad":
								try:
									if VERBOSE == "YES":
										print "Numeric value incoming..."
									value_leaf = str(round(value_leaf,4))
								except:
									if VERBOSE == "YES":
										print "ASCII string incoming..."
								if VERBOSE == "YES":
									print value_leaf
								bridge_value.append(value_leaf)
								target_value.append(leaf_opc_write_friendly)
								good_bridge = 1
							else:
								# WE SHOULD BE ABLE TO TELL THE USER WHICH DEVICE IS DOWN
								# EVEN IF IT IS A SOURCE DEVICE FROM A DIFFERENT ARRAY.
								# BUT, WE CAN'T, AND WE DON'T HAVE TIME TO FIX IT RIGHT NOW.
								# SO WE'LL TELL THE USER WHAT WE DO KNOW, AND FIX THE NOTIFICATION
								# SOME OTHER TIME.
								# THE BRIDGE STILL WORKS, THIS IS JUST A PROBLEM WITH FEEDBACK.
								print ""
								print "-- -- YOUR SOURCE DEVICE IS DOWN OR NOT RESPONDING!"
								print "-- -- WE CAN'T TELL YOU WHICH SOURCE IT IS, BUT WE"
								print "-- -- CAN TELL YOU THAT IT WOULD HAVE BEEN BRIDGED"
								print "-- -- OVER TO DEVICE WITH NAME..."
								print leaf_sql_name
								save_value = 0
								good_bridge = 1
						except:
							print leaf_sql_name 
							print "cannot be accessed... skipping."
							save_value = 0
							# GET OUT OF THIS LOOP NOW
							get_out_now = 1
							mod_openopc_fault_unk()
				if get_out_now != 1:
					if leafline_int == leafendofline:
						if save_value == 1:
							leafline_int = 0
							leaf_int = leaf_int + leaf_i
						else:
							leafline_int = 0
							leaf_int = leaf_int + leaf_i
					else:
						if save_value == 1:
							leafline_int = leafline_int + leafline_i
						else:
							leafline_int = leafline_int + leafline_i
							leaf_int = leaf_int + leaf_i
				else:
					leaf_int = leaf_lines
			# BUILD THE BRIDGE VALUE FOR EXPORT TO THE TARGET
			bridge_to_write  = []
			for identity, leaf in enumerate(target_value):
				x_target_value = target_value[identity]
				y_bridge_value = bridge_value[identity]
				xy_value = (x_target_value, y_bridge_value)
				bridge_to_write.append(xy_value)
			# NOW WRITE THE ENTIRE BRIDGE TO THE TARGET
			# ONLY WRITE IF NOT EMPTY SET...
			if save_value == 1:
				print "Writing value to target..."
				if VERBOSE == "YES":
					print bridge_to_write
				bridge_status = opc.write(bridge_to_write)
				print ""
				print "THE WRITE WAS..."
				print bridge_status
			else:
				print "We didn't have any data to perform a write with."
				print "-- patch for empty set writes, ignore, wait, recycle."
				print "-- if this was a legitimate fault (comm error, whatever),"
				print "-- then the 'BAD' tag from OPC comm would drop this"
				print "-- routine for full recycle."
				print "-- We'll just wait 5 seconds... and try again, but this"
				print "-- is usually an indication of a failure to communicate"
				print "-- with the SOURCE device."
				time.sleep(5)
			# END ONLY WRITE IF NOT EMPTY SET...
		# -- BUILD A GROUP
		def mod_openopc_group():
			# DECLARE GLOBAL VARS
			global GROUP_UPDATE, GROUP_SOURCE, YOURGROUP, YOURLEAFERS, YOURLEAFERS_NOXXX_NOYYY, THREADNAME, opc
			# DEFINE DELINEATION
			splitter = str(',')
			linesplitter = str(';')
			#
			# PARSE OUT LEAF LINES (SETS)
			leaflines = YOURLEAFERS.count('|')
			# REMOVE THE START AND END XXX YYY FLAGS FROM
			#   THE VARIABLE WHICH WILL BUILD OUR ARRAY
			YOURLEAFERS_NOXXX_NOYYY = YOURLEAFERS.replace('XXX', '')
			YOURLEAFERS_NOXXX_NOYYY = YOURLEAFERS_NOXXX_NOYYY.replace('YYY', '')
			leaflinearray = YOURLEAFERS_NOXXX_NOYYY.split('|')
			#
			# RESET COUNTERS
			leaf_int = 0
			leaf_i = 1
			#
			leafline_int = 0
			leafline_i = 1	
			#
			# RESET GROUP
			YOURGROUP = []
			# CYCLE THROUGH LEAFERS
			while leaf_int<leaflines:
				# DECLARE WHAT SET OF LEAVES WE ARE ON
				leafarray = leaflinearray[leaf_int]	
				leafarray = str(leafarray)
				# LEAVES IN LINE
				leafendofline = leafarray.count('&')
				leafendofline = leafendofline - 1
				leafarray = leafarray.split('&')
				leaf = leafarray[leafline_int]
				leaf = str(leaf)
				# ADD TO GROUP
				YOURGROUP.append(leaf)
				# INCREMENT
				if leafline_int == leafendofline:
					leafline_int = 0
					leaf_int = leaf_int + leaf_i	
				else:
					leafline_int = leafline_int + leafline_i
			# BUILD A GROUP
			if VERBOSE == "YES":
				print ""
				print "ARGUMENT TO BUILD YOUR GROUP..."
				print YOURGROUP
				print ""
			groupbuild = 0
			print ""
			print "ATTEMPTING TO BUILD GROUP..."
			while groupbuild == 0:
				try:
					groupbuild = 0
					# THE FOLLOWING TWO VALUES ARE SCALED BY 1,000 BECAUSE
					# OPENOPC and/or OPC SERVERS REGARD THEM IN MILLISECONDS (NOT SECONDS)
					openopc_group_build_timeout = GROUPBUILD_TIMEOUT_OVERRIDE * 1000
					# POLL DATA FROM DEVICE TWICE PER DATA SUBSCRIPTION PULL (SAFEGUARD)
					openopc_group_build_update = (GROUP_UPDATE * 1000) / 2
					opc.read(YOURGROUP, group=THREADNAME, source=GROUP_SOURCE, update=openopc_group_build_update, timeout=openopc_group_build_timeout)
					print "-- SUCCESS!"
					groupbuild = 1
				except:
					print "-- FAILED"
					if VERBOSE == "YES":
						print "-- usually caused by slow network"
						print "-- or bad comm.  You can lessen"
						print "-- the burden on slow networks by"
						print "-- trying to keep your presets to"
						print "-- less than 50 picks each."
						print "-- we'll try again in a few seconds,"
						print "-- and keep trying until we get it."
						print "-- Retry interval is a random number"
						print "-- of seconds between 5 and 15 to"
						print "-- help balance load."
					else:
						print "-- retry every few [random] seconds."
					groupbuild = 0
					mod_openopc_fault_group_build()
					time_to_sleep = random.randrange(5,15)
					time.sleep(time_to_sleep)
			print ""
			print "OPC GROUP IS BUILT"
			print "-- group name is..."
			print THREADNAME
			# WAIT A BIT
			time.sleep(5)
			return opc, YOURGROUP
		# -- WRITE
		# -- -- NEW STYLE, NOT PERFECT BUT MUCH MORE EFFICIENT
		# -- -- THAN THE OLDER LINEBYLINE STYLE.  WRITES A FULL 
		# -- -- GROUP AT ONCE RATHER THAN SINGLE TAGS.
		def mod_openopc_write():
			# DEFINE GLOBAL VARS
			global time, OPC_DEVICENAME_START_TRIM, OPC_DEVICENAME_END_TRIM, YOURLEAFERS, opc
			# DEFINE DELINEATION
			splitter = str(',')
			linesplitter = str(';')
			#
			# PARSE OUT LEAF LINES (SETS)
			leaflines = YOURLEAFERS.count('|')
			leaflinearray = YOURLEAFERS.split('|')
			#
			# RESET COUNTERS
			leaf_int = 0
			leaf_i = 1
			#
			leafline_int = 0
			leafline_i = 1
			#
			# WE NEED TO BE ABLE TO GET OUT OF THIS LOOP IF WE FAULT
			# DUE TO THE WAY WE ARE HANDLING GROUPS WE CANNOT STAY IN IT
			get_out_now = 0
			#
			# RESET THE WRITE VALUE ARRAY
			write_leaf = []
			write_value = []
			# CYCLE THROUGH LEAFERS
			while leaf_int<leaflines:
				if get_out_now == 0:
					try:
						# DECLARE WHAT SET OF LEAVES WE ARE ON
						leafarray = leaflinearray[leaf_int]	
						leafarray = str(leafarray)
						# LEAVES IN LINE
						leafendofline = leafarray.count('&')
						leafendofline = leafendofline - 1
						leafarray = leafarray.split('&')
						leaf = leafarray[leafline_int]
						leaf = str(leaf)
						# NOTE THE FOLLOWING IS A WAY TO 
						#   REMOVE THE START AND END XXX YYY FLAGS FROM
						#   THE VARIABLE WHICH WILL BUILD OUR WRITE ARRAY
						leaf_opc_write_friendly = leaf.replace('XXX', '')
						leaf_opc_write_friendly = leaf_opc_write_friendly.replace('YYY', '')
						contents = leafarray[leafline_int + 1]
						contents = str(contents)
						# NOTE THE FOLLOWING IS A WAY TO CHOP AND PARSE OUR
						# TAGS, WHERE A TAG IS A COMBINATION OF THE 'XXX'
						# START PLACEHOLDER, 'DEVICE' YOUR TALKING TO, 'YYY'
						# END PLACEHOLDER, AND THE 'TAG' ITSELF.
						# EXAMPLE1... XXXDEVICEYYYTAG 
						# EXAMPLE2... XXX[MYPLC1]YYYN7:10 (RSLinx)
						# EXAMPLE3... XXXCHANNEL1.MYPLC1YYYN7:10 (Kepware)
						leaf_sql_name = leaf.split('YYY')
						leaf_sql_name = leaf_sql_name[0]
						leaf_sql_name = str(leaf_sql_name)
						# THIS TRIM WILL GET RID OF OUR 'XXX' START
						leaf_sql_name = leaf_sql_name[3:]
						# WE DO NOT NEED TO TRIM THE 'YYY' FROM THE
						#   END BECAUSE THE 'SPLIT' ABOVE DOES THIS
						#   FOR US.
						leaf_sql_name = str(leaf_sql_name)
						try:
							# BUILD UP OUR WRITE PAIR ARRAY
							write_leaf.append(leaf_opc_write_friendly)
							write_value.append(contents)
						except:
							print ""
							print leaf_sql_name 
							print "cannot be accessed... skipping."
							# GET OUT OF THIS LOOP NOW
							get_out_now = 1
							mod_openopc_fault_unk()
					except:
						print ""
						print "CANNOT CONTINUE WITH THE WRITE..."
						print " -- something is wrong with your tags or values."
						print " -- we can't build the write array."
				if get_out_now != 1:
					leafline_int = 0
					leaf_int = leaf_int + leaf_i
				else:
					leaf_int = leaf_lines
			# BUILD THE WRITE VALUE FOR EXPORT TO THE TARGET
			array_to_write  = []
			for identity, leaf in enumerate(write_value):
				x_write_leaf = write_leaf[identity]
				y_write_value = write_value[identity]
				xy_value = (x_write_leaf, y_write_value)
				array_to_write.append(xy_value)
			# NOW WRITE THE ENTIRE ARRAY TO THE TARGET
			if VERBOSE == "YES":	
				print "Writing value to target..."
				print array_to_write
			array_status = opc.write(array_to_write)
			print ""
			print "THE WRITE WAS..."
			print array_status
		#
		# -- FAULT - A HEADER FOR ALL FAULT FUNCTIONS
		def mod_openopc_fault_all_header():
			print ""
			print "FAULT!"
		# -- FAULT - A FOOTER FOR ALL FAULT FUNCTIONS
		def mod_openopc_fault_all_footer():
			# DECLARE GLOBAL VARS
			global action, datestamp, VERBOSE, YOURCOMMAND1, fault, YOUROPTION1, YOUROPCSERVER, sql_query
			stamp_date()
			if YOURCOMMAND1 != 'WRITE_ONE_SHOT':
				action = YOURCOMMAND1 + "_" + YOUROPTION1
			else:
				action = YOURCOMMAND1 + "_" + "Variable"

			if (((fault == 'UNK_COMM_RST') or (fault == 'GRP_BLD_FAIL')) and (VERBOSE == 'NO')):
				fault = "\'" + datestamp + "\',\'" + fault + "\',\'" + action + "\',\'" + YOUROPCSERVER + "\',\'MINIMALRESPONSE\'"
			else:
				fault = "\'" + datestamp + "\',\'" + fault + "\',\'" + action + "\',\'" + YOUROPCSERVER + "\',NULL"
			fault = str(fault)
			# PUSH THE ROW INTO THE DATABASE
			# -- psuedo_query_example = INSERT INTO SQL_FAULTTABLE VALUES(fault)
			sql_query = "INSERT INTO " + SQL_FAULTTABLE + " () VALUES(" + fault + ")"
			print sql_query
			execute_sql_query('yes')
			# END PUSHING PUSH THE ROW INTO THE DATABASE
			# RETURN ARGS
			return datestamp
		# -- FAULT GROUP BUILD
		def mod_openopc_fault_group_build():
			# DECLARE GLOBAL VARS
			global datestamp, RESET_STATE, YOURCOMMAND1, fault, YOUROPTION1, OPC_SERVER_NAME
			mod_openopc_fault_all_header()
			print "FAILURE TO BUILD OPC GROUP for TOPIC(s)..."
			print " -- POSSIBLE CAUSES ARE AS FOLLOWS..."
			print " -- -- 1- OPC SERVER CRASH, or TIMEOUT"
			print " -- -- 2- THE OPC DEVICE (PLC, WHATEVER) HAS"
			print " -- -- -- BEEN TURNED OFF OR POWERED DOWN"
			print " -- -- 3- BAD ETHERNET COMMUNICATION"
			print " -- -- 4- TOPIC IS NOT SET UP ON THE OPC SERVER"
			print "DISCONNECTING and RECONNECTING."
			# TRY TO HANDLE this FAULT INSTEAD OF DYING
			# -- CLOSE THE OPC CONNECTION
			try:
				opc.close()
				print ""
				print "-- OPC CONNECTION CLOSED"
				print ""
			except:
				print ""
				print "-- Failure to close connection to OPC Server,"
				print "hard exit will follow."
				print ""
			fault = "GRP_BLD_FAIL"
			mod_openopc_fault_all_footer()
			# -- WAIT
			time.sleep(3)
			# -- RECONNECTING
			print "-- 1st RECONN TRY"
			try:
				fire_up_gw()
				fire_up_opc()
				time.sleep(2)
			except:
				print "-- -- FAILED"
				fault = "OPC_SVR_DOWN"
				mod_openopc_fault_all_footer()
				time.sleep(5)
				print "-- 2nd RECONN TRY"
				try:
					# -- TRY AGAIN
					fire_up_gw()
					fire_up_opc()
				except:
					restored_opc = 0
					while restored_opc == 0:
						try:
							# -- TRY AGAIN
							fire_up_gw()
							fire_up_opc()
							time.sleep(1)
							restored_opc = 1
						except:	
							fault = "OPC_SVR_DOWN_X"
							mod_openopc_fault_all_footer()
							time.sleep(10)
					if restored_opc == 0:		
						# -- FAIL
						print ""
						print "FAULT FATAL!!!! -- HARD EXIT NEXT"
						fault = "OPC_SVR_DOWN_FATAL"
						mod_openopc_fault_all_footer()
						exit()
					else:
						# -- UN-FAIL
						print ""
						print "OPC COMM RESTORED!!!"
						fault = "OPC_SVR_COMM_RESTORED"
						mod_openopc_fault_all_footer()
			print ""
			print "-- WAIT BRIEFLY, THEN RECYCLE"
			time.sleep(1)
			RESET_STATE = "RERUN"
			# RETURN ARGS
			return datestamp, RESET_STATE, fault
		# -- FAULT UNKNOWN
		def mod_openopc_fault_unk():
			# DECLARE GLOBAL VARS
			global datestamp, RESET_STATE, YOURCOMMAND1, fault, YOUROPTION1, OPC_SERVER_NAME
			mod_openopc_fault_all_header()
			print "UNKNOWN COMMUNICATION FAULT DURING RUNTIME..."
			print " -- POSSIBLE CAUSES ARE AS FOLLOWS..."
			print " -- -- 1- OPC SERVER CRASH, or TIMEOUT"
			print " -- -- 2- THE OPC DEVICE (PLC, WHATEVER) HAS"
			print " -- -- -- BEEN TURNED OFF OR POWERED DOWN"
			print " -- -- 3- BAD ETHERNET COMMUNICATION"
			print "DISCONNECTING and RECONNECTING."
			# TRY TO HANDLE this FAULT INSTEAD OF DYING
			# -- CLOSE THE OPC CONNECTION
			try:
				opc.close()
				print ""
				print "-- OPC CONNECTION CLOSED"
				print ""
			except:
				print ""
				print "-- Failure to close connection to OPC Server,"
				print "hard exit will follow."
				print ""
			fault = "UNK_COMM_RST"
			mod_openopc_fault_all_footer()
			# -- WAIT
			time.sleep(3)
			# -- RECONNECTING
			restored_gw = 0
			restored_opc = 0
			restored_hiccup = "unknown"
			print "-- 1st RECONN TRY"
			try:
				fire_up_gw()
				restored_gw = 1
			except:
				print "-- -- FAILED"
				mod_openopc_fault_gw()
				restored_hiccup = "gw"
			if restored_gw == 1:
				try:
					fire_up_opc()
					time.sleep(2)
					restored_opc = 1
				except:
					print "-- -- FAILED"
					mod_openopc_fault_opc()
					restored_hiccup = "opc"
					time.sleep(5)
			while restored_gw == 0 or restored_opc == 0:
				try:
					opc.close()
				except:
					pass
				time.sleep(2)
				try:
					fire_up_gw()
					print "-- -- GATEWAY RESTORED"
					if restored_hiccup == "gw":
						fault = "GW_RESTORED"
						mod_openopc_fault_all_footer()
					restored_gw = 1
				except:
					print "-- -- GATEWAY STILL DOWN"
					print "-- -- TRYING AGAIN IN 5 SECONDS"
					restored_gw = 0
					time.sleep(5)
				if restored_gw == 1:
					try:
						fire_up_opc()
						time.sleep(2)
						print "-- -- OPC SERVER COMM RESTORED"
						if restored_hiccup == "opc":
							fault = "OPC_COMM_RESTORED"
							mod_openopc_fault_all_footer()
						restored_opc = 1
					except:	
						print"-- -- OPC SERVER COMM STILL DOWN"
						print"-- -- TRYING AGAIN IN 5 SECONDS"
						restored_hiccup = "opc"
						time.sleep(5)
			# THIS NEXT CONDITIONAL SHOULD BE IMPOSSIBLE, BUT JUST INCASE, LET'S
			# ADDRESS IT AND BREAK HARD TO A FULL INSTANCE EXIT
			if restored_opc == 0 or restored_gw == 0:		
				# -- FAIL
				print ""
				print "FAULT FATAL!!!! -- HARD EXIT NEXT"
				fault = "UNK_COMM_TOTALFAILURE"
				mod_openopc_fault_all_footer()
				exit()
			else:
				pass
			print ""
			print "-- WAIT BRIEFLY, THEN RECYCLE"
			time.sleep(1)
			RESET_STATE = "RERUN"
			# RETURN ARGS
			return datestamp, RESET_STATE, fault
		# -- FAULT OPC SERVER
		def mod_openopc_fault_opc():
			# DECLARE GLOBAL VARS
			global datestamp, YOURCOMMAND1, fault, YOUROPTION1, OPC_SERVER_NAME, opc
			mod_openopc_fault_all_header()
			print "OPC SERVER IS DOWN..."
			fault = "OPC_SVR_DOWN"
			mod_openopc_fault_all_footer()
			try:
				opc.close()
				print "-- CONNECTION DIED GRACEFULLY."
			except:
				print "-- CONNECTION WOULD NOT DIE GRACEFULLY."
			# RETURN ARGS
			return datestamp, fault
		# -- FAULT INFINITE LOOP KILL OPC FUNCTION
		def mod_openopc_fault_infinite_loop_kill():
			# DECLARE GLOBAL VARS
			global datestamp, YOURCOMMAND1, fault, YOUROPTION1, OPC_SERVER_NAME, opc
			mod_openopc_fault_all_header()
			print "INFINITE LOOP FAULT DURING RUNTIME..."
			fault = "OPC_INFINITE_LOOP"
			mod_openopc_fault_all_footer()
			print "-- LOOP TERMINATED"
			# RETURN ARGS
			return datestamp, fault
		# -- FAULT GATEWAY
		def mod_openopc_fault_gw():
			# DECLARE GLOBAL VARS
			global datestamp, YOURCOMMAND1, fault, YOUROPTION1, OPC_SERVER_NAME, opc
			mod_openopc_fault_all_header()
			print "GATEWAY IS DOWN..."
			fault = "GATEWAY_DOWN"
			mod_openopc_fault_all_footer()
			try:
				opc.close()
				print "-- CONNECTION DIED GRACEFULLY."
			except:
				print "-- CONNECTION WOULD NOT DIE GRACEFULLY."
			# RETURN ARGS
			return datestamp, fault
#
# --------------------- -- SUBROUTINES ------------------------------
		# SPACE_BRIDGE
		if YOURCOMMAND1 == 'SPACE_BRIDGE':
			print ""
			print "STARTING ROUTINE - SPACE_BRIDGE"
			if OK_SPACE_BRIDGE >= 2:
			# -- -- A ROUTINE TO BRIDGE TWO COMM OPC DEVICES BY READING
			# -- -- FROM ONE AND WRITING TO THE OTHER AT A HIGH RATE.
			# -- -- -- DEVICES ACROSS DISSIMILAR NETWORKS / OPC SERVERS
			# -- -- YOURCOMMAND1 	... SPACE_BRIDGE
			# -- -- YOUROPTION1	... PRESET FILE NAME wo EXTENSION
			# -- -- YOUROPTION2	... UPDATE INTERVAL in SECONDS 
			# 			... ... 2 to 5 seconds suggested minimum.
			# -- -- YOUROPTION3	... OVERRIDE (or) [blank]
			#			... ... allows you to override the
			#			... ... the opc server's preset minimum
			#			... ... scan interval
				# NAME THIS THREAD
				THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + YOUROPTION1
				name_that_thread()
				#
				# SCAN ALL PRESETS AND OPTIONS
				try:
					pull_in_preset()
					pull_in_opc()
					pull_in_sql()
					# DECLARE THAT WE HAVE ACHIEVED A GOOD PRESET AND OPTIONS PULL
					OK_PRE_OPT_PULL = 1
				except:
					OK_PRE_OPT_PULL = 0
				#
				if OK_PRE_OPT_PULL == 1:
					# CONNECT TO THE MySQL DATABASE
					try:
						fire_up_sql()
						mysql_is_down = 0
					except:
						mysql_is_down = 1
					# CONNECT TO THE OPC SERVER and GATEWAY
					try:
						fire_up_gw()
						gateway_is_down = 0
					except:
						gateway_is_down = 1
					try:
						fire_up_opc()
						opcserver_is_down = 0
					except:
						opcserver_is_down = 1
					# PROCEED ONLY IF THE GATEWAY / OPC / and SQL ARE UP
					# PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					if mysql_is_down != 1:
						if gateway_is_down != 1:
							# PROCEED ONLY if THE OPCSERVER IS UP
							if opcserver_is_down != 1:
								YOUROPTION2 = int(YOUROPTION2)
								# ZERO OUT DEAD TIME FOR MYSQL KEEPALIVE
								dead_time = 0
								# ZERO OUT STATE FILE INDICATOR
								reset_statefile_added = 0
								RESET_STATE = "RUN"
								# BUILD THE OPC GROUP
								GROUP_UPDATE = int(YOUROPTION2)
								mod_openopc_group()
								print ""
								print "NOTICE! -- SUCCESSFULLY ENTERED THE SPACE_BRIDGE CYCLE."
								time.sleep(5)
								# DEAL WITH THE SCAN OVERRIDE IF ANY
								if OK_BRIDGE != 3:
									SCAN_OVERRIDE = 0
								else:
									SCAN_OVERRIDE = YOUROPTION3
									print "WARNING! - ! - YOUR OPC SERVER'S MINIMUM SCAN INTERVAL"
									print "HAS BEEN OVERRIDDEN.  IF YOU HAVE PROBLEMS, THEN RUN"
									print "THIS FUNCTION WITHOUT THE 'OVERRIDE' INSTRUCTION."
								while True:
									try:
										voodoo_again = 0
										pull_in_reset_CHECK_READ_AND_BRIDGE_TYPE_ROUTINES()
										print "-- PERFORMING SPACE_BRIDGE."
										voodoo = timeit.Timer('mod_openopc_space_bridge()', 'from __main__ import mod_openopc_space_bridge')
										print "-- CALCULATING CYCLE TIME."
										witching_time = int(round(voodoo.timeit(number=1), 0))
										if witching_time < 0:
											witching_time = 0
										voodoo_again = YOUROPTION2
										voodoo_again = voodoo_again - witching_time
										if SCAN_OVERRIDE != "OVERRIDE":								
											if voodoo_again < OPC_MINIMUM_SCAN_INTERVAL:
												voodoo_again = OPC_MINIMUM_SCAN_INTERVAL
											else:
												voodoo_again = voodoo_again
										if voodoo_again < 0:
											voodoo_again = OPC_MINIMUM_SCAN_INTERVAL
										print ""
										print "-- SPACE BRIDGE COMPLETE."
										print "-- -- CYCLE TIME WAS..."
										print witching_time
										print "-- -- RECYCLING."
										print "NOTICE! -- SECONDS UNTIL NEXT SCAN..."
										print voodoo_again
										# WAIT UNTIL WE ARE SUPPOSED TO PROCEED AGAIN
										pull_in_reset_CHECK_READ_AND_BRIDGE_TYPE_ROUTINES()
										dead_time = dead_time + voodoo_again + witching_time
										if dead_time > 10000:
											# KEEP ALIVE FUNCTION
											fire_up_sql_refresh()
											dead_time = 0
										else:
											dead_time = dead_time								
									# END KEEP RUNNING UNTIL WE HAVE A PROBLEM
									except:
										mod_openopc_fault_unk()
							# END PROCEED ONLY IF THE OPC SERVER IS UP
							else:
								# EXPORT OPC SERVER FAULT
								mod_openopc_fault_opc()
						# END PROCEED ONLY IF THE GATEWAY IS UP
						else:
							# EXPORT GATEWAY FAULT TO A TEMP FILE
							mod_openopc_fault_gw()
						# CLOSE THE OPC CONNECTION WITH GRACE
						print ""
						print "NOTICE! -- ATTEMPTING TO CLOSE OPC CONNECTION."
						try:
							opc.close()
							print "-- CONNECTION DIED GRACEFULLY."
						except:
							print "-- CONNECTION WOULD NOT DIE GRACEFULLY."
					# END PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					else:
						mod_openopc_error_sql()
					# CLOSE CONNECTION TO MySQL DB
					try:
						sql_cursor.close ()
						sql_connect.close ()
					except:
						mod_openopc_error_sql_close()
				else:
					mod_openopc_error_options()
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# BRIDGE
		if YOURCOMMAND1 == 'BRIDGE':
			print ""
			print "STARTING ROUTINE - BRIDGE"
			if OK_BRIDGE >= 2:
			# -- BRIDGE
			# -- -- A ROUTINE TO BRIDGE TWO COMM OPC DEVICES BY READING
			# -- -- FROM ONE AND WRITING TO THE OTHER AT A HIGH RATE.
			# -- -- -- DEVICES ON THE SAME NETWORK / OPC SERVER.
			# -- -- YOURCOMMAND1 	... BRIDGE
			# -- -- YOUROPTION1	... PRESET FILE NAME wo EXTENSION
			# -- -- YOUROPTION2	... UPDATE INTERVAL in SECONDS 
			# 			... ... 2 to 5 seconds suggested minimum.
			# -- -- YOUROPTION3	... OVERRIDE (or) [blank]
			#			... ... allows you to override the
			#			... ... the opc server's preset minimum
			#			... ... scan interval
				# NAME THIS THREAD
				THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + YOUROPTION1
				name_that_thread()
				#
				# SCAN ALL PRESETS AND OPTIONS
				try:
					pull_in_preset()
					pull_in_opc()
					pull_in_sql()
					# DECLARE THAT WE HAVE ACHIEVED A GOOD PRESET AND OPTIONS PULL
					OK_PRE_OPT_PULL = 1
				except:
					OK_PRE_OPT_PULL = 0
				#
				if OK_PRE_OPT_PULL == 1:
				# PN ------------------ BEGIN GUTS_OF_BRIDGE ------------------- END PN
					# CONNECT TO THE MySQL DATABASE
					try:
						fire_up_sql()
						mysql_is_down = 0
					except:
						mysql_is_down = 1
					# CONNECT TO THE OPC SERVER and GATEWAY
					try:
						fire_up_gw()
						gateway_is_down = 0
					except:
						gateway_is_down = 1
					try:
						fire_up_opc()
						opcserver_is_down = 0
					except:
						opcserver_is_down = 1
					# PROCEED ONLY IF THE GATEWAY / OPC / and SQL ARE UP
					# PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					if mysql_is_down != 1:
						if gateway_is_down != 1:
							# PROCEED ONLY if THE OPCSERVER IS UP
							if opcserver_is_down != 1:
								YOUROPTION2 = int(YOUROPTION2)
								# ZERO OUT DEAD TIME FOR MYSQL KEEPALIVE
								dead_time = 0
								# ZERO OUT STATE FILE INDICATOR
								reset_statefile_added = 0
								RESET_STATE = "RUN"
								# BUILD THE OPC GROUP
								GROUP_UPDATE = int(YOUROPTION2)
								mod_openopc_group()
								print ""
								print "NOTICE! -- SUCCESSFULLY ENTERED THE BRIDGE CYCLE."
								time.sleep(5)
								# DEAL WITH THE SCAN OVERRIDE IF ANY
								if OK_BRIDGE != 3:
									SCAN_OVERRIDE = 0
								else:
									SCAN_OVERRIDE = YOUROPTION3
									print "WARNING! - ! - YOUR OPC SERVER'S MINIMUM SCAN INTERVAL"
									print "HAS BEEN OVERRIDDEN.  IF YOU HAVE PROBLEMS, THEN RUN"
									print "THIS FUNCTION WITHOUT THE 'OVERRIDE' INSTRUCTION."
								while True:
									try:
										voodoo_again = 0
										pull_in_reset_CHECK_READ_AND_BRIDGE_TYPE_ROUTINES()
										print "-- PERFORMING BRIDGE."
										voodoo = timeit.Timer('mod_openopc_bridge()', 'from __main__ import mod_openopc_bridge')
										print "-- CALCULATING CYCLE TIME."
										witching_time = int(round(voodoo.timeit(number=1), 0))
										if witching_time < 0:
											witching_time = 0
										voodoo_again = YOUROPTION2
										voodoo_again = voodoo_again - witching_time
										if SCAN_OVERRIDE != "OVERRIDE":								
											if voodoo_again < OPC_MINIMUM_SCAN_INTERVAL:
												voodoo_again = OPC_MINIMUM_SCAN_INTERVAL
											else:
												voodoo_again = voodoo_again
										if voodoo_again < 0:
											voodoo_again = OPC_MINIMUM_SCAN_INTERVAL
										print ""
										print "-- BRIDGE COMPLETE."
										print "-- -- CYCLE TIME WAS..."
										print witching_time
										print "-- -- RECYCLING."
										print "NOTICE! -- SECONDS UNTIL NEXT SCAN..."
										print voodoo_again
										# WAIT UNTIL WE ARE SUPPOSED TO PROCEED AGAIN
										pull_in_reset_CHECK_READ_AND_BRIDGE_TYPE_ROUTINES()
										dead_time = dead_time + voodoo_again + witching_time
										if dead_time > 10000:
											# KEEP ALIVE FUNCTION
											fire_up_sql_refresh()
											dead_time = 0
										else:
											dead_time = dead_time								
									# END KEEP RUNNING UNTIL WE HAVE A PROBLEM
									except:
										mod_openopc_fault_unk()
							# END PROCEED ONLY IF THE OPC SERVER IS UP
							else:
								# EXPORT OPC SERVER FAULT
								mod_openopc_fault_opc()
						# END PROCEED ONLY IF THE GATEWAY IS UP
						else:
							# EXPORT GATEWAY FAULT TO A TEMP FILE
							mod_openopc_fault_gw()
						# CLOSE THE OPC CONNECTION WITH GRACE
						print ""
						print "NOTICE! -- ATTEMPTING TO CLOSE OPC CONNECTION."
						try:
							opc.close()
							print "-- CONNECTION DIED GRACEFULLY."
						except:
							print "-- CONNECTION WOULD NOT DIE GRACEFULLY."
					# END PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					else:
						mod_openopc_error_sql()
					# CLOSE CONNECTION TO MySQL DB
					try:
						sql_cursor.close ()
						sql_connect.close ()
					except:
						mod_openopc_error_sql_close()
				else:
					mod_openopc_error_options()
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# READ_DAEMON
		if YOURCOMMAND1 == 'READ_DAEMON':
			print ""
			print "STARTING ROUTINE - READ_DAEMON"
			if OK_READ_DAEMON == 1:
			# -- READ_DAEMON
			# -- -- A ROUTINE TO MONITOR FLAT FILES DUMPED A DIRECTORY,
			# -- -- AND EXECUTE OPC WRITES BASED UPON SAID FILES
			# -- -- YOURCOMMAND1 	... READ_DAEMON
			# -- -- YOUROPTION1	... PRESET FILE NAME wo EXTENSION
				# NAME THIS THREAD
				THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + YOUROPTION1
				name_that_thread()
				#
				# SCAN ALL PRESETS AND OPTIONS
				try:
					pull_in_preset()
					pull_in_opc()
					pull_in_sql()
					# DECLARE THAT WE HAVE ACHIEVED A GOOD PRESET AND OPTIONS PULL
					OK_PRE_OPT_PULL = 1
				except:
					OK_PRE_OPT_PULL = 0
				#
				if OK_PRE_OPT_PULL == 1:
					# CONNECT TO THE MySQL DATABASE
					try:
						fire_up_sql()
						mysql_is_down = 0
					except:
						mysql_is_down = 1
					# CONNECT TO THE OPC SERVER and GATEWAY
					try:
						fire_up_gw()
						gateway_is_down = 0
					except:
						gateway_is_down = 1
					try:
						fire_up_opc()
						opcserver_is_down = 0
					except:
						opcserver_is_down = 1
					# PROCEED ONLY IF THE GATEWAY / OPC / and SQL ARE UP
					# PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					if mysql_is_down != 1:
						if gateway_is_down != 1:
							# PROCEED ONLY if THE OPCSERVER IS UP
							if opcserver_is_down != 1:
								# ZERO OUT STATE FILE INDICATOR
								reset_statefile_added = 0
								RESET_STATE = "RUN"
								pull_in_reset()
								# DECLARE OUR CONFIG PULL IN VAR FOR THE EVENT FILES
								section_read = 0
								dead_time = 0
								print ""
								print "NOTICE! -- SUCCESSFULLY LAUNCHED READ DAEMON."
								print " -- YOUR DAEMON IS..."
								print YOURDAEMON
								print "NOTICE! -- WAITING for EVENT INPUT..."
								print YOURDAEMON
								while True:
									# DIRECTORY VALIDATION
									if os.path.exists(YOURDAEMON):
										pass
									else:
										os.makedirs(YOURDAEMON, 0777)
										time.sleep(1)
										os.chmod(YOURDAEMON, 0777)
									# KEEP RUNNING UNTIL WE HAVE A PROBLEM
									try:
										pull_in_reset_CHECK_READ_AND_WRITE_DAEMON_TYPE_ROUTINES()
										file_count = len(os.walk(YOURDAEMON).next()[2])
										if file_count > 0:
											time.sleep(0.01)
											for file_in_daemon in os.listdir(YOURDAEMON):
												# -- INTERVAL BETWEEN SCANS IS preset TO 0.02 Secs.
												time.sleep(0.02)
												print ""
												print "NOTICE! -- YOUR EVENT NAME IS..."
												print file_in_daemon
												file_in_daemon = os.path.join(YOURDAEMON, file_in_daemon)
												file_in_daemon_o = open(file_in_daemon,"r")
												print "-- opened."
												if section_read != 1:
													config.add_section("your_read")
													print "-- -- added section 'your_read'."
													section_read = 1
												else:
													print "-- -- section 'your_read' exists."
												# -- READ FROM THE EVENT FILE
												config.readfp(file_in_daemon_o)
												# -- ASSIGN VARS BASED ON THE EVENT FILE
												YOURREAD = config.get("your_read","YOURREAD")
												file_in_daemon_o.close()
												# -- READ FROM PRESET FILE
												jump_to_preset = os.path.join(PROGPATH_PRE, YOURREAD) + ".pre"
												jump_to_preset = open(jump_to_preset,"r")
												# -- READ FROM THE PRESET FILE
												config.readfp(jump_to_preset)
												# -- ASSIGN VARS BASED ON THE PRESET FILE
												YOURLEAFERS = config.get("your_read","YOURLEAFERS")
												YOURSQLTABLE = config.get("your_server","YOURSQLTABLE")
												COMMENTENABLE = config.get("your_server","COMMENTENABLE")
												SQL_COMMENT_TABLE = config.get("your_server","YOURSQLCOMMENTTABLE")
												SQL_TABLE = config.get("your_server","YOURSQLTABLE")
												YOURSQLFILLERCOUNT = config.get("your_server","YOURSQLFILLERCOUNT")
												YOURSQLCOLUMNCOUNT = config.get("your_server","YOURSQLCOLUMNCOUNT")
												THREADNAME = "mod_openopc_READ_DAEMON_" + SQL_TABLE 
												GROUP_SOURCE = "hybrid"
												#
												print "-- -- read section 'your_read'."
												print "-- PERFORMING READ."
												voodoo = timeit.Timer('mod_openopc_read()', 'from __main__ import mod_openopc_read')
												witching_time = int(round(voodoo.timeit(number=1), 0))
												if witching_time < 0:
													witching_time = 0
												print "-- READ COMPLETE."
												print "-- -- CYCLE TIME WAS..."
												print witching_time
												print "-- -- DELETING EVENT FILE..."
												jump_to_preset.close()
												os.remove(file_in_daemon)
												print "-- -- -- DELETED."
	                                                                                        print "-- -- REMOVING OPC GROUP FROM SERVER..."
	                                							opc.remove(THREADNAME)
	                                                                                        print "-- -- -- REMOVED."
												print "-- -- RECYCLING."
												print ""
												print "NOTICE! -- WAITING for EVENT INPUT..."
												print YOURDAEMON
												dead_time = dead_time + 1
										else:
											time.sleep(0.05)
											dead_time = dead_time + 1
											if dead_time > 10000:
												# KEEP ALIVE FUNCTION
												fire_up_sql_refresh()
												dead_time = 0
											else:
												dead_time = dead_time
										# END KEEP RUNNING UNTIL WE HAVE A PROBLEM
									except:
										mod_openopc_fault_unk()
							# END PROCEED ONLY IF THE OPC SERVER IS UP
							else:
								# EXPORT OPC SERVER FAULT
								mod_openopc_fault_opc()
						# END PROCEED ONLY IF THE GATEWAY IS UP
						else:
							# EXPORT GATEWAY FAULT TO A TEMP FILE
							mod_openopc_fault_gw()
						# CLOSE THE OPC CONNECTION WITH GRACE
						print ""
						print "NOTICE! -- ATTEMPTING TO CLOSE OPC CONNECTION."
						try:
							opc.close()
							print "-- CONNECTION DIED GRACEFULLY."
						except:
							print "-- CONNECTION WOULD NOT DIE GRACEFULLY."
					# END PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					else:
						mod_openopc_error_sql()
					# CLOSE CONNECTION TO MySQL DB
					try:
						sql_cursor.close ()
						sql_connect.close ()
					except:
						mod_openopc_error_sql_close()
				else:
					mod_openopc_error_options()
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# READ
		if YOURCOMMAND1 == 'READ':
			print ""
			print "STARTING ROUTINE - READ"
			if OK_READ == 2:
			# -- READ
			# -- -- A ROUTINE TO READ FROM THE OPC SERVER AND LOG DATA TO A DB
			# -- -- YOURCOMMAND1 	... READ
			# -- -- YOUROPTION1	... PRESET FILE NAME wo EXTENSION
			# -- -- YOUROPTION2	... SCAN INTERVAL in SECONDS
				# NAME THIS THREAD
				THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + YOUROPTION1
				name_that_thread()
				#
				# MODE OF READ
				if YOUROPTION3 == 'UPDATE':
					print "-- RUNNING IN 'UPDATE' MODE"
					print "-- -- NO NEW RECORDS WILL BE CREATED"
					print "-- -- UPDATE LIMITED TO LAST (MOST RECENT) RECORD!"
				else:
					if YOUROPTION3 == 'ACK':
						print "-- RUNNING IN ADD MODE W/ ACKNOWLEDGE"
						print "-- -- UPON A SUCCESSFUL READ, A WRITE PRESET"
						print "-- -- YOU DECLARE ON THE COMMAND LINE WILL"
						print "-- -- BE EXECUTED (WITH A 10 SECOND TIMEOUT)"
						print "-- -- ACKNOWLEDGING RECEIPT OF DATA!"
						print "-- NEW RECORDS WILL BE ADDED BASED UPON"
						print "-- THE FINAL LEAFER (DATA TAG)"
						print "-- -- 0 = ACK'ED - DO NOT ADD, DISCARD"
						print "-- -- 1 = NEW - MUST BE ADDED"
					else:
						print "-- RUNNING IN STANDARD 'ADD' MODE"
						print "-- -- NEW RECORDS WILL BE ADDED"
				#
				# SCAN ALL PRESETS AND OPTIONS
				try:
					pull_in_preset()
					pull_in_opc()
					pull_in_sql()
					# DECLARE THAT WE HAVE ACHIEVED A GOOD PRESET AND OPTIONS PULL
					OK_PRE_OPT_PULL = 1
				except:
					OK_PRE_OPT_PULL = 0
				#
				if OK_PRE_OPT_PULL == 1:
					# CONNECT TO THE MySQL DATABASE
					try:
						fire_up_sql()
						mysql_is_down = 0
					except:
						mysql_is_down = 1
					# CONNECT TO THE OPC SERVER and GATEWAY
					try:
						fire_up_gw()
						gateway_is_down = 0
					except:
						gateway_is_down = 1
					try:
						fire_up_opc()
						opcserver_is_down = 0
					except:
						opcserver_is_down = 1
					# PROCEED ONLY IF THE GATEWAY / OPC / and SQL ARE UP
					# PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					if mysql_is_down != 1:
						if gateway_is_down != 1:
							# PROCEED ONLY if THE OPCSERVER IS UP
							if opcserver_is_down != 1:
								YOUROPTION2 = int(YOUROPTION2)
								# ZERO OUT STATE FILE INDICATOR
								reset_statefile_added = 0
								RESET_STATE = "RUN"
								# ZERO OUT THE MYSQL KEEPALIVE
								dead_time = 0
								# BUILD THE OPC GROUP
								GROUP_UPDATE = int(YOUROPTION2)
								mod_openopc_group()
								print ""
								print "NOTICE! -- SUCCESSFULLY ENTERED THE READ CYCLE."
								time.sleep(5)
								while True:
									try:
										voodoo_again = 0
										pull_in_reset_CHECK_READ_AND_BRIDGE_TYPE_ROUTINES()
										print "-- PERFORMING READ."
										voodoo = timeit.Timer('mod_openopc_read()', 'from __main__ import mod_openopc_read')
										print "-- CALCULATING CYCLE TIME."
										witching_time = int(round(voodoo.timeit(number=1), 0))
										if witching_time < 0:
											witching_time = 0
										voodoo_again = YOUROPTION2
										voodoo_again = voodoo_again - witching_time
										if voodoo_again < OPC_MINIMUM_SCAN_INTERVAL:
											voodoo_again = OPC_MINIMUM_SCAN_INTERVAL
										else:
											voodoo_again = voodoo_again
										print ""
										print "-- READ COMPLETE."
										print "-- -- CYCLE TIME WAS..."
										print witching_time
										if YOUROPTION3 == 'ACK':
											if save_value_ack_ok_PROOF == 1:
												# SEND ACKNOWLEDGEMENT IF NECESSARY
												CMD_ACK = PYTHON_EXECUTABLE + " " + MOD_OPENOPC_EXECUTABLE + " " + "WRITE " + str(YOUROPTION4) + " 10"
												# FIRE IT OFF
												try:
													print "-- -- ATTEMPTING ACK WITH COMMAND..."
													print CMD_ACK
													CMD_ACK_PROC_MONITOR = subprocess.Popen(CMD_ACK)
												except:
													print "-- -- SOMETHING WRONG WITH YOUR ACK CLI REQUEST"
													print "-- -- ACK FAILED!"
											else:
												pass
										else:
											pass
										print "-- -- RECYCLING."
										print "NOTICE! -- SECONDS UNTIL NEXT SCAN..."
										print voodoo_again
										# WAIT UNTIL WE ARE SUPPOSED TO PROCEED AGAIN
										pull_in_reset_CHECK_READ_AND_BRIDGE_TYPE_ROUTINES()
										dead_time = dead_time + voodoo_again + witching_time
										if dead_time > 10000:
											# KEEP ALIVE FUNCTION
											fire_up_sql_refresh()
											dead_time = 0
										else:
											dead_time = dead_time								
									# END KEEP RUNNING UNTIL WE HAVE A PROBLEM
									except:
										mod_openopc_fault_unk()
							# END PROCEED ONLY IF THE OPC SERVER IS UP
							else:
								# EXPORT OPC SERVER FAULT
								mod_openopc_fault_opc()
						# END PROCEED ONLY IF THE GATEWAY IS UP
						else:
							# EXPORT GATEWAY FAULT TO A TEMP FILE
							mod_openopc_fault_gw()
						# CLOSE THE OPC CONNECTION WITH GRACE
						print ""
						print "NOTICE! -- ATTEMPTING TO CLOSE OPC CONNECTION."
						try:
							opc.close()
							print "-- CONNECTION DIED GRACEFULLY."
						except:
							print "-- CONNECTION WOULD NOT DIE GRACEFULLY."
					# END PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					else:
						mod_openopc_error_sql()
					# CLOSE CONNECTION TO MySQL DB
					try:
						sql_cursor.close ()
						sql_connect.close ()
					except:
						mod_openopc_error_sql_close()
				else:
					mod_openopc_error_options()
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# READ_ONE_SHOT
		if YOURCOMMAND1 == 'READ_ONE_SHOT':
			print ""
			print "STARTING ROUTINE - READ_ONE_SHOT"
			if OK_READ_ONE_SHOT == 2:
			# -- READ_ONE_SHOT
			# -- -- A ROUTINE TO READ FROM THE OPC SERVER AND LOG DATA TO A DB
			# -- -- BUT TO ONLY BE PERFORMED ONCE (USEFUL FOR ITEMS YOU WANT
			# -- -- TO RUN ONLY ONCE PER HOUR OR ONCE PER DAY OR WHATEVER,
			# -- -- AND THAT YOU CAN SCHEDULE WITH CRON IN YOUR CRONTAB FILE.
			# -- -- YOURCOMMAND1 	... READ_ONE_SHOT
			# -- -- YOUROPTION1	... PRESET FILE NAME wo EXTENSION
			# -- -- YOUROPTION2	... SCAN INTERVAL in SECONDS (SERVES AS A TIMEOUT)
				# NAME THIS THREAD
				THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + YOUROPTION1
				name_that_thread()
				#
				# SCAN ALL PRESETS AND OPTIONS
				try:
					pull_in_preset()
					pull_in_opc()
					pull_in_sql()
					# DECLARE THAT WE HAVE ACHIEVED A GOOD PRESET AND OPTIONS PULL
					OK_PRE_OPT_PULL = 1
				except:
					OK_PRE_OPT_PULL = 0
				#
				if OK_PRE_OPT_PULL == 1:
					# CONNECT TO THE MySQL DATABASE
					try:
						fire_up_sql()
						mysql_is_down = 0
					except:
						mysql_is_down = 1
					# CONNECT TO THE OPC SERVER and GATEWAY
					try:
						fire_up_gw()
						gateway_is_down = 0
					except:
						gateway_is_down = 1
					try:
						fire_up_opc()
						opcserver_is_down = 0
					except:
						opcserver_is_down = 1
					# PROCEED ONLY IF THE GATEWAY / OPC / and SQL ARE UP
					# PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					if mysql_is_down != 1:
						if gateway_is_down != 1:
							# PROCEED ONLY if THE OPCSERVER IS UP
							if opcserver_is_down != 1:
								print ""
								print "NOTICE! -- SUCCESSFULLY ENTERED THE READ_ONE_SHOT CYCLE."
								# ZERO OUT STATE FILE INDICATOR
								reset_statefile_added = 0
								RESET_STATE = "RUN"
								pull_in_reset()
								# SCAN UNTIL WE HAVE 1 GOOD SCAN
								YOUROPTION2 = int(YOUROPTION2)
								scan_count = 0
								# BUILD a GROUP
								pull_in_reset()
								GROUP_UPDATE = YOUROPTION2
								mod_openopc_group()
								while scan_count == 0:
									# KEEP RUNNING UNTIL WE HAVE A GOOD SCAN
									try:
										voodoo_again = 0
										pull_in_reset_CHECK_READ_AND_BRIDGE_TYPE_ROUTINES()
										print "-- PERFORMING READ."
										voodoo = timeit.Timer('mod_openopc_read()', 'from __main__ import mod_openopc_read')
										witching_time = int(round(voodoo.timeit(number=1), 0))
										if witching_time < 0:
											witching_time = 0
										print "-- CALCULATING CYCLE TIME."
										voodoo_again = YOUROPTION2
										if witching_time > YOUROPTION2:
											voodoo_again = "NOTICE! -- SCAN MAY HAVE FAILED, EXCEEDED TIMEOUT, CHECK YOUR SETTINGS."
										else:
											voodoo_again = witching_time
										scan_count = 1
									# END KEEP RUNNING UNTIL WE HAVE A PROBLEM
									except:
										mod_openopc_fault_unk()
									# WAIT UNTIL WE ARE SUPPOSED TO PROCEED AGAIN
									if scan_count == 0:
										voodoo_again = YOUROPTION2
										print ""
										print "NOTICE! -- SUSPECT SCAN."
										print "(HENCE, THE FAULT YOU JUST SAW)"
										print "RESCANNING..."
									else:
										print ""
										print "NOTICE! -- GOOD SCAN."
										print "SCAN TIME WAS..."
										print voodoo_again
										time.sleep(5)
								# CLEANUP
								opc.remove(THREADNAME)
							# END PROCEED ONLY IF THE OPC SERVER IS UP
							else:
								# EXPORT OPC SERVER FAULT
								mod_openopc_fault_opc()
						# END PROCEED ONLY IF THE GATEWAY IS UP
						else:
							# EXPORT GATEWAY FAULT TO A TEMP FILE
							mod_openopc_fault_gw()
						# CLOSE THE OPC CONNECTION WITH GRACE
						print ""
						print "NOTICE! -- ATTEMPTING TO CLOSE OPC CONNECTION."
						try:
							opc.close()
							print "-- CONNECTION DIED GRACEFULLY."
						except:
							print "-- CONNECTION WOULD NOT DIE GRACEFULLY."
					# END PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					else:
						mod_openopc_error_sql()
					# CLOSE CONNECTION TO MySQL DB
					try:
						sql_cursor.close ()
						sql_connect.close ()
					except:
						mod_openopc_error_sql_close()
				else:
					mod_openopc_error_options()
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# WRITE_DAEMON
		if YOURCOMMAND1 == 'WRITE_DAEMON':
			print ""
			print "STARTING ROUTINE - WRITE_DAEMON"
			if OK_WRITE_DAEMON == 1:
			# -- WRITE_DAEMON
			# -- -- A ROUTINE TO MONITOR FLAT FILES DUMPED A DIRECTORY,
			# -- -- AND EXECUTE OPC WRITES BASED UPON SAID FILES
			# -- -- YOURCOMMAND1 	... WRITE_DAEMON
			# -- -- YOUROPTION1	... PRESET FILE NAME wo EXTENSION
				# NAME THIS THREAD
				THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + YOUROPTION1
				name_that_thread()
				#
				# SCAN ALL PRESETS AND OPTIONS
				try:
					pull_in_preset()
					pull_in_opc()
					pull_in_sql()
					# DECLARE THAT WE HAVE ACHIEVED A GOOD PRESET AND OPTIONS PULL
					OK_PRE_OPT_PULL = 1
				except:
					OK_PRE_OPT_PULL = 0
				#
				if OK_PRE_OPT_PULL == 1:
					# CONNECT TO THE MySQL DATABASE
					try:
						fire_up_sql()
						mysql_is_down = 0
					except:
						mysql_is_down = 1
					# CONNECT TO THE OPC SERVER and GATEWAY
					try:
						fire_up_gw()
						gateway_is_down = 0
					except:
						gateway_is_down = 1
					try:
						fire_up_opc()
						opcserver_is_down = 0
					except:
						opcserver_is_down = 1
					# PROCEED ONLY IF THE GATEWAY / OPC / and SQL ARE UP
					# PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					if mysql_is_down != 1:
						if gateway_is_down != 1:
							# PROCEED ONLY if THE OPCSERVER IS UP
							if opcserver_is_down != 1:
								# ZERO OUT STATE FILE INDICATOR
								reset_statefile_added = 0
								RESET_STATE = "RUN"
								pull_in_reset()
								# DECLARE OUR CONFIG PULL IN VAR FOR THE EVENT FILES
								section_leafers = 0
								dead_time = 0
								print ""
								print "NOTICE! -- SUCCESSFULLY LAUNCHED WRITE DAEMON."
								print " -- YOUR DAEMON IS..."
								print YOURDAEMON
								print "NOTICE! -- WAITING for EVENT INPUT..."
								print YOURDAEMON
								while True:
									# DIRECTORY VALIDATION
									if os.path.exists(YOURDAEMON):
										pass
									else:
										os.makedirs(YOURDAEMON, 0777)
										time.sleep(1)
										os.chmod(YOURDAEMON, 0777)
									# KEEP RUNNING UNTIL WE HAVE A PROBLEM
									try:
										pull_in_reset_CHECK_READ_AND_WRITE_DAEMON_TYPE_ROUTINES()
										file_count = len(os.walk(YOURDAEMON).next()[2])
										time.sleep(0.01)
										if file_count > 0:
											for file_in_daemon in os.listdir(YOURDAEMON):
												# -- INTERVAL BETWEEN FILE SCANS IS preset TO 0.02 Secs.
												# -- RESULTS IN ABSOLUTE MAX WRITES PER MINUTE BEING 3000
												# -- IN AN IDEAL WORLD - HOWEVER GIVEN NORMAL LATENCY, 
												# -- YOU SHOULD NOT PLAN ON MORE THAN 1500 MAX WRITES PER
												# -- MINUTE PER WRITE_DAEMON INSTANCE.
												# -- IF YOU GET JAMMED UP, YOU CAN SET UP MORE WRITE
												# -- DAEMONS FOR THE SAME OPC SERVER.
												time.sleep(0.02)
												print ""
												print "NOTICE! -- YOUR EVENT NAME IS..."
												print file_in_daemon
												file_in_daemon = os.path.join(YOURDAEMON, file_in_daemon)
												file_in_daemon_o = open(file_in_daemon,"r")
												print "-- opened."
												if section_leafers != 1:
													config.add_section("your_write_type")
													print "-- -- added section 'your_write_type'."
													config.add_section("your_leafers")
													print "-- -- added section 'your_leafers'."
													section_leafers = 1
												else:
													print "-- -- section 'your_leafers' exists."
												# -- READ FROM THE EVENT FILE
												config.readfp(file_in_daemon_o)
												# -- ASSIGN VARS BASED ON THE EVENT FILE
												YOURWRITETYPE = config.get("your_write_type","YOURWRITETYPE")
												print "-- -- read section 'your_write_type'."
												EVENT_FILE_INPUT_GOOD = "GOOD"
												while EVENT_FILE_INPUT_GOOD == "GOOD":
													if YOURWRITETYPE == "DECLARED":
														YOURLEAFERS = config.get("your_leafers","YOURLEAFERS")
														print "-- -- read section 'your_leafers'."
														file_in_daemon_o.close()
													else:
														if YOURWRITETYPE == "PRESET":
															YOURWRITEPRESET = config.get("your_leafers","YOURWRITEPRESET")
															print "-- -- read section 'your_leafers'."
															file_in_daemon_o.close()
															# -- READ FROM PRESET FILE
															jump_to_preset = os.path.join(PROGPATH_PRE, YOURWRITEPRESET) + ".wrt"
															jump_to_preset = open(jump_to_preset,"r")
															config.readfp(jump_to_preset)
															# LOGICALLY YOU WOULD THINK THAT WE SHOULD REMOVE
															# THE CONFIGURATION SECTION AND THEN READD IT FOR
															# THIS FILE.  HOWEVER, DOING SO THROWS AN ERROR
															# BUT NORMAL OPERATION OCCURS WHEN THE NEXT TWO
															# LINES ARE COMMENTED OUT...
															#config.remove_section("your_write")
															#config.add_section("your_write")
															# -- ASSIGN VARS BASED ON THE PRESET FILE
															YOURLEAFERS = config.get("your_write","YOURLEAFERS")
															jump_to_preset.close()
														else:
															print "-- -- WARNING! SOMETHING IS WRONG WITH"
															print "-- -- YOUR PRESET FILE.  NO WRITE_TYPE"
															print "-- -- DECLARED."
															print "-- -- SKIPPING WRITE AND DELETING EVENT"
															print "-- -- FILE."
															EVENT_FILE_INPUT_GOOD = "BAD"
													print ""
													print "-- EVENT FILE STATE IS..."
													print EVENT_FILE_INPUT_GOOD
													print ""
													print "-- PERFORMING WRITE."
													voodoo = timeit.Timer('mod_openopc_write()', 'from __main__ import mod_openopc_write')
													witching_time = int(round(voodoo.timeit(number=1), 0))
													if witching_time < 0:
														witching_time = 0
													print "-- WRITE COMPLETE."
													print "-- -- CYCLE TIME WAS..."
													print witching_time
													EVENT_FILE_INPUT_GOOD = "ALL DONE"
													print ""
													print "-- EVENT FILE STATE IS..."
													print EVENT_FILE_INPUT_GOOD
													print ""
												print "-- -- DELETING EVENT FILE..."
												os.remove(file_in_daemon)
												print "-- -- -- DELETED."
												print "-- -- RECYCLING."
												dead_time = dead_time + 1
												print ""
												print "NOTICE! -- WAITING for EVENT INPUT..."
										else:
											dead_time = dead_time + 1
											if dead_time > 10000:
												# KEEP ALIVE FUNCTION
												fire_up_sql_refresh()
												dead_time = 0
											else:
												dead_time = dead_time
										# END KEEP RUNNING UNTIL WE HAVE A PROBLEM
									except:
										mod_openopc_fault_unk()
									# INTERVAL BETWEEN DIRECTORY SCANS
									# -- PRESET TO 0.01 Secs.
									# -- GIVES OS TIME TO DELETE ABOVE FILES AFTER DELETE
									#    CMD SENT BY mod_openopc
									time.sleep(0.01)
							# END PROCEED ONLY IF THE OPC SERVER IS UP
							else:
								# EXPORT OPC SERVER FAULT
								mod_openopc_fault_opc()
						# END PROCEED ONLY IF THE GATEWAY IS UP
						else:
							# EXPORT GATEWAY FAULT TO A TEMP FILE
							mod_openopc_fault_gw()
						# CLOSE THE OPC CONNECTION WITH GRACE
						print ""
						print "NOTICE! -- ATTEMPTING TO CLOSE OPC CONNECTION."
						try:
							opc.close()
							print "-- CONNECTION DIED GRACEFULLY."
						except:
							print "-- CONNECTION WOULD NOT DIE GRACEFULLY."
					# END PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					else:
						mod_openopc_error_sql()
					# CLOSE CONNECTION TO MySQL DB
					try:
						sql_cursor.close ()
						sql_connect.close ()
					except:
						mod_openopc_error_sql_close()
				else:
					mod_openopc_error_options()
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# WRITE
		if YOURCOMMAND1 == 'WRITE':
			print ""
			print "STARTING ROUTINE - WRITE"
			if OK_WRITE == 2:
			# -- WRITE
			# -- -- A ROUTINE TO WRITE TO THE OPC SERVER A LEAF ARRAY.
			# -- -- BUT TO ONLY BE PERFORMED ONCE (USEFUL FOR ITEMS YOU WANT
			# -- -- TO RUN ONLY ONCE PER HOUR OR ON QUE OR COMMAND,
			# -- -- AND THAT YOU CAN SCHEDULE WITH CRON OR CALL VIA A WEBPAGE.
			# -- -- YOURCOMMAND1 	... WRITE
			# -- -- YOUROPTION1	... PRESET FILE, PROPERLY FORMATTED
			# -- -- YOUROPTION2	... SCAN INTERVAL in SECONDS
				# NAME THIS THREAD
				THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + YOUROPTION1
				name_that_thread()
				#
				# SCAN ALL PRESETS AND OPTIONS
				try:
					pull_in_preset()	# FOR THIS SUBROUTINE THE pull_in_preset
								# FUNCTION WILL SIMPLY SUBSTITUTE THE 
								# CLI ARGS FOR THE PRESET VARS.
					pull_in_opc()
					pull_in_sql()
					# DECLARE THAT WE HAVE ACHIEVED A GOOD PRESET AND OPTIONS PULL
					OK_PRE_OPT_PULL = 1
				except:
					OK_PRE_OPT_PULL = 0
				#
				if OK_PRE_OPT_PULL == 1:
					# CONNECT TO THE MySQL DATABASE
					try:
						fire_up_sql()
						mysql_is_down = 0
					except:
						mysql_is_down = 1
					# CONNECT TO THE OPC SERVER and GATEWAY
					try:
						fire_up_gw()
						gateway_is_down = 0
					except:
						gateway_is_down = 1
					try:
						fire_up_opc()
						opcserver_is_down = 0
					except:
						opcserver_is_down = 1
					# PROCEED ONLY IF THE GATEWAY / OPC / and SQL ARE UP
					# PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					if mysql_is_down != 1:
						if gateway_is_down != 1:
							# PROCEED ONLY if THE OPCSERVER IS UP
							if opcserver_is_down != 1:
								# ZERO OUT STATE FILE INDICATOR
								reset_statefile_added = 0
								RESET_STATE = "RUN"
								pull_in_reset()
								# SCAN UNTIL WE HAVE 1 GOOD SCAN
								YOUROPTION2 = int(YOUROPTION2)
								scan_count = 0
								infinite_loop_killer = 0
								print ""
								print "NOTICE! -- SUCCESSFULLY ENTERED THE WRITE CYCLE."
								while scan_count == 0 and infinite_loop_killer < 3:
									pull_in_reset()
									# KEEP RUNNING UNTIL WE HAVE A GOOD SCAN
									try:
										print "-- PERFORMING WRITE (ONE SHOT)."
										voodoo = timeit.Timer('mod_openopc_write()', 'from __main__ import mod_openopc_write')
										witching_time = int(round(voodoo.timeit(number=1), 0))
										if witching_time < 0:
											witching_time = 0
										print "-- CALCULATING CYCLE TIME."
										voodoo_again = YOUROPTION2
										if witching_time > YOUROPTION2:
											voodoo_again = "NOTICE! -- SCAN MAY HAVE FAILED, EXCEEDED TIMEOUT, CHECK YOUR SETTINGS."
										else:
											voodoo_again = witching_time
										scan_count = 1
									# END KEEP RUNNING UNTIL WE HAVE A PROBLEM
									except:
										mod_openopc_fault_unk()
									# WAIT UNTIL WE ARE SUPPOSED TO PROCEED AGAIN
									if scan_count == 0:
										voodoo_again = YOUROPTION2
										if infinite_loop_killer == 2:
											print ""
											print "NOTICE! -- WE'VE TRIED ENOUGH,"
											print "AND THIS SCAN WILL NOT SUCCEED."
											print "GIVING UP..."
											mod_openopc_fault_infinite_loop_kill()
										else:
											print ""
											print "NOTICE! -- SUSPECT SCAN."
											print "(HENCE, THE FAULT YOU JUST SAW)"
											print "RESCANNING..."
										infinite_loop_killer = infinite_loop_killer + 1
									else:
										print ""
										print "NOTICE! -- GOOD SCAN."
										print "SCAN TIME WAS..."
										print voodoo_again
										time.sleep(5)
							# END PROCEED ONLY IF THE OPC SERVER IS UP
							else:
								# EXPORT OPC SERVER FAULT
								mod_openopc_fault_opc()
						# END PROCEED ONLY IF THE GATEWAY IS UP
						else:
							# EXPORT GATEWAY FAULT TO A TEMP FILE
							mod_openopc_fault_gw()
						# CLOSE THE OPC CONNECTION WITH GRACE
						print ""
						print "NOTICE! -- ATTEMPTING TO CLOSE OPC CONNECTION."
						try:
							opc.close()
							print "-- CONNECTION DIED GRACEFULLY."
						except:
							print "-- CONNECTION WOULD NOT DIE GRACEFULLY."
					# END PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					else:
						mod_openopc_error_sql()
					# CLOSE CONNECTION TO MySQL DB
					try:
						sql_cursor.close ()
						sql_connect.close ()
					except:
						mod_openopc_error_sql_close()
				else:
					mod_openopc_error_options()
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# WRITE_ONE_SHOT
		if YOURCOMMAND1 == 'WRITE_ONE_SHOT':
			print ""
			print "STARTING ROUTINE - WRITE_ONE_SHOT"
			if OK_WRITE_ONE_SHOT == 4:
			# -- WRITE_ONE_SHOT
			# -- -- A ROUTINE TO WRITE TO THE OPC SERVER A LEAF ARRAY.
			# -- -- BUT TO ONLY BE PERFORMED ONCE (USEFUL FOR ITEMS YOU WANT
			# -- -- TO RUN ONLY ONCE PER HOUR OR ON QUE OR COMMAND,
			# -- -- AND THAT YOU CAN SCHEDULE WITH CRON OR CALL VIA A WEBPAGE.
			# -- -- YOURCOMMAND1 	... WRITE_ONE_SHOT
			# -- -- YOUROPTION1	... LEAF TO WRITE, PROPERLY FORMATTED
			# -- -- YOUROPTION2	... SCAN INTERVAL in SECONDS (SERVES AS A TIMEOUT)
			# -- -- YOUROPTION3	... OPC SERVER NAME
			# -- -- YOUROPTION4	... SQL SERVER NAME (FOR FAULT LOGGING)
				# NAME THIS THREAD
				THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + YOUROPTION3
				name_that_thread()
				#
				# SCAN ALL PRESETS AND OPTIONS
				try:
					pull_in_preset()	# FOR THIS SUBROUTINE THE pull_in_preset
								# FUNCTION WILL SIMPLY SUBSTITUTE THE 
								# CLI ARGS FOR THE PRESET VARS.
					pull_in_opc()
					pull_in_sql()
					# DECLARE THAT WE HAVE ACHIEVED A GOOD PRESET AND OPTIONS PULL
					OK_PRE_OPT_PULL = 1
				except:
					OK_PRE_OPT_PULL = 0
				#
				if OK_PRE_OPT_PULL == 1:
					# CONNECT TO THE MySQL DATABASE
					try:
						fire_up_sql()
						mysql_is_down = 0
					except:
						mysql_is_down = 1
					# CONNECT TO THE OPC SERVER and GATEWAY
					try:
						fire_up_gw()
						gateway_is_down = 0
					except:
						gateway_is_down = 1
					try:
						fire_up_opc()
						opcserver_is_down = 0
					except:
						opcserver_is_down = 1
					# PROCEED ONLY IF THE GATEWAY / OPC / and SQL ARE UP
					# PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					if mysql_is_down != 1:
						if gateway_is_down != 1:
							# PROCEED ONLY if THE OPCSERVER IS UP
							if opcserver_is_down != 1:
								# ZERO OUT STATE FILE INDICATOR
								reset_statefile_added = 0
								RESET_STATE = "RUN"
								pull_in_reset()
								# SCAN UNTIL WE HAVE 1 GOOD SCAN
								YOUROPTION2 = int(YOUROPTION2)
								infinite_loop_killer = 0
								scan_count = 0
								print ""
								print "NOTICE! -- SUCCESSFULLY ENTERED THE WRITE CYCLE."
								while scan_count == 0 and infinite_loop_killer < 3:
									pull_in_reset()
									# KEEP RUNNING UNTIL WE HAVE A GOOD SCAN
									try:
										print "-- PERFORMING WRITE_ONE_SHOT (WITH Cmd Line ARGS)."
										voodoo = timeit.Timer('mod_openopc_write()', 'from __main__ import mod_openopc_write')
										witching_time = int(round(voodoo.timeit(number=1), 0))
										if witching_time < 0:
											witching_time = 0
										print "-- CALCULATING CYCLE TIME."
										voodoo_again = YOUROPTION2
										if witching_time > YOUROPTION2:
											voodoo_again = "NOTICE! -- SCAN MAY HAVE FAILED, EXCEEDED TIMEOUT, CHECK YOUR SETTINGS."
										else:
											voodoo_again = witching_time
										scan_count = 1
									# END KEEP RUNNING UNTIL WE HAVE A PROBLEM
									except:
										mod_openopc_fault_unk()
									# WAIT UNTIL WE ARE SUPPOSED TO PROCEED AGAIN
									if scan_count == 0:
										voodoo_again = YOUROPTION2
										if infinite_loop_killer == 2:
											print ""
											print "NOTICE! -- WE'VE TRIED ENOUGH,"
											print "AND THIS SCAN WILL NOT SUCCEED."
											print "GIVING UP..."
											mod_openopc_fault_infinite_loop_kill()
										else:
											print ""
											print "NOTICE! -- SUSPECT SCAN."
											print "(HENCE, THE FAULT YOU JUST SAW)"
											print "RESCANNING..."
										infinite_loop_killer = infinite_loop_killer + 1
									else:
										print ""
										print "NOTICE! -- GOOD SCAN."
										print "SCAN TIME WAS..."
										print voodoo_again
										time.sleep(5)
							# END PROCEED ONLY IF THE OPC SERVER IS UP
							else:
								# EXPORT OPC SERVER FAULT
								mod_openopc_fault_opc()
						# END PROCEED ONLY IF THE GATEWAY IS UP
						else:
							# EXPORT GATEWAY FAULT TO A TEMP FILE
							mod_openopc_fault_gw()
						# CLOSE THE OPC CONNECTION WITH GRACE
						print ""
						print "NOTICE! -- ATTEMPTING TO CLOSE OPC CONNECTION."
						try:
							opc.close()
							print "-- CONNECTION DIED GRACEFULLY."
						except:
							print "-- CONNECTION WOULD NOT DIE GRACEFULLY."
					# END PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					else:
						mod_openopc_error_sql()
					# CLOSE CONNECTION TO MySQL DB
					try:
						sql_cursor.close ()
						sql_connect.close ()
					except:
						mod_openopc_error_sql_close()
				else:
					mod_openopc_error_options()
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# MAINT_DB
		if YOURCOMMAND1 == 'MAINT_DB':
			print ""
			print "STARTING ROUTINE - MAINT_DB"
			if OK_MAINT_DB == 1:
			# -- MAINT_DB
			# -- -- A ROUTINE TO CLEAN UP OLD RECORDS FROM THE MYSQL DB,
			# -- -- BASED ON THE CURRENT DATE AND THE RETENTION TIMES
			# -- -- DEFINED IN YOUR PRESET FILE.
			# -- -- YOURCOMMAND1 	... MAINT_DB
			# -- -- YOUROPTION1	... OPTIMIZE (or leave blank)
				# NAME THIS THREAD
				if YOUROPTION1 == 'OPTIMIZE':
					THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + YOUROPTION1
				else:
					THREADNAME = "mod_openopc_" + YOURCOMMAND1
				name_that_thread()
				#
				# SCAN ALL PRESETS AND OPTIONS
				try:
					pull_in_preset()
					pull_in_sql()
					# DECLARE THAT WE HAVE ACHIEVED A GOOD PRESET AND OPTIONS PULL
					OK_PRE_OPT_PULL = 1
				except:
					OK_PRE_OPT_PULL = 0
				#
				if OK_PRE_OPT_PULL == 1:
					# CONNECT TO THE MySQL DATABASE
					try:
						fire_up_sql()
						mysql_is_down = 0
					except:
						mysql_is_down = 1
					# PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					if mysql_is_down != 1:
						print ""
						print "NOTICE! -- SUCCESSFULLY ENTERED THE MAINT_DB CYCLE"
						print "-- -- ---- FOR DB IDENTIFIED AS..."
						print YOURSQLSERVER
						# RUN ROUTINE UNLESS FAULT
						try:
							print ""
							print "-- DETERMINGING DATE TIMEFRAME FOR OLD RECORD REMOVAL."
							datestamp = datetime.now()
							datestamp_today = datestamp.strftime("%Y_%m%d_%H")
							datestamp_now_year = int(datestamp.strftime("%Y"))
							datestamp_delete_year = int(SQL_RETENTION)
							datestamp_delete_year = datestamp_now_year - datestamp_delete_year
							datestamp_delete_year = str(datestamp_delete_year)
							datestamp_delete_tail = datestamp.strftime("_%m%d_%H")
							datestamp_delete_tail = str(datestamp_delete_tail)
							datestamp_delete = datestamp_delete_year + datestamp_delete_tail
							datestamp_delete = str(datestamp_delete)
							print "-- -- TODAY IS..."
							print datestamp_today
							print "-- -- SO WE SHALL DELETE ALL DATA RECORDED ON OR BEFORE..."
							print datestamp_delete
							# CYCLE THROUGH ALL TABLES LISTED IN MYSQL PRESET FILE
							# -- PERFORM SAME MAINTENANCE FOR ALL
							for SQL_MAINTTABLES_INDEX in range(len(SQL_MAINTTABLES)):
								print ""
								print "-- WORKING WITH TABLE IDENTIFIED AS..."
								print SQL_MAINTTABLES[SQL_MAINTTABLES_INDEX]
								# CHECK IF TABLE EXISTS
								sql_query = "SHOW TABLES LIKE '" + SQL_MAINTTABLES[SQL_MAINTTABLES_INDEX] + "'";
								execute_sql_query()
								SQL_MAINTTABLES_INDEX_TEST_IF_EXIST = 0
								SQL_TABLE = "NULL";
								SQL_MAINTTABLES_INDEX_TEST_IF_EXIST = sql_cursor.rowcount
								if SQL_MAINTTABLES_INDEX_TEST_IF_EXIST > 0:
									print "-- -- TABLE PRESENT, PERFORMING MAINTENANCE..."
									SQL_TABLE = SQL_MAINTTABLES[SQL_MAINTTABLES_INDEX]
									try:
										print "-- -- -- PERFORMING NULL or GARBAGE DATA REMOVAL."
										# BEGIN NULL QUERY
										# -- psuedo_query_example = DELETE FROM YOURSQLTABLE WHERE FIELDRETENTION LIKE NULL
										sql_query = "DELETE FROM " + SQL_TABLE + " WHERE " + SQL_RETENTIONFIELD + " LIKE \'NULL%\'"
										print "-- -- -- -- OUR DELETE QUERY IS..."
										print sql_query
										execute_sql_query()
										# END NULL QUERY
										print "-- -- -- -- NULL DATA SUCCESSFULLY REMOVED."
										print "-- -- -- PERFORMING OLD RECORD DATA REMOVAL."
										# BEGIN OLD QUERY
										# -- psuedo_query_example = DELETE FROM YOURSQLTABLE WHERE FIELDRETENTION BETWEEN 0000 AND DATESTAMP_DELETE
										sql_query = "DELETE FROM " + SQL_TABLE + " WHERE " + SQL_RETENTIONFIELD + " BETWEEN \'0000%\' AND \'" + datestamp_delete + "%\'"
										print "-- -- -- -- OUR DELETE QUERY IS..."
										print sql_query
										execute_sql_query()
										# END OLD QUERY
										print "-- -- -- OPTIMIZING MyISAM or INNODB ENGINES ON THIS TABLE."
										# BEGIN OPTIMIZE QUERY 
										if YOUROPTION1 == "OPTIMIZE":
											# -- psuedo_query_example = OPTIMIZE TABLE YOURSQLTABLE
											sql_query = "OPTIMIZE TABLE " + SQL_TABLE
											print "-- -- -- -- OUR OPTIMIZE QUERY IS..."
											print sql_query
											print "-- -- -- -- PERFORMING FULL RE-INDEX and/or REBUILD"
											print "-- -- -- -- PER YOUR REQUEST."
										else:
											# -- psuedo_query_example = CHECK TABLE YOURSQLTABLE [QUICK | FAST | MEDIUM | EXTENDED ]
											sql_query = "CHECK TABLE " + SQL_TABLE + " MEDIUM"
											print "-- -- -- -- OUR OPTIMIZE QUERY IS..."
											print sql_query
											print "-- -- -- -- YOU MUST DECLARE 'OPTIMIZE' TO DO AN ACTUAL"
											print "-- -- -- -- RE-INDEX OR REBUILD."
										execute_sql_query()
										# END OPTIMIZE QUERY
									except:
										print "-- -- -- FATAL ERROR FOR THIS TABLE!"
										print "-- -- -- -- COULD NOT EXECUTE MAINTENANCE QUERIES"
								else:
									print "-- -- YOUR TABLE DOES NOT EXIST!"
						# FAULT
						except:
							mod_openopc_error_options()
						# HOLD A FEW SECONDS TO USERS CAN SEE INFO ON SCREEN
						time.sleep(5)
					# END PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED
					else:
						mod_openopc_error_sql()
					# CLOSE CONNECTION TO MySQL DB
					try:
						sql_cursor.close ()
						sql_connect.close ()
					except:
						mod_openopc_error_sql_close()
				else:
					mod_openopc_error_options()
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# AUTO_LAUNCH
		if YOURCOMMAND1 == 'AUTO_LAUNCH':
			print ""
			print "STARTING ROUTINE - AUTO_LAUNCH"
			if OK_AUTO_LAUNCH == 1:
			# -- AUTO_LAUNCH
			# -- -- A ROUTINE TO AUTO LAUNCH YOUR PRESET SUBROUTINES,
			# -- -- BASED ON YOUR ENTRY IN THE GLOBAL OPTIONS FILE.
			# -- -- YOURCOMMAND1 	... AUTO_LAUNCH
			# -- -- YOUROPTION1	... CONFIRM (anything else just prints help)
				# NAME THIS THREAD
				if YOUROPTION1 == 'CONFIRM':
					THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + YOUROPTION1
				else:
					THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + "VOID"
				name_that_thread()
				print ""
				print "NOTICE! -- SUCCESSFULLY ENTERED THE AUTO_LAUNCH ROUTINE"
				# FIRST TIME THROUGH ROUTINE?
				dumb_waiter_first = 1
				dumb_waiter_first_server = 1
				AUTO_LAUNCH_PROCESS_MONITOR = []
				AUTO_LAUNCH_PROCESS_MONITOR_SERVER = []
				# RUN ROUTINE UNLESS FAULT
				try:
					# RUN INDEFINATELY
					while True:
						# CYCLE THROUGH ALL PRESETS LISTED IN GLOBAL OPTIONS FILE
						# -- PERFORM SAME LAUNCH (FORK) FOR ALL
						AUTO_LAUNCH_INDEX_INTEGER = 0
						for AUTO_LAUNCH_INDEX in range(len(AUTO_LAUNCH)):
							print ""
							print "-- WORKING WITH PRESET IDENTIFIED AS..."
							print AUTO_LAUNCH[AUTO_LAUNCH_INDEX]
							AUTO_LAUNCH_COMMAND_PARTS = AUTO_LAUNCH[AUTO_LAUNCH_INDEX]
							AUTO_LAUNCH_COMMAND_PARTS = AUTO_LAUNCH_COMMAND_PARTS.split(',')
							AUTO_LAUNCH_COMMAND = [PYTHON_EXECUTABLE,MOD_OPENOPC_EXECUTABLE]
							AUTO_LAUNCH_PROCESS = "mod_openopc_" + AUTO_LAUNCH_COMMAND_PARTS[0] + "_" + AUTO_LAUNCH_COMMAND_PARTS[1];
							for AUTO_LAUNCH_COMMAND_PARTS_INDEX in range(len(AUTO_LAUNCH_COMMAND_PARTS)):
								AUTO_LAUNCH_COMMAND.append(AUTO_LAUNCH_COMMAND_PARTS[AUTO_LAUNCH_COMMAND_PARTS_INDEX])
							if dumb_waiter_first == 1:
								print "-- -- ATTEMPTING SPAWN..."
								try:
									AUTO_LAUNCH_PROCESS_MONITOR.insert(AUTO_LAUNCH_INDEX_INTEGER,subprocess.Popen(AUTO_LAUNCH_COMMAND))
									print "-- -- -- SUCCESSFUL LAUNCH."
								except:
									print "-- -- -- FATAL ERROR !"
									print "-- -- -- UNABLE TO EXECUTE LAUNCH."
								# HOLD A FEW SECONDS SO WE DON'T PUMMEL THE OPC SERVER
								# INTO AN OVERLOAD
								time_to_sleep = random.randrange(3,6)
								time.sleep(time_to_sleep)
							else:
								print "-- -- VERIFYING LAUNCHED PROCESS'S PERSISTENCE..."
								print AUTO_LAUNCH_PROCESS
								try:
									AUTO_LAUNCH_PROCESS_PERSISTENCE = AUTO_LAUNCH_PROCESS_MONITOR[AUTO_LAUNCH_INDEX_INTEGER].poll()
									if AUTO_LAUNCH_PROCESS_PERSISTENCE:
										print "-- -- -- ERROR !"
										print "-- -- -- PROCESS HAS FAILED, RE-LAUNCHING."
										AUTO_LAUNCH_PROCESS_MONITOR[AUTO_LAUNCH_INDEX_INTEGER].wait()
										AUTO_LAUNCH_PROCESS_MONITOR[AUTO_LAUNCH_INDEX_INTEGER] = "x"
										time.sleep(3)
										AUTO_LAUNCH_PROCESS_MONITOR[AUTO_LAUNCH_INDEX_INTEGER] = subprocess.Popen(AUTO_LAUNCH_COMMAND)
										print "-- -- -- -- SUCCESSFULLY RE-LAUNCHED."
										time.sleep(0.5)
									else:
										print "-- -- -- VERIFIED."
								except:
									print "-- -- -- FATAL ERROR !"
									print "-- -- -- COULD NOT VERIFY -NOR- RE-LAUNCH PROCESS."
							AUTO_LAUNCH_INDEX_INTEGER = AUTO_LAUNCH_INDEX_INTEGER + 1
						# UNSET FIRST TIME THROUGH ROUTINE
						dumb_waiter_first = 0

						# CYCLE THROUGH ALL OPC SERVERS LISTED IN GLOBAL OPTIONS FILE
						# -- PERFORM SAME SCHEDULED RESET FOR ALL (BASED ON A CYCLE, NOT
						#    A PARTICULAR TIME.  SO, DEPENDING ON WHEN YOU LAUNCHED THE
						#    AUTO LAUNCHER, IT'LL RESET EVERY 'X' HOURS, NOT AT A 
						#    PARTICULAR TIME.
						if GATEWAY_LIST_TO_RESET[0] != 'NONE':
							AUTO_LAUNCH_INDEX_INTEGER_SERVER = 0
							for GATEWAY_LIST_TO_RESET_INDEX in range(len(GATEWAY_LIST_TO_RESET)):
								print "-- WORKING WITH AUTO-RESETTING OPC SERVER"
								print "   IDENTIFIED AS..."
								print GATEWAY_LIST_TO_RESET[GATEWAY_LIST_TO_RESET_INDEX]
								GATEWAY_RESET_COMMAND_PARTS = GATEWAY_LIST_TO_RESET[GATEWAY_LIST_TO_RESET_INDEX]
								GATEWAY_RESET_COMMAND_PARTS = GATEWAY_RESET_COMMAND_PARTS.split(',')
								GATEWAY_RESET_COMMAND = [PYTHON_EXECUTABLE,MOD_OPENOPC_EXECUTABLE,"GATEWAY_RESET_DAEMON"]
								GATEWAY_RESET_PROCESS = "mod_openopc_GATEWAY_RESET_DAEMON_" + "_" + GATEWAY_RESET_COMMAND_PARTS[0];
								GATEWAY_RESET_COMMAND_PARTS_COUNT = 0
								for GATEWAY_RESET_COMMAND_PARTS_INDEX in range(len(GATEWAY_RESET_COMMAND_PARTS)):
									GATEWAY_RESET_COMMAND_PARTS_COUNT = GATEWAY_RESET_COMMAND_PARTS_COUNT + 1
									if GATEWAY_RESET_COMMAND_PARTS_COUNT == 1:
										GATEWAY_RESET_COMMAND_PARTS_ID_OPCSERVER = GATEWAY_RESET_COMMAND_PARTS[GATEWAY_RESET_COMMAND_PARTS_INDEX]
									if GATEWAY_RESET_COMMAND_PARTS_COUNT == 2:
										GATEWAY_RESET_COMMAND_PARTS_ID_DISCONNECTDELAY = GATEWAY_RESET_COMMAND_PARTS[GATEWAY_RESET_COMMAND_PARTS_INDEX]
									if GATEWAY_RESET_COMMAND_PARTS_COUNT == 3:
										GATEWAY_RESET_COMMAND_PARTS_ID_HOURSBETWEENRESETS = GATEWAY_RESET_COMMAND_PARTS[GATEWAY_RESET_COMMAND_PARTS_INDEX]
								GATEWAY_RESET_COMMAND.append(GATEWAY_RESET_COMMAND_PARTS_ID_OPCSERVER)
								GATEWAY_RESET_COMMAND.append(GATEWAY_RESET_COMMAND_PARTS_ID_DISCONNECTDELAY)
								GATEWAY_RESET_COMMAND.append(GATEWAY_RESET_COMMAND_PARTS_ID_HOURSBETWEENRESETS)
								if GATEWAY_RESET_COMMAND_PARTS_COUNT == 3:
									if dumb_waiter_first_server == 1:
										print "-- -- ATTEMPTING SPAWN..."
										try:
											AUTO_LAUNCH_PROCESS_MONITOR_SERVER.insert(AUTO_LAUNCH_INDEX_INTEGER_SERVER,subprocess.Popen(GATEWAY_RESET_COMMAND))
											print "-- -- -- SUCCESSFUL LAUNCH."
										except:
											print "-- -- -- FATAL ERROR !"
											print "-- -- -- UNABLE TO EXECUTE LAUNCH."
									else:
										print "-- -- VERIFYING LAUNCHED SERVER DAEMON PROCESS'S PERSISTENCE..."
										print GATEWAY_RESET_PROCESS
										try:
											AUTO_LAUNCH_PROCESS_PERSISTENCE_SERVER = AUTO_LAUNCH_PROCESS_MONITOR_SERVER[AUTO_LAUNCH_INDEX_INTEGER_SERVER].poll()
											if AUTO_LAUNCH_PROCESS_PERSISTENCE_SERVER:
												print "-- -- -- ERROR !"
												print "-- -- -- GATEWAY_RESET_DAEMON PROCESS HAS FAILED, RE-LAUNCHING."
												AUTO_LAUNCH_PROCESS_MONITOR_SERVER[AUTO_LAUNCH_INDEX_INTEGER_SERVER].wait()
												AUTO_LAUNCH_PROCESS_MONITOR_SERVER[AUTO_LAUNCH_INDEX_INTEGER_SERVER] = "x"
												time.sleep(3)
												AUTO_LAUNCH_PROCESS_MONITOR_SERVER[AUTO_LAUNCH_INDEX_INTEGER_SERVER] = subprocess.Popen(GATEWAY_RESET_COMMAND)
												print "-- -- -- -- SUCCESSFULLY RE-LAUNCHED."
												time.sleep(0.5)
											else:
												print "-- -- -- VERIFIED."
										except:
											print "-- -- -- FATAL ERROR !"
											print "-- -- -- COULD NOT VERIFY -NOR- RE-LAUNCH PROCESS."
								else:
									print "-- -- -- FATAL ERROR !"
									print "-- -- -- UNABLE TO EXECUTE LAUNCH."
								AUTO_LAUNCH_INDEX_INTEGER_SERVER = AUTO_LAUNCH_INDEX_INTEGER_SERVER + 1

							# UNSET FIRST TIME THROUGH ROUTINE
							dumb_waiter_first_server = 0
						else:
							pass

						# RECYCLE DELAY
						print ""
						print "-- waiting 5 seconds before next verification of process persistence..."
						time.sleep(5)
						print ""

				# FAULT
				except:
					mod_openopc_error_autolaunch()
				# HOLD A FEW SECONDS TO USERS CAN SEE INFO ON SCREEN
				time.sleep(5)
			# PN ------------------ END GUTS_OF_AUTO_LAUNCH ------------------- END PN
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# GATEWAY_RESET_DAEMON
		if YOURCOMMAND1 == 'GATEWAY_RESET_DAEMON':
			print ""
			print "STARTING ROUTINE - GATEWAY_RESET_DAEMON"
			if OK_GATEWAY_RESET_DAEMON == 3:
			# -- GATEWAY_RESET_DAEMON
			# -- -- A ROUTINE TO RESET THE mod_openopopc GATEWAY
			# -- -- YOURCOMMAND1 	... GATEWAY_RESET
			# -- -- YOUROPTION1	... IPv4 or IPv6 ADDRESS OF GATEWAY
			# -- -- YOUROPTION2	... DELAY IN SECONDS TO ALLOW 
			#			CLIENTS TO DISCONNECT
			# -- -- YOUROPTION3	... RECYCLE TIME BETWEEN RESETS IN HOURS
				# NAME THIS THREAD
				THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + str(YOUROPTION1) + "_" + YOUROPTION2 + "s_" + YOUROPTION3 + "h"
				name_that_thread()
				#
				# WHICH ONE ARE WE RUNNING
				#
				print ""
				print "NOTICE! -- SUCCESSFULLY ENTERED THE GATEWAY_RESET_DAEMON CYCLE."
				# MASH VARS AS NEEDED
				GATEWAY_RESET_DAEMON_RECYCLE_DELAY = float(YOUROPTION3)
				GATEWAY_RESET_DAEMON_RECYCLE_DELAY_DISPLAY = str(GATEWAY_RESET_DAEMON_RECYCLE_DELAY)
				GATEWAY_RESET_DAEMON_RECYCLE_DELAY_HALVED = GATEWAY_RESET_DAEMON_RECYCLE_DELAY / 2
				GATEWAY_RESET_DAEMON_RECYCLE_DELAY_HALVED_DISPLAY = str(GATEWAY_RESET_DAEMON_RECYCLE_DELAY_HALVED)
				GATEWAY_RESET_DAEMON_RECYCLE_DELAY_HALVED_SECONDS = GATEWAY_RESET_DAEMON_RECYCLE_DELAY_HALVED * 3600
				GATEWAY_RESET_DAEMON_DISCONNECT_DELAY = float(YOUROPTION2) * 125 / 100
				GATEWAY_RESET_DAEMON_DISCONNECT_DELAY = int(GATEWAY_RESET_DAEMON_DISCONNECT_DELAY)
				GATEWAY_RESET_DAEMON_OPC_SERVER = YOUROPTION1
				# BUILD RESET COMMAND
				GATEWAY_RESET_DAEMON_COMMAND_TO_CALL_RESET = [PYTHON_EXECUTABLE,MOD_OPENOPC_EXECUTABLE,str("GATEWAY_RESET"),str(GATEWAY_RESET_DAEMON_OPC_SERVER),str(GATEWAY_RESET_DAEMON_DISCONNECT_DELAY)]
				GATEWAY_RESET_DAEMON_COMMAND_TO_CALL_RESET_DISPLAY = str(GATEWAY_RESET_DAEMON_COMMAND_TO_CALL_RESET[0]) + " " + str(GATEWAY_RESET_DAEMON_COMMAND_TO_CALL_RESET[1]) + " " + str(GATEWAY_RESET_DAEMON_COMMAND_TO_CALL_RESET[2]) + " " + str(GATEWAY_RESET_DAEMON_COMMAND_TO_CALL_RESET[3]) + " " + str(GATEWAY_RESET_DAEMON_COMMAND_TO_CALL_RESET[4])
				# RUN ROUTINE UNLESS FAULT
				GATEWAY_RESET_DAEMON_FAULT = 0
				while GATEWAY_RESET_DAEMON_FAULT == 0:
					try:
						print ""
						stamp_date()
						print "-- UPDATE - THE CURRENT TIME IS: " + datestamp + "."
						print "-- -- NEXT RESET IN " + GATEWAY_RESET_DAEMON_RECYCLE_DELAY_HALVED_DISPLAY + " hours."
						print "-- -- WILL USE COMMAND..."
						print "-- -- " + GATEWAY_RESET_DAEMON_COMMAND_TO_CALL_RESET_DISPLAY
						print "-- -- snoooooooooooooozzzzzzeeeeeee..."
						time.sleep(GATEWAY_RESET_DAEMON_RECYCLE_DELAY_HALVED_SECONDS)
						print ""
						stamp_date()
						print "-- UPDATE - THE CURRENT TIME IS: " + datestamp + "."
						print "-- -- CALLING FOR A RESET"
						print ""
						GATEWAY_RESET_FORK_COMPLETE = 0
						GATEWAY_RESET_FORK_TIME = 0
						GATEWAY_RESET_FORK = subprocess.Popen(GATEWAY_RESET_DAEMON_COMMAND_TO_CALL_RESET)
						while GATEWAY_RESET_FORK_COMPLETE == 0:
							GATEWAY_RESET_FORK_RETURNCODE = GATEWAY_RESET_FORK.poll()
							if GATEWAY_RESET_FORK_RETURNCODE != None:
								stamp_date()
								print "-- UPDATE - THE CURRENT TIME IS: " + datestamp + "."
								print "-- -- RESET PROCESS JOB COMPLETE"
								GATEWAY_RESET_FORK = "x"
								GATEWAY_RESET_FORK_COMPLETE = 1
							else:
								stamp_date()
								print "-- UPDATE - THE CURRENT TIME IS: " + datestamp + "."
								print "-- -- RESET PROCESS JOB STILL RUNNING"
							time.sleep(30)
							GATEWAY_RESET_FORK_TIME = GATEWAY_RESET_FORK_TIME + 30
							if GATEWAY_RESET_FORK_TIME > 600:
								GATEWAY_RESET_FORK.terminate()
								GATEWAY_RESET_FORK.wait()
								GATEWAY_RESET_FORK = "x"
								stamp_date()
								print "-- UPDATE - THE CURRENT TIME IS: " + datestamp + "."
								print "-- -- RESET PROCESS KILLED"
								GATEWAY_RESET_FORK_COMPLETE = 1
						print ""
						stamp_date()
						print "-- UPDATE - THE CURRENT TIME IS: " + datestamp + "."
						print "-- -- CALL FOR RESET COMPLETE"
						print ""
						stamp_date()
						print "-- UPDATE - THE CURRENT TIME IS: " + datestamp + "."
						print "-- -- NEXT RESET IN " + GATEWAY_RESET_DAEMON_RECYCLE_DELAY_DISPLAY + " hours."
						print "-- -- WILL USE COMMAND..."
						print "-- -- " + GATEWAY_RESET_DAEMON_COMMAND_TO_CALL_RESET_DISPLAY
						print "-- -- snoooooooooooooozzzzzzeeeeeee..."
						time.sleep(GATEWAY_RESET_DAEMON_RECYCLE_DELAY_HALVED_SECONDS)
					# FAULT
					except:
						print ""
						stamp_date()
						print "-- UPDATE - THE CURRENT TIME IS: " + datestamp + "."
						print "ERROR!-- RESET EXECUTION FAILED!"
						time.sleep(5)
						GATEWAY_RESET_DAEMON_FAULT = 1
				#HOLD A FEW SECONDS TO USERS CAN SEE INFO ON SCREEN
				time.sleep(5)			
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# GATEWAY_RESET
		if YOURCOMMAND1 == 'GATEWAY_RESET':
			print ""
			print "STARTING ROUTINE - GATEWAY_RESET"
			if OK_GATEWAY_RESET == 2:
			# -- GATEWAY_RESET
			# -- -- A ROUTINE TO RESET THE OPENOPC GATEWAY AND SERVER
			# -- -- YOURCOMMAND1 	... GATEWAY_RESET
			# -- -- YOUROPTION1	... TARGET, THE NAME OF THE SERVER
			#			AS CORRESPONDS TO YOUR SERVER PRESETS
			# -- -- YOUROPTION2	... DELAY IN SECONDS TO ALLOW 
			#			CLIENTS TO DISCONNECT
				# NAME THIS THREAD
				THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + str(YOUROPTION1) + "_IN_PROGRESS"
				name_that_thread()
				#
				# WHICH ONE ARE WE RUNNING
				YOUROPCSERVER = YOUROPTION1
				IP_OF_GATEWAY_FOR_SERVER = YOUROPTION1
				YOURDELAY = YOUROPTION2
				# THE DELAY IS DEPENDANT UPON SYSTEM PERFORMANCE, SLOW BUGGERS NEED
				# MORE TIME, BUT 15 SECONDS SHOULD BE A REASONABLE ABSOLUTE MINIMUM
				# THAT'LL COVER EVEN THE SLOWEST MACHINES (AGAIN, WITHIN REASON, YOUR
				# PENTIUM II RUNNING OFF FLOPPIES DOESN'T COUNT).  WE ASSUME THE ADMIN
				# CAN CHOOSE A GOOD DELAY FOR HIS SYSTEM, BUT JUST INCASE THEY TRY TO
				# PASS A 1 SECOND DELAY, WE'LL OVERRIDE HERE.
				if YOURDELAY < 15:
					YOURDELAY = 15
				#
				# SCAN NEEDED PRESETS AND OPTIONS
				try:
					pull_in_opc()
					OK_PRE_OPT_PULL = 1
				except:
					OK_PRE_OPT_PULL = 0
				#
				if OK_PRE_OPT_PULL == 1:
					print ""
					print "NOTICE! -- SUCCESSFULLY ENTERED THE GATEWAY_RESET CYCLE."
					# RUN ROUTINE UNLESS FAULT
					try:
						GW_HANDSHAKE_BREAK = 0
						while GW_HANDSHAKE_BREAK == 0:
							# SEND RESET COMMAND TO OPC SERVER
							print ""
							print "-- -- SENDING RESET COMMAND TO OPC SERVER..."
							GW_MONITOR_HANDSHAKE = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							GW_MONITOR_HANDSHAKE.connect((IP_OF_GATEWAY_FOR_SERVER, mod_openopc_SOCKET))
							if SERVER_RESTART_WITH_GATEWAY == 'yes':
								# -- RESET GATEWAY AND OPC SERVER ON REMOTE HOST
								GW_MONITOR_HANDSHAKE.send(str(GATEWAY_COMM_CMD_GATEWAY_RESET_WITH_OPC_SERVER_TO_SEND + "XXX" + SERVER_STOP_CMD_LINE_INPUT + "YYY" + SERVER_START_CMD_LINE_INPUT + "ZZZ"))
							else:
								# -- RESET JUST GATEWAY
								GW_MONITOR_HANDSHAKE.send(GATEWAY_COMM_CMD_GATEWAY_RESET_TO_SEND)
							GW_MONITOR_HANDSHAKE_DATA = GW_MONITOR_HANDSHAKE.recv(4096)
							# THIS IS SUPPOSED TO JIVE, ELSE WE DON'T KNOW WHO WE'RE TALKING TO
							if GW_MONITOR_HANDSHAKE_DATA == GATEWAY_COMM_CMD_CONFIRM_TO_SEND:
								print "-- STARTING RESET JOB on " + YOUROPCSERVER + "."
								YOURDELAY = str(YOURDELAY)
								print ""
								print "-- -- your fudged delay to allow clients to disconnect is..."
								print "-- -- " + YOURDELAY + " seconds."
								# RESET HOOK FILES
								RESETSERVERSTATEFILE = IP_OF_GATEWAY_FOR_SERVER + ".state"
								RESETSERVERSTATEFILE = os.path.join(PROGPATH_RESET, RESETSERVERSTATEFILE)
								# LEAVE RUN MODE BY UPDATING STATE FILE
								ACTIVE_FILE = open(RESETSERVERSTATEFILE, "w")
								ACTIVE_FILE.write("[reset_state]\n")
								ACTIVE_FILE.write("RESET_STATE:RESET\n")
								ACTIVE_FILE.write("HANG_TIME:" + YOURDELAY + "\n")
								ACTIVE_FILE.close()
								# RELEASE PERMISSIONS ON STATE FILE
								os.chmod(RESETSERVERSTATEFILE, 0777)
								# WAIT YOURDELAY TO ALLOW CLIENTS TO DISCONNECT
								print ""
								print "-- -- WAITING 'YOURDELAY' SECONDS TO ALLOW CLIENTS"
								print "-- -- TO DISCONNECT CLEANLY."
								YOURDELAY = int(YOURDELAY)
								time.sleep(YOURDELAY)
								# PUSH CONFIRMATION TO GATEWAY_DAEMON
								print ""
								print "-- -- DONE WAITING - SENDING 'OK' TO RESET SIGNAL TO GATEWAY_DAEMON."
								GW_MONITOR_HANDSHAKE.send(GATEWAY_COMM_CMD_CONFIRM_TO_SEND)
							else:
								GW_HANDSHAKE_BREAK = 1
							# CHECK IF OK TO RESUME JOBS
							GW_MONITOR_HANDSHAKE_DATA = GW_MONITOR_HANDSHAKE.recv(4096)
							GW_MONITOR_HANDSHAKE.close()
							if GW_MONITOR_HANDSHAKE_DATA == GATEWAY_COMM_CMD_PROCEED_WITH_JOBS_TO_SEND:
								print ""
								print "-- -- RE-ENTERING RUN MODE..."
							else:
								print ""
								print "-- -- WARNING: GARBAGE DATA RECEIVED BACK ON THE LINE"
								print "-- -- -- WE WILL RE-ENTER RUN MODE, BUT WAIT 3 MINUTES"
								print "-- -- -- FIRST."
								print "-- -- -- YOUR DEVICES MAY GENERATE FAULTS, AS THERE"
								print "-- -- - -MAY BE AN ISSUE!"
								time.sleep(180)
							# RE-ENTER RUN MODE BY UPDATING STATE FILE
							YOURDELAY = str(YOURDELAY)
							ACTIVE_FILE = open(RESETSERVERSTATEFILE, "w")
							ACTIVE_FILE.write("[reset_state]\n")
							ACTIVE_FILE.write("RESET_STATE:RUN\n")
							ACTIVE_FILE.write("HANG_TIME:" + YOURDELAY + "\n")
							ACTIVE_FILE.close()
							# RELEASE PERMISSIONS ON STATE FILE
							os.chmod(RESETSERVERSTATEFILE, 0777)
							# RESET IS COMPLETE
							print ""
							print "-- RESET JOB COMPLETE."
							GW_HANDSHAKE_BREAK = 1
					# FAULT
					except:
						print ""
						print "ERROR!-- RESET FAILED!"
						print "-- CHECK YOUR GLOBAL OPTIONS AND"
						print "THE MANNER IN WHICH YOU CALL THIS"
						print "ROUTINE, THEN TRY AGAIN."
						print "ALSO! -- YOU MAY HAVE TO MANUALLY"
						print "RESTART ALL OF YOUR CLIENTS."
						print "USE SYSTEM MONITOR or TOP TO"
						print "ASSESS YOUR STATUS FIRST."
					#HOLD A FEW SECONDS TO USERS CAN SEE INFO ON SCREEN
					time.sleep(5)			
				else:
					mod_openopc_error_options()
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# TEST_FOR_ECHO
		if YOURCOMMAND1 == 'TEST_FOR_ECHO':
			print ""
			print "STARTING ROUTINE - TEST_FOR_ECHO"
			if OK_TEST_FOR_ECHO == 1:
			# -- TEST_FOR_ECHO
			# -- -- A ROUTINE TO CHECK CONNECTIVITY BETWEEN
			# -- -- MOD_OPENOPC and YOUR OPC SERVER
			# -- -- YOURCOMMAND1 	... TEST_FOR_ECHO
			# -- -- YOUROPTION1	... YOUR OPC SERVER (FROM PRESET FILE)
				# NAME THIS THREAD
				THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + YOUROPTION1
				name_that_thread()
				#
				# SCAN ALL PRESETS AND OPTIONS
				try:
					pull_in_preset()
					pull_in_opc()
					# DECLARE THAT WE HAVE ACHIEVED A GOOD PRESET AND OPTIONS PULL
					OK_PRE_OPT_PULL = 1
				except:
					OK_PRE_OPT_PULL = 0
				#
				if OK_PRE_OPT_PULL == 1:
				# PN ------------------ BEGIN GUTS_OF_TEST_FOR_ECHO ----------- END PN
					try:
						fire_up_gw()
						gateway_is_down = 0
						print ""
						print "NOTICE! -- GATEWAY IS UP AT ADDRESS..."
						print IP_OF_GATEWAY_FOR_SERVER
					except:
						gateway_is_down = 1
						print ""
						print "NOTICE! -- GATEWAY IS DOWN AT ADDRESS..."
						print IP_OF_GATEWAY_FOR_SERVER
					try:
						fire_up_opc()
						opcserver_is_down = 0
						print ""
						print "NOTICE! -- OPC SERVER IS UP WITH NAME..."
						print OPC_SERVER_NAME
					except:
						opcserver_is_down = 1
						print ""
						print "NOTICE! -- OPC SERVER IS DOWN WITH NAME..."
						print OPC_SERVER_NAME
					# PROCEED ONLY IF THE GATEWAY / OPC ARE UP
					# PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED.
					if gateway_is_down != 1:
						# PROCEED ONLY if THE OPCSERVER IS UP
						if opcserver_is_down != 1:
							# IO TEST
							value_test = str(OPC_SERVER_TEST)
							try:
								print ""
								print "TEST FOR ECHO -- POLLING the DESIGNATED TEST PLC"
								value_test = opc.read(value_test)
								# 20160621 -- unsure how this next line came to be, or at
								#             what point it became part of the program.
								#             Observed FAILURE of TEST_FOR_ECHO when using
								#		      brackets, rather than parenthesis, as above.
								# value_test = opc[value_test]
								print "RESPONSE IS..."
								print value_test
								print ""
							except:
								print ""
								print "FAULT -- ATTEMPT TO POLL THE TEST PLC FAILED"
								print "... either the test plc is turned off or the"
								print "opc server (RSLinx) is running in a fault."
								print ""
								print "SUGGESTION -- MAKE SURE TEST PLC IS TURNED ON"
								print "AND THAT YOU CAN PING IT... IF THAT CHECKS OUT,"
								print "RESTART OPC Server (RSLinx) SERVICE ON MACHINE..."
								print IP_OF_GATEWAY_FOR_SERVER
								print ""
						else:
							print ""
							print "FAULT -- OPC SERVER IS DOWN WITH NAME"
							print OPC_SERVER_NAME
							print ""
							print "SUGGESTION -- RESTART OPC Server (RSLinx) SERVICE ON MACHINE..."
							print IP_OF_GATEWAY_FOR_SERVER
							print ""
					else:
						print ""
						print "FAULT -- GATEWAY IS DOWN AT ADDRESS"
						print IP_OF_GATEWAY_FOR_SERVER
						print ""
						print "SUGGESTION -- RESTART mod_openopc GATEWAY_DAEMON ON MACHINE..."
						print IP_OF_GATEWAY_FOR_SERVER
						print ""
					# CLOSE THE OPC CONNECTION
					try:
						opc.close()
						print ""
						print "OPC CONNECTION CLOSED, ALL DONE"
						print ""
					except:
						print ""
						print "NOTICE! -- Failure to close connection to OPC Server,"
						print "hard exit will follow."
						print ""
				#
				# DISPLAY RESULTS
				print ""
				print "NOTICE -- THIS WINDOW WILL STAY VISIBLE FOR 90 SECONDS"
				print "OR UNTIL YOU CLOSE IT."
				time.sleep(90)		
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# SERVER_SEEK
		if YOURCOMMAND1 == 'SERVER_SEEK':
			print ""
			print "STARTING ROUTINE - SERVER_SEEK"
			if OK_SERVER_SEEK == 1:
			# -- SERVER_SEEK
			# -- -- A ROUTINE TO CHECK FOR SERVER_NAME VALUES
			# -- -- AS BROADCOAST BY VARIOUS OPC SERVER SOFTWARE
			# -- -- TO THE GATEWAY SERVICE
			# -- -- YOURCOMMAND1 	... SERVER_SEEK
			# -- -- YOUROPTION1	... YOUR GATEWAY'S IP ADDRESS OR HOSTNAME
				# NAME THIS THREAD
				THREADNAME = "mod_openopc_" + YOURCOMMAND1 + "_" + YOUROPTION1
				name_that_thread()
				#
				# SCAN ALL PRESETS AND OPTIONS
				try:
					pull_in_preset()
					IP_OF_GATEWAY_FOR_SERVER = YOURGATEWAY
					# DECLARE THAT WE HAVE ACHIEVED A GOOD PRESET AND OPTIONS PULL
					OK_PRE_OPT_PULL = 1
				except:
					OK_PRE_OPT_PULL = 0
				#
				if OK_PRE_OPT_PULL == 1:
				# PN ------------------ BEGIN GUTS_OF_TEST_FOR_ECHO ----------- END PN
					try:
						fire_up_gw()
						gateway_is_down = 0
						print ""
						print "NOTICE! -- GATEWAY IS UP AT ADDRESS..."
						print IP_OF_GATEWAY_FOR_SERVER
					except:
						gateway_is_down = 1
						print ""
						print "NOTICE! -- GATEWAY IS DOWN AT ADDRESS..."
						print IP_OF_GATEWAY_FOR_SERVER
					# PROCEED ONLY IF THE GATEWAY IS UP
					# PROCEED ONLY IF THE MySQL SERVER CAN BE CONTACTED.
					if gateway_is_down != 1:
						# IO TEST
						value_test = str(IP_OF_GATEWAY_FOR_SERVER)
						try:
							print ""
							print "SERVER_SEEK -- POLLING the DESIGNATED GATEWAY FOR AVAILABLE OPC SERVER INSTANCES (ONLY RUNNING DISPLAYED)"
							value_test = opc.servers()
							print "RESPONSE IS..."
							print value_test
							print ""
						except:
							print ""
							print "FAULT -- ATTEMPT TO POLL GATEWAY FAILED"
							print "... the gateway may be down."
							print ""
							print "SUGGESTION -- MAKE SURE THE ADDRESS YOU ENTERED"
							print "IS CORRECT AND THE GATEWAY IS RUNNING."
							print IP_OF_GATEWAY_FOR_SERVER
							print ""
					else:
						print ""
						print "FAULT -- GATEWAY IS DOWN AT ADDRESS"
						print IP_OF_GATEWAY_FOR_SERVER
						print ""
						print "SUGGESTION -- RESTART mod_openopc GATEWAY_DAEMON ON MACHINE..."
						print IP_OF_GATEWAY_FOR_SERVER
						print ""
					# CLOSE THE OPC CONNECTION
					try:
						opc.close()
						print ""
						print "OPC CONNECTION CLOSED, ALL DONE"
						print ""
					except:
						print ""
						print "NOTICE! -- Failure to close connection to OPC Server,"
						print "hard exit will follow."
						print ""
				#
				# DISPLAY RESULTS
				print ""
				print "NOTICE -- THIS WINDOW WILL STAY VISIBLE FOR 90 SECONDS"
				print "OR UNTIL YOU CLOSE IT."
				time.sleep(90)		
			else:
				mod_openopc_error_command()
		else:
			pass
		#
		# SETTINGS
		if YOURCOMMAND1 == 'SETTINGS':
			print ""
			print "STARTING ROUTINE - SETTINGS"
			# -- SETTINGS
			# -- -- A ROUTINE TO DISPLAY YOUR GLOBAL OPTIONS SETTINGS
			# -- -- YOURCOMMAND1 	... SETTINGS
			# NAME THIS THREAD
			THREADNAME = "mod_openopc_" + YOURCOMMAND1
			name_that_thread()
			#
			print ""
			print "NOTICE! -- YOUR PATHS ARE AUTO-DEFINED"
			print "AS FOLLOWS..."
			print "-- PROGPATH= " + PROGPATH
			print "-- PROGPATH_OPTIONS= " + PROGPATH_OPTIONS
			print "-- PROGPATH_OPC= " + PROGPATH_OPC
			print "-- PROGPATH_SQL= " + PROGPATH_SQL
			print "-- PROGPATH_PRE= " + PROGPATH_PRE
			print "-- PROGPATH_PROG= " + PROGPATH_PROG
			print "-- PROGPATH_RESET= " + PROGPATH_RESET
			print "-- PROGPATH_GWCOMM= " + PROGPATH_GWCOMM
			print "-- TEMPDIR= " + TEMPDIR
			print ""
			print "NOTICE! -- YOUR RUNTIME PARAMETERS ARE DEFINED"
			print "IN THE GLOBAL OPTIONS FILE AS FOLLOWS..."
			print "-- FLAVOR= " + FLAVOR
			print "-- MINIMALRESPONSE= " + VERBOSE
			print ""
			print "NOTICE! -- YOUR SYSTEM COMMANDS ARE DEFINED IN"
			print "THE GLOBAL OPTIONS FILE AS FOLLOWS..."
			print "-- YOUR CMD TO PYTHON IS..."
			print PYTHON_EXECUTABLE
			print ""
			print "NOTICE! -- YOUR THROTTLING and LOAD HANDLING IS"
			print "DEFINED IN THE GLOBAL OPTIONS FILE AS FOLLOWS..."
			print "-- YOUR GROUPBUILD_TIMEOUT_OVERRIDE IS (seconds)..."
			print GROUPBUILD_TIMEOUT_OVERRIDE
			print ""
			print "NOTICE! -- YOUR NETWORK IS DEFINED IN THE GLOBAL"
			print "OPTIONS FILE AS FOLLOWS..."
			print "-- YOUR IP ADDRESS= " + MYIP
			print "-- YOUR GATEWAY= " + MYDEFAULTGATEWAY
			print ""
			print "NOTICE! -- YOUR OPENOPC TIE IN IS DEFINED IN THE"
			print "GLOBAL OPTIONS FILE AS FOLLOWS..."
			print OPENOPC_TIE_IN
			print ""
			print "NOTICE! -- THE FOLLOWING PRESETS ARE SETUP FOR AUTO LAUNCH"
			print "IN THE GLOBAL OPTIONS FILE AS FOLLOWS..."
			for AUTO_LAUNCH_INDEX in range(len(AUTO_LAUNCH)):
				print "-- SPAWN --> " + AUTO_LAUNCH[AUTO_LAUNCH_INDEX]
			print ""
			print "NOTICE! -- THE FOLLOWING OPC SERVERS ARE SET TO AUTOMATICALLY"
			print "RESET AS IN THE GLOBAL OPTIONS FILE AS FOLLOWS..."
			for GATEWAY_LIST_TO_RESET_INDEX in range(len(GATEWAY_LIST_TO_RESET)):
				print "-- SCHEDULE AUTO RESET FOR --> " + GATEWAY_LIST_TO_RESET[GATEWAY_LIST_TO_RESET_INDEX]
			print ""
			print "NOTICE -- THIS WINDOW WILL STAY VISIBLE FOR 90 SECONDS"
			print "OR UNTIL YOU CLOSE IT."
			time.sleep(90)
		else:
			pass
	#
	else:
		mod_openopc_error_global_options()
	#
else:
	pass

# -------------------------------------------------------------------
#
# --------------------- MODE EXECUTION ------------------------------
# --------------------- -- HELP -------------------------------------
if YOURCOMMAND1 == 'HELP':
	print ""
	print "STARTING ROUTINE - HELP"
	print ""
	print "Welcome to mod_openopc(2)."
	print "-------------------------"
	print ""
	print "This is a fork two projects..."
	print "-- the original mod_openopc, version 0.1.1_rc_2"
	print "-- OpenOPC, version 1.1.6"
	print ""
	print "Editing the global options file and making some standard"
	print "Unix/Linux -to- Win32 file/path name changes in"
	print "presets and such, the program is also cross-platform."
	print ""
	print "This is a very generic helpfile, so you really should"
	print "refer to the README file and other documentation"
	print "within the HELP folder, it will do you much better"
	print "to properly set this program up prior to running it,"
	print "because the consequences of writing improper values"
	print "to what may be your mission critical OPC devices, or"
	print "worse, corrupting those devices, is very possible..."
	print ""
	print "Why?  Because this is a power tool... enabling you"
	print "to do as much as possible - it assumes you"
	print "to be competent and to have 'RTFM' already."
	print ""
	print "BASIC USAGE..."
	print "--------------"
	print ""
	print "/path/to/python /opt/mod_openopc_2/prog/mod_openopc.py [ARGS]"
	print ""
	print "ARGUMENTS..."
	print "------------"
	print ""
	print "mod_openopc.py READ [preset_file] [scan_interval] [UPDATE | -blank-]"
	print "-- -- READ, repeatedly, from an OPC device and log to DB"
	print "-- -- the 'UPDATE' command line option requires a modified preset"
	print "-- -- file, and it will delete all but the most recent record for"
	print "-- -- each individual 'leaf_name' ('leaf_sql_name' / 'machine name');"
	print "-- -- so please reference the README first!"
	print "mod_openopc.py READ_ONE_SHOT [preset_file] [scan_interval}"
	print "-- -- READ, once, from an opc device and log to DB"
	print "mod_openopc.py WRITE [preset_file] [scan_interval]"
	print "-- -- WRITE, only one time, values from your preset file to"
	print "-- -- an OPC device."
	print "mod_openopc.py WRITE_ONE_SHOT [LEAFS&VALUES] [scan_interval] [OPC_SERVER] [SQL_SERVER]"
	print "-- -- WRITE, only one time, value provided on command line to an"
	print "-- -- OPC device.  The declaration of a scan_interval is more"
	print "-- -- for a timeout of sorts than anything else, sames goes"
	print "-- -- for the BRIDGE routine later on.  And the declaration of"
	print "-- -- and SQL_SERVER is to allow error and fault logging only."
	print "mod_openopc.py BRIDGE [preset_file] [bridge_interval] [OVERRIDE | -blank- ]"
	print "-- -- performs a bridge (read from source OPC device, write"
	print "-- -- to target OPC device) between two OPC devices on the"
	print "-- -- same OPC server.  Good as a simpler messaging routine"
	print "-- -- when otherwise complex PLC or device messaging would"
	print "-- -- be necessary. OVERRIDE must be declared unless the"
	print "-- -- bridge interval (in seconds) is equal to or greater"
	print "-- -- than the mod_openopc global minimum scan interval."
	print "mod_openopc.py SPACE_BRIDGE [preset_file] [bridge_interval] [OVERRIDE | -blank- ]"
	print "-- -- performs a bridge (read from source OPC device, write"
	print "-- -- to target OPC device) between two OPC devices on"
	print "-- -- different OPC servers / networks.  Good as an effective"
	print "-- -- means of communicating across dissimilar vendor networks,"
	print "-- -- such as MODBUS to Data Highway, or Allen Bradley Ethernet"
	print "-- -- to Koyo Ethernet, etc... OVERRIDE must be declared unless"
	print "-- -- bridge interval (in seconds) is equal to or greater"
	print "-- -- than the mod_openopc global minimum scan interval."
	print "mod_openopc.py MAINT_DB [OPTIMIZE | -blank- ]"
	print "-- -- performs deletion and cleanup of NULL records"
	print "-- -- in your MySQL databases, and deletes old"
	print "-- -- records based upon their RETENTION field, as"
	print "-- -- defined by you in the database configuration files."
	print "-- -- 'OPTIMIZE' flag will call for a MySQL OPTIMIZE to be"
	print "-- -- issued upon the table in question."
	print "-- -- you should optimize MyISAM but not InnoDB tables."
	print "mod_openopc.py AUTO_LAUNCH CONFIRM"
	print "-- -- auto launches all subroutines or mod_openopc commands"
	print "-- -- which are defined to auto launch in the global options"
	print "-- -- file."
	print "-- -- this is a great command to use at system startup,"
	print "-- -- rather than calling all of your presets individually."
	print "-- -- you should still test your individual presets first by"
	print "-- -- running them individually, so you can observe their"
	print "-- -- output in verbose mode... the auto launcher hides all"
	print "-- -- output in the background."
	print "-- -- the CONFIRM argument is required, anything else"
	print "-- -- will simply display all the items listed to auto launch"
	print "-- -- along with the help-file, but not actually launch them."
	print "-- -- NOTE!"
	print "-- -- -- Unix flavors should call AUTO_LAUNCH as follows..."
	print "-- -- -- [path-to]/nohup [path-to]/python [path-to]mod_openopc.py AUTO_LAUNCH CONFIRM 2>/dev/null 1>/dev/null &"
	print "-- -- -- The above is recommend for use in your 'rc.local' or"
	print "-- -- -- startup file."
	print "mod_openopc.py GATEWAY_RESET_DAEMON [gateway] [delay] [recycle time]"
	print "-- -- this is intended to be called internally by AUTO_LAUNCH"
	print "-- -- in order to provide a psuedo-scheduler for GATEWAY_RESET"
	print "-- -- calls, rather than having to call GATEWAY_RESET from your"
	print "-- -- OS task scheduler."
	print "-- -- delay = delay in seconds"
	print "-- -- recycle time = hours between resets"
	print "mod_openopy.py GATEWAY_RESET [opc_server] [delay]"
	print "-- -- performs a reset of the mod_openopc GATEWAY_DAEMON"
	print "-- -- This is used as a measure to deal with the OPC"
	print "-- -- Automation DLL memory leak.  Workaround, not a fix."
	print "-- -- The 'delay' is the delay in seconds that you wish"
	print "-- -- to give your clients to finish up what they're"
	print "-- -- doing and disconnect.  This should be set to no"
	print "-- -- less than the maximum scan time of any client"
	print "-- -- routine accessing the server in question."
	print "mod_openopc.py GATEWAY_DAEMON [opc_server]"
	print "-- -- this will launch the GATEWAY startup and monitoring"
	print "-- -- service.  This should be run on your Win32 based"
	print "-- -- OPC Server virtual guest or dedicated machine, and"
	print "-- -- and controlls startup and recycling of your mod_openopc"
	print "-- -- Gateway and your OPC Server(s). You must supply the"
	print "-- -- actual win service name of your OPC Server Software."
	print "mod_openopc.py TEST_FOR_ECHO [opc_server]"
	print "-- -- an easy way to check for problems with"
	print "-- -- the connection between 'this' machine, running"
	print "-- -- mod_openopc, and the machine running your OPC"
	print "-- -- server.  Even if they're the same machine,"
	print "-- -- such as if you're running Win32, this will"
	print "-- -- allow you to determine what is and isn't"
	print "-- -- working if you have trouble getting started"
	print "-- -- or experience a system failure."
	print "mod_openopc.py SERVER_SEEK [gateway_ip_address]"
	print "-- -- the best way to check for the SERVER_NAME(s)"
	print "-- -- of OPC server software packages running on the"
	print "-- -- same machine that the GATEWAY service is on."
	print "-- -- Sometimes, server software packages don't use"
	print "-- -- common or simple names, and sometimes they're"
	print "-- -- not consistent.  In the case of RSLinx (Rockwell),"
	print "-- -- the Windows Service, SERVER_NAME, and"
	print "-- -- Administrative Tools entry do not match.... so,"
	print "-- -- it is up to you to be sure."
	print "mod_openopc.py SETTINGS"
	print "-- -- will give you a rundown of your globaloptions"
	print "-- -- file settings, as you entered them."
	print "-- -- useful as a reference or for troubleshooting."
	print "mod_openopc.py HELP (or -h , --help, help)"
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

