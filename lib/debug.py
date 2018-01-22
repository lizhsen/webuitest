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
# Date:   Nov 2017

"""
@file debug.py
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
import sys
from logger import logger
import datetime
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf-8')

# get screenshot
def get_img(driver, nowtime, filename):
    logger("INFO", "screenshot start")
    base_dir = os.path.dirname(os.path.realpath(__file__))
    ntime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filedir = base_dir.replace('lib', '') + 'test/webui/result/' + nowtime
    if os.path.isdir(filedir):
        pass
    else:
        os.makedirs(filedir)
    file_path = filedir + "/" + filename + "-" + ntime + '.png'
    logger("INFO", file_path)
    driver.get_screenshot_as_file(file_path)
    logger("INFO", "screenshot end")

##
# @}
# @}
#
