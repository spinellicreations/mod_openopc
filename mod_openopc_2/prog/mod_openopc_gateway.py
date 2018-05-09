#!/usr/bin/python
# -------------------------------------------------------------------
# mod_openopc	
# -------------------------------------------------------------------
# ... integrating the Python OpenOPC project to run HMI
#     over Linux, BSD, any Unix, and now Shitty Windows
#     in an unfettered manner.
# -------------------------------------------------------------------
# GATEWAY
# ------------------------------------------------------------------- 
#
# --------------------- HARDCODED VARIABLES -------------------------
# --------------------- -- COMMON VARS ------------------------------
import mod_openopc_common
OPC_CLASS = mod_openopc_common.OPC_CLASS
OPC_GATE_PORT = mod_openopc_common.OPC_GATEWAY_PORT
_svc_name_ = mod_openopc_common.OPC_SERVICE_NAME
_svc_display_name_ = mod_openopc_common.OPC_SERVICE_NAME_DISPLAY
mod_openopc_GARBAGE_0 = mod_openopc_common.GARBAGE_0
mod_openopc_GARBAGE_1 = mod_openopc_common.GARBAGE_1
mod_openopc_GARBAGE_2 = mod_openopc_common.GARBAGE_2
# --------------------- -- GARBAGE COLLECTION -----------------------
import gc
gc.set_threshold(mod_openopc_GARBAGE_0,mod_openopc_GARBAGE_1,mod_openopc_GARBAGE_2)
gc.enable()
# --------------------- LOAD LIBRARIES ------------------------------
# --------------------- -- STANDARD ---------------------------------
import socket
import os
import time
import select
# --------------------- -- CORE -------------------------------------
import mod_openopc_library
# --------------------- -- DEPENDANCIES -----------------------------
import win32event
import Pyro.core
import Pyro.protocol
Pyro.config.PYRO_MULTITHREADED = 1
#
# --------------------- GATEWAY -------------------------------------
# --------------------- -- DEFINE COMMAND I/O -----------------------
class opc(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
		self._remote_hosts = {}
		self._init_times = {}
		self._tx_times = {}
#
	def get_clients(self):
		# RETURN A LIST OF SERVER INSTANCES (GUID,host,time) tuples
		reg = self.getDaemon().getRegistered()
		hosts = self._remote_hosts
		init_times = self._init_times
		tx_times = self._tx_times
		hlist = [(k, hosts[k] if hosts.has_key(k) else '', init_times[k], tx_times[k]) for k,v in reg.iteritems() if v == None]
		return hlist
#   
	def create_client(self):
		# CREATE A NEW OPENOPC INSTANCE IN THE PYRO SERVER
		print "-- CREATING A NEW CLIENT INSTANCE"
		try:
			opc_obj = mod_openopc_library.client(OPC_CLASS)
		except:
			print "-- -- FATAL ERROR - CANNOT FIND ANY OF THE AUTOMATION DLL'S"
			print "      (also called 'OPC CLASSES') REGISTERED ON THE SYSTEM."
			print "      DID YOU MAKE SURE TO INSTALL AN OPC SERVER YET?"
			print "      ALSO, IF YOU'RE NOT USING A MAINSTREAM SERVER, THEN YOU"
			print "      MUST BE SURE TO REGISTER THE GRAYBOX AUTOMATION DLL"
			print "      USING SOME VARIANT OF 'regsvr32' WIN OS UTILITY."
		base_obj = Pyro.core.ObjBase()
		base_obj.delegateTo(opc_obj)
		uri = self.getDaemon().connect(base_obj)
		opc_obj._open_serv = self
		opc_obj._open_self = base_obj
		opc_obj._open_host = self.getDaemon().hostname
		opc_obj._open_port = self.getDaemon().port
		opc_obj._open_guid = uri.objectID
		remote_ip = self.getLocalStorage().caller.addr[0]
		try:
			remote_name = socket.gethostbyaddr(remote_ip)[0]
			self._remote_hosts[uri.objectID] = '%s (%s)' % (remote_ip, remote_name)
			print "-- -- SUCCESS @ " + str(remote_ip)
		except socket.herror:
			self._remote_hosts[uri.objectID] = '%s' % (remote_ip)
			print "-- -- FAILED for " + str(remote_ip)
		self._init_times[uri.objectID] =  time.time()
		self._tx_times[uri.objectID] =  time.time()
		return Pyro.core.getProxyForURI(uri)
#
	def release_client(self, obj):
		# RELEASE OPENOPC INSTANCE IN PYRO SERVER
		print "-- RELEASING CLIENT INSTANCE"
		self.getDaemon().disconnect(obj)
		del self._remote_hosts[obj.GUID()]
		del self._init_times[obj.GUID()]
		del self._tx_times[obj.GUID()]
		del obj
		print "-- -- RELEASED"
#
# --------------------- -- DEFINE SERVICE JOB -----------------------
class OpcService():
	def __init__(self):
		self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
#
	def SvcStop(self):
		win32event.SetEvent(self.hWaitStop)
#
	def SvcDoRun(self):
		daemon = Pyro.core.Daemon(port = OPC_GATE_PORT)
		daemon.connect(opc(), "opc")
		print "-- PYRO OPENED LISTENING PORT on " + str(OPC_GATE_PORT)
		while win32event.WaitForSingleObject(self.hWaitStop, 0) != win32event.WAIT_OBJECT_0:
			socks = daemon.getServerSockets()
			ins,outs,exs = select.select(socks,[],[],1)
			for s in socks:
				if s in ins:
					daemon.handleRequests()
					break
				else:
					pass
		print "-- PYRO IS -CLOSING- LISTENING PORT!"
		daemon.shutdown()
# --------------------- -- LAUNCH SERVICE JOB -----------------------
DAEMONIZE_GATEWAY = OpcService()
DAEMONIZE_GATEWAY.SvcDoRun()
# -------------------------------------------------------------------
