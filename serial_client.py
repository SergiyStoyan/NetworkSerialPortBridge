from __future__ import with_statement
from logger import LOG
import sys
import time
import serial
import settings
import threading

try:
	connection
except:
	connection = serial.Serial(
		port = settings.SERIAL['port'],
		baudrate = settings.SERIAL['baudrate'],
		parity = settings.SERIAL['parity'],
		stopbits = settings.SERIAL['stopbits'],
		bytesize = settings.SERIAL['bytesize'],
		timeout = settings.SERIAL['timeout'],
		write_timeout = 10,
		#exclusive = True
	)
	try: 
		if not connection.isOpen():
			connection.open()
		LOG.info('Serial port open: ' + str(settings.SERIAL))
	except:
		LOG.exception(sys.exc_info()[0])
		exit()

def Close():
	LOG.info('Closing serial port connection.')
	if connection.isOpen(): connection.close()

lock = threading.Lock()
	
PacketOversize = 1000	
	
def RequestDNP3(data_in, comment):
	global lock, connection
	with lock:
		try:
			LOG.info(comment + '\r\nIn:' + str(data_in))
			connection.flushInput() #flush input buffer, discarding all its contents
			connection.flushOutput()#flush output buffer, aborting current output 
			#if not connection.isOpen():
			#try:
			written_len = connection.write(data_in)			
			#except SerialTimeoutException, e:
			#	print "timeout writing: " + str(e)
			if written_len < len(data_in):
				raise Exception('Serial port: written less than should: ' + written_len + ' < ' + len(data_in))  
			
			out = connection.read(PacketOversize)
			LOG.info(comment + '\r\nOut:' + out)
			if len(out) == PacketOversize:
				raise Exception('Serial port: not all read from serial port.')
			return out
			
			# out1 = connection.read(3)
			# if not out1 or len(out1) < 3:
				# raise Exception('Response timeout in serial port.')
			# LOG.info('Packet size:' + str(ord(out1[2]) + 5))
			# out2 = connection.read(ord(out1[2]) + 2)
			# LOG.info('Out:' + out1 + out2)
			# connection.timeout = 0
			# r = connection.read(1)				
			# connection.timeout = settings.SERIAL['timeout']
			# if r:
				# raise Exception('not all read from serial port.')
			# return out1 + out2
		except:
			LOG.exception(sys.exc_info()[0])