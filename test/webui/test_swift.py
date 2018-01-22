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
# Date:   sep 2017

import sys
sys.path.append("../../lib/")
from webuitest import webdriver, WebUITest
from ddt import ddt, data, file_data, unpack
from get_element import GetElement
from logger import logger


@ddt
class BasicSwift(WebUITest):

    @file_data('swift.json')
    def test_swift(self, data):
        logger("INFO", "CaseName is %s" % self._testMethodName)
        driver = GetElement(self.driver)
        GetElement.CaseName = self._testMethodName
        data = driver.perconditon(self.get_json_file(), data)
        driver.ui_engine(data)
