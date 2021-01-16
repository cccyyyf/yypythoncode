from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class KeyBoardUtil:
	@classmethod
	def enter(cls, driver):
		actions = ActionChains(driver)
		actions.send_keys(Keys.ENTER).perform()

	@classmethod
	def esc(cls, driver):
		actions = ActionChains(driver)
		actions.send_keys(Keys.ESCAPE).perform()

	@classmethod
	def page_down(cls, driver):
		actions = ActionChains(driver)
		actions.send_keys(Keys.PAGE_DOWN).perform()

	@classmethod
	def page_up(cls, driver):
		actions = ActionChains(driver)
		actions.send_keys(Keys.UP).perform()