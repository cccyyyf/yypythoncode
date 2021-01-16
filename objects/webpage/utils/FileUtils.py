import shutil, os, time
from objects.webpage.utils.Logging import *
import win32gui, win32con

logger = get_console_logger(__name__)


def clear_folder(path):
	if os.path.isdir(path):
		shutil.rmtree(path)
		if not os.path.exists(path):
			os.mkdir(path)
			logger.info("成功清空文件夹" + path)
	else:
		raise IOError("文件夹不存在")


def is_folder_empty(path):
	if not os.listdir(path):
		logger.info(path + "为空")
		return True
	else:
		logger.info(path + "不为空")
		return False

def get_single_file_from_folder(path):
	return os.listdir(path)[0]

def winUpLoadFile(path, title="打开"):
	time.sleep(2)
	dialog = win32gui.FindWindow("#32770", title)
	ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)
	comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)
	edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)
	button = win32gui.FindWindowEx(dialog, 0, 'Button', None)
	win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, path)
	win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)
