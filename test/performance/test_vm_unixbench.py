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
@file test_vm_unixbench.py
"""

##
# @addtogroup disk unixbench
# @brief This is disk unixbench
# @{
# @addtogroup disk unixbench
# @brief This is disk unixbench
# @{
##

import os
import time
import sys
sys.path.append("../../lib/")
from controller_test import ControllerTest
from helper import shell_cmd_timeout
import re
from ddt import ddt, data, file_data, unpack


@ddt
class VMUnixbench(ControllerTest):
    """
    @class test_vm_small_unixbench
    """

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/test_vm_unixbench_" + Time + "_result.log")
    repeat_times = 7

    @file_data('unixbench.json')
    def test_vm_unixbench(self, params):
        '''do unixbench test in VM
        @fn test_vm_unixbench_string
        @param self
        @return
        '''
        flavor = params[0]
        mode = params[1]

        # create an instance firstly
        ControllerTest.init(self)
        # create a virtual disk
        vm = ControllerTest.create_instance(self,
                                            "test_vm_perf",
                                            vm_flavor = "m1." + flavor)
        time.sleep(10)
        # get into target via SSH without password
        exp = os.path.join(os.path.dirname(__file__),
                           "../../tools/pass_to_vm.exp")
        # ensure ssh without passwd
        cmd = 'expect %s %s %s dddd2014' % (exp, self.router, vm.target_ip)
        (ret, output) = shell_cmd_timeout(cmd)
        time.sleep(30)

        temp = []
        cmd = 'cd /root/UnixBench;./Run ' + mode
        # Go into target to run performance test
        resultString = "------------------------\
" + flavor + " run " + mode + " test:-----------------------------\n"
        for i in range(0, self.repeat_times):
            (ret, output) = vm.execute(self.router, cmd)
            time.sleep(1)

            # record output string into a result file
            ldddd = output.split('\n')
            for line in ldddd:
                if "System Benchmarks Index Score" in line:
                    reg = re.compile(r"\d+\.?\d*")
                    match = reg.search(line)
                    resultString = resultString + match.group(0) + "\n"
                    temp.append(match.group(0))

        vm.delete_instance()
        temp.sort()
        result = open("./result/test_vm_unixbench_" + self.Time + "\
_result.log", 'a')
        result.write(resultString + "\n----------------Median value: " +
                     temp[3] + "--------------\n")
        result.close()
##
# @}
# @}
##
