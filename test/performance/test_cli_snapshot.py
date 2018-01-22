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
import ddt
sys.path.append("../../lib/")
from controller_test import ControllerTest
from helper import shell_cmd_timeout
import re


@ddt.ddt
class CreateSnapshot(ControllerTest):

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/CreateSnapshot_" + Time + "_result.log")

    @ddt.data(["small"],
              ["medium"],
              ["large"],
              ["xlarge"])

    @ddt.unpack
    def test_snapshot(self, flavor):

        t = []
        resultString = 'test create ' + flavor + ' flavor \
snapshot for 7 times\n'
        ControllerTest.init(self)
        for i in range(0, 7):
            vm_name = "test_" + flavor + "_snapshot_" + str(i)
            vm = ControllerTest.create_instance(
                self,
                vm_name,
                vm_flavor = "m1." + flavor)
            snapshot_name = flavor + "_snapshot_" + str(i)
            t_start = time.time()
            ControllerTest.create_snapshot(self,
                                           vm.target_id,
                                           snapshot_name)
            ControllerTest.determine_status(self,
                                            "image",
                                            snapshot_name,
                                            "ACTIVE")
            t_end = time.time()
            output = t_end - t_start
            resultString = resultString + str(output) + '  '
            t.append(output)
            ControllerTest.delete_image(self, snapshot_name)
            vm.delete_instance()

        t.sort()
        result = open("./result/CreateSnapshot_" + self.Time + "_result.log",
                      'a')
        result.write(resultString + "\n------------------Median time:" +
                     str(t[3]) + "-----------------\n")
        result.close()
