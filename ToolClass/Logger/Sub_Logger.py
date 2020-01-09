
from Flask_Logger import sub_logger

if __name__ == '__main__':
	try:
	    open("sklearn.txt", "rb")
	except (SystemExit, KeyboardInterrupt):
	    raise
	except Exception:
	    # exc_info = True用于跟踪trackback
	    sub_logger.error("Faild to open sklearn.txt from logger.error", exc_info=True)
