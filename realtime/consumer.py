import json
import time
import threading


CONN_TIMEOUT = {} # Maintains a dict of all the running connections with their timeouts
KILL_LIST = {} # Initialised to 0 for each running request, specifies that the request should be killed if set to 1


def _execute(message, connId, timeToSleep):
	"""
	Helper function for the request API. Executes each request as 
	a separate thread for allowing concurrency.
	Parameters:
		message - standard Django-channel object
		connId - Connection ID specified by the user
		timeToSleep - Timeout for the current request
	"""
	CONN_TIMEOUT[connId] = timeToSleep
	KILL_LIST[connId] = 0
	isKilled = False

	for i in range(0, timeToSleep):
		if KILL_LIST[connId] == 0:
			time.sleep(1)
			CONN_TIMEOUT[connId] -= 1
		else:
			isKilled = True
			break

	CONN_TIMEOUT.pop(connId)
	KILL_LIST.pop(connId)

	if isKilled:
		message.reply_channel.send({'text':str('{\'status\':\'Killed\'}')})
	else:  
		message.reply_channel.send({'text':str('{\'status\':\'Ok\'}')})	

def ws_message(message):
	"""
	Consumer to start a new running request on the server.
	Parameters:
		message - standard Django-channel object
	"""
	jsonObj = json.loads(message['text'])
	timeToSleep = int(jsonObj['time'])
	connId = jsonObj['connid']

	# Check for avoiding running same requests
	if CONN_TIMEOUT.get(connId) > 0:
		pass
	else:
		threading.Thread(target=_execute, args=(message, connId, timeToSleep)).start()

def ws_kill(message):
	"""
	Consumer to kill a running request on the server.
	Parameters:
		message - standard Django-channel object
	"""
	jsonObj = json.loads(message['text'])
	connId = jsonObj['connid']

	# Check for finding out whether the request with given ConnId is alive or not
	if KILL_LIST.get(connId) == 0:
		KILL_LIST[connId] = 1
		message.reply_channel.send({'text':str('{\'status\':\'Ok\'}')})
	else:
		message.reply_channel.send({'text':str('{\'status\':\'Invalid connection Id\'}')})

def ws_status(message):
	"""
	Consumer to return status of all the running requests.
	Parameters:
		message - standard Django-channel object
	"""
	message.reply_channel.send({'text':str(CONN_TIMEOUT)})

def ws_resolver(message):
	"""
	This consumer identifies which function should be called for the given request.
	Parameters:
		message - standard Django-channel object
	"""
	jsonObj = json.loads(message['text'])

	if jsonObj['route'] == 'request':
		ws_message(message)
	elif jsonObj['route'] == 'kill':
		ws_kill(message)
	else:
		ws_status(message)

def ws_connect(message):
    print 'Connection established'

def ws_disconnect(message):
    print 'Connection disconnected'