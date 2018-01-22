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
# Author: zhounh@rc.dddd.com
# Date:   Sep 2017

"""
@file get_element.py
"""

##
# @addtogroup webui
# @brief This is webui component
# @{
# @addtogroup webui
# @brief This is webui module
# @{
##

import datetime
import json
import os
import re
import sys
import time
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
#from pymouse import PyMouse

import webuitest
from debug import get_img
from get_config import getconfig
from get_js import GetJs
from run_command import Command
from logger import logger

reload(sys)
sys.setdefaultencoding('utf-8')
url = getconfig("webui", "url")
wait_time = int(getconfig("webui", "wait_time"))


class GetElement(unittest.TestCase):
    """
    @class GetElement
    """

    # global var
    delstep = []
    nowtime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    CaseName = "default_name"
    casetime = None
    SelectVal = None
    username = getconfig("webui", "username")
    password = getconfig("webui", "password")

    def __init__(self, selenium_driver):
        self.driver = selenium_driver
        self.element_text = ''

    # for WebDriverWait
    def find_element(self, *loc):
        return self.driver.find_element(*loc)

    # operate element
    def handle_element(self, element, optype, content):
        if optype == "click":
            element.click()
        if optype == "fill":
            element.clear()
            filltext = content
            if content == "getValue":
                filltext = self.element_text
            if content.find("$") != -1:
                filltext = getconfig("webui", content[1:])
            element.send_keys(filltext)
        if optype == "select":
            if "getValue" in content:
                content = content.replace("getValue", self.element_text)
            if content == "列表已有值":
                content = Select(element).options[1].text
                self.SelectVal = content
            Select(element).select_by_visible_text(content)
        logger("INFO", "find element successfully in page")

    # circular process elements
    def cycle_element(self, elemtype, elements, optype, content):
        element = None
        for i in elements:
            logger("DEBUG", i)
            try:
                if elemtype == "id":
                    element = self.driver.find_element_by_id(i)
                elif elemtype == "css":
                    element = self.driver.find_element_by_css_selector(i)
                elif elemtype == "xpath":
                    element = self.driver.find_element_by_xpath(i)
                else:
                    logger("ERROR", "%s elemtype not in ['id','css','xpath']" % elemtype)
                    assert False, "%s element type not in ['id','css','xpath']" % elemtype
                self.handle_element(element, optype, content)
                return element
            except:
                logger("DEBUG", "I am not the correct one")
                element = None
        return element

    # get element from json files
    def get_allelement(self, elementname, optype=None, content=None):
        logger("INFO", "start to find %s from element json" % elementname)
        path = os.path.split(os.path.realpath(__file__))[0]
        id_file = open(os.path.join(path, "element_id.json"))
        id_dict = json.load(id_file)
        css_file = open(os.path.join(path, "element_css.json"))
        css_dict = json.load(css_file)
        xpath_file = open(os.path.join(path, "element_xpath.json"))
        xpath_dict = json.load(xpath_file)
        element_dict = {}
        if elementname in id_dict.keys():
            element_dict["id"] = id_dict[elementname]
        if elementname in css_dict.keys():
            element_dict["css"] = css_dict[elementname]
        if elementname in xpath_dict.keys():
            element_dict["xpath"] = xpath_dict[elementname]
        logger("INFO", "element dict is " + str(element_dict))
        for i in range(wait_time):
            logger("DEBUG", "consume %d seconds already" %i)
            time.sleep(1)
            try:
                element = self.driver.find_element_by_link_text(elementname)
                self.handle_element(element, optype, content)
                return element
            except:
                for key, value in element_dict.items():
                    if key == "id":
                        try:
                            element = self.driver.find_element_by_id(value)
                            self.handle_element(element, optype, content)
                            return element
                        except:
                            if isinstance(value, list):
                                element = self.cycle_element(
                                    key, value, optype, content)
                                if element is not None:
                                    return element
                    if key == "css":
                        try:
                            element = self.driver.find_element_by_css_selector(
                                value)
                            self.handle_element(element, optype, content)
                            return element
                        except:
                            if isinstance(value, list):
                                element = self.cycle_element(
                                    key, value, optype, content)
                                if element is not None:
                                    return element
                    if key == "xpath":
                        try:
                            element = self.driver.find_element_by_xpath(value)
                            self.handle_element(element, optype, content)
                            return element
                        except:
                            if isinstance(value, list):
                                element = self.cycle_element(
                                    key, value, optype, content)
                                if element is not None:
                                    return element
        logger("WARN", "failed to find element in page")
        return None

    # verify tabname exist or not
    def get_tab_element(self, tab_name):
        element = self.get_allelement(tab_name)
        if element is None:
            try:
                xpath = "//*[@data-display='" + tab_name + "']"
                element = self.driver.find_element_by_xpath(xpath)
            except:
                dds = self.driver.find_elements_by_tag_name("dd")
                tds = self.driver.find_elements_by_tag_name("td")
                dts = self.driver.find_elements_by_tag_name("dt")
                h5s = self.driver.find_elements_by_tag_name("h5")
                nodelable = self.driver.find_elements_by_css_selector("text.nodeLabel")
                elemlist = dds + tds + dts + nodelable + h5s
                for i in elemlist:
                    if re.search(re.compile(tab_name), i.text):
                        element = i
                        logger("DEBUG", "find element successfully in dd|td|dt")
                        break
        if element:
            return element.is_displayed()
        return element

    # verify element value correct or not
    def check_value(self, elementstr):
        getjs = GetJs(self.driver)
        command = Command(self.driver)
        # get screenshot before checking
        if elementstr.find(u"为") != -1:
            val = elementstr.split(u"为")
            if val[0].find(u"本地") != -1:
                srcval = str(command.get_local_cmd(val[0]))
            elif val[0].find(u"虚拟机") != -1:
                if val[0].find('getValue') != -1:
                    val[0] = val[0].replace("getValue", self.element_text)
                if val[0].find("windows") != -1:
                    srcval = command.handle_winnlp(val[0])
                else:
                    srcval = command.get_cmd(val[0])
            elif val[0].find(u"行中") != -1 and val[0].find(u"列") != -1:
                tab = val[0].replace(u'页面上', "")
                srcval = getjs.get_tdtext(tab)
            elif re.match(re.compile(u'页面上.*的数量'), val[0]):
                tab = val[0].replace(u'页面上', "").replace(u"的数量", "")
                srcval = getjs.get_number(tab)
            elif val[0].find(u"系统提示") != -1:
                srcval = getjs.get_hintinfo()
            elif val[0].find(u"必填项提示") != -1:
                tab = val[0].replace(u'页面上', "").replace(u"必填项提示", "")
                srcval = getjs.get_promptinfo(tab)
            elif re.match(re.compile(u'页面上.*表的数目的值'), val[0]):
                tab = val[0].replace(u'页面上',"").replace(u"表的数目的值","")
                srcval = self.get_table_number(tab)
            elif re.match(re.compile(u'页面上.*的值'), val[0]):
                tab = val[0].replace(u'页面上', "").replace(u"的值", "")
                srcval = self.get_elemtext(tab)
            else:
                logger("ERROR", "Sync Error: check format is error")
                assert False, "Sync Error: check format is error"
            if val[1] == "列表已有值":
                destval = self.SelectVal
            else:
                destval = val[1]
            logger("INFO", "srcval is %s" % srcval)
            logger("INFO", "destval is %s" % destval)
            get_img(self.driver, self.nowtime, self.CaseName)
            if destval.find("+") != -1:
                number = destval.split("+")[1]
                destval = int(self.element_text) + int(number)
                srcval = int(srcval)
                logger("INFO", "destval+ is %s" % destval)
            if val[0].find(u"数量") != -1 or val[1].find("getValue+") != -1:
                if srcval == destval:
                    logger("INFO", "check successfully")
                    self.assertTrue(True)
                else:
                    logger("INFO", "check failed")
                    self.assertTrue(False, msg="%s is not equal to %s" %(srcval, destval))
            elif val[0].find(u"提示") != -1 or val[0].find(u"windows虚拟机") != -1:
                if srcval.find(destval) != -1:
                    logger("INFO", "check successfully")
                    self.assertTrue(True)
                else:
                    logger("INFO", "check failed")
                    self.assertTrue(False, msg="%s is not in %s" %(destval, srcval))
            else:
                if re.match(re.compile(destval), srcval):
                    logger("INFO", "check successfully")
                    self.assertTrue(True)
                else:
                    logger("INFO", "check failed")
                    self.assertTrue(False, msg="%s is not in %s" %(destval, srcval))
        elif elementstr.find(u"不存在") != -1:
            val = elementstr.split(u"不存在")
            result = self.get_tab_element(val[1])
            get_img(self.driver, self.nowtime, self.CaseName)
            if result:
                logger("INFO", "check failed")
                self.assertTrue(False, msg="%s is exist" % val[1])
            else:
                logger("INFO", "check successfully")
                self.assertTrue(True)
        elif elementstr.find(u"存在") != -1:
            val = elementstr.split(u"存在")
            result = self.get_tab_element(val[1])
            get_img(self.driver, self.nowtime, self.CaseName)
            if result:
                logger("INFO", "check successfully")
                self.assertTrue(True)
            else:
                logger("INFO", "check failed")
                self.assertTrue(False, msg="%s is not exist" % val[1])
        else:
            logger("ERROR", "Sync Error: check format is error")
            assert False, "Sync Error: check format is error"

    # handle login nlp
    def handle_loginnlp(self, element):
        self.password = element.split(u'密码为')[1]
        self.username = element.split(u'密码为')[0].split(u'用户名为')[1]
        webuitest.login(self.driver, self.username, self.password)

    # handle click nlp
    def handle_clicknlp(self, element):
        for item in element.split('->'):
            if item == "getValue":
                item = self.element_text
            self.click_button(item)

    # handle sleep nlp
    def handle_sleepnlp(self, element):
        seconds = float(element[:-1])
        time.sleep(seconds)

    # handle fill nlp
    def handle_fillnlp(self, element):
        fillcontent = element.split(",")
        for i in fillcontent:
            con = i.split(u"为")
            label = con[0]
            content = con[1]
            self.fill_input_box(label, content)

    # handle choose nlp
    def handle_choosenlp(self, element):
        choosecontent = element.split(",")
        for i in choosecontent:
            con = i.split(u"为")
            label = con[0]
            content = con[1]
            self.select_element(label, content)

    # handle get nlp
    def handle_getnlp(self, element):
        getjs = GetJs(self.driver)
        tablist = element.split(u"为")
        tabname = tablist[0][:-2]
        if u"表的数目" in tabname:
            self.element_text = self.get_table_number(tabname[:-4])
        elif tabname.find(u"行中") != -1 and tabname.find(u"列") != -1:
            result = getjs.get_tdtext(tabname)
            self.element_text = result.split("<li>")[1].split("</li>")[0]
        else:
            self.element_text = self.get_elemtext(tabname)
        logger("INFO", "getValue is %s" % self.element_text)


    # handle wait nlp
    def handle_waitnlp(self, element):
        conlist = element.split(",")
        seconds = float(conlist[0][:-1])
        waittype = None
        text = None
        exist = "True"
        if conlist[1].find(u"类型为") != -1:
            waittype = conlist[1][3:]
            tabname = conlist[2].split(u'的对象')[0][3:]
            text = conlist[2].split(u"状态为")[1]
        elif conlist[1].find(u'不存在') != -1:
            tabname = conlist[1][6:]
            exist = "False"
        elif conlist[1].find(u'存在') != -1:
            tabname = conlist[1][5:]
            if tabname == u'上传成功':
                waittype = u"上传文件"
                text = u'上传成功'
        else:
            logger("ERROR", "Sync Error: wait format is not correct!")
            assert False, "Sync Error: wait format is not correct!"
        self.wait_element(tabname, seconds, waittype, exist, text)

    # handle destroy nlp
    def handle_destroynlp(self, element):
        logger("INFO", "start to destroy object")
        if element == u'浮动IP':
            self.floatIP_destroy()
        else:
            deltype = element.split(u"为")[0]
            delname = element.split(u"为")[1]
            logger("INFO", "删除对象为: %s, %s" % (deltype, delname))
            # read destroy_data.json
            path = os.path.split(os.path.realpath(__file__))[0]
            data_file = open(os.path.join(path, "destroy_data.json"))
            data_dict = json.load(data_file)
            if deltype == u"容器":
                self.container_destroy(delname)
            elif deltype == u"容器对象":
                self.visualdir_destroy(delname)
            elif deltype == u"主机集合":
                self.host_aggregates_destroy(delname)
            elif deltype == u"镜像":
                self.image_destroy(delname)
            elif deltype in data_dict.keys():
                clickpath = data_dict[deltype][0]
                butname = data_dict[deltype][1]
                if delname.find("->") != -1:
                    namelist = delname.split("->")
                    delname = namelist[-1]
                    clickpath = clickpath + "->" + "->".join(namelist[:-1])
                self.object_destroy(clickpath, delname, butname)
            else:
                logger("ERROR", "Sync Error: destroy format is not correct!")
                assert False, "Sync Error: destroy format is not correct!"

    # click element
    def click_button(self, button_name):
        if u'的管理规则' in button_name:
            group = button_name.split(u'的管理规则')[0]
            xpath = "//*[@data-display='" + group + "']/td[4]/div/a"
            i = self.driver.find_element_by_xpath(xpath).click()
            return i
        elif re.match(re.compile(u'增加.*内网'), button_name):
            result = True
            netname = button_name.replace("增加", "").replace("内网", "")
            logger("INFO", button_name + " " +  netname)
            getjs = GetJs(self.driver)
            selected_network = getjs.add_net(netname, "selected_network")
            if selected_network == "success":
                logger("INFO", "inter network %s is default selected" % netname)
            else:
                available_network = getjs.add_net(netname, "available_network")
                if available_network != "success":
                    result = None
                else:
                    logger("INFO", "inter network %s is selected successfully" % netname)
        else:
            result = self.get_allelement(button_name, optype="click")
            if result is None:
                elements = self.driver.find_elements_by_css_selector(".nodeLabel")
                for i in elements:
                    if i.text == button_name:
                        i.click()
                        logger("INFO", "find element by .nodeLabel, success to click")
                        result = i
                        break
        if result is None:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("ERROR", "%s Element is not found!" % button_name)
            assert False, "%s Element is not found!" % button_name

    # fill input box
    def fill_input_box(self, label, content):
        result = self.get_allelement(label, "fill", content)
        if result is None:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("ERROR", "%s Element is not found!" % label)
            assert False, "%s Element is not found!"  % label

    # operate select element
    def select_element(self, label, c):
        result = self.get_allelement(label, "select", c)
        if result is None:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("ERROR", "%s Element is not found!" % label)
            assert False, "%s Element is not found!"  % label

    # get element text
    def get_elemtext(self, tab_name):
        elemtext = None
        if tab_name == u'拓扑连线':
            ldddd = self.driver.find_elements_by_tag_name('line')
            elemtext = str(len(ldddd))
            return elemtext
        element = self.get_allelement(tab_name)
        if element is not None:
            elemtext = element.text
        else:
            getjs = GetJs(self.driver)
            elemtext = getjs.get_details(tab_name)
        if elemtext is None:
            get_img(self.driver, self.nowtime, self.CaseName)
        elemtext = elemtext.strip()
        return elemtext

    # wait for element tp appear
    def wait_element(self, elementname, seconds, type=None, exist="True", text=None):
        xpathstr = None
        if type == u'实例':
            xpathstr = "//*[@data-display='" + elementname + "']/td[7]"
            #text = u"运行中"
        if type == u'管理员实例':
            xpathstr = "//*[@data-display='" + elementname + "']/td[8]"
            #text = u"运行中"
        if type == u"实例快照":
            xpathstr = "//*[@data-display='" + elementname + "']/td[3]"
            #text = u"运行中"
        if type == u"云硬盘":
            xpathstr = "//*[@data-display='" + elementname + "']/td[5]"
            #text = u"可用配额"
        if type == u"绑定云硬盘":
            xpathstr = "//*[@data-display='" + elementname + "']/td[5]"
            #text = u"正在使用"
        if type == u"上传文件":
            xpathstr = "//*[@id='upload-object-btn']"
            #text = u"上传成功"
        if type == u"栈":
            xpathstr = "//*[@data-display='" + elementname + "']/td[6]"
            #text = u"创建完成"
        # if elementname is not link, then use xpath
        xpath = "//*[@data-display='" + elementname + "']"
        try:
            self.driver.find_element_by_link_text(elementname)
            element = (By.LINK_TEXT, elementname)
        except:
            element = (By.XPATH, xpath)
        # start to execute wait
        if exist == "True":
            if xpathstr:
                element = (By.XPATH, xpathstr)
                try:
                    WebDriverWait(self, 60, 1).until_not(
                        EC.text_to_be_present_in_element(element, "错误"))
                    WebDriverWait(self, seconds, 1).until(
                        EC.text_to_be_present_in_element(element, text))
                except Exception as msg:
                    logger("ERROR", "wait %s %s timeout" %(elementname, text))
                    logger("ERROR", msg)
                    get_img(self.driver, self.nowtime, self.CaseName)
                    assert False, msg
            else:
                try:
                    WebDriverWait(self, seconds, 1).until(
                        EC.presence_of_element_located(element))
                except Exception as msg:
                    logger("ERROR", "wait %s timeout" %elementname)
                    logger("ERROR", msg)
                    get_img(self.driver, self.nowtime, self.CaseName)
                    assert False, msg
        else:
            try:
                WebDriverWait(self, seconds, 1).until_not(
                    EC.presence_of_element_located(element))
            except Exception as msg:
                logger("ERROR", "wait %s timeout" % elementname)
                logger("ERROR", msg)
                get_img(self.driver, self.nowtime, self.CaseName)
                assert False, msg
        logger("INFO", "WebDriverWait is successfull")

    # test engine
    def ui_engine(self, steps, startidx=None, endidx=None):
        self.add_time_string(self.casetime, steps)
        # add 清理 step to self.delstep
        for step in steps:
            if step[:2] == u"清理" and step not in self.delstep:
                self.delstep.append(step)
        # start to execute step
        if startidx is None:
            startidx = 1
        if endidx is None:
            endidx = len(steps)
        for i in range(startidx - 1, endidx):
            step = steps[i]
            logger("INFO", "CaseStep is %s" % step)
            # 如果为已经封装好的方法，则跳转至common.json
            path = os.path.split(os.path.realpath(__file__))[0]
            data_file = open(os.path.join(path, "common.json"))
            data_dict = json.load(data_file)

            for key in data_dict:
                if step == key:
                    key_steps = data_dict[key]
                    other_steps = []
                    for j in range(i + 1, endidx):
                        other_step = steps[j]
                        other_steps.append(other_step)
                    new_step = key_steps + other_steps
                    return GetElement.ui_engine(self, new_step)

            action = step[:2]
            element = step[2:]
            # 对于鼠标点击操作
            if action == u"触发" and element == u"鼠标点击":
                self.mouse_click()
            # 对于登录操作
            elif action == u"登录":
                self.handle_loginnlp(element)
            # 对于点击操作
            elif action == u"点击":
                self.handle_clicknlp(element)
            # 对于延时操作
            elif action == u"等待":
                self.handle_sleepnlp(element)
            # 对于填表操作
            elif action == u"输入":
                self.handle_fillnlp(element)
            # 对于检查操作
            elif action == u"检查":
                self.check_value(element)
            # 对于选择操作
            elif action == u"选择":
                self.handle_choosenlp(element)
            # 获取元素的text
            elif action == u"获取":
                self.handle_getnlp(element)
            # 对于等待某个元素出现
            elif action == u"循环":
                self.handle_waitnlp(element)
            # 对于删除操作
            elif action == u"删除":
                self.handle_destroynlp(element)
            # 对于清理操作
            elif action == u"清理":
                pass
            # 容器上传对象
            elif action == u"上传":
                self.handle_fillnlp(element)
            # 选中元素的checkbox
            elif action == u"选中":
                self.click_checkbox(element)
            else:
                logger("ERROR", "Sync Error, %s action is not correct!" % action)
                assert False, "Sync Error, %s action is not correct!" % action

    # 增加时间戳,将%符号转成当前日期精确到秒
    def add_time_string(self, casetime, data):
        for idx, steps in enumerate(data):
            if steps.find("%时间戳") != -1:
                steps = steps.replace('%时间戳', str(casetime))
                data[idx] = steps

    # 处理json中case存在perconditon的情况
    def perconditon(self, jsonfiles, data):
        destroylist = []
        json_dicts = {}
        for jsonfile in jsonfiles:
            json_file = open(jsonfile)
            json_dict = json.load(json_file)
            json_dicts = dict(json_dict, **json_dicts)
        for idx, val in enumerate(data):
            if "前提条件" in val:
                precondition = val.split(u"为")[1]
                if precondition in json_dicts.keys():
                    prelist = json_dicts[precondition]
                    for step in prelist[:]:
                        if step[:2] == u"清理":
                            prelist.remove(step)
                            destroylist.append(step)
                    data[idx:idx] = prelist
                    data.remove(val)
                    data.insert(idx, "0")
                if precondition not in json_dicts.keys():
                    self.assertEquals(
                        True, False, "precondition value not in json file")
        data.extend(destroylist)
        num = data.count("0")
        if data.count("0") > 0:
            for i in range(num):
                data.remove("0")
        return data

    # def instance_destroy(self, menus,objectname,buttonname):
    def object_destroy(self, menus, delname, buttonname):
        self.driver.get(url)
        time.sleep(2)
        self.login_again()
        try:
            self.driver.find_element_by_link_text("管理员").click()
        except:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("WARN", "not exist 管理员 page")
            self.driver.find_element_by_link_text("项目").click()
        objectname = delname.split(",")
        for item in menus.split('->'):
            self.click_button(item)
        time.sleep(2)
        for i in objectname:
            xpathstr = "//*[@data-display='" + i + "']/td[1]/input"
            try:
                self.driver.find_element_by_xpath(xpathstr).click()
            except:
                logger("WARN", "%s is not exist!" % i)
        try:
            self.click_button(buttonname)
        except:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("WARN", "%s can not be clicked, destroy action is finished" % buttonname)
            return None
        time.sleep(2)
        self.driver.find_element_by_link_text(buttonname).click()
        time.sleep(1)
        get_img(self.driver, self.nowtime, self.CaseName)
        logger("INFO", "destroy action is finished")

    # delete containter
    def container_destroy(self, name):
        time.sleep(2)
        try:
            xpath = ".//*[@id='containers__row__" + name + "']/td[4]/div/a[2]"
            self.driver.find_element_by_xpath(xpath).click()
        except:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("WARN", "%s is not exist!" % name)
            return None
        time.sleep(1)
        xpath = ".//*[@id='containers__row_" + name + "__action_delete']"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(1)
        xpath = ".//*[@id='modal_wrapper']/div/div/div/div[3]/a[2]"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(1)
        get_img(self.driver, self.nowtime, self.CaseName)
        logger("INFO", "destroy action is finished")

    # delete image
    def image_destroy(self, name):
        self.driver.get(url)
        time.sleep(2)
        self.login_again()
        menus = "项目->镜像"
        for item in menus.split('->'):
            self.click_button(item)
        time.sleep(2)
        try:
            self.driver.find_element_by_link_text(name).click()
        except:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("WARN", "%s is not exist!" % name)
            return None
        time.sleep(2)
        elementid = "//*[@help_text='删除的镜像均无法恢复。']"
        xpath = "//*[@id='content_body']/div[1]/div/div[1]/form/div/a[2]"
        self.driver.find_element_by_xpath(xpath).click()
        self.driver.find_element_by_xpath(elementid).click()
        time.sleep(2)
        self.driver.find_element_by_link_text("删除镜像").click()
        time.sleep(1)
        get_img(self.driver, self.nowtime, self.CaseName)
        logger("INFO", "destroy action is finished")

    # delete image
    def host_aggregates_destroy(self, name):
        self.driver.get(url)
        time.sleep(2)
        self.login_again()
        self.driver.find_element_by_link_text("主机集合").click()
        time.sleep(2)
        buttonname = u"删除主机聚合"
        xpath = "//*[@data-display='" + name + "']/td[6]/div/a[2]"
        try:
            self.driver.find_element_by_xpath(xpath).click()
        except:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("WARN", "%s is not exist!" % name)
            return None
        time.sleep(2)
        self.driver.find_element_by_link_text("管理主机").click()
        time.sleep(2)
        try:
            self.driver.find_element_by_link_text("-").click()
            self.driver.find_element_by_link_text("-").click()
        except:
            logger("INFO", "host_aggregate do not bind host!")
        xpath = "//*[@id='modal_wrapper']/div/form/div/div/div[3]/input"
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(2)
        xpathstr = "//*[@data-display='" + name + "']/td[1]/input"
        self.driver.find_element_by_xpath(xpathstr).click()
        self.click_button(buttonname)
        time.sleep(2)
        self.driver.find_element_by_link_text(buttonname).click()
        time.sleep(1)
        get_img(self.driver, self.nowtime, self.CaseName)
        logger("INFO", "destroy action is finished")

    # visual dir destroy
    def visualdir_destroy(self, name):
        for i in name.split(','):
            xpathstr = "//*[@data-display='" + i + "']/td[1]/input"
            try:
                self.driver.find_element_by_xpath(xpathstr).click()
            except:
                logger("WARN", "%s is not exist!" % i)
        try:
            self.click_button(u"删除对象")
        except:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("WARN", "%s is not exist!" % name)
            return None
        time.sleep(2)
        self.driver.find_element_by_link_text(u"删除对象").click()
        time.sleep(1)
        get_img(self.driver, self.nowtime, self.CaseName)
        logger("INFO", "destroy action is finished")

    # 删除浮动IP
    def floatIP_destroy(self):
        self.driver.get(url)
        time.sleep(2)
        self.login_again()
        # self.driver.find_element_by_xpath('//*[@id="navbar-collapse"]/ul[1]/li').click()
        # self.driver.find_element_by_link_text('admin').click()
        """
        menus = "项目->访问 & 安全"
        for item in menus.split('->'):
            self.click_button(item)
        """
        self.click_button("项目")
        try:
            self.click_button("访问 & 安全")
        except:
            self.click_button("项目")
            self.click_button("访问 & 安全")
        time.sleep(2)
        self.driver.find_element_by_link_text('浮动IP').click()
        xpath_tfoot = '//*[@id="floating_ips"]/tfoot/tr/td/span'
        number = self.driver.find_element_by_xpath(xpath_tfoot).text
        match_re = re.match(r".*?(\d+).*", number)
        number = match_re.group(1)
        logger("INFO", "There is %s float IP here !" % number)
        if number == '1':
            checkbox_xpath = '//*[@id="floating_ips"]/thead/tr[2]/th[1]/input'
        else:
            checkbox_xpath = '//*[@id="floating_ips"]/thead/tr[2]/th[1]/div/input'
        try:
            self.driver.find_element_by_xpath(checkbox_xpath).click()
            self.driver.find_element_by_id('floating_ips__action_release').click()
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="modal_wrapper"]/div/div/div/div[3]/a[2]').click()
            logger("INFO", "Delete them all successfully !")
        except:
            logger("INFO", "There is no float IP here !")

    # 获取对应id的表中的数据总数
    def get_table_number(self, id):
        logger("INFO", "start find table %s" % id)
        time.sleep(2)
        xpath_foot = "//*[@id='" + id + "']/tfoot/tr/td/span"
        try:
            foot_text = self.driver.find_element_by_xpath(xpath_foot).text
            match_re = re.match(r".*?(\d+).*", foot_text)
            logger("INFO", "successful get number of %s table" % id)
            return match_re.group(1)
        except:
            logger("WARN", "%s table is not exist!" % id)

    # 选中对象
    def click_checkbox(self, name):
        logger("INFO", "start click %s" % name)
        time.sleep(2)
        if '全部' in name:
            self.driver.find_element_by_css_selector("input.table-row-multi-select").click()
        else:
            for i in name.split(','):
                xpathstr = "//*[@data-display='" + i + "']/td[1]/input"
                try:
                    result = self.driver.find_element_by_xpath(xpathstr)
                except:
                    self.driver.find_element_by_link_text(i).click()
                    xpath = '//*[@id="subnet_details__overview"]/div/dl/dd[2]'
                    id = self.driver.find_element_by_xpath(xpath).text
                    self.driver.back()
                    xpathstr = "//*[@data-display='" + id + "']/td[1]/input"
                try:
                    self.driver.find_element_by_xpath(xpathstr).click()
                    logger("INFO", "click %s successfully" % i)
                except:
                    logger("WARN", "%s is not exist!" % i)

    # 如果页面过期跳转至登录界面，则再次登录
    def login_again(self):
        try:
            self.driver.find_element_by_id("loginBtn")
            logger("INFO", "This is login page!")
            webuitest.login(self.driver, self.username, self.password)
            logger("INFO", "%s,%s login again successfully!" % (self.username, self.password))
        except:
            logger("INFO", "This is not login page, keep going!")

    """
    # 模拟鼠标点击动作
    def mouse_click(self):
        m = PyMouse()
        place = m.position()
        m.click(83, 421)
        logger("INFO", "mouse click finished")
    """
##
# @}
# @}
##
