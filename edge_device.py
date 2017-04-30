from logger import LOG

LOG.info('STARTING')

import sys
import server
import scheduler
import signal

def signal_handler(signal, frame):
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
	

	

