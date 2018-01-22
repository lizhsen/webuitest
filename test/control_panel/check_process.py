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
# Date:   Aug 2017

"""
@file check_process.py
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
from ddt import ddt, data, file_data, unpack
from helper import shell_cmd_timeout


def check_process_status(output, host, process):
    '''check check_process_status
        @fn check_process_status
        @param output, the output of the order
        @param host, the pythical node such as ha01, compute01
        @param process, the systemctl daemon name
        @return
        '''
    cmd = "ssh %s ps -ef | grep %s" % (host, process)
    (ret, output) = shell_cmd_timeout(cmd)
    if re.findall(process, output):
        pass
    else:
        assert False, "process %s status is not %s, please check %s \
! " % (process, "running", host)


@ddt
class ProcessStatus(unittest.TestCase):
    """
    @class ProcessStatus
    """

    output = ''

    @file_data('process.json')
    def test_process_status(self, data):
        print(data)
        host = data[0]
        process = data[1]
        check_process_status(self.output, host, process)

##
# @}
# @}
##
