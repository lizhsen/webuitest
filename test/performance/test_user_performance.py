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
# Date:   Oct 2017

import json
import os
import time
import sys
sys.path.append("../../lib/")
from webuitest import webdriver, WebUITest
from ddt import ddt, data, file_data, unpack
from get_element import GetElement
import logging
logger = logging.getLogger(__name__)
repeat_time = 7

@ddt
class UserPerformance(WebUITest):

    Time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    os.mknod("./result/test_user_performance__" + Time + "_result.log")

    # test case in user_performance.json
    @file_data('user_performance.json')
    def test_normal_acceptance(self, params):
        t = []
        json_path = "../webui/" + params[0]
        json_file = open(json_path)
        case_name = params[1]
        case_dict = json.load(json_file)
        if case_name in case_dict.keys():
            data = case_dict[case_name]
        driver = GetElement(self.driver)
        data = driver.perconditon(json_path, data)
        resultStr = self._testMethodName + "\n"
        for n in range(repeat_time):
            for i in range(len(data)):
                if data[i][0] == "循环":
                    endat = i
            driver.ui_engine(data, startidx=1, endidx=endat)
            start_time = time.time()
            driver.ui_engine(data, startidx=endat+1, endidx=endat+1)
            end_time = time.time()
            driver.ui_engine(data, startidx=endat+2, endidx=len(data))
            run_time = end_time - start_time
            resultStr = resultStr + str(run_time) + '   '
            t.append(run_time)

        t.sort()
        result = open("./result/test_user_performance__" + self.Time + "_result.log",
                      'a')
        result.write(resultStr + "\n-------------------Median time: " +
                     str(t[3]) + "-----------------------\n")
        result.close()
