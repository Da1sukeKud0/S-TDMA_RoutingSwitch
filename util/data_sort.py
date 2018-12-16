#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import numpy
from matplotlib import pyplot
# from matplotlib.font_manager import FontProperties
# fp = FontProperties(fname = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf")


class JsonHelper:
    def __init__(self, file_name):
        with open(file_name) as f:
            self.dics = json.load(f)
            # print(self.dics)

    # sortbyの要素毎に処理時間の平均値を算出
    def sort_by(self, sortby):
        print("")
        print("each: " + sortby)
        result = {}
        for d in self.dics:
            if not (d["tf"]):
                continue
            if (d[sortby] not in result):
                result[d[sortby]] = []
            result[d[sortby]].append(d["time"])
        self.__ave(result)

    def __ave(self, dic):
        xval = []
        yval = []
        for k, v in sorted(dic.items(), key=lambda x: x[0]):
            ave = sum(v)/len(v)
            print("key: " + str(k) + ", ave: " + str(ave))
            xval.append(k)
            yval.append(ave)
        pyplot.plot(xval, yval, "o")
        pyplot.ylabel(u'during time [s]')  # , fontproperties=fp)
        pyplot.xlabel(u'xlabel')  # , fontproperties=fp)
        # pyplot.xticks(
        # [1.25, 2.25], [u'目盛りは', 'fontproperties=fp'], fontproperties=fp)
        # pyplot.title(u'タイトルはfontproperties=fp', fontproperties=fp)
        pyplot.show()
        # pyplot.savefig("tmp.png")


if __name__ == '__main__':
    jh = JsonHelper("test/rtcm_test_s5to100_c1to5_rtcr5.json")
    jh.sort_by("turn")
    jh.sort_by("snum")
    jh.sort_by("cplx")
    jh.sort_by("lnum")

"""
取得したデータは配列内dict
dictのkey, valの内訳は以下
r.store("type", @type) ## トポロジタイプ
r.store("snum", @switchNum) ## スイッチ数
r.store("rnum", num) ## RTC数
r.store("lnum", @edges.size) ## リンク数(switchNum-complexity)*complexityで算出可能
r.store("turn", n) ## RTC実行順
r.store("time", time) ## 処理時間
r.store("tf", tf) ## add_rtc?
result.push(r)
if (@type == "BA")
    r.store("cplx", @complexity) ## 複雑度
elsif (@type == "tree")
    r.store("dep", @depth) ## 深さ(ホストの階層を含む)
    r.store("fan", @fanout) ## 1つの親ノードに接続する子ノードの数
end
"""
