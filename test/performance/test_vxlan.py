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
@file test_vm_netperf.py
"""

##
# @addtogroup netperf
# @brief This is netperf
# @{
# @addtogroup netperf
# @brief This is netperf
# @{
##

import os
import time
import sys
import ddt
from bitmath import *
sys.path.append("../../lib/")
from controller_test import ControllerTest
from controller_test import Virtual_Machine
from helper import shell_cmd_timeout
import re
import ConfigParser


conf = ConfigParser.ConfigParser()
conf.read("config.ini")
netserver_ip = conf.get("global", "netserver_ip")


class TestVxlan(ControllerTest):
    """
    @class test_vm_small_netperf
    """

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/test_vxlan_" + Time + "_result.log")
    repeat_times = 5

    @classmethod
    def setUpClass(cls):
        '''Init a VM instance and do performance test
        @fn setUpClass
        @param cls
        @return
        '''
        cls.vm_list = []
        # create instances firstly
        ControllerTest.init(cls)
        vm1 = ControllerTest.create_instance(cls, "netperf-01")
        cls.vm_list.append(vm1)
        vm2 = ControllerTest.create_instance(cls, "netperf-02",
                                             node = cls.alt_node)
        cls.vm_list.append(vm2)
        vm3 = ControllerTest.create_instance(cls, "netperf-03",
                                             nic = cls.alt_internal_nic)
        cls.vm_list.append(vm3)
        vm4 = ControllerTest.create_instance(cls, "netperf-04",
                                             node = cls.alt_node,
                                             nic = cls.alt_internal_nic)
        cls.vm_list.append(vm4)

        time.sleep(10)
        # get into target via SSH without password
        exp = os.path.join(os.path.dirname(__file__),
                           "../../tools/pass_to_vm.exp")
        # ensure ssh without passwd
        for i in range(4):
            cmd = 'expect %s %s %s dddd2014' % (exp, cls.router,
                                                 cls.vm_list[i].target_ip)
            (ret, output) = shell_cmd_timeout(cmd)
        time.sleep(30)

    def test_vm_netperf_TCP(self):
        '''use do TCP netperf test in VM
        @fn test_vm_netperf_TCP
        @param self
        @return
        '''
        for i in range(4):
            target_ip = self.vm_list[i].target_ip
            temp = []
            # Go into target to run performance test
            resultString = "-----------------------TCP test in \
" + target_ip + " :------------------------\n"
            print resultString
            for j in range(0, self.repeat_times):
                cmd = 'netperf -t TCP_STREAM -H %s -l 60' % netserver_ip
                print cmd
                (ret, output) = self.vm_list[i].execute(self.router, cmd)
                print("doing TCP test in " + target_ip + " .........")
                time.sleep(1)

                # record output string into a result file
                ldddd = output.split('\n')
                value = ldddd[6].split(' ')
                data = []
                for v in value:
                    if v != '':
                        data.append(v)
                speed = float(data[4])*MB(bits=1000000)
                speed = str(speed) + "/s"
                resultString = resultString + speed + "\n"
                temp.append(speed)

            temp.sort()
            result = open("./result/test_vxlan_" + self.Time + "\
_result.log", 'a')
            result.write(resultString + "\n----------------Median value: " +
                         temp[2] + "--------------\n")
            result.close()

    def test_vm_netperf_UDP(self):
        '''use do UDP netperf test in VM block size 1024B
        @fn test_vm_netperf_UDP
        @param self
        @return
        '''
        for i in range(4):
            target_ip = self.vm_list[i].target_ip
            temp_send = []
            temp_receive = []
            temp_lose = []
            # Go into target to run performance test
            resultString = "-----------------------UDP test in \
" + target_ip + " :------------------------\n"
            for j in range(0, self.repeat_times):
                cmd = 'netperf -t UDP_STREAM -H %s -l 60 \
-- -m 2048' % netserver_ip
                (ret, output) = self.vm_list[i].execute(self.router, cmd)
                time.sleep(1)

                # record output string into a result file
                # use value_send list to store line 5
                # use value_receive list to store line 6
                # use data_send list to store digits line 5
                # use data_receive list to store digits line 6
                # use temp_send list to store repeat_times'send speed
                # use temp_receive list to store repeat_times'receive speed

                ldddd = output.split('\n')
                value_send = ldddd[5].split(' ')
                value_receive = ldddd[6].split(' ')
                data_send = []
                data_receive = []
                data_lose = []
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
                resultString = resultString + send_speed + "/\
" + receive_speed + '     lose percent:' + lose_percent + '\n'
                temp_send.append(send_speed)
                temp_receive.append(receive_speed)
                temp_lose.append(lose_percent)

            temp_send.sort()
            temp_receive.sort()
            temp_lose.sort()
            result = open("./result/test_vm_netperf_" + self.Time + "\
_result.log", 'a')
            result.write(resultString + "\n----------------Median value: " +
                         temp_send[2] + '/' + temp_receive[2] +
                         "    lose percent:" + temp_lose[2] +
                         "--------------\n")
            result.close()

    @classmethod
    def tearDownClass(cls):
        for i in range(4):
            cls.vm_list[i].delete_instance()
