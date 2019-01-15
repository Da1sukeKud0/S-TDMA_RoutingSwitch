#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import log
from math import factorial


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


def ave_number_of_executions():
    # rtcの数が十分大きいケース向け
    # tsl=5,turn=5の時は平均19.25
    periods = [2.0, 3.0, 4.0, 5.0]
    tsls = [2.0, 3.0, 4.0, 5.0, 6.0, 10.0, 12.0, 15.0, 20.0, 60.0]
    tmp = []
    for p in periods:
        for tsl in tsls:
            tmp.append(tsl/p)


if __name__ == '__main__':
    snum = 100
    c = 2
    v = v_dijkstra(snum, c)
    e = e_dijkstra(snum, c)
    maybe_e = maybe_e_dijkstra(snum, c)
    print("real: ")
    print(tc_dijkstra(v))
    print(tc_dijkstra_2heap(v, e))
    print(tc_dijkstra_fheap(v, e))
    print(tc_bfs(v))
    print("maybe: ")
    print(tc_dijkstra(snum))
    print(tc_dijkstra_2heap(snum, maybe_e))
    print(tc_dijkstra_fheap(snum, maybe_e))
    print(tc_bfs(snum))
    print(tc_dijkstra(snum))
