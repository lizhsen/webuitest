#!/bin/bash

set -x

CONF=$1
if [ ! -z $2 ]; then
    IP=$2
else
    IP="10.200.43.216"
fi
# this file is run on controller node
. /root/keystonerc_admin

# command
cirros_id=`nova image-list | grep "| cirros" | awk '{print $2}'`
admin_tenant_id=`openstack project list | grep admin | awk '{print $2}'`
keystone_ip=$IP
tempest_tenant_id=`openstack project list | grep project_for_tempest | awk '{print $2}'`
tempest_user_id=`openstack user list | grep user_for_tempest | awk '{print $2}'`
public_network_id=`neutron net-list | grep external | awk '{print $2}'`
router_id=`neutron router-list | grep router | awk '{print $2}'`

# function run command and change configuration file
function run_and_modify()
{
   item=$1
   result=$2
   sed -i "s/<$item>/$result/g" $CONF
}

run_and_modify "cirros_id" $cirros_id
run_and_modify "admin_tenant_id" $admin_tenant_id
run_and_modify "keystone_ip" $keystone_ip
run_and_modify "tempest_tenant_id" $tempest_tenant_id
run_and_modify "tempest_user_id" $tempest_user_id
run_and_modify "public_network_id" $public_network_id
run_and_modify "router_id" $router_id

