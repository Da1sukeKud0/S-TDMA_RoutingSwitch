#!/bin/sh
sudo ovs-vsctl show |grep Bridge |sed -e 's/    Bridge "//g' |sed -e 's/"//g'| sed -e 's/" "/\n/g' | sudo xargs -L 1 -t ovs-vsctl del-br
