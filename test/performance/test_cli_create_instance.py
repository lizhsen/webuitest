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
class CliCreateIns(ControllerTest):

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/CliCreateIns_" + Time + "_result.log")

    @ddt.data(["medium", "CentOS-7.2"],
              ["small", "CentOS-7.2"],
              ["large", "CentOS-7.2"],
              ["xlarge", "CentOS-7.2"],
              ["tiny", "cirros"],
              ["large", "Windows-2012R2"])

    @ddt.unpack
    def test_create_instance(self, flavor, image):

        temp = []
        vm_flavor = 'm1.' + flavor
        resultString = 'test create ' + flavor + image + ' \
instance for 7 times\n'
        # create a instance and wait until state is active
        for i in range(0, 7):
            vm_name = "test_create_" + flavor + "_" + str(i)
            time_start = time.time()
            ControllerTest.init(self)
            vm = ControllerTest.alt_create_instance(
                self,
                vm_flavor,
                image,
                vm_name)
            time_end = time.time()
            output = time_end - time_start
            resultString = resultString + str(output) + ' '
            temp.append(output)
            vm.delete_instance()

        temp.sort()
        result = open("./result/CliCreateIns_" + self.Time + "_result.log",
                      'a')
        result.write(resultString + "\n-------------------Median time: " +
                     str(temp[3]) + "-----------------------\n")
        result.close()
