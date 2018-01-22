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
# Date:   Sep 2017

"""
@file webuitest1.py
"""

##
# @addtogroup webui
# @brief This is webui component
# @{
# @addtogroup webui
# @brief This is webui module
# @{
##

import os
import unittest
from selenium import webdriver
import xmlrunner
import time
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pdfkit
import os
import ConfigParser
from optparse import OptionParser

conf = ConfigParser.ConfigParser()
BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
conf.read(os.path.join(BASEDIR, "config.ini"))
ip = conf.get("webui", "ip_address")
report_path = conf.get("webui", "report_path")


class WebUITest(unittest.TestCase):
    """
    @class WebUITest
    """
    HtmlString = ''

    def setUp(self):
        self.driver = webdriver.Chrome("")

    def admin_login(self, username, password, step1, step2):
        self.driver.get("http://" + ip + "/saod/login")
        time.sleep(3)
        element_username = self.driver.find_element_by_id("username")
        element_password = self.driver.find_element_by_id("password")
        element_username.clear()
        element_username.send_keys(username)
        element_password.clear()
        element_password.send_keys(password)
        time.sleep(3)
        Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
        PATH = "/test_login_" + Time
        self.makeDirs(PATH + "/snapshot")
        self.PrintReportHead("WebUI test report for case:test_login")
        self.GetSnapshot(PATH + "/snapshot/test_login_1.png")
        self.PrintReportBody("第一步:输入用户名和密码: <br> username:" +
                             username + "<br> password:" +
                             password + "<br><font color=\"#FF0000\">" +
                             step1 + "</font>", "snapshot/test_login_1.png")
        self.driver.find_element_by_css_selector(
            "button[type=\"submit\"]").click()
        time.sleep(3)
        self.GetSnapshot(PATH + "/snapshot/test_login_2.png")
        self.PrintReportBody("第二步：登录" + "<br><font color=\"#FF0000\">" +
                             step2 + "</font>", "snapshot/test_login_2.png")
        self.PrintReportTail(PATH)

    def get_tab_element(self, tab_name):
        tab = self.driver.find_element_by_link_text(tab_name)
        time.sleep(1)
        return tab

    def get_element_by_xpath(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        return element

    def fill_input_box(self, label, content):
        self.driver.find_element_by_id(label).clear()
        self.driver.find_element_by_id(label).send_keys(content)

    def select_element(self, label, c):
        Select(self.driver.find_element_by_id(
            label)).select_by_visible_text(c)

    def get_element_by_id(self, id_string):
        if id_string == u"身份管理-项目":
            css_selector = "a[href=\"/dashboard/identity/\"]"
            element = self.driver.find_element_by_css_selector(
                css_selector)
        elif id_string == u"创建用户":
            xpath = ".//*[@id='create_user_form']/div[2]/input"
            element = self.driver.find_element_by_xpath(xpath)
        elif id_string == u"创建项目":
            xpath = ".//*[@id='modal_wrapper']/div/form/div/div/div[3]/input"
            element = self.driver.find_element_by_xpath(xpath)
        elif id_string == u"创建容器":
            xpath = ".//*[@id='create_container_form']/div[2]/input"
            element = self.driver.find_element_by_xpath(xpath)
        elif id_string == u"创建云硬盘":
            xpath = ".//*[@id='None']/div[2]/input"
            element = self.driver.find_element_by_xpath(xpath)
        elif id_string == u"创建实例":
            xpath = ".//*[@id='modal_wrapper']/div/form/div/div/div[3]/input"
            element = self.driver.find_element_by_xpath(xpath)
        elif id_string == u"网络-网络":
            css_selector = "a[href=\"/dashboard/project/networks/\"]"
            element = self.driver.find_element_by_css_selector(css_selector)
        else:
            element = self.driver.find_element_by_id(id_string)
        return element

    def element_click(self, element):
        element.click()
        time.sleep(5)

    def instance_destroy(self, name):
        self.driver.find_element_by_link_text(name).click()
        time.sleep(2)
        xpath = ".//*[@id='instance_details__overview']/div[1]/dl/dd[2]"
        instance_id = self.driver.find_element_by_xpath(xpath).text
        xpath = "//div[@id='content_body']/div/div/div/form/div/a[2]"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(1)
        element_id = "instances__row_" + instance_id + "__action_terminate"
        self.driver.find_element_by_id(element_id).click()
        time.sleep(2)
        xpath = ".//*[@id='modal_wrapper']/div/div/div/div[3]/a[2]"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(5)
        filename = "/screenshot/instance_destroy.png"
        self.driver.get_screenshot_as_file(filename)

    def volume_destroy(self, name):
        self.driver.find_element_by_link_text(name).click()
        time.sleep(2)
        xpath = ".//*[@id='volume_details__overview']/div[1]/dl/dd[2]"
        volume_id = self.driver.find_element_by_xpath(xpath).text
        time.sleep(1)
        xpath = ".//*[@id='content_body']/div/div/div[1]/form/div/a[2]"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(1)
        xpath = ".//*[@id='volumes__row_" + volume_id + "__action_delete']"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(2)
        xpath = ".//*[@id='modal_wrapper']/div/div/div/div[3]/a[2]"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(5)
        filename = "/screenshot/volume_destroy.png"
        self.driver.get_screenshot_as_file(filename)

    def user_destroy(self, name):
        self.driver.find_element_by_link_text(name).click()
        time.sleep(2)
        time.sleep(1)
        xpath = ".//*[@id='content_body']/div/div/div[1]/form/div/a[2]"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(1)
        css_selector = "button[class=\"btn btn-default btn-sm btn-danger\"]"
        self.driver.find_element_by_css_selector(css_selector).click()
        time.sleep(2)
        xpath = ".//*[@id='modal_wrapper']/div/div/div/div[3]/a[2]"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(5)
        filename = "/screenshot/user_destroy.png"
        self.driver.get_screenshot_as_file(filename)

    def internet_destroy(self, name):
        self.element_click(self.get_tab_element(name))
        xpath = ".//*[@id='content_body']/div/div/div[2]/div/div/dl/dd[2]"
        internal_id = self.driver.find_element_by_xpath(xpath).text
        time.sleep(1)
        xpath = "//div[@id='content_body']/div/div/div/form/div/a[2]"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(1)
        element_id = "networks__row_" + internal_id + "__action_delete"
        self.element_click(self.get_element_by_id(element_id))
        time.sleep(1)
        css_selector = "a[class=\"btn btn-primary\"]"
        self.driver.find_element_by_css_selector(css_selector).click()

    def tenant_destroy(self, name):
        self.driver.find_element_by_link_text(name).click()
        time.sleep(2)
        xpath = ".//*[@id='content_body']/div/div/div[2]/div/div/dl/dd[4]"
        tenant_id = self.driver.find_element_by_xpath(xpath).text
        time.sleep(1)
        xpath = ".//*[@id='content_body']/div/div/div[1]/form/div/a[2]"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(1)
        css_selector = "button[class=\"btn btn-default btn-sm btn-danger\"]"
        self.driver.find_element_by_css_selector(css_selector).click()
        time.sleep(2)
        xpath = ".//*[@id='modal_wrapper']/div/div/div/div[3]/a[2]"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(3)
        filename = "/screenshot/tenant_destroy.png"
        self.driver.get_screenshot_as_file(filename)

    def container_destroy(self, name):
        time.sleep(5)
        xpath = ".//*[@id='containers__row__" + name + "']/td[4]/div/a[2]"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(1)
        xpath = ".//*[@id='containers__row_" + name + "__action_delete']"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(1)
        xpath = ".//*[@id='modal_wrapper']/div/div/div/div[3]/a[2]"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(3)
        filename = "/screenshot/container_destroy.png"
        self.driver.get_screenshot_as_file(filename)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()

    def isElementExist(self, css):

        try:
            elements = self.driver.find_element_by_link_text(css)
            return True
        except:
            return False

    def makeDirs(self, path):
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(report_path + path)
        else:
            os.remove(report_path + path)
            os.makedirs(report_path + path)

    def GetSnapshot(self, path):
        self.driver.get_screenshot_as_file(report_path + path)

    def PrintReportHead(self, title):

        self.HtmlString = '''
        <html>
        <head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>WebUI test report</title>
                <style>
                body{text-align:center}
                </style>
                </head>
              <body>
                  <br><h1 align="center">%s</h1><br>
                  ''' % title

    def PrintReportBody(self, step, pic_path):

        body = '''
            <p><align="center"><strong><h3>%s</h3></strong></p>
            <img src="%s" width="960px" height="540px"/>
''' % (step, "./" + pic_path)
        self.HtmlString = self.HtmlString + body

    def PrintReportTail(self, path):
        tail = '''
             </body>
             </html>
         '''
        self.HtmlString = self.HtmlString + tail

        os.mknod(report_path + path + "/" + path + "_report.html")
        report = open(report_path + path + "/" + path + "_report.html", 'w')
        report.write(self.HtmlString)
        report.close()
        pdfkit.from_file(report_path + path + "/" + path + "_report.html",
                         report_path + path + "/" + path + "_report.pdf")

##
# @}
# @}
##
