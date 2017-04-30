from logger import LOG
import sys
import server
import scheduler
import signal

LOG.info('STARTING')

def signal_handler(signal, frame):
	LOG.info('EXITING...')
	import serial_client
	serial_client.Close()
	sys.exit()

signal.signal(signal.SIGINT, signal_handler)

scheduler.Start()
server.Start()

import time
while True:
	time.sleep(1)
	

	

