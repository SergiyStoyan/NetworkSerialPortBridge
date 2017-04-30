import serial

LOCAL_HOST = {
	#'ip': '127.0.0.1',
	#'ip': '71.246.43.250',	
	'ip': '0.0.0.0',	
	'port': 20000,
}

REMOTE_HOST = {
	'ip': '71.246.43.242', 	
	'port': 63842,
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
	{
		'period': 30,
		'request_file': '/home/develop/edge_device/test_files/0',
		'tcp': True,
	},
]