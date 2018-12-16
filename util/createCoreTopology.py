#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import pickle
import copy

conf = []


def main():
    args = sys.argv
    if (len(args) != 2):
        print 'usage: *.py switchNum'
        quit()
    switchNum = int(args[1])

    # create switch.
    makeSwitch(switchNum)
    makeHost(2)
    makeLink(switchNum)

    # set output file and write
    path = "test/resource/core_" + str(switchNum) + ".conf"
    if os.path.exists(path):
        os.remove(path)
    with open(path, mode='w') as file:
        file.write('\n'.join(conf))


def makeSwitch(num):
    for n in range(1, num+1):
        name = "0x" + str(n)
        cmd = "vswitch('" + name + "') { dpid '" + name + "' }"
        conf.append(cmd)
    conf.append("")


def makeHost(num):
    for n in range(1, num+1):
        name = "h" + str(n)
        ip = "192.168.0." + str(n)
        cmd = "vhost ('" + name + "') { ip '" + ip + "' }"
        conf.append(cmd)
    conf.append("")


def makeLink(num):
    for n in range(2, num+1):
        src = "0x1"
        dst = "0x" + str(n)
        cmd_s2s = "link '" + src + "', '" + dst + "'"
        conf.append(cmd_s2s)
    src = "0x1"
    hst = "h1"
    cmd_s2h = "link '" + src + "', '" + hst + "'"
    conf.append(cmd_s2h)
    hst = "h2"
    cmd_s2h = "link '" + src + "', '" + hst + "'"
    conf.append(cmd_s2h)
    conf.append("")


def toHex(num):
    return num.zfill(16)


if __name__ == '__main__':
    main()
