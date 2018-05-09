#!/usr/bin/python
# -------------------------------------------------------------------
# mod_openopc	
# -------------------------------------------------------------------
# ... integrating the Python OpenOPC project to run HMI
#     over Linux, BSD, any Unix, and now Shitty Windows
#     in an unfettered manner.
# -------------------------------------------------------------------
# COMMON
# -------------------------------------------------------------------
# 
# --------------------- CORE VARIABLES ------------------------------
# --------------------- -- OPC --------------------------------------
OPC_STATUS = (0, 'Running', 'Failed', 'NoConfig', 'Suspended', 'Test')
BROWSER_TYPE = (0, 'Hierarchical', 'Flat')
ACCESS_RIGHTS = (0, 'Read', 'Write', 'Read/Write')
OPC_QUALITY = ('Bad', 'Uncertain', 'Unknown', 'Good')
OPC_CLASS = 'Graybox.OPC.DAWrapper;'
#OPC_CLASS = 'Graybox.OPC.DAWrapper;Matrikon.OPC.Automation;HSCOPC.Automation;RSI.OPCAutomation;OPC.Automation'
OPC_SERVER = 'iTools OPC Server;Hci.TPNServer;HwHsc.OPCServer;opc.deltav.1;AIM.OPC.1;Yokogawa.ExaopcDAEXQ.1;OSI.DA.1;OPC.PHDServerDA.1;Aspen.Infoplus21_DA.1;National Instruments.OPCLabVIEW;RSLinx OPC Server;KEPware.KEPServerEx.V4;Matrikon.OPC.Simulation;Prosys.OPC.Simulation'
OPC_CLIENT = 'mod_openopc_2'
OPC_SERVICE_NAME = 'mod_openopc_2_gateway'
OPC_SERVICE_NAME_DISPLAY = 'mod_openopc_2_gateway'
VERSION = 'modified_1.1.6_core_002'
# --------------------- -- GARBAGE COLLECTION -----------------------
GARBAGE_0 = 500 	# 200 aggressive / 500 nominal
GARBAGE_1 = 10		# 5 aggressive / 10 nominal
GARBAGE_2 = 10		# 5 aggressive / 10 nominal
# --------------------- -- PORTS ------------------------------------
OPC_GATEWAY_PORT = 7766
OPC_GATEWAY_MONITOR_PORT = 7767
#
# --------------------- GATEWAY DAEMON VARIABLES --------------------
# --------------------- -- DIGI-COM ---------------------------------
# ---------------------    DIGITAL REPRESENTATION OF COMM BETWEEN ---
# ---------------------    GATEWAY_DAEMON AND GATEWAY_RESET ----------
GATEWAY_COMM_CMD_INVALID = 77000
GATEWAY_COMM_CMD_INVALID_TO_SEND = str(GATEWAY_COMM_CMD_INVALID)
GATEWAY_COMM_CMD_GATEWAY_RESET = 77001
GATEWAY_COMM_CMD_GATEWAY_RESET_TO_SEND = str(GATEWAY_COMM_CMD_GATEWAY_RESET)
GATEWAY_COMM_CMD_CONFIRM = 77002
GATEWAY_COMM_CMD_CONFIRM_TO_SEND = str(GATEWAY_COMM_CMD_CONFIRM)
GATEWAY_COMM_CMD_PROCEED_WITH_JOBS = 77003
GATEWAY_COMM_CMD_PROCEED_WITH_JOBS_TO_SEND = str(GATEWAY_COMM_CMD_PROCEED_WITH_JOBS)
GATEWAY_COMM_CMD_GATEWAY_RESET_WITH_OPC_SERVER = 77004
GATEWAY_COMM_CMD_GATEWAY_RESET_WITH_OPC_SERVER_TO_SEND = str(GATEWAY_COMM_CMD_GATEWAY_RESET)
# --------------------- -- FIRSTBOOT --------------------------------
# ---------------------    ON FIRSTBOOT, HOW LONG DO WE WAIT TO ALLOW
# ---------------------    BACKEND OPC SERVERS TO STARTUP? (SECONDS)
# ---------------------    SUGGESTED MIN = 30, MAX = 120 ------------
OPC_GATEWAY_MONITOR_FIRSTBOOT_WAIT = 3
# ---------------------	-- RESTART ----------------------------------
# ---------------------    ON RESTART, HOW LONG DO WE WAIT BEFORE ---
# ---------------------    ALLOWING CLIENTS TO ATTEMPT RECONNECT ----
# ---------------------    (SECONDS) SUGGESTED = 5 ------------------
OPC_GATEWAY_MONITOR_RESTART_WAIT = 5
# --------------------- GARBAGE COLLECTION --------------------------
import gc
gc.set_threshold(GARBAGE_0,GARBAGE_1,GARBAGE_2)
gc.enable()
# -------------------------------------------------------------------
