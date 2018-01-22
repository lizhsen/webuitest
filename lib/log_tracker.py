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
# Date:   Dec 2017

import paramiko
import time


class TrackRemoteLog:
    def __init__(self):
        # ssh远程连接
        host = '10.200.43.216'
        port = 22
        user_name = 'root'
        password = 'Inesa2014!'
        paramiko.util.log_to_file('paramiko.log')
        self._ssh = paramiko.SSHClient()
        self._ssh.load_system_host_keys()

        self._ssh.connect(host, port, user_name, password)

    def start_logging(self, filepath, casename):
        # 在client端开启monitor
        cmd = 'python /opt/log_monitor/start_logging.py %s %s' % (filepath, casename)
        self._ssh.exec_command(cmd)

    def kill_log_process(self):
        # 杀死client端monitor进程
        cmd = 'python /opt/log_monitor/kill_log_process.py'
        self._ssh.exec_command(cmd)

    def collect_logfile(self):
        # 将结果log收集到server端
        time.sleep(3)
        cmd = 'python /opt/log_monitor/collect_logfile.py'
        self._ssh.exec_command(cmd)

    def sort_log_and_upload(self):
        # 整合log文件
        time.sleep(3)
        cmd = 'python /opt/log_monitor/sort_log.py'
        self._ssh.exec_command(cmd)

        # 上传至本地
        time.sleep(3)
        log_name_cmd = 'ls -rt /opt/log_monitor/remote_log | tail -n 1'
        stdin, stdout, stderr = self._ssh.exec_command(log_name_cmd)
        log_name = stdout.readldddd()[0].strip()
        remote_file = os.path.join('/opt/log_monitor/remote_log', log_name)
        local_file = os.path.join('/opt/remote_log', log_name)
        _sftp = self._ssh.open_sftp()
        _sftp.get(remote_file, local_file)
