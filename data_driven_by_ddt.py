# encoding=utf-8
from selenium import webdriver
import unittest, time
import logging, traceback
import ddt
from selenium.common.exceptions import NoSuchElementException

# 初始化日志对象
logging.basicConfig(
    # 日志级别
    level = logging.INFO,
    # 日志格式
    # 时间、代码所在文件名、代码行号、日志级别名字、日志信息
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    # 打印日志的时间
    datefmt = '%a, %d %b %Y %H:%M:%S',
    # 日志文件存放的目录（目录必须存在）及日志文件名
    filename = 'D:/phpStudy/unittest_ddt/log.txt',
    # 打开日志文件的方式
    filemode = 'w'
)

@ddt.ddt
class TestDemo(unittest.TestCase):
    def setUp(self):
         #self.driver = webdriver.Ie(executable_path = "d:\\IEDriverServer")
         self.driver = webdriver.Chrome(executable_path = "d:\\chromedriver")
         self.driver.set_page_load_timeout(10)
         
    @ddt.data([u"hello", u"哈喽"],
              [u"glory", u"光荣"],
              [u"morning", u"早晨"])
    @ddt.unpack   #解包，将测试数据对应到testdata 和 expectdata
    def test_dataDrivenByObj(self, testdata, expectdata):
        url = "https://www.iciba.com"
        # 访问百度首页
        self.driver.get(url)
        # 设置隐式等待时间为5秒
        #self.driver.implicitly_wait(5)
        
        try:
            # 找到搜索输入框，并输入测试数据
            self.driver.find_element_by_xpath("//input[@type='search']").send_keys(testdata)
            # 找到搜索按钮，并点击
            self.driver.find_element_by_xpath('//input[@placeholder="请输入您要翻译的单词"]/following-sibling::div').click()
            time.sleep(5)
            # 断言期望结果是否出现在页面源代码中
            self.assertTrue(expectdata in self.driver.page_source)

        except NoSuchElementException as e:
            logging.error(u"查找的页面元素不存在，异常堆栈信息：" \
                          + str(traceback.format_exc()))
            raise NoSuchElementException
        except AssertionError as e:
            logging.info(u"搜索“%s”，期望“%s”，失败" %(testdata, expectdata))
            raise e
        except Exception as e:
            logging.error(u"未知错误，错误信息：" + str(traceback.format_exc()))
            raise e
        else:
            logging.info(u"搜索“%s”，期望“%s”通过" %(testdata, expectdata))

        

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()