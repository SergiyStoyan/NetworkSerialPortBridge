from logger import LOG
import socket
import sys
import threading
import serial_client

def service_tcp()
	try:
		LOG.info('Starting tcp server')
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = (settings.HOST['ip'], settings.HOST['port'])
		s.bind(server_address)
		#s.settimeout(3)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
		s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)#activates after after_idle_sec seconds of idleness
		s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)#sends a keepalive ping once every interval_sec seconds
		s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)#closes the connection after max_fails failed pings
		s.listen(1)

		while True:
			try:
				connection, client_address = s.accept()
				LOG.info('Connection accepted from: ' + str(client_address))
				connection.settimeout(3)
				while True:
					try:
						data_in = connection.recv(1000)
					except socket.timeout:
						pass
					LOG.info('TCP received: ' + data_in)
					if !data_in:
						break	
					data_out = serial_client.Request(data_in)
					if !data_out:
						break
					connection.sendall(data_out)
			finally:
				connection.close()
				LOG.info('Connection closed')
	except:
		LOG.exception(sys.exc_info()[0])
		#thread.interrupt_main() 
		os.kill(os.getpid(), signal.SIGINT)
		exit()
	
def service_udp()
	try:
		LOG.info('Starting udp server')
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		server_address = (settings.HOST['ip'], settings.HOST['port'])
		s.bind(server_address)

		while True:
			try:
				data_in, client_address = s.recvfrom(1000)
				LOG.info('UDP received: ' + data_in)
			if !data_in:
				continue	
			data_out = serial_client.Request(data_in)
			if !data_out:
				continue
			s.sendto(data_out, client_address)
	except:
		LOG.exception(sys.exc_info()[0])
		#thread.interrupt_main() 
		os.kill(os.getpid(), signal.SIGINT)
		exit()
	
service_tcp_t = None
service_udp_t = None
			
# def Stop:
	# LOG.info('STOPPING SERVER')
	# if thread != None:
		# thread.stop()	

def Start():
	global service_tcp_t
	if service_tcp_t == None:
		service_tcp_t = threading.Thread(target = service_tcp, args = ())
		service_tcp_t.daemon = True
		service_tcp_t.start()
	global service_udp_t
	if service_udp_t == None:
		service_udp_t = threading.Thread(target = service_udp, args = ())
		service_udp_t.daemon = True
		service_udp_t.start()