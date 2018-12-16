#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import pickle
import copy
import networkx
from networkx.generators.random_graphs import barabasi_albert_graph
from matplotlib import pyplot


conf = []


def main():  # ランダムなトポロジを生成(Barabási-Albertモデルに従う)
    print("Requirement: 1 <= complexity < switchNum")
    switchNum = input("スイッチ数(switchNum): ")
    complexity = input("新しいノードから既存のノードに接続するエッジの数(complexity): ")
    # 入力値の妥当性を確認 (1 <= complexity < switchNum)
    if (type(switchNum) is not int) or (type(complexity) is not int) or (not 1 <= complexity < switchNum):
        print("数値以外が入力されたか、上記の制約を満たしていません")
        exit()

    # 指定数のスイッチとホストを生成し接続
    makeSwitch(switchNum)
    makeHostAndLink(switchNum)

    # Barabási-Albertモデルのグラフを生成
    G = barabasi_albert_graph(switchNum, complexity)
    print(G.edges())

    # 生成されたグラフに基づいてスイッチ間を接続
    makeLinks(G.edges())

    # グラフをpngで出力
    networkx.draw(G, with_labels=True)
    pngpath = "test/resource/topo_image/ba_random_" + \
        str(switchNum) + "_" + str(complexity) + ".png"
    pyplot.savefig(pngpath)
    # pyplot.show()

    # ファイルに出力
    path = "test/resource/ba_random_" + \
        str(switchNum) + "_" + str(complexity) + ".conf"
    if os.path.exists(path):
        os.remove(path)
    with open(path, mode='w') as file:
        file.write('\n'.join(conf))
    print "\nDone."


def makeSwitch(num):
    for n in range(1, num+1):
        name = "s" + str(n)
        dpid = "0x" + str(n)
        cmd = "vswitch('" + name + "') { dpid '" + dpid + "' }"
        conf.append(cmd)
    conf.append("")


def makeHostAndLink(num):
    for n in range(1, num+1):
        hostname = "h" + str(n)
        ip = "192.168.0." + str(n)
        cmd = "vhost ('" + hostname + "') { ip '" + ip + "' }"
        conf.append(cmd)
        switch = "s" + str(n)
        cmd_link = "link '" + switch + "', '" + hostname + "'"
        conf.append(cmd_link)
    conf.append("")


def makeLinks(edgeList):
    for edge in edgeList:
        makeLink(edge[0] + 1, edge[1] + 1)


def makeLink(src, dst):
    src = "s" + str(src)
    dst = "s" + str(dst)
    cmd_s2s = "link '" + src + "', '" + dst + "'"
    conf.append(cmd_s2s)


def toHex(num):
    return num.zfill(16)


if __name__ == '__main__':
    main()
