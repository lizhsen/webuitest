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
# Author: yuy@rc.dddd.com
# Date:   July 2017

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
import re


class CephThroughputTest(ControllerTest):
    """
    @class StreamTest
    """
    cmd_prefix = 'ssh ha01-mon02-osd01'

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/CephThroughputTest_" + Time + "_result.log")

    def test_IO_1M(self):
        '''ceph block size:1M
           Sequentially read & write
        '''
        # Go into target to run performance test
        temp_write = []
        temp_read = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'cd /root/iozone3_465/src/current;./iozone \
-Rab ../../results/16results.xls -i 0 -i 1 -s 5g -r 1m -f /dev/sdc1'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            ldddd = output.split('\n')
            value = ldddd[29].split(' ')

            resultString = resultString + "\nIO block size:1M   \
Sequentially read & write write: " + value[15] + " / " + value[19]
            temp_write.append(value[15])
            temp_read.append(value[19])

        temp_write.sort()
        temp_read.sort()
        result = open("./result/CephThroughputTest_" + self.Time + "\
_result.log", 'a')
        result.write(resultString + "\n----------ceph block size:1M \
Sequentially read & write Median write: \
" + temp_write[3] + " / " + temp_read[3] + "---------")
        result.close()

    def test_IO_4M(self):
        '''ceph block size:4M
           Sequentially read & write
        '''
        # Go into target to run performance test
        temp_write = []
        temp_read = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'cd /root/iozone3_465/src/current;./iozone \
-Rab ../../results/16results.xls -i 0 -i 1 -s 5g -r 4m -f /dev/sdc1'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            ldddd = output.split('\n')
            value = ldddd[29].split(' ')

            resultString = resultString + "\nIO block size:4M   \
Sequentially read & write write: " + value[15] + " / " + value[19]
            temp_write.append(value[15])
            temp_read.append(value[19])

        temp_write.sort()
        temp_read.sort()
        result = open("./result/CephThroughputTest_" + self.Time + "\
_result.log", 'a')
        result.write(resultString + "\n----------ceph block size:\
4M Sequentially read & write Median write: \
" + temp_write[3] + " / " + temp_read[3] + "---------")
        result.close()

    def test_IO_8M(self):
        '''ceph block size:8M
           Sequentially read & write
        '''
        # Go into target to run performance test
        temp_write = []
        temp_read = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'cd /root/iozone3_465/src/current;./iozone \
-Rab ../../results/16results.xls -i 0 -i 1 -s 5g -r 8m -f /dev/sdc1'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            ldddd = output.split('\n')
            value = ldddd[29].split(' ')

            resultString = resultString + "\nIO block size:8M   \
Sequentially read & write write: " + value[15] + " / " + value[19]
            temp_write.append(value[15])
            temp_read.append(value[19])

        temp_write.sort()
        temp_read.sort()
        result = open("./result/CephThroughputTest_" + self.Time + "\
_result.log", 'a')
        result.write(resultString + "\n----------ceph block size:\
8M Sequentially read & write Median write: \
" + temp_write[3] + " / " + temp_read[3] + "---------")
        result.close()

    def test_IO_16M(self):
        '''ceph block size:16M
           Sequentially read & write
        '''
        # Go into target to run performance test
        temp_write = []
        temp_read = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'cd /root/iozone3_465/src/current;./iozone \
-Rab ../../results/16results.xls -i 0 -i 1 -s 5g -r 16m -f /dev/sdc1'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            ldddd = output.split('\n')
            value = ldddd[29].split(' ')

            resultString = resultString + "\nIO block size:16M   \
Sequentially read & write write: " + value[14] + " / " + value[18]
            temp_write.append(value[14])
            temp_read.append(value[18])

        temp_write.sort()
        temp_read.sort()
        result = open("./result/CephThroughputTest_" + self.Time + "\
_result.log", 'a')
        result.write(resultString + "\n----------ceph block size:\
16M Sequentially read & write Median write\
: " + temp_write[3] + " / " + temp_read[3] + "---------")
        result.close()
##
# @}
# @}
##
