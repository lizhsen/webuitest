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
@file test_vm_iozone.py
"""

##
# @addtogroup disk fio
# @brief This is disk fio
# @{
# @addtogroup disk fio
# @brief This is disk fio
# @{
##

import os
import time
import sys
from ddt import ddt, data, file_data, unpack
sys.path.append("../../lib/")
from controller_test import ControllerTest
from helper import shell_cmd_timeout
import re


@ddt
class VMIozoneTest(ControllerTest):
    """
    @class VMIozoneTest
    """

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/VMIozoneTest_" + Time + "_result.log")

    @classmethod
    def setUpClass(cls):
        '''Init a VM instance and do performance test
        @fn setUpClass
        @param cls
        @return
        '''
        # create an instance firstly
        ControllerTest.init(cls)
        cls.vm = ControllerTest.create_instance(cls, "test_vm_perf")
        time.sleep(10)
        # get into target via SSH without password
        exp = os.path.join(os.path.dirname(__file__),
                           "../../tools/pass_to_vm.exp")
        # ensure ssh without passwd
        cmd = 'expect %s %s %s dddd2014' % (exp, cls.router, cls.vm.target_ip)
        (ret, output) = shell_cmd_timeout(cmd)
        time.sleep(30)

        # create a virtual disk
        cls.volume_id = ControllerTest.create_volume("test_volume_perf",20)
        # attach disk to the vm
        cls.instance_id = cls.vm.target_id
        ControllerTest.attach_disk_to_vm(cls.instance_id, cls.volume_id)
        ControllerTest.determine_status(cls,
                                        "volume",
                                        cls.volume_id,
                                        "in-use")
        # in vm, format /dev/sdb and mount /dev/sdb to a folder

    @file_data('iozone_test.json')
    def test_vm_iozone(self, params):
        '''do iozone test in VM
        @fn test_vm_iozone
        @param self
        @return
        '''
        # Go into target to run performance test
        temp_write = []
        temp_read = []
        resultString = ''
        bs_size = params[0]
        for i in range(0, 7):
            cmd = 'cd /root/iozone3_465/src/current;./iozone -Rab ../../\
results/16results.xls -i 0 -i 1 -s 5g -r %s -f /dev/vdb' % bs_size
            (ret, output) = self.vm.execute(self.router, cmd)
            time.sleep(1)

            # record output string into a result file
            ldddd = output.split('\n')
            value = ldddd[29].split(' ')
            data = []
            for v in value:
                if v.isdigit():
                    data.append(v)

            resultString = resultString + "\non-VM IO block size:\
"+ bs_size + "   Sequentially read & write write: " + data[2] + " / " + data[4]

            temp_write.append(data[2])
            temp_read.append(data[4])

        temp_write.sort()
        temp_read.sort()
        result = open("./result/VMIozoneTest_" + self.Time +
"_result.log", 'a')
        result.write(resultString + "\n----------on-VM ceph block size:" +
bs_size + "1M Sequentially read & write Median write: " +
temp_write[3] + " / " + temp_read[3] + "---------")
        result.close()

    @classmethod
    def tearDownClass(cls):
        cls.vm.delete_instance()
        status_yes = ""
        ControllerTest.determine_status(cls,
                                        "instance",
                                        cls.instance_id,
                                        status_yes)
        ControllerTest.delete_volume(cls.volume_id)
##
# @}
# @}
##
