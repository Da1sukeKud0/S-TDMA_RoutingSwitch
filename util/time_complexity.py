#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import log
from math import factorial
from fractions import gcd
import random
from scipy import optimize
import numpy


def v_dijkstra(snum, c):
    return snum*(3+2*c)-2*c**2


def e_dijkstra(snum, c):
    return snum*(1+c)-c**2


def maybe_e_dijkstra(snum, c):
    return snum*(1+c)-c**2


def tc_dijkstra(v):
    return v**2


def tc_dijkstra_2heap(v, e):
    return (e + v) * log(v)


def tc_dijkstra_fheap(v, e):
    return e + v * log(v)


def tc_bfs(v):
    return v


def lcm(array):
    num = array[0]
    for i in array[1:]:
        num = num*i/gcd(num, i)
    return num


def get_fit_dijk_xval(xval, yval):
    # 計測された処理時間はほぼ最短経路探索処理に依存
    # tc_dijkstra(snum) * turn>=5での平均実行回数(19.25) * (1+initial_phaseずらし回数)
    def fit(x, a, b):
        return a * (x**2) + b
    xcur = optimize.curve_fit(fit, xval, yval)
    fitxval = []
    for x in xval:
        fitxval.append(fit(x, xcur[0][0], xcur[0][1]))
    print(str(xcur[0][0]) + " x^2 " + str(xcur[0][1]))
    return numpy.array(fitxval)


def ave_number_of_executions(turn):
    # 連続実行回数=turnのとき、initial_phase=0でtrueになる場合の最短経路探索回数
    # turnが十分大きいケース(tsl=60)だと平均19.25
    # turn=5だとせいぜい10.5回程度
    periods = [2, 3, 4, 5]
    number_of_executions = []
    for i in range(100):
        array = []
        tmp = []
        for t in range(1, turn+1):
            period = random.choice(periods)
            array.append(period)
            tmp.append(lcm(array)/period)
        number_of_executions.append(tmp)
    eachturn = []
    for i in range(turn):
        eachturn.append([])
    for noe in number_of_executions:
        for i in range(turn):
            eachturn[i].append(noe[i])
    for et in eachturn:
        print(1.0*sum(et)/len(et))


if __name__ == '__main__':
    snum = 100
    c = 5
    v = v_dijkstra(snum, c)
    e = e_dijkstra(snum, c)
    maybe_e = maybe_e_dijkstra(snum, c)
    print("real: ")
    print(tc_dijkstra(v))
    # print(tc_dijkstra_2heap(v, e))
    # print(tc_dijkstra_fheap(v, e))
    # print(tc_bfs(v))
    print("maybe: ")
    print(tc_dijkstra(snum))
    # print(tc_dijkstra_2heap(snum, maybe_e))
    # print(tc_dijkstra_fheap(snum, maybe_e))
    # print(tc_bfs(snum))
    ave_number_of_executions(5)
    get_fit_dijk_xval([1, 2, 3, 4, 5], [1.0, 2.723, 5.326, 8.192, 10.687])
