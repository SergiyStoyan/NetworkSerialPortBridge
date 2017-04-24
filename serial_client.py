from logger import LOG
import sys
import time
import serial
from __future__ import with_statement
#import array

connection = serial.Serial(
    port = settings.SERIAL['port'],
    baudrate = settings.SERIAL['baudrate'],
    parity = settings.SERIAL['parity'],
    stopbits = settings.SERIAL['stopbits'],
    bytesize = settings.SERIAL['bytesize'],
	timeout = settings.SERIAL['timeout'],
	write_timeout = 10,
	exclusive = True,
)
try: 
    connection.open()
except:
	LOG.exception(sys.exc_info()[0])
    exit()

def Close():
    if connection.isOpen(): connection.close()

lock = Lock()
	
def Request(content):
	global lock, connection
	with lock:
		try:
			connection.flushInput() #flush input buffer, discarding all its contents
			connection.flushOutput()#flush output buffer, aborting current output 
			#if not connection.isOpen():
			#try:
			written_len = connection.write(content)			
			#except SerialTimeoutException, e:
			#	print "timeout writing: " + str(e)
			if written_len < len(content):
				raise Exception('written less then put: ' + written_len + ' < ' + len(content))  
			time.sleep(1)
			# out = connection.read(1000)
			# if connection.outWaiting() > 0:
				# raise Exception('not all read: ' + str(connection.outWaiting()))
			#return out
			out1 = connection.read(3)
			if !out1 or len(out1) < 3:
				raise Exception('Response timeout in serial port.')
			out2 = connection.read(out1[2] + 2)
			if connection.outWaiting() > 0:
				#packet_size = out1[2] + 5
				raise Exception('Not all read. Waiting: ' + str(connection.outWaiting()) + '. Read: ' + str(len(out1) + len(out2)) + '. Packet size:' + str(out1[2] + 5))
			return out1 + out2
		except:
			LOG.exception(sys.exc_info()[0])