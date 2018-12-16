#!/bin/sh
util/iplinkdelete_all.sh  > /dev/null 2>&1
util/delbr_all.sh  > /dev/null 2>&1
sudo rm -rf /tmp/TopologyController*  > /dev/null 2>&1
sudo rm -rf /tmp/vhost*  > /dev/null 2>&1
