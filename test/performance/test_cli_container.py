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


class ContainerTest(ControllerTest):

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/CliContainer_" + Time + "_result.log")

    @classmethod
    def SetupClass(name, bs_size):
        for i in range(0, 7):
            name = "test-" + str(bs_size) + "M-" + str(i)
            cmd = "dd if=/dev/zero of=/usr/local/dddd-test/test/\
performance/object_test/%s bs=%sM count=1" % (name, bs_size)
            shell_cmd_timeout(cmd)

    @classmethod
    def TeardownClass(cmd, bs_size):
        cmd = "rm -rf /usr/local/dddd-test/test/performance/\
object_test/test-%sM-*" % (bs_size)
        shell_cmd_timeout(cmd)

    @classmethod
    def test_create_containers(self):

        t1 = []
        t2 = []

        ControllerTest.init(self)
        for i in range(0, 7):
            name = "test" + str(i)
            # create a container
            c_start = time.time()
            ControllerTest.create_container(name)
            c_end = time.time()
            c_time = c_end - c_start
            # delete a container
            d_start = time.time()
            ControllerTest.delete_container(name)
            d_end = time.time()
            d_time = d_end - d_start

            t1.append(c_time)
            t2.append(d_time)
            t1.sort()
            t2.sort()

        result = open("./result/CliContainer_" + self.Time + "_result.log",
                      'a')
        result.write("create container for 7 times" + "\n" + str(t1) + "\n---\
--------------------\n" "delete container for 7 times" + "\n" + str(t2) + "\n\
------------------------\n")
        result.close()

    @classmethod
    def test_object_20M(self):

        t1 = []
        t2 = []
        t3 = []

        self.SetupClass(20)
        ControllerTest.init(self)
        # create a container
        ControllerTest.create_container("test")
        container = ControllerTest.get_container_status("test")
        for i in range(0, 7):
            name = "test-20M-" + str(i)
            path = "usr/local/dddd-test/test/performance/object_test/"
            upload_path = "/" + path + name
            # upload an object
            u_start = time.time()
            ControllerTest.upload_object(container, upload_path)
            u_end = time.time()
            u_t = u_end - u_start
            # download an object
            download_path = path + name
            download_speed = ControllerTest.download_object(container,
                                                            download_path)
            # delete an object
            d_start = time.time()
            ControllerTest.delete_object(container, download_path)
            d_end = time.time()
            d_t = d_end - d_start

            t1.append(u_t)
            t2.append(download_speed)
            t3.append(d_t)

        self.TeardownClass(20)
        t1.sort()
        t2.sort()
        t3.sort()

        result = open("./result/CliContainer_" + self.Time + "_result.log",
                      'a')
        result.write("size 20M" + "\n" + "upload \
object" + "\n" + str(t1) + "\n-----------------------\n" + "download object \
speed" + "\n" + str(t2) + "\n------------------------\n" + "delete \
object" + "\n" + str(t3) + "\n-----------------------------\n")
        result.close()

    @classmethod
    def test_object_1024M(self):

        t1 = []
        t2 = []
        t3 = []

        self.SetupClass(1024)
        ControllerTest.init(self)
        # create a container
        ControllerTest.create_container("test")
        container = ControllerTest.get_container_status("test")
        for i in range(0, 7):
            name = "test-1024M-" + str(i)
            path = "usr/local/dddd-test/test/performance/object_test/"
            upload_path = "/" + path + name
            # upload an object
            u_start = time.time()
            ControllerTest.upload_object(container, upload_path)
            u_end = time.time()
            u_t = u_end - u_start
            # download an object
            download_path = path + name
            download_speed = ControllerTest.download_object(container,
                                                            download_path)
            # delete an object
            d_start = time.time()
            ControllerTest.delete_object(container, download_path)
            d_end = time.time()
            d_t = d_end - d_start

            t1.append(u_t)
            t2.append(download_speed)
            t3.append(d_t)

        self.TeardownClass(1024)
        t1.sort()
        t2.sort()
        t3.sort()

        result = open("./result/CliContainer_" + self.Time + "_result.log",
                      'a')
        result.write("size 1024M" + "\n" + "upload \
object" + "\n" + str(t1) + "\n-----------------------\n" + "download object \
speed" + "\n" + str(t2) + "\n------------------------\n" + "delete \
object" + "\n" + str(t3) + "\n-----------------------------\n")
        result.close()
