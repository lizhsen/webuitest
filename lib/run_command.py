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
# Author: duanhc@rc.dddd.com
# Date:   Dec 2017

"""
@file run_command.py
"""

import time
import sys
import subprocess
import os
import platform
from helper import shell_cmd_timeout
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from get_config import getconfig
from logger import logger

reload(sys)
sys.setdefaultencoding('utf-8')
url = getconfig("webui", "url")
win_user = getconfig("webui", "win_user")
win_passwd = getconfig("webui", "win_pwd")


class Command(object):
    def __init__(self, selenium_driver):
        self.driver = selenium_driver

    # 通过ssh连接到虚拟机执行命令并拿到返回值
    def run_cmd(self, host, cmd):
        ip = host[0]
        port = host[1]
        user = host[2]
        passwd = host[3]
        # 生成ssh客户端实例
        s = SSHClient()
        s.set_missing_host_key_policy(AutoAddPolicy())
        logger("INFO", "Start SSH into %s" % ip)
        for i in range(60):
            try:
                s.connect(ip, port, user, passwd)
                logger("INFO", "ssh connect successfully")
                break
            except Exception as msg:
                logger("INFO", "ssh connect failed, try again")
                time.sleep(5)
                logger("DEBUG", "consume %d seconds already" % ((i+1)*5))
                if i == 59:
                    logger("ERROR", msg)
                    assert False, "ssh connect failed, %s" %msg
        stdin, stdout, stderr = s.exec_command(cmd)
        logger("INFO", "Command is %s" % cmd)
        std = stdout.read()
        logger("INFO", "Result is %s" % std)
        stder = stderr.read()
        logger("INFO", "System info is %s" % stder)
        s.close()
        return std

    # 通过实例的名称拿到浮动IP
    def get_floatIP(self, instance):
        self.driver.get(url)
        time.sleep(2)
        self.driver.find_element_by_link_text('项目').click()
        time.sleep(2)
        try:
            self.driver.find_element_by_link_text('实例').click()
        except:
            self.driver.find_element_by_link_text('项目').click()
            time.sleep(1)
            self.driver.find_element_by_link_text('实例').click()
        time.sleep(3)
        xpath_floatIP = "//*[@data-display='" + instance + "']/td[4]/ul[2]/li"
        try:
            floatIP = self.driver.find_element_by_xpath(xpath_floatIP).text
            return floatIP
        except:
            logger("ERROR", "floatIP doesn't exist !")

    # 通过实例的名称拿到内网IP
    def get_internalIP(self, instance):
        self.driver.get(url)
        time.sleep(2)
        self.driver.find_element_by_link_text('项目').click()
        time.sleep(2)
        try:
            self.driver.find_element_by_link_text('实例').click()
        except:
            self.driver.find_element_by_link_text('项目').click()
            time.sleep(2)
            self.driver.find_element_by_link_text('实例').click()
        time.sleep(3)
        try:
            xpath_internalIP = "//*[@data-display='" + instance + "']/td[4]/ul/li"
            internalIP = self.driver.find_element_by_xpath(xpath_internalIP).text
            return internalIP
        except:
            logger("ERROR", "get internalIP failed")

    # 通过分析自然语言得到虚拟机控制台输出
    def get_cmd(self, element):
        val = element.split(u"执行")
        instance = val[0].split(u"虚拟机")[1]
        floatIP = self.get_floatIP(instance)
        cmd = val[1].split(u"的值")[0]
        if "ping -c 1 虚拟机" in cmd:
            instance1 = cmd.split(u"虚拟机")[1]
            cmd = cmd.replace(u"虚拟机" + instance1, self.get_internalIP(instance1))
        host = [floatIP, '22', 'dddd', 'Inesa2016!!']
        std = self.run_cmd(host, cmd)
        return std

    # 通过分析自然语言得到本地控制台的返回值(0或1)
    def get_local_cmd(self, element):
        cmd = element.split(u"执行")[1].split(u"的值")[0]
        if "ping 虚拟机" in cmd:
            instance = cmd.split(u"虚拟机")[1]
            os = platform.system()
            if os == 'Windows':
                cmd = cmd.replace(u"虚拟机" + instance, '-n 1 ' + self.get_floatIP(instance))
            elif os == 'Linux':
                cmd = cmd.replace(u"虚拟机" + instance, '-c 1 ' + self.get_floatIP(instance))
        for i in range(60):
            time.sleep(5)
            logger("DEBUG", "consume %d seconds already" % i)
            r = subprocess.call(cmd, shell=True)
            if r == 0:
                return r
        return 1
    
    # 通过分析自然语言得到windows虚拟机控制台输出
    def handle_winnlp(self, element):
        val = element.split(u"执行")
        instance = val[0].split(u"虚拟机")[1]
        floatIP = self.get_floatIP(instance)
        if val[1].find(u"登录") != -1:
            win_pwds = val[1].split(u"登录")[0].split(u"密码")[1]
            win_cmd = "dir"
            result = self.win_execute_cmd(floatIP, win_user, win_pwds, win_cmd)
            logger("INFO", result)
            if result.find("DIR") != -1:
                return u"成功"
            else:
                return u"失败"
        else:
            win_cmd = val[1].split(u"的值")[0]
            result = self.win_execute_cmd(floatIP, win_user, win_passwd, win_cmd)
            return result

    # 获取windows虚机命令执行结果
    def win_execute_cmd(self, ip, user, pwd, cmd):
        path = os.path.split(os.path.realpath(__file__))[0]
        exp = "expect " + path + "/../tools/windows-execute.exp "
        args = ip + " " + user + " " + pwd + " " + cmd
        expcmd = exp + args
        logger("INFO", "windows cmd is %s" % expcmd)
        (ret, output) = shell_cmd_timeout(expcmd)
        return output
