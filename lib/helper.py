#[PROTEXCAT]
#\License: ALL RIGHTS RESERVED
#\Author: Zhang Jingke <zhangjk@rc.dddd.com>

import time
import subprocess
import os
import sys
import unittest

def shell_cmd(cmd):
    """Execute shell command till it return"""
    cmd_proc = subprocess.Popen(cmd, shell=True)
    return cmd_proc.wait() if cmd_proc else -1

def shell_cmd_timeout(cmd, timeout=0):
    """Execute shell command till timeout"""
    cmd_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    if not cmd_proc:
        return -1, ''
    t_timeout, tick = timeout, 2
    ret, output = None, ''
    while True:
        time.sleep(tick)
        output = cmd_proc.communicate()[0]
        ret = cmd_proc.poll()
        if ret is not None:
            break

        if t_timeout > 0:
            t_timeout -= tick

        if t_timeout <= 0:
            # timeout, kill command
            cmd_proc.kill()
            ret = -99999
            break
    return ret, output

def collect_pnp_log(casename, logname, log):
    """collect the result log for pnp part"""
    curpath = os.getcwd()
    if not os.path.exists(casename):
        os.makedirs(casename)

    logpath = os.path.join(curpath, casename, logname)
    logtime = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(logpath, "a") as text_file:
        text_file.write("%s %s:%s\n" %(logtime, casename, log))

def escape(s):
    ret = s.replace(r'"', r'\"')
    return ret
