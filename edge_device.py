from logger import LOG

LOG.info('STARTING')

import sys
import server
import scheduler
import signal

exiting = False
def signal_handler(signal, frame):
	global exiting
	if exiting:
		return
	exiting = True
	#signal.signal(signal.SIGINT, None)
	LOG.info('EXITING...')
	scheduler.Stop()
	server.Stop()
	import serial_client
	serial_client.Close()
	sys.exit()	
signal.signal(signal.SIGINT, signal_handler)

scheduler.Start()
server.Start()

import time
while True:
	time.sleep(1)
	

	

