import serial

HOST = {
	'ip': '172.0.0.1',
	'port': 512,
}
		
SERIAL = {
	'port': '/dev/ttyUSB1',
    'baudrate': 9600,
    'parity': serial.PARITY_ODD,
    'stopbits': serial.STOPBITS_TWO,
    'bytesize': serial.SEVENBITS,
	'timeout': 10, #read timeout in seconds
}
	
SCHEDULES = [
	{
		'period': 300,
		'request_file': '/home/develop/edge_device/requests/1',
		'tcp': True,
	},
]