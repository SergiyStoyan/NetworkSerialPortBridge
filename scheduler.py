from logger import LOG
import sys
import time
import serial_client
import socket
import threading

def service(period, request_file, tcp):
	try:
		while True:
			time1 = int(time.time())
			
			with open(request_file, mode='rb') as file:
				data_in = file.read()	
			data_out = serial_client.RequestDNP3(data_in)
			if !data_out:
				continue
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_address = (settings.HOST['ip'], settings.HOST['port'])
			if tcp:
				s.connect(server_address)
				try:
					s.send(data_out)
				finally:
					s.close()
			else:
				s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				s.sendto(data_out, server_address)		
			
			period1 = time1 + period - int(time.time())
			if period1 < 0: 
				period1 = 0
			time.sleep(period1) 
	except:
		LOG.exception(sys.exc_info()[0])
		#thread.interrupt_main() 
		os.kill(os.getpid(), signal.SIGINT)
		exit()

request_files2thread = {}
	
def start_schedule(period, request_file, tcp):	
	global request_files2thread	
	if request_files2thread[request_file] != None:
		return
	LOG.info('Starting schedule: ' + request_file)
	t = threading.Thread(target = service, args = (period, request_file, tcp))
	t.daemon = True
	t.start()
	request_files2thread[request_file] = t
	
def Start():
	for schedule in settings.SCHEDULES:
		start_schedule(schedule['period'], schedule['request_file'], schedule['tcp'])

