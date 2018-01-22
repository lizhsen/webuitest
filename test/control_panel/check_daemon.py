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

"""
@file check_daemon.py
"""

##
# @addtogroup control_panel
# @brief This is control_panel test for daemon status
# @{
##

import os
import re
import sys
import json
import unittest
sys.path.append("../../lib/")
from ddt import ddt, data, file_data, unpack
from helper import shell_cmd_timeout


def check_daemon_status(output, host, daemon):
    '''check check_daemon_status
        @fn check_daemon_status
        @param dictionary, the json file for data driven
        @param host, the pythical node such as ha01, compute01
        @param daemon, the systemctl daemon name
        @return
        '''
    cmd = "ssh %s systemctl status %s" % (host, daemon)
    (ret, output) = shell_cmd_timeout(cmd)
    if re.findall(r'Active: %s' % "active", output):
        pass
    else:
        assert False, "Daemon %s status is not %s, please check %s \
! " % (daemon, "active", host)


@ddt
class DaemonStatus(unittest.TestCase):
    """
    @class DaemonStatus
    """

    output = ''

    @file_data('daemon.json')
    def test__daemon_status(self, data):
        print(data)
        host = data[0]
        daemon = data[1]
        check_daemon_status(self.output, host, daemon)

##
# @}
# @}
##
