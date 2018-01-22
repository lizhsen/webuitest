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
# Author: lizs@rc.dddd.com
# Date:   Sep 2017

"""
@file check_download_image.py
"""

##
# @addtogroup control_panel
# @brief This is control_panel test for daemon status
# @{
##


import os
import re
import json
import unittest
import sys
sys.path.append("../../lib/")
import ddt
from helper import shell_cmd_timeout
from helper import shell_cmd
from controller_test import ControllerTest


class DownloadImage(unittest.TestCase):
    '''
    @class DownloadImage
    '''
    def test_download_image(self):
        ret2 = ControllerTest.download_image()
        if ret2 == 0:
            pass
        else:
            assert False, "download image fail, please check "

##
# @}
# @}
##
