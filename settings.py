import serial

HOST = {
	'ip': '127.0.0.1',
	'port': 20000,
}
		
SERIAL = {
	'port': '/dev/ttyUSB0',
    'baudrate': 9600,
    'parity': serial.PARITY_NONE,
    'stopbits': serial.STOPBITS_ONE,
    'bytesize': serial.EIGHTBITS,
	'timeout': 10, #read timeout in seconds
}
	
SCHEDULES = [
	# {
		# 'period': 300,
		# 'request_file': '/home/develop/edge_device/test_files/1',
		# 'tcp': True,
	# },
]