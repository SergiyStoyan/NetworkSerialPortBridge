from logger import LOG
import socket
import threading
import serial_client
import settings

def service_tcp():
	import sys
	import os
	import signal
	try:
		LOG.info('Starting tcp server: ' + str(settings.LOCAL_HOST))
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = (settings.LOCAL_HOST['ip'], settings.LOCAL_HOST['port'])
		s.bind(server_address)
		#s.settimeout(3)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
		s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)#activates after after_idle_sec seconds of idleness
		s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)#sends a keepalive ping once every interval_sec seconds
		s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)#closes the connection after max_fails failed pings
		s.listen(1)

		#file_id = 0
		while run:
			try:
				connection, client_address = s.accept()
				LOG.info('Tcp connection accepted from: ' + str(client_address))
				connection.settimeout(3)
				while True:
					try:
						data_in = connection.recv(serial_client.PacketOversize)
					except socket.timeout:
						pass
					LOG.info('TCP received.')					
					#with open('/home/develop/edge_device/test_files/' + str(file_id), 'w') as file:
					#	file.write(data_in)	
					#	file_id = file_id + 1
					if len(data_in) == serial_client.PacketOversize:
						raise Exception('not all read from network port.')					
					if not data_in:
						break	
					data_out = serial_client.RequestDNP3(data_in)
					if not data_out:
						break
					connection.sendall(data_out)
			finally:
				connection.close()
				LOG.info('Connection closed')
	except:
		LOG.exception(sys.exc_info()[0])
		#thread.interrupt_main() 
		os.kill(os.getpid(), signal.SIGINT)
	
def service_udp():
	import sys
	import os
	import signal
	try:
		LOG.info('Starting udp server: ' + str(settings.LOCAL_HOST))
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		server_address = (settings.LOCAL_HOST['ip'], settings.LOCAL_HOST['port'])
		s.bind(server_address)

		while run:
			data_in, client_address = s.recvfrom(serial_client.PacketOversize)
			LOG.info('UDP received.')					
			if len(data_in) == serial_client.PacketOversize:
				raise Exception('not all read from network port.')	
			if not data_in:
				continue	
			data_out = serial_client.RequestDNP3(data_in)
			if not data_out:
				continue
			s.sendto(data_out, client_address)
	except:
		LOG.exception(sys.exc_info()[0])
		#thread.interrupt_main() 
		os.kill(os.getpid(), signal.SIGINT)
	
socket_tcp = None
socket_udp = None
	
service_tcp_t = None
service_udp_t = None

def Stop():
	LOG.info('Stopping network server.')
	global run
	run = False
	global socket_tcp
	if socket_tcp:
		#socket_tcp.shutdown(socket.SHUT_RDWR)
		socket_tcp.close()	
		socket_tcp = None
	global socket_udp
	if socket_udp:
		#socket_udp.shutdown(socket.SHUT_RDWR)
		socket_udp.close()	
		socket_udp = None
		
def Start():
	global run
	run = True
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
