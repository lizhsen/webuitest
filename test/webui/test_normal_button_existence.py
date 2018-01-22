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
# Author: zhangjk@rc.dddd.com
# Date:   Aug 2017

import sys
sys.path.append("../../lib/")
from webuitest import webdriver, WebUITest, url, login
from ddt import ddt, data, file_data, unpack
from get_element import GetElement


@ddt
class UIButtonExistence(WebUITest):

    def setUp(self):
        try:
            self.driver.get(url)
            self.driver.find_element_by_link_text("webuitest")
            self.driver.find_element_by_link_text("项目").click()
        except:
            login(self.driver, "webuitest", "dddd2014")

    @file_data('normal_button_existence.json')
    def test_webui_normal(self, data):
        driver = GetElement(self.driver)
        driver.ui_engine(data)
