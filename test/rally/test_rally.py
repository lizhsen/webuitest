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
# Author: sunrx@rc.dddd.com
# Date:   Sep 2017

"""
@file test_rally.py
"""

import os
import time
import unittest
import sys
sys.path.append("../../lib/")
from helper import shell_cmd_timeout
import re
from ddt import ddt, data, file_data, unpack


@ddt
class RallyTest(unittest.TestCase):
    """
    @class test_rally
    """

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/test_rally_" + Time + "_result.log")

    @file_data('rally.json')
    def test_rally(self, params):
        test = params[0] + '.yaml'
        resultString = ''
        cmd = "rally task start " + test
        (ret, output) = shell_cmd_timeout(cmd)
        reg1 = re.compile(r".*?(?=% )")
        reg2 = re.compile(r"\d+\.?\d+(?=% )")
        match = reg1.findall(output)
        rate = reg2.findall(output)
        self.assertTrue(rate, "test failed:\n" + output)
        for v in match:
            if v != '':
                line = v.split('|')
                resultString = resultString + line[1] + "      \
success rate: " + line[8] + "%\n"

        result = open("./result/test_rally_" + self.Time + "\
_result.log", 'a')
        result.write(resultString)
        result.close()
        for r in rate:
            self.assertEqual(r, '100.0', "test failed:\n" + output)
