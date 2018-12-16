#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import copy

cmdList = []
cmd01 = "rvmsudo ./bin/trema send_packets -n 1 -s".split(" ")
cmd02 = "-d h1".split(" ")


def main():
    args = sys.argv
    if (len(args) != 3):
        print 'usage: *.py hostNum packetInNum'
        quit()
    hostNum = int(args[1])
    packetInNum = int(args[2])

    # let's packet_In !!!
    addHostLink(hostNum)
    additional_packet_in(packetInNum)
    for cmd in cmdList:
        subprocess.call(cmd)


def addHostLink(num):
    for n in range(1, num+1):
        name = "h" + str(n)
        cmd = []
        cmd.extend(cmd01)
        cmd.append(name)
        cmd.extend(cmd02)
        cmdList.append(cmd)
        # subprocess.call(cmd)


def additional_packet_in(num):
    cmd = "rvmsudo ./bin/trema send_packets -n 1 -s h1 -d h2".split(" ")
    for n in range(1, num+1):
        cmdList.append(cmd)
        # subprocess.call(cmd)


if __name__ == '__main__':
    main()
