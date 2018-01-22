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
class StartAndDelIns(ControllerTest):

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/StartAndDelIns_" + Time + "_result.log")

    @ddt.data(["medium", "CentOS-7.2"],
              ["small", "CentOS-7.2"],
              ["large", "CentOS-7.2"],
              ["xlarge", "CentOS-7.2"],
              ["tiny", "cirros"])

    @ddt.unpack
    def test_start_and_delete_instance(self, flavor, image):

        temp = []
        temp2 = []
        vm_flavor = 'm1.' + flavor
        resultString = 'test start ' + flavor + image + ' instance for 7 times\n'
        resultString2 = 'test delete ' + flavor + image + ' instance for 7 times\n'
        # create a instance and wait for ping is OK
        for i in range(0, 7):
            vm_name = vm_name = "test_start_" + flavor + "_" + str(i)
            time_start = time.time()
            ControllerTest.init(self)
            vm = ControllerTest.alt_create_instance(
                self,
                vm_flavor,
                image,
                vm_name)
            n = 1
            while True:
                ping_status = vm.ping_network(self.router)
                n = n + 1
                if ping_status:
                    break
                elif n == 1200:
                    break
            time_end = time.time()
            output = time_end - time_start
            resultString = resultString + str(output) + '  '
            temp.append(output)
            del_time_start = time.time()
            vm.delete_instance()
            ControllerTest.determine_status(self,
                                            "instance",
                                            vm.target_id,
                                            "")
            del_time_end = time.time()
            del_time = del_time_end - del_time_start - 30
            resultString2 = resultString2 + str(del_time) + '  '
            temp2.append(del_time)

        temp.sort()
        temp2.sort()
        result = open("./result/StartAndDelIns_" + self.Time + "_result.log",
                      'a')
        result.write(resultString + "\n------------------Medain start time:" +
                     str(temp[3]) + "----------------\n" + resultString2 +
                     "\n-----------------Medain delete time:" +
                     str(temp2[3]) + "----------------\n")
        result.close()
