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
# Author: lizs@rc.dddd.com
# Date:   Sep 2017

"""
@file check_create_user.py
"""

##
# @addtogroup control_panel
# @brief This is control_panel test for daemon status
# @{
##


import os
import re
import json
import unittest
import sys
sys.path.append("../../lib/")
import ddt
from helper import shell_cmd_timeout
from controller_test import ControllerTest


@ddt.ddt
class CreateUser(unittest.TestCase):
    '''
    @class CreateUser
    '''

    @ddt.data(["autotestuser1", "123456", "admin"],
              ["autotestuser2", "654321", "admin"],
              ["autotestuser3", "123456", "admin"],
              ["autotestuser4", "654321", "admin"]
              )
    @ddt.unpack
    def test_create_user(self, user_name, password, project_name):
        ret = ControllerTest.create_user(user_name, password, project_name)
        if re.findall(r"%s" % user_name, ret):
            pass
            ControllerTest.delete_user(user_name)
        else:
            assert False, "create user %s fail, please check " % user_name

##
# @}
# @}
##
