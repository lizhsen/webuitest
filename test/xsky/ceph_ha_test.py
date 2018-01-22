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


class CephHATest(ControllerTest):
    """
    @class StreamTest
    """
    cmd_prefix = 'ssh ha01-mon02-osd01'

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/CephHATest_" + Time + "_result.log")

    def test_randomread_4k(self):
        '''ceph size:4k
           random read
        '''
        # Go into target to run performance test
        temp = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'fio -name=test -filename=/dev/sdc1 -ioengine=libaio \
-direct=1 -size=5g -thread -bs=4K -iodepth=128 -numjobs=8 \
-rw=randread -group_reporting -runtime=30'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            reg = re.compile(r"(?<=iops=)\d+")
            match = reg.search(output)
            resultString = resultString + "\nceph size:4k    \
random read IOPS:" + match.group(0)
            temp.append(match.group(0))

        temp.sort()
        result = open("./result/CephHATest_" + self.Time + "_result.log", 'a')
        result.write(resultString + "\n------------ceph 4k random \
read Median iops = " + temp[3] + "--------------")
        result.close()

    def test_randomwrite_4k(self):
        '''ceph size:4k
           random write
        '''
        # Go into target to run performance test
        temp = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'fio -name=test -filename=/dev/sdc1 -ioengine=\
libaio -direct=1 -size=5g -thread -bs=4K -iodepth=128 -numjobs=8 \
-rw=randwrite -group_reporting -runtime=30 --allow_mounted_write=1'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            reg = re.compile(r"(?<=iops=)\d+")
            match = reg.search(output)
            resultString = resultString + "\nceph size:4k    \
random write IOPS:" + match.group(0)
            temp.append(match.group(0))

        temp.sort()
        result = open("./result/CephHATest_" + self.Time + "_result.log", 'a')
        result.write(resultString + "\n------------ceph 4k \
random write Median iops = " + temp[3] + "--------------")
        result.close()

    def test_randomrw_4k(self):
        '''ceph size:4k
           random write and read=7:3
        '''
        # Go into target to run performance test
        temp = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'fio -name=4krw -filename=/dev/sdc1 -ioengine=libaio \
-direct=1 -size=5g -thread -bs=4k -iodepth=128 -numjobs=8 -rw=randrw \
-rwmixread=70 -group_reporting -runtime=30 --allow_mounted_write=1'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            reg = re.compile(r"(?<=iops=)\d+")
            match = reg.search(output)
            resultString = resultString + "\nceph size:4k    \
random write and read IOPS:" + match.group(0)
            temp.append(match.group(0))

        temp.sort()
        result = open("./result/CephHATest_" + self.Time + "_result.log", 'a')
        result.write(resultString + "\n------------ceph 4k \
random write Median iops = " + temp[3] + "--------------")
        result.close()

    def test_randomread_8k(self):
        '''ceph size:8k
           random read
        '''
        # Go into target to run performance test
        temp = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'fio -name=test -filename=/dev/sdc1 \
-ioengine=libaio -direct=1 -size=5g -thread -bs=8K \
-iodepth=128 -numjobs=8 -rw=randread -group_reporting -runtime=30'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            reg = re.compile(r"(?<=iops=)\d+")
            match = reg.search(output)
            resultString = resultString + "\nceph size:8k    \
random read IOPS:" + match.group(0)
            temp.append(match.group(0))

        temp.sort()
        result = open("./result/CephHATest_" + self.Time + "_result.log", 'a')
        result.write(resultString + "\n------------ceph 8k \
random read Median iops = " + temp[3] + "--------------")
        result.close()

    def test_randomwrite_8k(self):
        '''ceph size:8k
           random write
        '''
        # Go into target to run performance test
        temp = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'fio -name=test -filename=/dev/sdc1 \
-ioengine=libaio -direct=1 -size=5g -thread -bs=8K -iodepth=128 -numjobs=8 \
-rw=randwrite -group_reporting -runtime=30 --allow_mounted_write=1'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            reg = re.compile(r"(?<=iops=)\d+")
            match = reg.search(output)
            resultString = resultString + "\nceph size:8k    \
random write IOPS:" + match.group(0)
            temp.append(match.group(0))
        temp.sort()
        result = open("./result/CephHATest_" + self.Time + "_result.log", 'a')
        result.write(resultString + "\n------------ceph 8k random \
write Median iops = " + temp[3] + "--------------")
        result.close()

    def test_randomrw_8k(self):
        '''ceph size:8k
           random write and read=7:3
        '''
        # Go into target to run performance test
        temp = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'fio -name=8krw -filename=/dev/sdc1 -ioengine=libaio \
-direct=1 -size=5g -thread -bs=8k -iodepth=128 -numjobs=8 -rw=randrw \
-rwmixread=70 -group_reporting -runtime=30 --allow_mounted_write=1'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            reg = re.compile(r"(?<=iops=)\d+")
            match = reg.search(output)
            resultString = resultString + "\nceph size:8k    \
random write and read IOPS:" + match.group(0)
            temp.append(match.group(0))
        temp.sort()
        result = open("./result/CephHATest_" + self.Time + "_result.log", 'a')
        result.write(resultString + "\n------------ceph 8k random \
write and read Median iops = " + temp[3] + "--------------")
        result.close()

    def test_randomread_16k(self):
        '''ceph size:16k
           random read
        '''
        # Go into target to run performance test
        temp = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'fio -name=test -filename=/dev/sdk1 -ioengine=libaio \
-direct=1 -size=5g -thread -bs=16K -iodepth=128 -numjobs=8 -rw=randread \
-group_reporting -runtime=30'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            reg = re.compile(r"(?<=iops=)\d+")
            match = reg.search(output)
            resultString = resultString + "\nceph size:16k    \
random read IOPS:" + match.group(0)
            temp.append(match.group(0))
        temp.sort()
        result = open("./result/CephHATest_" + self.Time + "_result.log", 'a')
        result.write(resultString + "\n------------ceph 16k \
random read Median iops = " + temp[3] + "--------------")
        result.close()

    def test_randomwrite_16k(self):
        '''ceph size:16k
           random write
        '''
        # Go into target to run performance test
        temp = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'fio -name=test -filename=/dev/sdc1 -ioengine=libaio \
-direct=1 -size=5g -thread -bs=16K -iodepth=128 -numjobs=8 -rw=randwrite \
-group_reporting -runtime=30 --allow_mounted_write=1'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            reg = re.compile(r"(?<=iops=)\d+")
            match = reg.search(output)
            resultString = resultString + "\nceph size:16k    \
random write IOPS:" + match.group(0)
            temp.append(match.group(0))
        temp.sort()
        result = open("./result/CephHATest_" + self.Time + "_result.log", 'a')
        result.write(resultString + "\n------------ceph 16k random write \
Median iops = " + temp[3] + "--------------")
        result.close()

    def test_randomrw_16k(self):
        '''ceph size:16k
           random write and read=7:3
        '''
        # Go into target to run performance test
        temp = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'fio -name=16krw -filename=/dev/sdc1 -ioengine=libaio \
-direct=1 -size=5g -thread -bs=16k -iodepth=128 -numjobs=8 -rw=randrw \
-rwmixread=70 -group_reporting -runtime=30 --allow_mounted_write=1'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            reg = re.compile(r"(?<=iops=)\d+")
            match = reg.search(output)
            resultString = resultString + "\nceph size:16k    \
random write and read IOPS:" + match.group(0)
            temp.append(match.group(0))
        temp.sort()
        result = open("./result/CephHATest_" + self.Time + "_result.log", 'a')
        result.write(resultString + "\n------------ceph 16k random write \
and read Median iops = " + temp[3] + "--------------")
        result.close()

    def test_randomread_64k(self):
        '''ceph size:64k
           random read
        '''
        # Go into target to run performance test
        temp = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'fio -name=test -filename=/dev/sdc1 -ioengine=libaio \
-direct=1 -size=5g -thread -bs=64K -iodepth=128 -numjobs=8 -rw=randread \
-group_reporting -runtime=30'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            reg = re.compile(r"(?<=iops=)\d+")
            match = reg.search(output)
            resultString = resultString + "\nceph size:64k    \
random read IOPS:" + match.group(0)
            temp.append(match.group(0))

        temp.sort()
        result = open("./result/CephHATest_" + self.Time + "_result.log", 'a')
        result.write(resultString + "\n------------ceph 64k \
random read Median iops = " + temp[3] + "--------------")
        result.close()

    def test_randomwrite_64k(self):
        '''ceph size:64k
           random write
        '''
        # Go into target to run performance test
        temp = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'fio -name=test -filename=/dev/sdc1 -ioengine=libaio \
-direct=1 -size=5g -thread -bs=64K -iodepth=128 -numjobs=8 -rw=randwrite \
-group_reporting -runtime=30 --allow_mounted_write=1'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            reg = re.compile(r"(?<=iops=)\d+")
            match = reg.search(output)
            resultString = resultString + "\nceph size:64k    \
random write IOPS:" + match.group(0)
            temp.append(match.group(0))

        temp.sort()
        result = open("./result/CephHATest_" + self.Time + "_result.log", 'a')
        result.write(resultString + "\n------------ceph 64k \
random write Median iops = " + temp[3] + "--------------")
        result.close()

    def test_randomrw_64k(self):
        '''ceph size:64k
           random write and read=7:3
        '''
        # Go into target to run performance test
        temp = []
        resultString = ''
        for i in range(0, 7):
            cmd = 'fio -name=64krw -filename=/dev/sdc1 -ioengine=libaio \
-direct=1 -size=5g -thread -bs=64k -iodepth=128 -numjobs=8 -rw=randrw \
-rwmixread=70 -group_reporting -runtime=30 --allow_mounted_write=1'
            (ret, output) = shell_cmd_timeout('%s \
"%s"' % (self.cmd_prefix, cmd))
            time.sleep(1)

            # record output string into a result file
            reg = re.compile(r"(?<=iops=)\d+")
            match = reg.search(output)
            resultString = resultString + "\nceph size:64k    \
random write and read IOPS:" + match.group(0)
            temp.append(match.group(0))

        temp.sort()
        result = open("./result/CephHATest_" + self.Time + "_result.log", 'a')
        result.write(resultString + "\n------------ceph 64k \
random read & write Median iops = " + temp[3] + "--------------")
        result.close()
##
# @}
# @}
##
