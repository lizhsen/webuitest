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
@file test_vm_fio_distributed.py
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
import threading
import commands


@ddt
class VMFioDistributedTest(ControllerTest):
    """
    @class VMFioTest in severalinstacnces
    """

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/test_vm_fio_distributed_" + Time + "_result.log")

    def execute_backend_thread(self, router, ip_address, cmd, data):
        target_cmd = 'ip netns exec qrouter-%s ssh root@%s \
"%s"' % (router, ip_address, cmd)
        output = commands.getoutput(target_cmd)
        reg = re.compile(r"(?<=iops=)\d+")
        match = reg.search(output)
        data.append(match.group(0))

    @file_data('fio_distribute.json')
    def test_vm_fio_distribute(self, params):
        '''do distributed fio test on serveral instances simultaneously
        @fn test_vm_fio_distribute
        @param self
        @return
        '''
        # create several instances firstly
        ControllerTest.init(self)
        instance_number = params[0]
        self.vmlist = ControllerTest.create_several_instances(self,
                                                             "test_vm_fio",
                                                             instance_number)
        # create several volumes
        vdlist = ControllerTest.create_several_volumes(self,
                                                       "test_volume_fio-",
                                                       "20", instance_number)

        for i in range(instance_number):
            # get into target via SSH without password
            exp = os.path.join(os.path.dirname(__file__),
                               "../../tools/pass_to_vm.exp")
            # ensure ssh without passwd
            cmd = 'expect %s %s %s dddd2014' % (exp, self.router,
                                                 self.vmlist[i].target_ip)
            (ret, output) = shell_cmd_timeout(cmd)
            # attach volume to instance
            ControllerTest.attach_disk_to_vm(self.vmlist[i].target_id,
                                             vdlist[i])
            ControllerTest.determine_status(self,
                                            "volume",
                                            vdlist[i],
                                            "in-use")

        data = []
        bs_size = params[1]
        mode = params[2]
        # Go into target to run performance test
        temp = []
        resultString = 'test_'+ str(instance_number) +'_vm_fio_\
' + mode + '_' + bs_size + ':\n'
        cmd = '/usr/bin/fio -name=test -filename=/dev/vdb -ioengine=libaio -direct=1 \
-size=5g -thread -bs=%s -iodepth=32 -numjobs=1 -rw=%s \
-group_reporting -runtime=30' % (bs_size, mode)

        threads = []
        for i in range(0, instance_number):
            temp_thread = threading.Thread(target=self.execute_backend_thread,
                                           args=(self.router,
                                                 self.vmlist[i].target_ip,
                                                 cmd, data))
            threads.append(temp_thread)

        for t in threads:
            t.setDaemon(True)
            t.start()
            t.join()

        for d in data:
            resultString = resultString + d + "   "

        data.sort()
        result = open("./result/test_vm_fio_distributed_" +
                      self.Time + "_result.log", 'a')
        if instance_number == 5:
            result.write(resultString + "    ----------->>>" + data[2] + "\n")
        elif instance_number == 10:
            result.write(resultString + "    ----------->>>" + data[5] + "\n")
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
