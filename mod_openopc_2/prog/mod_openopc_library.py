#!/usr/bin/python
# -------------------------------------------------------------------
# mod_openopc	
# -------------------------------------------------------------------
# ... integrating the Python OpenOPC project to run HMI
#	  over Linux, BSD, any Unix, and now Shitty Windows
#	  in an unfettered manner.
# -------------------------------------------------------------------
# CORE
# ------------------------------------------------------------------- 
#
# --------------------- HARDCODED VARIABLES -------------------------
# --------------------- -- COMMON VARS ------------------------------
import mod_openopc_common
__version__ = mod_openopc_common.VERSION
OPC_STATUS = mod_openopc_common.OPC_STATUS
BROWSER_TYPE = mod_openopc_common.BROWSER_TYPE
ACCESS_RIGHTS = mod_openopc_common.ACCESS_RIGHTS
OPC_QUALITY = mod_openopc_common.OPC_QUALITY
OPC_CLASS = mod_openopc_common.OPC_CLASS
OPC_SERVER = mod_openopc_common.OPC_SERVER
OPC_CLIENT = mod_openopc_common.OPC_CLIENT
OPC_GATE_PORT = mod_openopc_common.OPC_GATEWAY_PORT
mod_openopc_GARBAGE_0 = mod_openopc_common.GARBAGE_0
mod_openopc_GARBAGE_1 = mod_openopc_common.GARBAGE_1
mod_openopc_GARBAGE_2 = mod_openopc_common.GARBAGE_2
# --------------------- -- GARBAGE COLLECTION -----------------------
import gc
gc.set_threshold(mod_openopc_GARBAGE_0,mod_openopc_GARBAGE_1,mod_openopc_GARBAGE_2)
gc.enable()
# --------------------- LOAD LIBRARIES ------------------------------
# --------------------- -- STANDARD ---------------------------------
import os
import sys
import time
import types
import string
import socket
import re
import Queue
# --------------------- -- DEPENDANCIES -----------------------------
import Pyro
import Pyro.core
import Pyro.protocol
Pyro.config.PYRO_MULTITHREADED = 1
# --------------------- SERVER LIBRARIES ----------------------------
# --------------------- -- DCOM INTEGRATION -------------------------
try:
	import win32com.client
	import win32com.server.util
	import win32event
	import pythoncom
	import pywintypes
	# VARIANT TYPES
	vt = dict([(pythoncom.__dict__[vtype], vtype) for vtype in pythoncom.__dict__.keys() if vtype[:2] == "VT"])
	# GENERATE CACHED WRAPPER OBJECTS
	win32com.client.gencache.is_readonly = False
	# REDUNDANT, BUT SAFE
	win32com.client.gencache.Rebuild()
	# ONLY REQUIRED ON WIN OPC SERVER, NOT ON CLIENT SIDE
	# SO DON'T GO CRAZY IF WE CAN'T LOAD, JUST FLAG
	win32com_found = True
except:
	# FLAG FAIL TO LOAD
	win32com_found = False
# -------------------------------------------------------------------
current_client = None
#
# OPC Constants
SOURCE_CACHE = 1
SOURCE_DEVICE = 2
#
# --------------------- BASIC FUNCTIONS -----------------------------
def quality_str(quality_bits):
	# CONVERT OPC QUALITY BITS TO DESCRIPTIVE STRING
	quality = (quality_bits >> 6) & 3
	return OPC_QUALITY[quality]
#
def type_check(tags):
	# TYPE CHECK AGAINST LIST OF TAGS
	if type(tags) in (types.ListType, types.TupleType):
		single = False
	elif tags == None:
		tags = []
		single = False
	else:
		tags = [tags]
		single = True
	if len([t for t in tags if type(t) not in types.StringTypes]) == 0:
		valid = True
	else:
		valid = False
	return tags, single, valid
#
def wild2regex(string):
	# CONVERT UNIX WILDCARD GLOB INTO REGULAR EXPRESSION
	return string.replace('.','\.').replace('*','.*').replace('?','.').replace('!','^')
#
def tags2trace(tags):
	# CONVERT A LIST OF TAGS INTO A STRING SUITABLE FOR CALLBACK TRACE LOG
	arg_str = ''
	for i,t in enumerate(tags[1:]):
		if i > 0: arg_str += ','
		arg_str += '%s' % t
	return arg_str
#
def exceptional(func, alt_return=None, alt_exceptions=(Exception,), final=None, catch=None):
	# TURN EXCEPTIONS INTO ALTERNATIVE RETURN VALUES
	def _exceptional(*args, **kwargs):
		try:
			try:
				return func(*args, **kwargs)
			except alt_exceptions:
				return alt_return
			except:
				if catch: return catch(sys.exc_info(), lambda:func(*args, **kwargs))
				raise
		finally:
			if final: final()
	return _exceptional
#
def get_sessions(host='localhost', port=OPC_GATE_PORT):
	# RETURN SESSIONS AS GUID:host hash
	Pyro.core.initClient(banner = 0)
	server_obj = Pyro.core.getProxyForURI("PYROLOC://%s:%s/opc" % (host, port))
	return server_obj.get_clients()
#
def open_client(host='localhost', port=OPC_GATE_PORT):
	# CONNECT TO SPECIFIED GATEWAY
	Pyro.core.initClient(banner=0)
	server_obj = Pyro.core.getProxyForURI("PYROLOC://%s:%s/opc" % (host, port))
	return server_obj.create_client()
#
class TimeoutError(Exception):
	def __init__(self, txt):
		Exception.__init__(self, txt)
#
class OPCError(Exception):
	def __init__(self, txt):
		Exception.__init__(self, txt)
#
class GroupEvents:
	def __init__(self):
		self.client = current_client
	def OnDataChange(self, TransactionID, NumItems, ClientHandles, ItemValues, Qualities, TimeStamps):
		self.client.callback_queue.put((TransactionID, ClientHandles, ItemValues, Qualities, TimeStamps))
#
# --------------------- CLIENT CONSTRUCTION -------------------------
class client():
	def __init__(self, opc_class=None, client_name=None):
		# INSTANTIATE OPC AUTOMATION CLASS
		self.callback_queue = Queue.Queue()
		pythoncom.CoInitialize()
		opc_class = OPC_CLASS
		opc_class_list = opc_class.split(';')
		for i,c in enumerate(opc_class_list):
			try:
				self._opc = win32com.client.gencache.EnsureDispatch(c, 0)
				self.opc_class = c
				break
			except pythoncom.com_error, err:
				if i == len(opc_class_list)-1:
					error_msg = 'Dispatch: %s' % self._get_error_str(err)
					raise OPCError, error_msg
				else:
					pass
		self._event = win32event.CreateEvent(None,0,0,None)
		self.opc_server = None
		self.opc_host = None
		self.client_name = client_name
		self._groups = {}
		self._group_tags = {}
		self._group_valid_tags = {}
		self._group_server_handles = {}
		self._group_handles_tag = {}
		self._group_hooks = {}
		self._open_serv = None
		self._open_self = None
		self._open_host = None
		self._open_port = None
		self._open_guid = None
		self._prev_serv_time = None
		self._tx_id = 0
		self.trace = None
		self.cpu = None
		try:
			pythoncom.CoUnInitialize()
		except:
			pass
#
	def set_trace(self, trace):
		if self._open_serv == None:
			self.trace = trace
#
	def connect(self, opc_server=None, opc_host='localhost'):
		# CONNECT TO SPECIFIED OPC SERVER
		pythoncom.CoInitialize()
		if opc_server == None:
			# FIRST CONNECT
			if self.opc_server == None:
				opc_server = OPC_SERVER
			# RECONNECT
			else:
				opc_server = self.opc_server
				opc_host = self.opc_host
		else:
			pass
		opc_server_list = opc_server.split(';')
		connected = False
		for s in opc_server_list:
			try:
				if self.trace: self.trace('Connect(%s,%s)' % (s, opc_host))
				self._opc.Connect(s, opc_host)
			except pythoncom.com_error, err:
				if len(opc_server_list) == 1:
					error_msg = 'Connect: %s' % self._get_error_str(err)
					raise OPCError, error_msg
			else:
				# Set client name since some OPC servers use it for security
				if self.client_name == None:
					 self._opc.ClientName = OPC_CLIENT
				else:
					 self._opc.ClientName = self.client_name
				connected = True
				break
		if not connected:
			raise OPCError, 'Connect: Cannot connect to any of the servers in the OPC_SERVER list'
		# OFTEN, CALL IMMEDIATELY AFTER Connect() FAILS, WAIT A MOMENT
		# TO AVOID ISSUE.
		time.sleep(0.01)
		self.opc_server = opc_server
		if opc_host == 'localhost':
			opc_host = socket.gethostname()
		self.opc_host = opc_host
		# ON RECONNECT, REMOVE OLD GROUP NAMES THAT ARE NOW INVALID
		self._groups = {}
		self._group_tags = {}
		self._group_valid_tags = {}
		self._group_server_handles = {}
		self._group_handles_tag = {}
		self._group_hooks = {}
		try:
			pythoncom.CoUnInitialize()
		except:
			pass
#
	def close(self, del_object=True):
		# GRACEFUL DISCONNECT FROM CURRENTLY CONNECTED OPC SERVER
		try:
			pythoncom.CoInitialize()
			self.remove(self.groups())
		except pythoncom.com_error, err:
			error_msg = 'Disconnect: %s' % self._get_error_str(err)
			raise OPCError, error_msg
		except OPCError:
			pass
		finally:
			if self.trace: self.trace('Disconnect()')
			self._opc.Disconnect()
			# REMOVE OBJECT FROM GATEWAY
			if self._open_serv and del_object:
				self._open_serv.release_client(self._open_self)
		try:
			pythoncom.CoUnInitialize()
		except:
			pass
#
	def iread(self, tags=None, group=None, size=None, pause=0, source='hybrid', update=-1, timeout=5000, sync=False, include_error=False, rebuild=False):
		# ITERABLE VERSION OF READ
		def add_items(tags):
			names = list(tags)
			names.insert(0,0)
			errors = []
			if self.trace: 
				self.trace('Validate(%s)' % tags2trace(names))
			try:
				errors = opc_items.Validate(len(names)-1, names)
			except:
				pass
			valid_tags = []
			valid_values = []
			client_handles = []
			if not self._group_handles_tag.has_key(sub_group):
				self._group_handles_tag[sub_group] = {}
				n = 0
			else:
				n = max(self._group_handles_tag[sub_group]) + 1
			for i, tag in enumerate(tags):
				if errors[i] == 0:
					valid_tags.append(tag)
					client_handles.append(n)
					self._group_handles_tag[sub_group][n] = tag 
					n += 1
				elif include_error:
					error_msgs[tag] = self._opc.GetErrorString(errors[i])
			client_handles.insert(0,0)
			valid_tags.insert(0,0)
			server_handles = []
			errors = []
			if self.trace: self.trace('AddItems(%s)' % tags2trace(valid_tags))
		 
			try:
				server_handles, errors = opc_items.AddItems(len(client_handles)-1, valid_tags, client_handles)
			except:
				pass
				 
			valid_tags_tmp = []
			server_handles_tmp = []
			valid_tags.pop(0)
			if not self._group_server_handles.has_key(sub_group):
				self._group_server_handles[sub_group] = {}
		 
			for i, tag in enumerate(valid_tags):
				if errors[i] == 0:
					valid_tags_tmp.append(tag)
					server_handles_tmp.append(server_handles[i])
					self._group_server_handles[sub_group][tag] = server_handles[i]
				elif include_error:
					error_msgs[tag] = self._opc.GetErrorString(errors[i])
			valid_tags = valid_tags_tmp
			server_handles = server_handles_tmp
			return valid_tags, server_handles
#
		def remove_items(tags):
			if self.trace: self.trace('RemoveItems(%s)' % tags2trace(['']+tags))
			server_handles = [self._group_server_handles[sub_group][tag] for tag in tags]
			server_handles.insert(0,0)
			errors = []
			try:
				errors = opc_items.Remove(len(server_handles)-1, server_handles)
			except pythoncom.com_error, err:
				error_msg = 'RemoveItems: %s' % self._get_error_str(err)
				raise OPCError, error_msg
#
		try:
			self._update_tx_time()
			pythoncom.CoInitialize()
			if include_error:
				sync = True
			if sync:
				update = -1
			tags, single, valid = type_check(tags)
			if not valid:
				raise TypeError, "iread(): 'tags' parameter must be a string or a list of strings"
			if self._groups.has_key(group) and not rebuild:
				# GROUP EXISTS
				num_groups = self._groups[group]
				data_source = SOURCE_CACHE
			else:
				# GROUP DOES NOT EXIST
				if size:
					# Break-up tags into groups of 'size' tags
					tag_groups = [tags[i:i+size] for i in range(0, len(tags), size)]
				else:
					tag_groups = [tags]
				num_groups = len(tag_groups)
				data_source = SOURCE_DEVICE
			results = []
			for gid in range(num_groups):
				if gid > 0 and pause > 0: time.sleep(pause/1000.0)
				error_msgs = {}
				opc_groups = self._opc.OPCGroups
				opc_groups.DefaultGroupUpdateRate = update
				# ANONYMOUS GROUP
				if group == None:
					try:
						if self.trace: self.trace('AddGroup()')
						opc_group = opc_groups.Add()
					except pythoncom.com_error, err:
						error_msg = 'AddGroup: %s' % self._get_error_str(err)
						raise OPCError, error_msg
					sub_group = group
					new_group = True
				else:
					sub_group = '%s.%d' % (group, gid)
					# EXISTING NAMED GROUP
					try:
						if self.trace: self.trace('GetOPCGroup(%s)' % sub_group)
						opc_group = opc_groups.GetOPCGroup(sub_group)
						new_group = False
					# NEW NAMED GROUP
					except:
						try:
							if self.trace: self.trace('AddGroup(%s)' % sub_group)
							opc_group = opc_groups.Add(sub_group)
						except pythoncom.com_error, err:
							error_msg = 'AddGroup: %s' % self._get_error_str(err)
							raise OPCError, error_msg
						self._groups[str(group)] = len(tag_groups)
						new_group = True
				opc_items = opc_group.OPCItems
				if new_group:
					opc_group.IsSubscribed = 1
					opc_group.IsActive = 1
					if not sync:
						if self.trace: self.trace('WithEvents(%s)' % opc_group.Name)
						global current_client
						current_client = self
						self._group_hooks[opc_group.Name] = win32com.client.WithEvents(opc_group, GroupEvents)
					tags = tag_groups[gid]
					valid_tags, server_handles = add_items(tags)
					self._group_tags[sub_group] = tags
					self._group_valid_tags[sub_group] = valid_tags
				elif rebuild:
				# REBUILD EXISTING GROUP
					tags = tag_groups[gid]
					valid_tags = self._group_valid_tags[sub_group]
					add_tags = [t for t in tags if t not in valid_tags]
					del_tags = [t for t in valid_tags if t not in tags]
					if len(add_tags) > 0:
						valid_tags, server_handles = add_items(add_tags)
						valid_tags = self._group_valid_tags[sub_group] + valid_tags
					if len(del_tags) > 0:
						remove_items(del_tags)
						valid_tags = [t for t in valid_tags if t not in del_tags]
					self._group_tags[sub_group] = tags
					self._group_valid_tags[sub_group] = valid_tags
					
					if source == 'hybrid': data_source = SOURCE_DEVICE
				# EXISTING GROUP
				else:
					tags = self._group_tags[sub_group]
					valid_tags = self._group_valid_tags[sub_group]
					if sync:
						server_handles = [item.ServerHandle for item in opc_items]
				tag_value = {}
				tag_quality = {}
				tag_time = {}
				tag_error = {}
#
				# SYNC READ
				if sync:	
					values = []
					errors = []
					qualities = []
					timestamps= []
					if len(valid_tags) > 0:
						 server_handles.insert(0,0)
						 if source != 'hybrid':
							 data_source = SOURCE_CACHE if source == 'cache' else SOURCE_DEVICE
						 if self.trace: self.trace('SyncRead(%s)' % data_source)
						 try:
							 values, errors, qualities, timestamps = opc_group.SyncRead(data_source, len(server_handles)-1, server_handles)
						 except pythoncom.com_error, err:
							 error_msg = 'SyncRead: %s' % self._get_error_str(err)
							 raise OPCError, error_msg
						 for i,tag in enumerate(valid_tags):
							 tag_value[tag] = values[i]
							 tag_quality[tag] = qualities[i]
							 tag_time[tag] = timestamps[i]
							 tag_error[tag] = errors[i]
				# ASYNC READ
				else:
					if len(valid_tags) > 0:
						if self._tx_id >= 0xFFFF:
							 self._tx_id = 0
						self._tx_id += 1
						if source != 'hybrid':
							data_source = SOURCE_CACHE if source == 'cache' else SOURCE_DEVICE
						if self.trace: self.trace('AsyncRefresh(%s)' % data_source)
						try:
							opc_group.AsyncRefresh(data_source, self._tx_id)
						except pythoncom.com_error, err:
							error_msg = 'AsyncRefresh: %s' % self._get_error_str(err)
							raise OPCError, error_msg
						tx_id = 0
						start = time.time() * 1000
						while tx_id != self._tx_id:
							now = time.time() * 1000
							if now - start > timeout:
								raise TimeoutError, 'Callback: Timeout waiting for data'
							if self.callback_queue.empty():
								pythoncom.PumpWaitingMessages()
							else:
								tx_id, handles, values, qualities, timestamps = self.callback_queue.get()
						for i,h in enumerate(handles):
							tag = self._group_handles_tag[sub_group][h]
							tag_value[tag] = values[i]
							tag_quality[tag] = qualities[i]
							tag_time[tag] = timestamps[i]
				for tag in tags:
					if tag_value.has_key(tag):
						if (not sync and len(valid_tags) > 0) or (sync and tag_error[tag] == 0):
							value = tag_value[tag]
							if type(value) == pywintypes.TimeType:
								value = str(value)
							quality = quality_str(tag_quality[tag])
							timestamp = str(tag_time[tag])
						else:
							value = None
							quality = 'Error'
							timestamp = None
						if include_error:
							error_msgs[tag] = self._opc.GetErrorString(tag_error[tag]).strip('\r\n')
					else:
						value = None
						quality = 'Error'
						timestamp = None
						if include_error and not error_msgs.has_key(tag):
							error_msgs[tag] = ''
					if single:
						if include_error:
							yield (value, quality, timestamp, error_msgs[tag])
						else:
							yield (value, quality, timestamp)
					else:
						if include_error:
							yield (tag, value, quality, timestamp, error_msgs[tag])
						else:
							yield (tag, value, quality, timestamp)
				if group == None:
					try:
						if not sync and self._group_hooks.has_key(opc_group.Name):
							if self.trace: self.trace('CloseEvents(%s)' % opc_group.Name)
							self._group_hooks[opc_group.Name].close()
						if self.trace: self.trace('RemoveGroup(%s)' % opc_group.Name)
						opc_groups.Remove(opc_group.Name)
					except pythoncom.com_error, err:
						error_msg = 'RemoveGroup: %s' % self._get_error_str(err)
						raise OPCError, error_msg
		except pythoncom.com_error, err:
			error_msg = 'read: %s' % self._get_error_str(err)
			raise OPCError, error_msg
		try:
			pythoncom.CoUnInitialize()
		except:
			pass
	def read(self, tags=None, group=None, size=None, pause=0, source='hybrid', update=-1, timeout=5000, sync=False, include_error=False, rebuild=False):
		# RETURN LIST OF (VALUE, QUALITY, TIME) TUPBLES FOR THE SPECIFIED TAG(S)
		tags_list, single, valid = type_check(tags)
		if not valid:
			raise TypeError, "read(): 'tags' parameter must be a string or a list of strings"
		num_health_tags = len([t for t in tags_list if t[:1] == '@'])
		num_opc_tags = len([t for t in tags_list if t[:1] != '@'])
		if num_health_tags > 0:
			if num_opc_tags > 0:
				raise TypeError, "read(): system health and OPC tags cannot be included in the same group"
			results = self._read_health(tags)
		else:
			results = self.iread(tags, group, size, pause, source, update, timeout, sync, include_error, rebuild)
		if single:
			return list(results)[0]
		else:
			return list(results)
#
	def iwrite(self, tag_value_pairs, size=None, pause=0, include_error=False):
		# ITERABLE VERSION OF WRITE
		try:
			self._update_tx_time()
			pythoncom.CoInitialize()
#
			def _valid_pair(p):
				if type(p) in (types.ListType, types.TupleType) and len(p) >= 2 and type(p[0]) in types.StringTypes:
					return True
				else:
					return False

			if type(tag_value_pairs) not in (types.ListType, types.TupleType):
				raise TypeError, "write(): 'tag_value_pairs' parameter must be a (tag, value) tuple or a list of (tag,value) tuples"
			if tag_value_pairs == None:
				tag_value_pairs = ['']
				single = False
			elif type(tag_value_pairs[0]) in types.StringTypes:
				tag_value_pairs = [tag_value_pairs]
				single = True
			else:
				single = False
			invalid_pairs = [p for p in tag_value_pairs if not _valid_pair(p)]
			if len(invalid_pairs) > 0:
				raise TypeError, "write(): 'tag_value_pairs' parameter must be a (tag, value) tuple or a list of (tag,value) tuples"
			names = [tag[0] for tag in tag_value_pairs]
			tags = [tag[0] for tag in tag_value_pairs]
			values = [tag[1] for tag in tag_value_pairs]
			# BREAK UP TAGS AND VALUES INTO GROUP OF 'SIZE' TAGS
			if size:
				name_groups = [names[i:i+size] for i in range(0, len(names), size)]
				tag_groups = [tags[i:i+size] for i in range(0, len(tags), size)]
				value_groups = [values[i:i+size] for i in range(0, len(values), size)]
			else:
				name_groups = [names]
				tag_groups = [tags]
				value_groups = [values]
			num_groups = len(tag_groups)
			status = []
			for gid in range(num_groups):
				if gid > 0 and pause > 0: 
					time.sleep(pause/1000.0)
				else:
					pass
				opc_groups = self._opc.OPCGroups
				opc_group = opc_groups.Add()
				opc_items = opc_group.OPCItems
				names = name_groups[gid]
				tags = tag_groups[gid]
				values = value_groups[gid]
				names.insert(0,0)
				errors = []
				try:
					errors = opc_items.Validate(len(names)-1, names)
				except:
					pass
				n = 1
				valid_tags = []
				valid_values = []
				client_handles = []
				error_msgs = {}
				for i, tag in enumerate(tags):
					if errors[i] == 0:
						valid_tags.append(tag)
						valid_values.append(values[i])
						client_handles.append(n)
						error_msgs[tag] = ''
						n += 1
					elif include_error:
						error_msgs[tag] = self._opc.GetErrorString(errors[i])
				client_handles.insert(0,0)
				valid_tags.insert(0,0)
				server_handles = []
				errors = []
				try:
					server_handles, errors = opc_items.AddItems(len(client_handles)-1, valid_tags, client_handles)
				except:
					pass
				valid_tags_tmp = []
				valid_values_tmp = []
				server_handles_tmp = []
				valid_tags.pop(0)
				for i, tag in enumerate(valid_tags):
					if errors[i] == 0:
						valid_tags_tmp.append(tag)
						valid_values_tmp.append(valid_values[i])
						server_handles_tmp.append(server_handles[i])
						error_msgs[tag] = ''
					elif include_error:
						error_msgs[tag] = self._opc.GetErrorString(errors[i])
				valid_tags = valid_tags_tmp
				valid_values = valid_values_tmp
				server_handles = server_handles_tmp
				server_handles.insert(0,0)
				valid_values.insert(0,0)
				errors = []
				if len(valid_values) > 1:
					try:
						# Ideally would use AsyncWrite, but this function does not work.
						errors = opc_group.SyncWrite(len(server_handles)-1, server_handles, valid_values)
						#errors = opc_group.AsyncWrite(len(server_handles)-1, server_handles, valid_values)
					except:
						pass
				n = 0
				for tag in tags:
					if tag in valid_tags:
						if errors[n] == 0:
							status = 'Success'
						else:
							status = 'Error'
						if include_error:  error_msgs[tag] = self._opc.GetErrorString(errors[n])
						n += 1
					else:
						status = 'Error'
					# STRIP ANY 'NEWLINE' OR 'CARRIAGE RETURN' CHARACTERS FROM INCOMING ERROR MESSAGE
					if include_error:  
						error_msgs[tag] = error_msgs[tag].strip('\r\n')
					if single:
						if include_error:
							yield (status, error_msgs[tag])
						else:
							yield status
					else:
						if include_error:
							yield (tag, status, error_msgs[tag])
						else:
							yield (tag, status)
				opc_groups.Remove(opc_group.Name)
		except pythoncom.com_error, err:
			error_msg = 'write: %s' % self._get_error_str(err)
			raise OPCError, error_msg
		try:
			pythoncom.CoUnInitialize()
		except:
			pass
#
	def write(self, tag_value_pairs, size=None, pause=0, include_error=False):
		# WRITE A LIST OF (TAG, VALUE) PAIRS TO THE SERVER
		if type(tag_value_pairs) in (types.ListType, types.TupleType) and type(tag_value_pairs[0]) in (types.ListType, types.TupleType):
			single = False
		else:
			single = True
		status = self.iwrite(tag_value_pairs, size, pause, include_error)
		if single:
			return list(status)[0]
		else:
			return list(status)
#
	def groups(self):
		# RETURN A LIST OF ACTIVE TAG GROUPS
		return self._groups.keys()
#
	def remove(self, groups):
		# REMOVE THE SPECIFIED TAG GROUP
		try:
			pythoncom.CoInitialize()
			opc_groups = self._opc.OPCGroups
			if type(groups) in types.StringTypes:
				groups = [groups]
				single = True
			else:
				single = False
			status = []
			for group in groups:					 
				if self._groups.has_key(group):
					for i in range(self._groups[group]):
						sub_group = '%s.%d' % (group, i)
						if self._group_hooks.has_key(sub_group):
							if self.trace: 
								self.trace('CloseEvents(%s)' % sub_group)
							self._group_hooks[sub_group].close()
						try:
							if self.trace: 
								self.trace('RemoveGroup(%s)' % sub_group)
							errors = opc_groups.Remove(sub_group)
						except pythoncom.com_error, err:
							error_msg = 'RemoveGroup: %s' % self._get_error_str(err)
							raise OPCError, error_msg
						del(self._group_tags[sub_group])
						del(self._group_valid_tags[sub_group])
						del(self._group_handles_tag[sub_group])
						del(self._group_server_handles[sub_group])
					del(self._groups[group])
		except pythoncom.com_error, err:
			error_msg = 'remove: %s' % self._get_error_str(err)
			raise OPCError, error_msg
		try:
			pythoncom.CoUnInitialize()
		except:
			pass
#
	def iproperties(self, tags, id=None):
		# ITERABLE VERSION OF PROPERTIES
		try:
			self._update_tx_time()
			pythoncom.CoInitialize()
			tags, single_tag, valid = type_check(tags)
			if not valid:
				raise TypeError, "properties(): 'tags' parameter must be a string or a list of strings"
			try:
				id.remove(0)
				include_name = True
			except:
				include_name = False
			if id != None:
				descriptions= []
				if isinstance(id, list) or isinstance(id, tuple):
					property_id = list(id)
					single_property = False
				else:
					property_id = [id]
					single_property = True
				for i in property_id:
					descriptions.append('Property id %d' % i)
			else:
				single_property = False
			properties = []
			for tag in tags:
				if id == None:
					descriptions = []
					property_id = []
					count, property_id, descriptions, datatypes = self._opc.QueryAvailableProperties(tag)
					# REMOVE ANY ERRONEOUS NEGATIVE PROPERTY ID
					tag_properties = map(None, property_id, descriptions)
					property_id = [p for p, d in tag_properties if p > 0]
					descriptions = [d for p, d in tag_properties if p > 0]
				property_id.insert(0, 0)
				values = []
				errors = []
				values, errors = self._opc.GetItemProperties(tag, len(property_id)-1, property_id)
 				property_id.pop(0)
				values = [str(v) if type(v) == pywintypes.TimeType else v for v in values]
				# REPLACE VARIANT ID WITH TYPE STRING
				try:
					i = property_id.index(1)
					values[i] = vt[values[i]]
				except:
					pass
				# REPLACE QUALITY BITS WITH STRINGS
				try:
					i = property_id.index(3)
					values[i] = quality_str(values[i])
				except:
					pass
				# REPLACE ACCESS RIGHTS WITH BIT STRINGS
				try:
					i = property_id.index(5)
					values[i] = ACCESS_RIGHTS[values[i]]
				except:
					pass
				if id != None:
					if single_property:
						if single_tag:
							tag_properties = values
						else:
							tag_properties = [values]
					else:
						tag_properties = map(None, property_id, values)
				else:
					tag_properties = map(None, property_id, descriptions, values)
					tag_properties.insert(0, (0, 'Item ID (virtual property)', tag))
				if include_name:	 tag_properties.insert(0, (0, tag))
				if not single_tag:  tag_properties = [tuple([tag] + list(p)) for p in tag_properties]
				for p in tag_properties: yield p
		except pythoncom.com_error, err:
			error_msg = 'properties: %s' % self._get_error_str(err)
			raise OPCError, error_msg
		try:
			pythoncom.CoUnInitialize()
		except:
			pass
#
	def properties(self, tags, id=None):
		# RETURN LIST OF PROPERTY TUPLES (ID, NAME, VALUE) FOR SPECIFIED TAGS
		if type(tags) not in (types.ListType, types.TupleType) and type(id) not in (types.NoneType, types.ListType, types.TupleType):
			single = True
		else:
			single = False
		props = self.iproperties(tags, id)
		if single:
			return list(props)[0]
		else:
			return list(props)
	def ilist(self, paths='*', recursive=False, flat=False, include_type=False):
		# ITERABLE VERSION OF LIST
		try:
			self._update_tx_time()
			pythoncom.CoInitialize()
			try:
				browser = self._opc.CreateBrowser()
			# FOR OPC SERVERS THAT DON'T SUPPORT BROWSING
			except:
				return
			paths, single, valid = type_check(paths)
			if not valid:
				raise TypeError, "list(): 'paths' parameter must be a string or a list of strings"
			if len(paths) == 0: paths = ['*']
			nodes = {}
			for path in paths:
				
				if flat:
					browser.MoveToRoot()
					browser.Filter = ''
					browser.ShowLeafs(True)
					pattern = re.compile('^%s$' % wild2regex(path) , re.IGNORECASE)
					matches = filter(pattern.search, browser)
					if include_type:  matches = [(x, node_type) for x in matches]
					for node in matches: yield node
					continue
				queue = []
				queue.append(path)
				while len(queue) > 0:
					tag = queue.pop(0)
					browser.MoveToRoot()
					browser.Filter = ''
					pattern = None
					path_str = '/'
					path_list = tag.replace('.','/').split('/')
					path_list = [p for p in path_list if len(p) > 0]
					found_filter = False
					path_postfix = '/'
					for i, p in enumerate(path_list):
						if found_filter:
							path_postfix += p + '/'
						elif p.find('*') >= 0:
							pattern = re.compile('^%s$' % wild2regex(p) , re.IGNORECASE)
							found_filter = True
						elif len(p) != 0:
							pattern = re.compile('^.*$')
							browser.ShowBranches()
							# MOVE DOWN ON BRANCH NODE
							if len(browser) > 0:
								try:
									browser.MoveDown(p)
									path_str += p + '/'
								except:
									if i < len(path_list)-1: return
									pattern = re.compile('^%s$' % wild2regex(p) , re.IGNORECASE)
							# LEAF NODE, SO APPEND ALL REMAINING PARTS TOGETHER
							# TO FORM SINGLE SEARCH EXPRESSION
							else:
								p = string.join(path_list[i:], '.')
								pattern = re.compile('^%s$' % wild2regex(p) , re.IGNORECASE)
								break
					browser.ShowBranches()
					if len(browser) == 0:
						browser.ShowLeafs(False)
						lowest_level = True
						node_type = 'Leaf'
					else:
						lowest_level = False
						node_type = 'Branch'
					matches = filter(pattern.search, browser)
					if not lowest_level and recursive:
						queue += [path_str + x + path_postfix for x in matches]
					else:
						if lowest_level:  matches = [exceptional(browser.GetItemID,x)(x) for x in matches]
						if include_type:  matches = [(x, node_type) for x in matches]
						for node in matches:
							if not nodes.has_key(node): yield node
							nodes[node] = True
		except pythoncom.com_error, err:
			error_msg = 'list: %s' % self._get_error_str(err)
			raise OPCError, error_msg
		try:
			pythoncom.CoUnInitialize()
		except:
			pass
#
	def list(self, paths='*', recursive=False, flat=False, include_type=False):
		# RETURN LIST OF NODES AT SPECIFIED PATH
		# -- TREE BROWSER
		nodes = self.ilist(paths, recursive, flat, include_type)
		return list(nodes)
#
	def servers(self, opc_host='localhost'):
		# RETURN LIST OF AVAILABLE OPC SERVERS
		try:
			pythoncom.CoInitialize()
			servers = self._opc.GetOPCServers(opc_host)
			servers = [s for s in servers if s != None]
			return servers
		except pythoncom.com_error, err:
			error_msg = 'servers: %s' % self._get_error_str(err)
			raise OPCError, error_msg
		try:
			pythoncom.CoUnInitialize()
		except:
			pass
#
	def info(self):
		# RETURN LIST OF (NAME, VALUE) PAIRS ABOUT AVAILABLE OPC SERVERS
		try:
			self._update_tx_time()
			pythoncom.CoInitialize()
			info_list = []
			if self._open_serv:
				mode = 'OpenOPC'
			else:
				mode = 'DCOM'
			
			info_list += [('Protocol', mode)]
			if mode == 'OpenOPC':
				info_list += [('Gateway Host', '%s:%s' % (self._open_host, self._open_port))]
				info_list += [('Gateway Version', '%s' % __version__)]
			info_list += [('Class', self.opc_class)]
			info_list += [('Client Name', self._opc.ClientName)]
			info_list += [('OPC Host', self.opc_host)]
			info_list += [('OPC Server', self._opc.ServerName)]
			info_list += [('State', OPC_STATUS[self._opc.ServerState])]
			info_list += [('Version', '%d.%d (Build %d)' % (self._opc.MajorVersion, self._opc.MinorVersion, self._opc.BuildNumber))]
			try:
				browser = self._opc.CreateBrowser()
				browser_type = BROWSER_TYPE[browser.Organization]
			except:
				browser_type = 'Not Supported'
			info_list += [('Browser', browser_type)]
			info_list += [('Start Time', str(self._opc.StartTime))]
			info_list += [('Current Time', str(self._opc.CurrentTime))]
			info_list += [('Vendor', self._opc.VendorInfo)]
			return info_list
		except pythoncom.com_error, err:
			error_msg = 'info: %s' % self._get_error_str(err)
			raise OPCError, error_msg
		try:
			pythoncom.CoUnInitialize()
		except:
			pass
#
	def ping(self):
		# CHECK IF WE ARE STILL TALKING TO THE OPC SERVER
		try:
			# CONVERT OPC SERVER TIME TO MILLISECONDS
			opc_serv_time = int(float(self._opc.CurrentTime) * 1000000.0)
			if opc_serv_time == self._prev_serv_time:
				return False
			else:
				self._prev_serv_time = opc_serv_time
				return True
		except pythoncom.com_error:
			return False
	def _get_error_str(self, err):
		# RETURN ERROR STRING FOR OPC OR COMM ERROR CODE
		hr, msg, exc, arg = err
		if exc == None:
			error_str = str(msg)
		else:
			scode = exc[5]
			try:
				opc_err_str = unicode(self._opc.GetErrorString(scode)).strip('\r\n')
			except:
				opc_err_str = None
			try:
				com_err_str = unicode(pythoncom.GetScodeString(scode)).strip('\r\n')
			except:
				com_err_str = None
			# OPC ERROR AND COMM ERROR OVERLAP, SO WE COMBINE INTO SINGLE
			# ERROR MESSAGE
			if opc_err_str == None and com_err_str == None:
				error_str = str(scode)
			elif opc_err_str == com_err_str:
				error_str = opc_err_str
			elif opc_err_str == None:
				error_str = com_err_str
			elif com_err_str == None:
				error_str = opc_err_str
			else:
				error_str = '%s (%s)' % (opc_err_str, com_err_str)
		return error_str
#
	def _update_tx_time(self):
		# UPDATE SESSION'S LAST TRANSACTION TIME IN GATEWAY 
		if self._open_serv:
			self._open_serv._tx_times[self._open_guid] = time.time()
#
	def __getitem__(self, key):
		# READ SINGLE ITEM (TAG AS DICTIONARY KEY)
		value, quality, time = self.read(key)
		return value
		
	def __setitem__(self, key, value):
		# WRITE SINGLE ITEM  (TAG AS DICTIONARY KEY)
		self.write((key, value))
		return
# -------------------------------------------------------------------
