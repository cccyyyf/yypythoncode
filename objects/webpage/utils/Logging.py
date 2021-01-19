import logging


def get_console_logger(file, level=logging.INFO):
	logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
	logger = logging.getLogger(file)
	console = logging.StreamHandler()
	console.setLevel(level)
	logger.addHandler(console)
	return logger
