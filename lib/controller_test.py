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
@file test.py
"""

from helper import shell_cmd_timeout
import time
import string
import unittest
import subprocess
import os
import ConfigParser


conf = ConfigParser.ConfigParser()
conf.read("config.ini")


class Virtual_Machine(object):
    """
    @class Virtual_Machine
    """
    target_name = ''
    target_ip = '10.0.0.1'
    target_id = ''

    def __init__(self, instance_id):
        """
        @fn __init__
        @param self
        @param name: the name of vm instance
        @return
        """
        self.target_id = instance_id
        cmd = "nova list | grep ' %s ' | \
awk -F'|' '{print $7}' | head -n 1 | cut -d'=' -f2" % instance_id
        (ret, ip) = shell_cmd_timeout(cmd)
        self.target_ip = ip.strip()
        print('new instance initialization finished, target ip is:' +
              self.target_ip)

    def execute(self, router, cmd):
        """
        @fn run
        @param self
        @param router: the system route id
        @param cmd: the command to be executed in vm target
        @return
        """
        # run a command in VM instance from controller node
        target_cmd = 'ip netns exec qrouter-%s ssh root@%s \
"%s"' % (router, self.target_ip, cmd)
        print target_cmd
        return shell_cmd_timeout(target_cmd)
        # subprocess.Popen(target_cmd, shell=True)

    def ping_network(self, router):
        """
        @fn run
        @param self
        @param router: the system route id
        @return BOOL
        """
        cmd = 'ip netns exec qrouter-%s ping -c1 %s' % (router, self.target_ip)

        (ret, output) = shell_cmd_timeout(cmd)
        print(cmd)
        if ret == 0:
            return True
        else:
            return False

    def get_instance_id(self, vm_name):
        '''on instance node, get instance id by vm_name
        @fn get_instance_id
        @param self
        @return
        '''
        cmd = "nova list | grep %s | awk '{print $2}'" % vm_name
        (ret, instance_id) = shell_cmd_timeout(cmd)
        return instance_id.strip()

    def delete_instance(self):
        '''on instance node, delete instance
        @fn get_instance_id
        @param self
        @return
        '''
        time.sleep(30)
        cmd = "nova delete %s" % self.target_id
        shell_cmd_timeout(cmd)

    def restart_instance(self):
        '''on instance node, restart instance
        @fn get_instance_id
        @param self
        @return
        '''
        cmd = "nova reboot %s" % self.target_id
        shell_cmd_timeout(cmd)


class ControllerTest(unittest.TestCase):
    """
    @class ControllerTest
    """
    image = conf.get("global", "image_id")
    flavor = conf.get("global", "flavor")
    compute_node = conf.get("global", "node")
    alt_compute_node = conf.get("global", "alt_node")
    internal_nic = conf.get("global", "internal_nic")
    alt_internal_nic = conf.get("global", "alt_internal_nic")
    router = object
    centos72_url = conf.get("global", "centos72_url")
    cirros_url = conf.get("global", "cirros_url")

    @staticmethod
    def init(self):
        """
        @fn init
        @param self
        @return
        """
        self.router = conf.get("global", "router_id")
        self.internal_nic = self.internal_nic
        self.alt_internal_nic = self.alt_internal_nic
        self.alt_node = self.alt_compute_node

    @staticmethod
    def get_volume_status(volume_id):
        '''on controller node, get volume id by disk_name
        @fn get_volume_status
        @param self
        @return
        '''
        cmd = "cinder list | grep %s | awk '{print $4}'" % volume_id
        (ret, volume_status) = shell_cmd_timeout(cmd)
        return volume_status.strip()

    @staticmethod
    def get_instance_status(instance_id):
        '''on controller node, get instance status by instance_id
        @fn get_instance_id
        @param self
        @return
        '''
        cmd = "nova list | grep %s | awk '{print $6}'" % instance_id
        (ret, instance_status) = shell_cmd_timeout(cmd)
        return instance_status.strip()

    @staticmethod
    def create_volume(name, size):
        '''on controller node, create a virtual disk by size(G)
        @fn create_volume
        @param self
        @return
        '''
        cmd = "cinder create --name %s %s" % (name, size)
        print(cmd)
        (ret, volume) = shell_cmd_timeout(cmd)
        time.sleep(10)
        for line in volume.split('\n'):
            if " id " in line:
                volume_id = line.split('|')[2].strip()

        return volume_id

    @staticmethod
    def delete_volume(volume_id):
        '''on controller node, delete a virtual disk by name
        @fn create_volume
        @param self
        @return
        '''
        cmd = "cinder delete %s" % volume_id
        shell_cmd_timeout(cmd)

    @staticmethod
    def create_several_volumes(self, name, size, number):
        '''on controller node, create several virtual disks by size(G)
        @fn create_volume
        @param self
        @return
        '''
        volumeList = []
        for i in range(0, number):
            volume_id = self.create_volume(name + str(i + 1), size)
            self.determine_status(self,
                                  "volume",
                                  volume_id,
                                  "available")
            volumeList.append(volume_id)

        return volumeList

    @staticmethod
    def create_volume_snapshot(self, name, volume_id):
        '''on controller node, create a snapshot for volume
        @fn create_volume_snapshot
        @param self
        @return
        '''
        cmd = "cinder snapshot-create --name %s %s" % (name, volume_id)
        print(cmd)
        (ret, vd_snapshot) = shell_cmd_timeout(cmd)
        vd_snapshot = vd_snapshot.split('|')
        return vd_snapshot[11].strip()

    @staticmethod
    def get_vd_snapshot_status(vd_snapshot_id):
        '''on controller node, get volume status by volume_id
        @fn get_volume_status
        @param self
        @return
        '''
        cmd = "cinder snapshot-list | grep %s | \
awk '{print $6}'" % vd_snapshot_id
        (ret, vd_snapshot_status) = shell_cmd_timeout(cmd)
        return vd_snapshot_status.strip()

    @staticmethod
    def delete_vd_snapshot(vd_snapshot_id):
        '''on controller node,delete volume snapshot
        @fn delete_vd_snapshot
        '''
        cmd = "cinder snapshot-delete %s" % vd_snapshot_id
        shell_cmd_timeout(cmd)

    @staticmethod
    def create_instance(self, vm_name, vm_flavor = flavor,
                        node = compute_node,
                        nic = internal_nic):
        '''on controller node, create an instance by command
        @fn create_instance
        @param self
        @return
        '''
        nic = '--nic net-id=%s' % nic
        cmd = 'nova boot --flavor %s --availability-zone nova:%s %s \
--image %s %s' % (self.flavor, node, nic, self.image, vm_name)
        # run command to create VM
        (ret, output) = shell_cmd_timeout(cmd)
        for line in output.split('\n'):
            if "| id" in line:
                instance_id = line.split('|')[2].strip()
        # ensure the vm instance boots up
        self.determine_status(self,
                              "instance",
                              instance_id,
                              "ACTIVE")
        instance = Virtual_Machine(instance_id)
        for i in range(20):
            time.sleep(20)
            if instance.ping_network(self.router):
                break

        return instance

    @staticmethod
    def create_several_instances(self, vm_name, number):
        '''on controller node, create several instances
        @fn create_serveral_instance
        @param self
        @return
        '''
        instanceList = []
        for i in range(0, number):
            vm = self.create_instance(self,
                                      vm_name + "-" + str(i+1))
            for j in range(0, 20):
                time.sleep(30)
                print('Let me ping vm again')
                if vm.ping_network(self.router):
                    instanceList.append(vm)
                    i = i + 1
                    print('ping successfullly count=' + str(i))
                    break

        return instanceList

    @staticmethod
    def alt_create_instance(self, vm_flavor, vm_image, vm_name):
        '''on controller node, create an instance without waiting for ready
        @fn alt_create_instance
        @param self
        @return
        '''
        nic = '--nic net-id=%s' % self.internal_nic
        cmd = 'nova boot --flavor %s %s --image %s %s ' % (vm_flavor, nic,
                                                           vm_image, vm_name)
        # run command to create VM
        (ret, output) = shell_cmd_timeout(cmd)
        for line in output.split('\n'):
            if "| id" in line:
                instance_id = line.split('|')[2].strip()
        self.determine_status(self,
                              "instance",
                              instance_id,
                              "ACTIVE")
        print('start booting a instance without waiting for ping status')
        instance = Virtual_Machine(instance_id)
        return instance

    @staticmethod
    def create_snapshot(self, instance_id, name):
        '''on controller node, create a snapshot of an instance
        @fn create_snapshot
        @param self
        '''
        cmd = "nova image-create %s %s" % (instance_id, name)
        (ret, output) = shell_cmd_timeout(cmd)

    @staticmethod
    def get_image_id(name):
        '''on controller node, get volume id by disk_name
        @fn get_volume_id
        @param self
        @return
        '''
        cmd = "nova image-list | grep %s | awk '{print $2}'" % name
        (ret, image_id) = shell_cmd_timeout(cmd)
        return image_id.strip()

    @staticmethod
    def get_image_status(name):
        '''
        '''
        cmd = "nova image-list | grep %s | awk '{print $6}'" % name
        (ret, image_status) = shell_cmd_timeout(cmd)
        return image_status.strip()

    @staticmethod
    def delete_image(self, name):
        '''on controller node, delete a image by name
        @fn create_snapshot
        @param self
        @return
        '''
        time.sleep(30)
        image_id = self.get_image_id(name)
        cmd = "glance image-delete %s" % image_id
        shell_cmd_timeout(cmd)

    @staticmethod
    def attach_disk_to_vm(instance_id, volume_id):
        '''on controller node, attach a volume to an instance
        @fn attach_disk_to_vm
        @param self
        @return
        '''
        cmd = "nova volume-attach %s %s /dev/vdb" % (instance_id, volume_id)
        (ret, output) = shell_cmd_timeout(cmd)

    @staticmethod
    def detach_disk_to_vm(instance_id, volume_id):
        '''on controller node, detach a volume to an instance
        @fn attach_disk_to_vm
        @param self
        @return
        '''
        cmd = "nova volume-detach %s %s" % (instance_id, volume_id)
        (ret, output) = shell_cmd_timeout(cmd)

    @staticmethod
    def create_container(name):
        '''on controller node, create a container
        @fn create_container
        '''
        cmd = "swift post %s" % name
        (ret, output) = shell_cmd_timeout(cmd)

    @staticmethod
    def get_container_status(name):
        '''on controller node, get the container by name
        @fn get_container
        @return
        '''
        cmd = "swift list | grep %s" % name
        (ret, output) = shell_cmd_timeout(cmd)

        return output.strip()

    @staticmethod
    def delete_container(name):
        '''on controller node, delete the container or object
        @fn delete_container
        @return
        '''
        cmd = "swift delete %s" % name
        (ret, output) = shell_cmd_timeout(cmd)

    @staticmethod
    def upload_object(container_name, file_path):
        '''on controller node, upload an object
        @fn upload_object
        '''
        cmd = "swift upload %s %s" % (container_name, file_path)
        shell_cmd_timeout(cmd)

    @staticmethod
    def download_object(container_name, file_path):
        '''on controller node, download an object
        @fn download_object
        @return
        '''
        cmd = "swift download %s %s" % (container_name, file_path)
        (ret, output) = shell_cmd_timeout(cmd)
        output = output.split(' ')
        speed = output[7]
        return speed

    @staticmethod
    def delete_object(container_name, file_path):
        '''on controller node, delete an object
        @fn delete_object
        '''
        cmd = "swift delete %s %s" % (container_name, file_path)
        shell_cmd_timeout(cmd)

    @staticmethod
    def determine_status(self, obj, obj_param, status_yes):
        n = 1
        while True:
            status = getattr(self, "get_%s_status" % obj)(obj_param)
            print("getting current status of the resource:" + status)
            n = n + 1
            result = string.find(status, status_yes) != -1
            if result:
                break
            elif n == 500:
                break

    @staticmethod
    def create_network(net_name, external_router='False', id='324',
                       type='vxlan'):
        '''on controller node, create_network
        @fn create_network
        @param name : network's name
        @param external_router : decide to create external or internal net
        @param type : vlan, vxlan, local ...
        @param id : segmentation_id
        @return
        '''
        if external_router == 'True':
            cmd = "neutron net-create %s --router:external %s \
            --provider:network_type %s \
            --provider:segmentation_id %s" % (net_name,
                                              external_router, type, id)
        else:
            cmd = "neutron net-create %s \
            --router:external %s " % (net_name, external_router)
        (ret, output) = shell_cmd_timeout(cmd)
        return output

    @staticmethod
    def create_external_subnet(sub_net_name, ex_net_name,
                               gateway='10.200.45.254',
                               ip_pool="start=10.200.45.190,end=10.200.45.195",
                               net_addr='10.200.45.0/24'):
        '''on controller node, create_subnet
        @fn create_external_subnet
        @param sub_net_name : subnet's name
        @param ex_net_name : network's name
        @param gateway : gateway addr
        @param net_addr : net_addr
        @return
        '''
        cmd = "neutron subnet-create --name %s --gateway %s \
    --allocation-pool %s --disable-dhcp %s %s" % (sub_net_name, gateway,
                                                ip_pool, ex_net_name,
                                                net_addr)
        (ret, output) = shell_cmd_timeout(cmd)
        return output

    @staticmethod
    def create_internal_subnet(sub_net_name, in_net_name,
                               gateway='192.168.1.1',
                               net_addr='192.168.1.0/24'):
        '''on controller node, create_network
        @fn create_network
        @param sub_net_name : subnet's name
        @param in_net_name : network's name
        @param gateway : gateway
        @param net_addr : net_addr
        @return
        '''
        cmd = "neutron subnet-create --name %s --gateway %s \
     --enable-dhcp %s %s" % (sub_net_name, gateway, in_net_name, net_addr)
        (ret, output) = shell_cmd_timeout(cmd)
        return output

    @staticmethod
    def delete_network(net_name):
        '''on controller node, create_network
        @fn delete_network
        @param net_name : network's name
        @return
        '''
        cmd = "neutron net-delete %s" % net_name
        (ret, output) = shell_cmd_timeout(cmd)
        return output

    @staticmethod
    def create_project(project_name):
        '''on controller node, create_project
        @fn create_project
        @param project_name : project's name
        @return
        '''
        cmd = "openstack project create %s" % project_name
        (ret, output) = shell_cmd_timeout(cmd)
        return output

    @staticmethod
    def delete_project(project_name):
        '''on controller node, delete_project
        @fn delete_project
        @param project_name : project's name
        @return
        '''
        cmd = "openstack project delete %s" % project_name
        (ret, output) = shell_cmd_timeout(cmd)
        return output

    @staticmethod
    def create_user(user_name, password, project_name='admin'):
        '''on controller node, create_user
        @fn create_user
        @param user_name : user's name
        @param password : password
        @param project_name : project's name
        @return
        '''
        cmd = "openstack user create %s --password %s \
        --project %s" % (user_name, password, project_name)
        (ret, output) = shell_cmd_timeout(cmd)
        return output

    @staticmethod
    def delete_user(user_name):
        '''on controller node, delete_user
        @fn delete_user
        @param users_name : user's name
        @return
        '''
        cmd = "openstack user delete %s " % user_name
        (ret, output) = shell_cmd_timeout(cmd)
        return output

    @staticmethod
    def download_image():
        '''on controller node, download_image
        @fn download_image
        @return
        '''
        cmd2 = "wget %s" % ControllerTest.cirros_url
        (ret2, output2) = shell_cmd_timeout(cmd2)
        return ret2

    @staticmethod
    def upload_image(file='CentOS-7.2.qcow2', name='centos7.2',
                     image_type='linux'):
        '''on controller node, upload_image
        @fn create_network
        @param file : file's name
        @param name : image's name
        @param image_type : windows or linux
        @return
        '''
        if ((image_type == 'linux') or (image_type == 'Linux')):
            cmd = "glance image-create --disk-format=qcow2 \
            --container-format=bare --visibility=public \
            --property hw_scsi_model=virtio-scsi \
            --property hw_qemu_guest_agent=yes \
            --property os_require_quiesce=yes \
            --property os_admin_user=root \
            --file %s --name %s" % (file, name)
        else:
            cmd = "glance image-create --disk-format=qcow2 \
            --container-format= bare  --visibility=public \
            --property hw_scsi_model=virtio-scsi \
            --property hw_qemu_guest_agent=yes \
            --property os_require_quiesce=yes\
            --property os_admin_user=Administrator \
            --property os_system= windows \
            --file %s --name %s" % (file, name)
        (ret, output) = shell_cmd_timeout(cmd)
        return output
##
# @}
# @}
##
