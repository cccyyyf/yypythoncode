from objects.webpage.utils.PropertiesUtil import ConfigUtil
from selenium import webdriver
import os
from RootPath import RootPath
from objects.webpage.utils.Logging import *
from selenium.webdriver.chrome.options import Options

logger = get_console_logger(__name__)
conf = ConfigUtil(RootPath.getWebIniPath())


class DriverFactory():
	'''
	此类用来产生浏览器对象，openBrowser和openBrowserWithSpecifedDownloadPath都是静态方法可以直接调用
	openBrowser方法用来启动默认的浏览器，目前支持chrome，firefox
	openBrowserWithSpecifedDownloadPath方法用来产生定义过下载路径的浏览器对象，目前只实现了chrome
	'''
	driver_type = conf.get("SZ_ACTIVE", "DRIVER")  # 获取配置文件，配置文件中会定义默认启动的浏览器类型

	@classmethod
	def openBrowser(cls) -> webdriver:
		if cls.driver_type == "CHROME":
			return webdriver.Chrome(executable_path=os.path.join(RootPath.getRootPath(), "drivers/chromedriver.exe"))

		elif cls.driver_type == "FIREFOX":
			return webdriver.Firefox(executable_path=os.path.join(RootPath.getRootPath(), "drivers/geckodriver.exe"))

	@classmethod
	def openBrowserWithSpecifedDownloadPath(cls, path) -> webdriver:
		'''某些用例需要指定下载的路径，需要通过default_directory去修改webdriver默认下载路径'''
		if cls.driver_type == "CHROME":
			options = Options()
			options.add_experimental_option("prefs", {
				"download.default_directory": path,
				"download.prompt_for_download": False,
				"download.directory_upgrade": True,
				"safebrowsing.enabled": True
			})
			return webdriver.Chrome(executable_path=os.path.join(RootPath.getRootPath(), "drivers/chromedriver.exe"),
			                        options=options)
