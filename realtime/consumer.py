import json
import time
import threading


CONN_TIMEOUT = {}
KILL_LIST = {}


def _execute(message, connId, timeToSleep):
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
	print 'MSG'
	jsonObj = json.loads(message['text'])
	timeToSleep = int(jsonObj['time'])
	connId = jsonObj['connid']

	if CONN_TIMEOUT.get(connId) > 0:
		pass
	else:
		threading.Thread(target=_execute, args=(message, connId, timeToSleep)).start()

def ws_kill(message):
	print 'KILL'
	print KILL_LIST
	jsonObj = json.loads(message['text'])
	connId = jsonObj['connid']

	if KILL_LIST.get(connId) == 0:
		KILL_LIST[connId] = 1
		message.reply_channel.send({'text':str('{\'status\':\'Ok\'}')})
	else:
		message.reply_channel.send({'text':str('{\'status\':\'Invalid connection Id\'}')})

def ws_status(message):
	print 'Status'
	message.reply_channel.send({'text':str(CONN_TIMEOUT)})

def ws_connect(message):
    print 'Connection established'

def ws_disconnect(message):
    print 'Connection disconnected'