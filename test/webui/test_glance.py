from webuitest import webdriver, WebUITest

from ddt import ddt, data, file_data, unpack

from get_element import GetElement

from logger import logger

import sys

sys.path.append("C:\Users\lizhsen\Desktop\dddd-test\dddd-test\lib\webuitest")

@ddt
class BasicGlance(WebUITest):

    @file_data('glance.json')
    def test_glance(self, data):
        logger("INFO", "CaseName is %s" % self._testMethodName)
        driver = GetElement(self.driver)
        GetElement.CaseName = self._testMethodName
        data = driver.perconditon(self.get_json_file(), data)
        driver.ui_engine(data)
