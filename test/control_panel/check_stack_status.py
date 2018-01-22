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
@file check_stack_status.py
"""

##
# @addtogroup control_panel
# @brief This is control_panel test for stack status
# @{
##

import os
import re
import json
import sys
import unittest
sys.path.append("../../lib/")
from helper import shell_cmd_timeout
from ddt import ddt, data, file_data, unpack


# def check_service_status(status, dictionary, check_point):
def check_service_status(output, service, status):
    '''check service status by running openstack-status
        @fn check_service_status
        @param status, the output info of openstack-status
        @param dictionary, the json file of data driven cases
        @param check_point, the service name
        @return
        '''
    # value = dictionary[check_point]
    if re.findall(r'%s: +%s' % (service, status), output):
        pass
    else:
        assert False, "Service %s status is not %s" % (service, status)


@ddt
class StackStatus(unittest.TestCase):
    """
    @class StackStatus
    """
    output = ''

    @classmethod
    def setUpClass(cls):
        '''on controller node, run command to get stack status
        @fn setUpClass
        @param cls
        @return
        '''
        # Perform openstack-status on controller node
        cmd = 'openstack-status 2> /dev/null'
        (ret, cls.output) = shell_cmd_timeout(cmd)

    @file_data('method.json')
    def test_openstack_status(self, data):
        print(data)
        service = data[0]
        status = data[1]
        check_service_status(self.output, service, status)
##
# @}
# @}
##
