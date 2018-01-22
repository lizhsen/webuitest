# coding:utf-8

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
# Date:   August 2017

"""
@file test_vm_netperf_distributed.py
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
from bitmath import *
sys.path.append("../../lib/")
from controller_test import ControllerTest
from helper import shell_cmd_timeout
import re
import threading
import commands
import ConfigParser


conf = ConfigParser.ConfigParser()
conf.read("config.ini")

instance_number = 5
resultString = ''
temp = []
temp_send = []
temp_receive = []
temp_lose = []
netserver_ip = conf.get("global", "netserver_ip")


class VmNetperfDistributed(ControllerTest):
    """
    @class test_vm_netperf_distributed
    """

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/test_vm_netperf_distributed_" +
             Time + "_result.log")

    def execute_backend_thread(self, router, ip_address, cmd,
                               temp_send, temp_receive, temp_lose):
        target_cmd = 'ip netns exec qrouter-%s ssh root@%s \
"%s"' % (router, ip_address, cmd)
        output = commands.getoutput(target_cmd)
        # extract the needed values from the output
        # record output string into a result file
        # use value_send list to store line 5
        # use value_receive list to store line 6
        # use data_send list to store digits line 5
        # use data_receive list to store digits line 6
        # use temp_send list to store instances'send speed
        # use temp_receive list to store instances'receive speed
        ldddd = output.split('\n')
        value_send = ldddd[5].split(' ')
        value_receive = ldddd[6].split(' ')
        data_send = []
        data_receive = []
        for v in value_send:
            if v != '':
                data_send.append(v)
        for v in value_receive:
            if v != '':
                data_receive.append(v)
        send_speed = str(float(data_send[5]) *
                         MB(bits=1000000)) + "ps"
        receive_speed = str(float(data_receive[3]) *
                            MB(bits=1000000)) + "ps"
        lose = float(data_send[5]) - float(data_receive[3])
        lose_percent = lose / float(data_send[5])
        lose_percent = "%.2f%%" % (lose_percent * 100)
        temp_send.append(send_speed)
        temp_receive.append(receive_speed)
        temp_lose.append(lose_percent)

    def execute_backend_tcp_thread(self, router, ip_address, cmd,
                                   temp):
        target_cmd = 'ip netns exec qrouter-%s ssh root@%s \
"%s"' % (router, ip_address, cmd)
        output = commands.getoutput(target_cmd)
        # extract the needed values from the output
        # record output string into a result file
        # use value_send list to store line 5
        # use value_receive list to store line 6
        # use data_send list to store digits line 5
        # use data_receive list to store digits line 6
        # use temp_send list to store instances'send speed
        # use temp_receive list to store instances'receive speed
        ldddd = output.split('\n')
        value = ldddd[6].split(' ')
        data = []
        for v in value:
            if v != '':
                data.append(v)
        speed = float(data[4])*MB(bits=1000000)
        speed = str(speed) + "/s"
        temp.append(speed)

    @classmethod
    def setUpClass(cls):
        '''Init a VM instance and do performance test
        @fn setUpClass
        @param cls
        @return
        '''
        # create an instance firstly
        ControllerTest.init(cls)
        cls.vmlist = ControllerTest.create_several_instances(cls,
                                                             "test_vm_netperf",
                                                             instance_number)
        for i in range(instance_number):
            # get into target via SSH without password
            exp = os.path.join(os.path.dirname(__file__),
                               "../../tools/pass_to_vm.exp")
            # ensure ssh without passwd
            cmd = 'expect %s %s %s dddd2014' % (exp, cls.router,
                                                 cls.vmlist[i].target_ip)
            (ret, output) = shell_cmd_timeout(cmd)

    def test_vm_netperf_TCP_distributed(self):
        '''do TCP netperf test in serveral VMs
        @fn test_vm_netperf_UDP
        @param self
        @return
        '''
        # Go into target to run performance test
        resultString = "------------------------TCP distributed test\
-----------------------------\n"
        cmd = 'netperf -t TCP_STREAM -H %s -l 60' % netserver_ip
        threads = []
        for i in range(0, instance_number):
            temp_thread = threading.Thread(
                target=self.execute_backend_tcp_thread,
                args=(self.router,
                      self.vmlist[i].target_ip,
                      cmd, temp))
            threads.append(temp_thread)

        for t in threads:
            t.setDaemon(True)
            t.start()
            t.join()

        for i in range(instance_number):
            resultString = resultString + temp[i] + "\n"

        temp.sort()
        result = open("./result/test_vm_netperf_distributed_" +
                      self.Time + "_result.log", 'a')
        result.write(resultString + "    ----------->>>\
" + temp[2] + "\n")
        result.close()

    def test_vm_netperf_UDP_distributed(self):
        '''do UDP netperf test in several VMs block size 2048B
        @fn test_vm_netperf_UDP
        @param self
        @return
        '''
        # Go into target to run performance test
        resultString = "------------------------UDP distributed test:\
[send/receive]-----------------------------\n"
        cmd = 'netperf -t UDP_STREAM -H %s -l 60 -- -m 2048' % netserver_ip
        threads = []
        for i in range(0, instance_number):
            temp_thread = threading.Thread(target=self.execute_backend_thread,
                                           args=(self.router,
                                                 self.vmlist[i].target_ip,
                                                 cmd, temp_send,
                                                 temp_receive,
                                                 temp_lose))
            threads.append(temp_thread)

        for t in threads:
            t.setDaemon(True)
            t.start()
            t.join()

        for i in range(instance_number):
            resultString = resultString + temp_send[i] + "/\
" + temp_receive[i] + '     lose percent:' + temp_lose[i] + '\n'

        temp_send.sort()
        temp_receive.sort()
        temp_lose.sort()
        result = open("./result/test_vm_netperf_distributed_" +
                      self.Time + "_result.log", 'a')
        result.write(resultString + "\n----------------Median value: " +
                     temp_send[2] + '/' + temp_receive[2] +
                     "    lose percent:" + temp_lose[2] +
                     "--------------\n")
        result.close()

    @classmethod
    def tearDownClass(cls):
        for vm in cls.vmlist:
            vm.delete_instance()
##
# @}
# @}
##
