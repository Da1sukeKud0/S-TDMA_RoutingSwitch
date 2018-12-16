#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import copy
import time

cmdList = []
cmd01 = "sudo ovs-vsctl set-controller".split(" ")
cmd02 = "tcp:127.0.0.1:6653 -- set controller".split(" ")
cmd03 = "connection-mode=out-of-band"


def main():
    args = sys.argv
    if (len(args) != 2):
        print 'usage: *.py switchNum'
        quit()
    switchNum = int(args[1])

    # let's packet_In !!!
    setController(switchNum)
    counter = 0
    for cmd in cmdList:
        subprocess.call(cmd)
        # if (counter < 10):
        #     time.sleep(1.5)
        # elif (counter >= 10):
        #     time.sleep(2)
        # elif (counter >= 20):
        #     if (counter == 25):
        #         time.sleep(3)
        #     time.sleep(2.5)
        if (counter % 5 == 0):
            time.sleep(10)
        time.sleep(1)
        counter += 1


def setController(num):
    for n in range(1, num+1):
        name = "brs" + str(n)
        cmd = []
        cmd.extend(cmd01)
        cmd.append(name)
        cmd.extend(cmd02)
        cmd.append(name)
        cmd.append(cmd03)
        cmdList.append(cmd)
        # subprocess.call(cmd)


if __name__ == '__main__':
    main()
