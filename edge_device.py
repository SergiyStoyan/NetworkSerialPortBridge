from logger import LOG
import sys
import server
import scheduler
import serial_client

LOG.info('STARTING')

def signal_handler(signal, frame):
	LOG.info('EXITING...')
	serial_client.Close()
	raise ExitCommand()

signal.signal(signal.SIGUSR1, signal_handler)

server.Start()
scheduler.Start()

	

