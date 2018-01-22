"""
@file test_stream.py
"""

##
# @addtogroup memory stream
# @brief This is memory component
# @{
# @addtogroup test_stream test_stream
# @brief This is memory module
# @{
##

import os
import time
import sys
sys.path.append("../../lib/")
from controller_test import ControllerTest
from helper import shell_cmd_timeout

class Ceph_block_storage_throughput_performance(ControllerTest):
    """
    @class StreamTest
    """

    def test_IO_1M(self):
        '''ceph block size:1M
           Sequentially read & write
        '''
        # Go into target to run performance test
        cmd = 'ssh ha01-mon02-osd01;/root/iozone3_465/src/current;./iozone -Rab ../../results/16results.xls -i 0 -i 1 -s 5g -r 1m -f /dev/sdk2'
        (ret, output) = shell_cmd_timeout(cmd)
        time.sleep(3)

    def test_IO_4M(self):
        '''ceph block size:4M
           Sequentially read & write
        '''
        # Go into target to run performance test
        cmd = 'ssh ha01-mon02-osd01;/root/iozone3_465/src/current;./iozone -Rab ../../results/16results.xls -i 0 -i 1 -s 5g -r 4m -f /dev/sdk2'
        (ret, output) = shell_cmd_timeout(cmd)
        time.sleep(3)

    def test_IO_8M(self):
        '''ceph block size:8M
           Sequentially read & write
        '''
        # Go into target to run performance test
        cmd = 'ssh ha01-mon02-osd01;/root/iozone3_465/src/current;./iozone -Rab ../../results/16results.xls -i 0 -i 1 -s 5g -r 8m -f /dev/sdk2'
        (ret, output) = shell_cmd_timeout(cmd)
        time.sleep(3)

    def test_IO_16M(self):
        '''ceph block size:16M
           Sequentially read & write
        '''
        # Go into target to run performance test
        cmd = 'ssh ha01-mon02-osd01;/root/iozone3_465/src/current;./iozone -Rab ../../results/16results.xls -i 0 -i 1 -s 5g -r 16m -f /dev/sdk2'
        (ret, output) = shell_cmd_timeout(cmd)
        time.sleep(3)

##
# @}
# @}
##

