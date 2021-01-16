from objects.webpage.utils.PropertiesUtil import PropertiesUtil
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from abc import abstractmethod, ABCMeta
from objects.webpage.baseObjects.DriverFacory import DriverFactory
from objects.webpage.utils.Logging import *
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from threading import Lock

lock = Lock()
logger = get_console_logger(__name__)


class PageObjectPO(object):
    '''
    此类为操作类，所有的子类页面PO，都需要继承这个类，这样所有的PO页面对象类就有了可以操作webdriver的方法
    此类为抽象类，有一个抽象方法getPropertiesPath()
    '''
    __metaclass__ = ABCMeta
    driver: webdriver = webdriver.Chrome()
    implicitly_wait_timeout = 60#默认的隐式等待时间

    @abstractmethod
    def getPropertiesPath(self):
        '''抽象方法，所有继承本类的方法都需要实现这个方法
        这个方法会返回所在实现类所对应的yml配置文件的路径
        '''
        pass

    """
    pytest不允许有构造函数
    def __init__(self, *args, **kwargs):
        '''如果构造函数中有driver的数据那就将数据赋值给本类的变量driver
        如果构造函数中没有传入数据，并且本类的变量driver为空，那就自动去DriverFactory中获取一个webdriver对象
        并复制给本类的变量driver
        这样driver就会变成webdriver类型的变量，从而可以调用所有webdriver的方法
        '''
        if kwargs.get("driver"):
            self.setDriver(kwargs.get("driver"))
        elif self.driver == None:
            self.setDriver(self.getDriver())
    """
    def getDriver(self) -> webdriver:
        return DriverFactory().openBrowser()

    def setDriver(self, driver: webdriver):
        self.driver = driver
        self.driver.implicitly_wait(self.implicitly_wait_timeout)
        self.driver.maximize_window()

    def closeCurrentBrowser(self):
        logger.info("关闭当前窗口")
        self.driver.close()

    @property
    def page_url(self) -> str:
        return self.driver.current_url

    def closeAllBrowsers(self):
        logger.info("关闭浏览器")
        self.driver.quit()

    def goTo(self, URL):
        logger.info("跳转到链接: " + URL)
        self.driver.get(URL)

    def refresh(self):
        self.driver.refresh()

    def waiting_while_mask_exists(self, timeout=0.5):
        '''查找loading的蒙层是否存在，存在就等待，不存在退出
        神州系统在页面加载的时候会有一个页面的蒙层出现，现在在所有的操作之前都会去判断是否有这个蒙层的存在
        这样在大部分的用例中都不再需要通过time.sleep去强制等待
        '''
        global lock#多线程锁，在多线程时候来保证线程安全，因为方法需要修改隐式等待的时间
        masks = [(By.XPATH,
                  "//div[contains(@class,'el-loading-mask is-fullscreen')] [not(contains(@style,'display: none'))]")]
        lock.acquire()
        self.driver.implicitly_wait(timeout)
        for mask in masks:
            while True:
                try:
                    WebDriverWait(self.driver, timeout, 0.1).until(EC.visibility_of_element_located(mask))
                    continue
                except Exception:
                    break
        self.driver.implicitly_wait(self.implicitly_wait_timeout)
        lock.release()

    def getElementLocated(self, locator: str, timeout=implicitly_wait_timeout) -> WebElement:
        '''根据字符串读取对应的yml文件中查找（定位方法，定位字符串）然后调用find_element并返回WebElement对象
        在返回webelement对象之前都会用visibility_of_element_located去判断这个对象是否已经在页面展示
        '''
        locatorByTuple = PropertiesUtil.loadLocatorValueFromYml(self.getPropertiesPath(), locator)
        logger.info("查找元素: '" + locator + "' :" + str(locatorByTuple))
        WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_element_located(locatorByTuple))
        self.waiting_while_mask_exists()
        return self.driver.find_element(*locatorByTuple)

    def getElementLocatedReplaceLocatorValue(self, locator: str, newValue: str, index="1",timeout=implicitly_wait_timeout) -> WebElement:
        '''根据字符串读取对应的yml文件中查找（定位方法，定位字符串），然后将类似${1}的字符串进行替换
        形成新的xpath，然后调用find_element并返回WebElement对象'''
        locatorByTupleOriginal = PropertiesUtil.loadLocatorValueFromYml(self.getPropertiesPath(), locator)
        value = locatorByTupleOriginal[1].replace("${" + index + "}", newValue)
        locatorByTuple = (locatorByTupleOriginal[0], value)
        logger.info("查找元素: '" + locator + "' :" + str(locatorByTuple))
        WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_element_located(locatorByTuple))
        return self.driver.find_element(*locatorByTuple)

    def switchToIframe(self, locator: str, timeout=implicitly_wait_timeout):
        '''
        切换iframe
        '''
        locatorByTuple = PropertiesUtil.loadLocatorValueFromYml(self.getPropertiesPath(), locator)
        logger.info("正在切换到iframe: " + str(locatorByTuple))
        WebDriverWait(self.driver, timeout, 1).until(EC.frame_to_be_available_and_switch_to_it(locatorByTuple))

    def createSnapShot(self, file_name):
        self.driver.save_screenshot(file_name)

    def execute_js(self, js):
        self.driver.execute_script(js)

    def verifyElementExists(self, locator):
        exists = False
        try:
            if self.getElementLocated(locator):
                exists = True
                logger.info("元素 " + locator + " 存在，验证通过")
        except Exception as e:
            exists = False
            logger.info("元素 " + locator + " 不存在，验证不通过")
            logger.info(e)
        assert exists == True

    def clickElement(self, locator: str):
        logger.info("尝试点击元素 '" + locator + "'")
        self.getElementLocated(locator).click()

    def clickElementWithReplacedLocatorValue(self, locator, newValue, index="1"):
        logger.info("尝试点击元素 '" + locator + "'")
        self.getElementLocatedReplaceLocatorValue(locator, newValue, index).click()

    def click(self, locator: tuple):
        self.driver.find_element(*locator).click()

    def switchToDefaultIframe(self):
        self.driver.switch_to.default_content()

    def sendKeys(self, locator, keyWords):
        logger.info("尝试在元素 '" + locator + "' 上输入:" + str(keyWords))
        self.getElementLocated(locator).send_keys(str(keyWords))

    def clearAndSendKeys(self, locator, keyWords):
        logger.info("清空 '" + locator)
        self.clear(locator)
        logger.info("尝试在元素 '" + locator + "' 上输入:" + str(keyWords))
        self.getElementLocated(locator).send_keys(str(keyWords))

    def swithToNewTab(self):
        all_tabs: list = self.driver.window_handles
        cur_tab = self.driver.current_window_handle
        if all_tabs.__len__() == 2:
            for tab in all_tabs:
                if not tab == cur_tab:
                    self.driver.switch_to.window(tab)

    def swithToTab(self, window):
        self.driver.switch_to.window(window)

    def getCurrentWindowHandle(self):
        return self.driver.current_window_handle

    def clear(self, locator: str):
        self.getElementLocated(locator).clear()

    def get_text(self, locator) -> str:
        logger.info("获取文本内容：'" + self.getElementLocated(locator).text + "'")
        return self.getElementLocated(locator).text

    def get_text_with_locator_replace_value(self, locator, newValue, index="1") -> str:
        return self.getElementLocatedReplaceLocatorValue(locator, newValue, index).text

    def get_element_attribute(self, locator, attr):
        return self.getElementLocated(locator).get_attribute(attr)
