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
@file test_vm_fio.py
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
from ddt import ddt, data, file_data, unpack
import sys
sys.path.append("../../lib/")
from controller_test import ControllerTest
from helper import shell_cmd_timeout
import re


@ddt
class VMFioTest(ControllerTest):
    """
    @class VMFioTest
    """

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/VMFioTest_" + Time + "_result.log")

    @classmethod
    def setUpClass(cls):
        '''Init a VM instance and do performance test
        @fn setUpClass
        @param cls
        @return
        '''
        # create an instance firstly
        ControllerTest.init(cls)
        cls.vm = ControllerTest.create_instance(cls, "test_vm_fio")

        time.sleep(10)
        # get into target via SSH without password
        exp = os.path.join(os.path.dirname(__file__),
                           "../../tools/pass_to_vm.exp")
        # ensure ssh without passwd
        cmd = 'expect %s %s %s dddd2014' % (exp, cls.router, cls.vm.target_ip)
        (ret, output) = shell_cmd_timeout(cmd)
        time.sleep(30)

        # create a virtual disk
        cls.volume_id = ControllerTest.create_volume("test_volume_fio",20)
        # attach disk to the vm
        cls.instance_id = cls.vm.target_id
        ControllerTest.attach_disk_to_vm(cls.instance_id, cls.volume_id)
        ControllerTest.determine_status(cls,
                                        "volume",
                                        cls.volume_id,
                                        "in-use")

    @file_data('fio_test.json')
    def test_vm_fio(self, params):
        '''do fio test in VM
        @fn test_vm_fio
        @param self
        @return
        '''
        # Go into target to run performance test
        temp = []
        resultString = ''
        bs_size = params[0]
        mode = params[1]

        for i in range(0, 7):
            cmd = '/usr/bin/fio -name=test -filename=/dev/vdb -ioengine=posixaio \
-direct=1 -size=5G -thread -bs=%s -iodepth=32 -numjobs=1 -rw=%s \
-group_reporting -runtime=30' % (bs_size, mode)
            (ret, output) = self.vm.execute(self.router, cmd)
            # assert False, output
            time.sleep(10)

            # record output string into a result file
            reg = re.compile(r"(?<=iops=)\d+")
            match = reg.search(output)
            resultString = resultString + "\non vm-ceph size:\
" + bs_size + "    " + mode + " IOPS:" + match.group(0)
            temp.append(match.group(0))

        temp.sort()
        result = open("./result/VMFioTest_" + self.Time + "_result.log", 'a')
        result.write(resultString + "\n------------on vm-ceph do \
"+ bs_size + mode + " iodepth Median iops = " + temp[3] + "--------------")
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
