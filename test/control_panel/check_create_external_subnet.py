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
@file check_create_external_subnet.py
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
class CreateNetWork(unittest.TestCase):
    '''
    @class CreateNetWork
    '''
    @ddt.data(["autotest-external", "True", "395"]
              )
    @ddt.unpack
    def test_create_external_network(self, net_name, external_router, id):
        net_ret = ControllerTest.create_network(net_name, external_router, id)
        sub_net_name = "sub-" + net_name
        if re.findall('ACTIVE', net_ret):
            sub_net_ret = ControllerTest.create_external_subnet(sub_net_name,
                                                                net_name)
            if re.findall(r"%s" % sub_net_name, sub_net_ret):
                pass
            else:
                assert False, "create subnet %s fail, \
please check" % sub_net_name
            ControllerTest.delete_network(net_name)
        else:
            assert False, "create %s fail, please check if there is \
too much networks" % net_name

##
# @}
# @}
##
