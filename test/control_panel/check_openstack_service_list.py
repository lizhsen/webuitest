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
#:
# Author: lizs@rc.dddd.com
# Date:   Aug 2017

"""
@file check_openstack_service_list.py
"""

##
# @addtogroup control_panel
# @brief This is control_panel test for command check
# @{
##

import os
import re
import sys
import json
import unittest
import ddt
sys.path.append("../../lib/")
from helper import shell_cmd_timeout
from ddt import ddt, data, unpack, file_data


def check_list(cmd, output, name, type):
    '''ensure the string is in command output
    @fn check_list
    @param name, the service name
    @param type, the service type
    @return
    '''
    (ret, output) = shell_cmd_timeout(cmd)
    if re.findall(r'%s' % name, output):
        pass
    else:
        assert False, "service %s check fail, type is : %s do not exit,\
please check" % (name, type)


@ddt
class OpenstackServiceList(unittest.TestCase):
    '''
    @class OpenStackServiceList
    '''
    output = ""
    cmd = "openstack service list"

    @file_data("openstackservice.json")
    def test_service_list(self, data):
        print(data)
        name = data[0]
        type = data[1]
        check_list(self.cmd, self.output, name, type)


##
# @}
# @}
##
