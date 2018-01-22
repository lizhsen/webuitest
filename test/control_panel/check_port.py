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
@file check_port.py
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


def get_ip_by_hostname(name):
    '''get remote device IP address, by part of its hostname
        @fn get_ip_by_hostname
        @param name, part of hostname such as control01, ha01...
        @return, ip address found in /etc/hosts of the controller node.
    '''
    cmd = "cat /etc/hosts | grep %s | awk '{print $1}'" % name
    (ret, output) = shell_cmd_timeout(cmd)
    if ret == 0:
        return output.strip()
    else:
        assert False, "Not found hostname %s" % name


def telnet_ip_port(ip, port, local_ip="remote"):
    '''check IP and port working status, by telnet
        @fn telnet_ip_port
        @param ip, the remote ip address
        @param port, the port number of the device
        @return, 'open' means ip:port is enabled.
                 'close' is ip:port disabled
        '''
    if local_ip is "remote":
        cmd = "expect ../../tools/check_ip_port.exp %s %s" % (ip, port)
    else:
        cmd = "expect ../../tools/local_check_ip_port.exp %s %s \
%s" % (ip, local_ip, port)
    (ret, output) = shell_cmd_timeout(cmd)
    if ret == 0:
        pass
    else:
        assert False, "The ret is not expected. Output is: %s" % output


@ddt
class IPPortStatus(unittest.TestCase):
    """
    @class IPPortStatus
    """

    @file_data('ip_port.json')
    def test_ip_port_status(self, data):
        name = data[0]
        port = data[1]
        ip = get_ip_by_hostname(name)

        if len(data) == 3:
            local_ip = data[2]
            return telnet_ip_port(ip, port, local_ip)
        else:
            return telnet_ip_port(ip, port)

    def tearDown(self):
        cmd = 'killall telnet > /dev/null 2>&1'
        (ret, output) = shell_cmd_timeout(cmd)

##
# @}
# @}
##
