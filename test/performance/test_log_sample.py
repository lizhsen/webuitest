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
from demo import process_log
import re


@ddt.ddt
class CliCreateIns(ControllerTest):

    @ddt.data(["medium", "CentOS-7.2"])

    @ddt.unpack
    def test_create_instance(self, flavor, image):
        casename = self._testMethodName
        process_log('/var/log', casename, self.create_instance(flavor, image))

    def create_instance(self, flavor, image):
        vm_flavor = 'm1.' + flavor
        # create a instance and wait until state is active
        vm_name = "test_create_" + flavor + "_" + str(i)
        ControllerTest.init(self)
        vm = ControllerTest.alt_create_instance(
            self,
            vm_flavor,
            image,
            vm_name)
        vm.delete_instance()
