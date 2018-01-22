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

from webuitest import WebUITest
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait


class BasicAcceptance(WebUITest):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_user_log_in_1(self):
        username = "Feile0"
        password = "30649ef2a2a442b48ccbc419c3f7dd68"
        step1 = "正确用户和用户名"
        step2 = "预期结果：可以成功登录"
        self.admin_login(username, password, step1, step2)

    def test_user_log_in_wrong_username(self):
        username = "Feile2222"
        password = "30649ef2a2a442b48ccbc419c3f7dd68"
        step1 = "使用错误用户名登录"
        step2 = "预期结果：页面左上角有错误提示"
        self.admin_login(username, password, step1, step2)

    def test_user_log_in_wrong_password(self):
        username = "Feile0"
        password = "123456"
        step1 = "使用错误密码登录"
        step2 = "预期结果：页面左上角有错误提示"
        self.admin_login(username, password, step1, step2)
