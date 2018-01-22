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
@file check_command.py
"""

##
# @addtogroup control_panel
# @brief This is control_panel test for command check
# @{
##

import os
import re
import sys
import unittest
import ddt
sys.path.append("../../lib/")
from helper import shell_cmd_timeout
# from ddt import ddt, data, unpack


def in_wsrep_output(key, value):
            cmd = "mysql -e \"show status\""
            (ret, output) = shell_cmd_timeout(cmd)
            detail_message = re.findall(("%s\t%s") % (key, value), output)
            print(detail_message)
            if detail_message:
                pass
            else:
                assert False, "Command %s check fail,status is not : %s \
    " % (key, value)


def in_command_output(cmd, string):
            '''ensure the string is in command output
            @fn in_command_output
            @param cmd, the runninf command
            @param string, the string for command result check
            @return
            '''
            (ret, output) = shell_cmd_timeout(cmd)
            if string in output:
                pass
            else:
                assert False, "Command %s check fail, output is : %s \
        " % (cmd, output)


def in_wsrep_incoming_addresses_output(cmd, string):
            '''ensure the string is in command output
            @fn in_command_output
            @param cmd, the runninf command
            @param string, the string for command result check
            @return
            '''
            (ret, output) = shell_cmd_timeout(cmd)
            b = output.count(":3306")

            if string == str(b):
                pass
            else:
                assert False, "Command %s check fail, output is : %s \
                " % (cmd, output)


@ddt.ddt
class DaemonStatus(unittest.TestCase):
    """
    @class DaemonStatus
    """
    output = ''

    @ddt.data(["wsrep_cluster_size", "4"],
              ["wsrep_connected", "ON"],
              ["wsrep_provider_name", "Galera"])
    @ddt.unpack
    def test_wsrep_status(self, key, value):
        '''check some wsrep points, make sure they are running well '''
        in_wsrep_output(key, value)

    def test_ceph_osd_stat(self):
        '''check command ceph osd stat output
        @fn test_ceph_osd_stat
        @param self
        @return
        '''

        cmd = 'ceph osd stat'
        exp_out = '8 osds: 8 up, 8 in'
        in_command_output(cmd, exp_out)

    def test_wsrep_incoming_addresses(self):
        '''check the wsrep_incoming_addresses, openstack needs at least 2
 addresses, which means there needs 2 ports ":3306"'''

        cmd = "mysql -e \"show status like '%wsrep%'\"| grep \
wsrep_incoming_addresses"
        exp_out = '2'
        in_wsrep_incoming_addresses_output(cmd, exp_out)

##
# @}
# @}
##
