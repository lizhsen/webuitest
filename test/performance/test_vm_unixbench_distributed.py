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
# Date:   August 2017

"""
@file test_vm_unixbench_distributed_5.py
"""

##
# @addtogroup disk unixbench
# @brief This is disk unixbench
# @{
# @addtogroup disk unixbench
# @brief This is disk unixbench
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
import threading
import commands


resultString = ''
data_thread = []

@ddt
class TestVMUnixbenchDistributed(ControllerTest):
    """
    @class test_vm_unixbench_distributed
    """

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/test_vm_unixbench_distributed_" +
             Time + "_result.log")

    def execute_backend_thread(self, router, ip_address, cmd, data):
        target_cmd = 'ip netns exec qrouter-%s ssh root@%s \
"%s"' % (router, ip_address, cmd)
        print target_cmd
        # extract the needed values from the output
        output = commands.getoutput(target_cmd)
        print ">>>>>>>>>>>>>>>>>>>>>>........"
        print output
        ldddd = output.split('\n')
        for line in ldddd:
            if "System Benchmarks Index Score" in line:
                reg = re.compile(r"\d+\.?\d*")
                match = reg.search(line)
                data.append(match.group(0))

    @file_data('unixbench_distributed.json')
    def test_vm_unixbench_distributed(self,params):
        '''do distributed unixbench test on instances simultaneously
        @fn test_vm_unixbench_distributed
        @param self
        @return
        '''
        instance_number = params[0]
        mode = params[1]
        thread = params[2]

        # create an instance firstly
        ControllerTest.init(self)
        vmlist = ControllerTest.create_several_instances(self,
                                                         "test_vm_unixbench",
                                                         instance_number)
        time.sleep(10)
        for i in range(instance_number):
            # get into target via SSH without password
            exp = os.path.join(os.path.dirname(__file__),
                               "../../tools/pass_to_vm.exp")
            # ensure ssh without passwd
            cmd = 'expect %s %s %s dddd2014' % (exp, self.router,
                                                 vmlist[i].target_ip)
            (ret, output) = shell_cmd_timeout(cmd)
            time.sleep(5)

        resultString = '--------------------in ' + str(instance_number) + ' \
vms run ' + mode + ' in thread ' + thread + ':---------------------------\n'
        cmd = 'cd /root/UnixBench;./Run ' + mode + ' -c ' + thread

        threads = []
        for i in range(0, instance_number):
            temp_thread = threading.Thread(target=self.execute_backend_thread,
                                           args=(self.router,
                                                 vmlist[i].target_ip,
                                                 cmd, data_thread))
            threads.append(temp_thread)

        for t in threads:
            t.setDaemon(True)
            t.start()
            t.join()

        for d in data_thread:
            resultString = resultString + d + "\n"

        data_thread.sort()

        result = open("./result/test_vm_unixbench_distributed_" +
                      self.Time + "_result.log", 'a')
        if instance_number == 5:
            result.write(resultString + "    ----------->>>" +
                         data_thread[2] + "\n")
        elif instance_number == 10:
            result.write(resultString + "    ----------->>>" +
                         data_thread[5] + "\n")
        result.close()

        for vm in vmlist:
            vm.delete_instance()
##
# @}
# @}
##
