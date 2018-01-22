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
@file test_vm_iozone_distributed_5.py
"""

##
# @addtogroup disk iozone
# @brief This is disk iozone
# @{
# @addtogroup disk iozone
# @brief This is disk iozone
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


@ddt
class VMiozoneDistributedTest(ControllerTest):
    """
    @class VMiozoneTest 5 instacnces
    """

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/test_vm_iozone_distributed_" + Time + "_result.log")

    def execute_backend_thread(self, router,
                               ip_address, cmd, data_read, data_write):
        target_cmd = 'ip netns exec qrouter-%s ssh \
root@%s "%s"' % (router, ip_address, cmd)
        output = commands.getoutput(target_cmd)
        ldddd = output.split('\n')
        value = ldddd[29].split(' ')
        data = []
        for v in value:
            if v.isdigit():
                data.append(v)

        data_write.append(data[2])
        data_read.append(data[4])

    @file_data('iozone_distribute.json')
    def test_vm_iozone_distribute(self, params):
        '''do distributed iozone test on 5 instances simultaneously
        @fn test_vm_iozone_randread_1M
        @param self
        @return
        '''
        # create several instances firstly
        ControllerTest.init(self)
        instance_number = params[0]
        self.vmlist = ControllerTest.create_several_instances(self,
                                                             "test_vm_perf",
                                                             instance_number)
        # create several volumes
        vdlist = ControllerTest.create_several_volumes(self,
                                                       "test_volume_perf-",
                                                       "20", instance_number)

        for i in range(instance_number):
            # get into target via SSH without password
            exp = os.path.join(os.path.dirname(__file__),
                               "../../tools/pass_to_vm.exp")
            # ensure ssh without passwd
            cmd = 'expect %s %s %s dddd2014' % (exp, self.router,
                                                 self.vmlist[i].target_ip)
            (ret, output) = shell_cmd_timeout(cmd)

        # create a virtual disk
        # attach disk to the vm
        for i in range(0, instance_number):
            ControllerTest.attach_disk_to_vm(self.vmlist[i].target_id,
                                             vdlist[i])
            ControllerTest.determine_status(self,
                                            "volume",
                                            vdlist[i],
                                            "in-use")

        # Go into target to run performance test
        temp = []
        data_read = []
        data_write = []
        bs_size = params[1]
        resultString = 'test_' + str(instance_number) + '_vm_iozone\
_randread_' + bs_size + ': read/write \n'
        cmd = 'cd /root/iozone3_465/src/current;./iozone \
-Rab ../../results/16results.xls -i 0 -i 1 -s 5g -r %s -f /dev/vdb' % bs_size

        threads = []
        for i in range(0, instance_number):
            temp_thread = threading.Thread(target=self.execute_backend_thread,
                                           args=(self.router,
                                                 self.vmlist[i].target_ip,
                                                 cmd, data_read,
                                                 data_write))
            threads.append(temp_thread)

        for t in threads:
            t.setDaemon(True)
            t.start()
            t.join()

        for i in range(instance_number):
            resultString = resultString + data_read[i] + "/\
" + data_write[i] + "\n"

        data_read.sort()
        data_write.sort()
        result = open("./result/test_vm_iozone_distributed_" +
                      self.Time + "_result.log", 'a')
        if instance_number == 5:
            result.write(resultString + "    ----------->>>" +
                         data_read[2] + "/" + data_write[2] + "\n")
        elif instance_number == 10:
            result.write(resultString + "    ----------->>>" +
                         data_read[5] + "/" + data_write[5] + "\n")
        result.close()

        for i in range(0, instance_number):
            self.vmlist[i].delete_instance()
            ControllerTest.determine_status(self,
                                            "instance",
                                            self.vmlist[i].target_id,
                                            "")
            ControllerTest.delete_volume(vdlist[i])
##
# @}
# @}
##
