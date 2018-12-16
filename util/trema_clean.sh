#!/bin/sh
util/iplinkdelete_all.sh  > /dev/null 2>&1
util/delbr_all.sh  > /dev/null 2>&1
sudo rm -rf /tmp/*.log  > /dev/null 2>&1
sudo rm -rf /tmp/*.pid  > /dev/null 2>&1
sudo rm -rf /tmp/vhost*  > /dev/null 2>&1
