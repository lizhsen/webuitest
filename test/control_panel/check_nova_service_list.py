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
@file check_nova_service_list.py
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


def check_list(cmd, output, name, status, state):
    '''ensure the string is in command output
    @fn check_list
    @param name, the service name
    @param status, the service status
    @param state, the service state
    @return
    '''
    (ret, output) = shell_cmd_timeout(cmd)
    if re.findall(r'%s.*%s.*%s' % (name, status, state), output):
        cmd1 = "nova service-list | grep %s" % name
        (ret, output1) = shell_cmd_timeout(cmd1)
        assert False, "\n %s please restart %s on the expected \
node" % (output1, name)

    else:
        pass


@ddt.ddt
class NovaServiceList(unittest.TestCase):
    '''
    @class NovaServiceList
    '''
    output = ""
    cmd = "nova service-list"

    @ddt.data(["nova-consoleauth", "enabled", "down"],
              ["nova-scheduler", "enabled", "down"],
              ["nova-conductor ", "enabled", "down"],
              ["nova-cert", "enabled", "down"],
              ["nova-compute", "enabled", "down"],
              )
    @ddt.unpack
    def test_nova_service_list(self, name, status, type):
        check_list(self.cmd, self.output, name, status, type)


##
# @}
# @}
##
