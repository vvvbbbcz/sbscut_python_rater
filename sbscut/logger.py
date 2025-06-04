import logging
import sys
from logging.handlers import RotatingFileHandler

_logdir = "logs"
_logfile = f"{_logdir}/app.log"
_debug_logfile = f"{_logdir}/debug.log"

logger = logging.getLogger()

def init_logger(level=logging.INFO):
	logger.handlers.clear()
	logger.setLevel(logging.NOTSET)

	date_fmt = "%Y-%m-%d %H:%M:%S"
	fmt = logging.Formatter(
		'[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s',
		datefmt=date_fmt)

	file_handler = RotatingFileHandler(_logfile, 'a', 65536, 10)
	file_handler.setFormatter(fmt)
	file_handler.setLevel(logging.INFO)

	debug_handler = RotatingFileHandler(_debug_logfile, 'a', 65536, 10)
	debug_handler.setFormatter(fmt)
	debug_handler.setLevel(logging.DEBUG)

	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.setFormatter(fmt)
	console_handler.setLevel(level)

	logger.addHandler(file_handler)
	logger.addHandler(debug_handler)
	logger.addHandler(console_handler)
