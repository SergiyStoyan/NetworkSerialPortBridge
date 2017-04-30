from logger import LOG
import sys
import time
import serial_client
import socket
import settings
import threading

lock = threading.Lock()

def service(period, request_file, tcp):
	import sys
	import os
	import signal
	try:
		while run:
			time1 = int(time.time())
			
			with open(request_file, mode='rb') as file:
				data_in = file.read()	
			data_out = serial_client.RequestDNP3(data_in)
			if not data_out:
				continue
			global lock
			with lock:
				if not run:
					return
				global socket_
				socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				server_address = (settings.REMOTE_HOST['ip'], settings.REMOTE_HOST['port'])
				try:
					if tcp:
						socket_.connect(server_address)
						socket_.send(data_out)
					else:
						socket_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
						socket_.sendto(data_out, server_address)	
				finally:
					socket_.shutdown(socket.SHUT_RDWR)
					socket_.close()	
					socket_ = None
			
			period1 = time1 + period - int(time.time())
			if period1 < 0: 
				period1 = 0
			time.sleep(period1) 
	except:
		LOG.exception(sys.exc_info()[0])
		#thread.interrupt_main()
		os.kill(os.getpid(), signal.SIGINT)

run = False
socket_ = None

request_files2thread = {}
	
def start_schedule(schedule):	
	global request_files2thread	
	if request_file in request_files2thread:
		return
	LOG.info('Starting schedule: ' + str(schedule))
	t = threading.Thread(target = service, args = (schedule['period'], schedule['request_file'], schedule['tcp']))
	t.daemon = True
	t.start()
	request_files2thread[request_file] = t
	
def Stop():
	global run
	run = False
	global socket_
	if socket_:
		socket_.shutdown(socket.SHUT_RDWR)
		socket_.close()	
		socket_ = None
				
def Start():
	global run
	run = True
	for schedule in settings.SCHEDULES:
		start_schedule(schedule)

