#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
import numpy
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties
fp = FontProperties(fname = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf")


class JsonHelper:
    def __init__(self, file_name):
        self.file_name = file_name
        with open(file_name) as f:
            self.dics = json.load(f)

    # ソート要素、条件毎に処理時間の平均値を算出
    # ex) sort_by("turn", snum=100)
    def sort_by(self, sortkey, **kwargs):
        print("")
        print("each: " + sortkey)
        print("ExactMatch:" + str(kwargs))
        result = {}
        for d in self.dics:
            # falseの結果は除外
            if not (d["tf"]):
                continue
            # ExactMatch
            if not self.__exactMatch(d, kwargs):
                continue
            # resultに処理時間を格納
            if (d[sortkey] not in result):
                result[d[sortkey]] = []
            result[d[sortkey]].append(d["time"])
        self.__ave(result, sortkey)

    def __exactMatch(self, target, pattern):
        for k, v in pattern.items():
            if not (target[str(k)] == int(v)):
                return False
        return True

    def __ave(self, dic, sortby="all"):
        xval = []
        yval = []
        for k, v in sorted(dic.items(), key=lambda x: x[0]):
            ave = sum(v)/len(v)
            print("key: " + str(k) + ", ave: " + str(ave))
            xval.append(k)
            yval.append(ave)
        pyplot.plot(xval, yval, "o")
        pyplot.ylabel(u'スケジューリング処理に要した時間 [s]', fontproperties=fp)
        pyplot.xlabel(self.__getLabel(sortby), fontproperties=fp)
        # pyplot.xticks(
        # [1.25, 2.25], [u'目盛りは', 'fontproperties=fp'], fontproperties=fp)
        # pyplot.title(u'タイトルはfontproperties=fp', fontproperties=fp)
        pyplot.show()
        # pyplot.savefig("tmp.png")

    def __getLabel(self, key):
        labels = {
            "snum": u"ネットワーク内に存在するOpenFlowスイッチの数",
            "rnum": u"システムに入力された実時間要求の数",
            "lnum": u"ネットワーク内に存在するリンクの数",
            "turn": u"システムへの実時間通信要求の入力順",
            "cplx": u"BAモデルに基づくスケールフリーネットワークの混雑度"
        }
        return labels.get(key, "unknown")

    def getFlatAve(self):
        result = {}
        result["all"] = []
        for d in self.dics:
            result["all"].append(d["time"])
        print("")
        print("all average: " + str(sum(result["all"])/len(result["all"])))
        print("")


if __name__ == '__main__':
    args = sys.argv
    if (len(args) != 2):
        print 'usage: *.py file_name'
        quit()
    jh = JsonHelper(str(args[1]))
    jh.sort_by("turn", snum=100)
    jh.sort_by("snum")
    jh.sort_by("cplx")
    jh.sort_by("lnum")
    jh.getFlatAve()

"""
取得したデータは配列内dict形式。内訳は以下
## 結果出力に用いる各種情報
def save_tag
    @tagList = Hash.new ## データのタグリスト(rtcの実行順(turn)を除く)
    @tagList.store("type", @type) ## トポロジタイプ
    @tagList.store("snum", @numOfSwitch) ## スイッチ数
    @tagList.store("rnum", @numOfReq) ## RTC要求数
    @tagList.store("lnum", @edges.size) ## リンク数(switchNum-complexity)*complexityで算出可能
    if (@type == "BA")
        @tagList.store("cplx", @complexity) ## 複雑度
    elsif (@type == "tree")
        @tagList.store("dep", @depth)
        @tagList.store("fan", @fanout)
    end
end
## 計測結果をresultに格納
    r = @tagList.clone
    r.store("turn", n) ## RTC実行順
    r.store("time", time) ## 処理時間
    r.store("tf", tf) ## add_rtc?
"""
