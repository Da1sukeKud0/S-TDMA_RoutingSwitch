#!/bin/bash
mkdir -p ~/trema
cd ~/trema
git clone https://github.com/Da1sukeKud0/S-TDMA_RoutingSwitch.git
mv S-TDMA_RoutingSwitch routing_switch
cd routing_switch
bundle install --binstubs
