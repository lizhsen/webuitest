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
#:
# Author: lizs@rc.dddd.com
# Date:   Dec 2017


import os
import re
import sys
sys.path.append("../../lib/")
from helper import shell_cmd_timeout


def open_stack_command(cmd):
    (ret, output) = shell_cmd_timeout(cmd)
    print (output)


for i in sys.argv:
    open_stack_command(i)
