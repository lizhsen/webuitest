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
# Date:   July 2017

"""
@file test_cli_performance.py
"""

import os
import time
import sys
import string
sys.path.append("../../lib/")
from controller_test import ControllerTest
from helper import shell_cmd_timeout
import re
import ddt


@ddt.ddt
class CliVolume(ControllerTest):

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/CliVolume_" + Time + "_result.log")

    @ddt.data(["200"],
              ["1000"])

    @ddt.unpack
    def test_volume(self, size):

        t1 = []
        t2 = []
        t3 = []
        t4 = []
        create_time = ''
        snapshot_time = ''
        attach_time = ''
        delete_time = ''

        ControllerTest.init(self)
        vm = ControllerTest.create_instance(
            self,
            "test_volume")
        # create, create snapshot, attach, delete a volume
        for i in range(0, 7):
            vd_name = size + "_size_vd_" + str(i)
            # create a volume
            c_start = time.time()
            volume_id = ControllerTest.create_volume(vd_name, size)
            ControllerTest.determine_status(
                self,
                "volume",
                volume_id,
                "available")
            c_end = time.time()
            c_t = c_end - c_start - 10
            create_time = create_time + str(c_t) + '  '
            time.sleep(10)
            # do a snapshot
            s_start = time.time()
            vd_snapshot_id = ControllerTest.create_volume_snapshot(
                self,
                vd_name,
                volume_id)
            ControllerTest.determine_status(
                self,
                "vd_snapshot",
                vd_snapshot_id,
                "available")
            s_end = time.time()
            s_t = s_end - s_start
            snapshot_time = snapshot_time + str(s_t) + '  '
            time.sleep(10)
            ControllerTest.delete_vd_snapshot(vd_snapshot_id)
            # attach the volume to instance
            a_start = time.time()
            ControllerTest.attach_disk_to_vm(vm.target_id, volume_id)
            ControllerTest.determine_status(
                self,
                "volume",
                volume_id,
                "in-use")
            a_end = time.time()
            a_t = a_end - a_start
            attach_time = attach_time + str(a_t) + '  '
            time.sleep(10)
            # detach
            ControllerTest.detach_disk_to_vm(vm.target_id, volume_id)
            time.sleep(10)
            # delete the volume
            d_start = time.time()
            ControllerTest.delete_volume(volume_id)
            ControllerTest.determine_status(
                self,
                "volume",
                volume_id,
                "")
            d_end = time.time()
            d_t = d_end - d_start
            delete_time = delete_time + str(d_t) + '  '

            t1.append(c_t)
            t2.append(s_t)
            t3.append(a_t)
            t4.append(d_t)

        t1.sort()
        t2.sort()
        t3.sort()
        t4.sort()
        vm.delete_instance()
        resultString = "\n====volume size " + size + "====\n"
        result = open("./result/CliVolume_" + self.Time + "_result.log",
                      'a')
        result.write(resultString+ "create time\n" + create_time +
                     "\n-------------Median create time:" + str(t1[3]) +
                     "-------------\ncreate snapshot\n" +
                     snapshot_time + "\n-------------Median snapshot time:" +
                     str(t2[3]) + "--------------\nattach time\n" +
                     attach_time + "\n-------------Median attach time:" +
                     str(t3[3]) + "--------------\ndelete time\n" +
                     delete_time + "\n------------Median delete time:" +
                     str(t4[3]) + "------------\n")
        result.close()
