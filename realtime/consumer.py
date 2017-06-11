import json
import time
import threading


CONN_TIMEOUT = {}
KILL_LIST = {}


def _execute(message, connId, timeToSleep):
    CONN_TIMEOUT[connId] = timeToSleep
    KILL_LIST[connId] = False
    isKilled = False 

    for i in range(0, timeToSleep):
    	if not KILL_LIST[connId]:
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
    jsonObj = json.loads(message['text'])
    timeToSleep = jsonObj['time']
    connId = str(jsonObj['connid'])
    print 'Connection ID: ' + connId + ' and Timeout: ' + str(timeToSleep)

    threading.Thread(target=_execute, args=(message, connId, timeToSleep)).start()

def ws_kill(message):
	jsonObj = json.loads(message['text'])
	connId = str(jsonObj['connid'])

	if KILL_LIST.get(connId):
		KILL_LIST[connId] = True
		message.reply_channel.send({'text':str('{\'status\':\'Ok\'}')})
	else:
		message.reply_channel.send({'text':str('{\'status\':\'Invalid connection Id : <connId>\'}')})

def ws_status(message):
	message.reply_channel.send({'text':str(CONN_TIMEOUT)})

def ws_connect(message):
    print 'Connection established'

def ws_disconnect(message):
    print 'Connection disconnected'