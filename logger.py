import logging

# def get_start_module_name():
	# import inspect
	# caller = inspect.currentframe()
	# print caller.f_globals['__file__']
	# while caller.f_back:
		# print caller.f_globals['__file__']
		# caller = caller.f_back
#get_start_module_name()

log_dir = 'logs'
import os
import sys
if not os.path.exists(log_dir):
	os.makedirs(log_dir)
log_path = log_dir + '/' + sys.argv[0] + '.log'		

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

fh = logging.FileHandler(log_path)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
#LOG.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
LOG.addHandler(ch)

import logging.handlers

#rfh = logging.handlers.RotatingFileHandler(log_path, maxBytes=100000, backupCount=9)
#LOG.addHandler(rfh)

trfh = logging.handlers.TimedRotatingFileHandler(log_path, when='D', interval=1, backupCount=9)
trfh.setLevel(logging.INFO)
trfh.setFormatter(formatter)
LOG.addHandler(trfh)


