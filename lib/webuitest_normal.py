# coding:utf-8

# Copyright 2017 INESA (Group) Co., Ltd. R&D Center
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# Author: yuy@rc.dddd.com
# Date:   July 2017

"""
@file webuitest_normal.py
"""

##
# @addtogroup webui
# @brief This is webui component
# @{
# @addtogroup webui
# @brief This is webui module
# @{
##

import unittest
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import sys
#sys.path.append("../")
from get_config import getconfig
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

url = getconfig("webui", "url")
username = getconfig("webui", "normal_username")
password = getconfig("webui", "normal_pwd")
id_login_mode = getconfig("webui", "id_login_mode")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:% \
(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='/var/log/istack_autotest.log',
    filemode='a')


class WebUITest(unittest.TestCase):
    """
    @class WebUITest
    """

    @classmethod
    def setUpClass(self):
        self.driver = webdriver.Chrome()
        # self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(url)
        try:
            xpath = ".//*[@id='content_body']/div/div/div[1]/h1"
            self.driver.find_element_by_xpath(xpath)
        except:
            element_username = self.driver.find_element_by_id("id_username")
            element_password = self.driver.find_element_by_id("id_password")
            element_username.clear()
            element_username.send_keys(username)
            element_password.clear()
            element_password.send_keys(password)
            self.driver.find_element_by_id("loginBtn").click()
            time.sleep(3)

        # 设置语言为中文
        xpath = ".//*[@id='navbar-collapse']/ul[2]/li[1]/a"
        self.driver.find_element_by_xpath(xpath).click()
        css_selector = "a[href=\"/dashboard/settings/\"]"
        self.driver.find_element_by_css_selector(css_selector).click()
        Select(self.driver.find_element_by_id("id_language")). \
            select_by_visible_text(u"简体中文 (zh-cn)")
        css_selector = "input[class=\"btn btn-primary\"]"
        self.driver.find_element_by_css_selector(css_selector).click()

    @classmethod
    def tearDownClass(self):
        driver = self.driver
        driver.quit()

    def setUp(self):
        pass

    def tearDown(self):
        # pass
        self.driver.get(url)
        # self.driver.find_element_by_link_text(u"管理员")

##
# @}
# @}
##
