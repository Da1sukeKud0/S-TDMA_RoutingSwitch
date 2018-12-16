#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import pickle
import copy

switchList = []

# commands
# ovsによりOpenFlow1.0のスイッチを指定数生成し、OpenFlowコントローラに127.0.0.1:6653を指定
tmp = "sudo ovs-vsctl add-br"
cmd01 = tmp.split(" ")

tmp = "sudo ovs-vsctl set bridge"
cmd02 = tmp.split(" ")
cmd02_p = "protocols=OpenFlow10"

tmp = "sudo ovs-vsctl set-controller"
cmd03 = tmp.split(" ")
cmd03_ip = "tcp:127.0.0.1:6653"


class switch:
    def __init__(self, switchName):
        pass


def main():
    args = sys.argv
    if (len(args) != 2):
        print 'usage: *.py switchNum'
        quit()
    switchNum = int(args[1])

    # set output file and create switchList
    if os.path.exists('switchList.txt'):
        os.remove('switchList.txt')
    file = open('switchList.txt', 'w')

    # create switch.
    setSwitch(switchNum, file)
    pickle.dump(switchList, file)
    file.close()


def setSwitch(num, file):
    for n in range(1, num+1):
        # set bridgeName (s1, s2, ...) and add switchList
        bridgeName = "s" + str(n)
        switchList.append(bridgeName)
        # Complete the creation of the command
        c01 = []
        c01.extend(cmd01)
        c01.append(bridgeName)
        c02 = []
        c02.extend(cmd02)
        c02.append(bridgeName)
        c02.append(cmd02_p)
        c03 = []
        c03.extend(cmd03)
        c03.append(bridgeName)
        c03.append(cmd03_ip)
        subprocess.call(c01)
        subprocess.call(c02)
        subprocess.call(c03)
        # print c01
        # print c02
        # print c03


def toHex(num):
    return num.zfill(16)


if __name__ == '__main__':
    main()
