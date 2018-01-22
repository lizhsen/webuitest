# coding:utf-8

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
# Date:   Aug 2017
"""
@file test_stream.py
"""

##
# @addtogroup memory stream
# @brief This is memory component
# @{
# @addtogroup test_stream test_stream
# @brief This is memory module
# @{
##

import os
import time
import sys
sys.path.append("../../lib/")
from controller_test import ControllerTest
from helper import shell_cmd_timeout
from ddt import ddt, data, file_data, unpack


repeat_time = 10

@ddt
class StreamTest(ControllerTest):
    """
    @class StreamTest
    """
    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/test_vm_stream_" + Time + "_result.log")

    @file_data("stream.json")
    def test_stream_thread_4(self, params):
        '''use 4 threads to do stream test
        @fn test_stream_thread_4
        @param self
        @return
        '''
        flavor = params[0]
        mode = params[1]
        temp = []
        score = []
        resultString = mode + " result\n"

        # create an instance firstly
        ControllerTest.init(self)
        vm = ControllerTest.create_instance(
            self,
            "test_vm_" + flavor + "_stream",
            vm_flavor = "m1." + flavor)
        # get into target via SSH without password
        exp = os.path.join(os.path.dirname(__file__), 
                           "../../tools/pass_to_vm.exp")
        # ensure ssh without passwd 
        cmd = 'expect %s %s %s dddd2014' % (exp, self.router, vm.target_ip)
        (ret, output) = shell_cmd_timeout(cmd)
        print('insert sshkey')
        time.sleep(5)

        # Go into target to run performance test
        for i in range(0, repeat_time):
            cmd = 'export OMP_NUM_THREADS=4; /root/stream.out'
            print('begin to do ' + mode + ' test in ' + flavor + ' instance')
            (ret, output) = vm.execute(self.router, cmd)
            time.sleep(10)
            for line in output.split('\n'):
                if mode in line:
                    for n in range(0, len(line.split(' '))):
                        if line.split(' ')[n] != '':
                            score.append(line.split(' ')[n])
            temp.append(score[1])
            resultString = resultString + score[1] + '  '

        temp.sort()
        vm.delete_instance()
        result = open("./result/test_vm_stream_" + self.Time + "_result.log",
                      'a')
        result.write(resultString + "\n--------------Median score:" +
                     str(temp[5]) + "MB/s------------------\n")
        result.close()

##
# @}
# @}
##

