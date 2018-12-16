#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import pickle
import copy

switchList = []
tmp = "sudo ovs-vsctl set bridge"
cmd02 = tmp.split(" ")
cmd02_p = "protocols=OpenFlow"


def main():
    # mininetで生成したopenvswitchのOFPversionを一括で設定
    args = sys.argv
    if (len(args) != 3):
        print 'usage: *.py switchNum OFPversion(10 or 13)'
        quit()
    switchNum = int(args[1])
    OFP = int(args[2])
    cmd02_p = cmd02_p + str(OFP)

    # create switch.
    setOFP(switchNum)


def setOFP(num):

    for n in range(1, num+1):
        # set bridgeName (s1, s2, ...) and add switchList
        bridgeName = "s" + str(n)
        switchList.append(bridgeName)
        # Complete the creation of the command
        cmd = []
        cmd.extend(cmd02)
        cmd.append(bridgeName)
        cmd.append(cmd02_p)
        subprocess.call(cmd)


if __name__ == '__main__':
    main()
