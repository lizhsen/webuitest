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
@file webuitest.py
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
import os
from get_config import getconfig
from logger import logger
import datetime
from get_element import GetElement

reload(sys)
sys.setdefaultencoding('utf-8')

url = getconfig("webui", "url")
username = getconfig("webui", "username")
password = getconfig("webui", "password")
id_login_mode = getconfig("webui", "id_login_mode")
Browser = getconfig("webui", "browser")

# login browser
def login(driver, username, password):
    logger('INFO', "start to login browser")
    driver.get(url)
    time.sleep(1)
    try:
        # 退出系统
        xpath = "//*[@id='navbar-collapse']/ul[2]/li[1]/a"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(1)
        driver.find_element_by_link_text("退出").click()
        time.sleep(3)
    except:
        logger('DEBUG', 'with no need for login out, login direct')
    element_username = driver.find_element_by_id("id_username")
    element_password = driver.find_element_by_id("id_password")
    element_username.clear()
    element_username.send_keys(username)
    element_password.clear()
    element_password.send_keys(password)
    driver.find_element_by_id("loginBtn").click()
    time.sleep(3)
    logger('INFO', "login browser success")

    # 设置语言为中文
    xpath = ".//*[@id='navbar-collapse']/ul[2]/li[1]/a"
    driver.find_element_by_xpath(xpath).click()
    css_selector = "a[href=\"/dashboard/settings/\"]"
    driver.find_element_by_css_selector(css_selector).click()
    Select(driver.find_element_by_id("id_language")). \
        select_by_visible_text(u"简体中文 (zh-cn)")
    css_selector = "input[class=\"btn btn-primary\"]"
    driver.find_element_by_css_selector(css_selector).click()


# basic class
class WebUITest(unittest.TestCase):
    """
    @class WebUITest
    """

    def get_json_file(self):
        # 获取webui路径下所有json文件
        file_dir = os.path.abspath(os.path.dirname(os.getcwd())) + '/webui'
        json_list = []
        for root, dirs, files in os.walk(file_dir):
            for filee in files:
                if os.path.splitext(filee)[1] == '.json':
                    json_list.append(filee)
        return json_list

    @classmethod
    def setUpClass(self):
        if Browser == 'Chrome':
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        login(self.driver, username, password)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        logger('INFO', "login out browser")

    def setUp(self):
        GetElement.delstep = []
        GetElement.username = username
        GetElement.password = password
        GetElement.casetime = datetime.datetime.now().strftime("_%Y%m%d%H%M%S")
        #if token is out of date, login system again
        try:
            self.driver.get(url)
            self.driver.find_element_by_link_text("管理员").click()
        except:
            login(self.driver, username, password)

    def tearDown(self):
        # delete object
        logger("INFO", "清理数据为：%s" % ", ".join(GetElement.delstep))
        elemobject = GetElement(self.driver)
        for step in GetElement.delstep:
            action = step[:2]
            element = step[2:]
            if action == u"清理":
                logger("INFO", "正在清理：%s" % step)
                elemobject.handle_destroynlp(element)
##
# @}
# @}
#
