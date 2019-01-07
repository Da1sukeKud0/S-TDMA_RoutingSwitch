#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
import numpy
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties
fp = FontProperties(
    fname="/usr/share/fonts/truetype/fonts-japanese-gothic.ttf")


class JsonHelper:
    def __init__(self, *args):
        # self.file_name = file_name
        self.dics = []
        for files in args:
            for file in files:
                print("imported file: " + str(file))
                with open(str(file)) as f:
                    self.dics.extend(json.load(f))

    # x軸要素,完全一致条件,凡例を指定して処理時間の平均値を算出
    # ex) jh.sort_by("lnum", subeach="turn", exact={"snum": 100})
    def sort_by(self, each, subeach=None, **exact):
        print("")
        print("each: " + each)
        print("ExactMatch:" + str(exact))
        print("subeach:" + str(subeach))
        result = {}
        for d in self.dics:
            # falseの結果は除外
            if not (d["tf"]):
                continue
            # ExactMatch
            if not self.__exactMatch(d, exact):
                continue
            # resultに処理時間を格納
            if (subeach is None):
                if (d[each] not in result.keys()):
                    result[d[each]] = []
                result[d[each]].append(d["time"])
            else:
                if (d[subeach] not in result.keys()):
                    result[d[subeach]] = {}
                if (d[each] not in result[d[subeach]].keys()):
                    result[d[subeach]][d[each]] = []
                result[d[subeach]][d[each]].append(d["time"])
        if (subeach is None):
            self.__ave(result, each)
        else:
            ctr = 0
            for key, val in result.items():
                for k, v in val.items():
                    self.__ave(val, each, close=False, color="C{}".format(ctr))
                ctr += 1
            pyplot.close()

    def __exactMatch(self, target, pattern):
        if pattern is None:
            return True
        for key, val in pattern.items():
            for k, v in val.items():
                if not (target[str(k)] == int(v)):
                    return False
        return True

    def __ave(self, dic, each, close=True, color="C{}".format(0)):
        xval = []
        yval = []
        for k, v in sorted(dic.items(), key=lambda x: x[0]):
            ave = sum(v)/len(v)
            print("key: " + str(k) + ", ave: " + str(ave))
            xval.append(k)
            yval.append(ave)
        pyplot.plot(xval, yval, "o", color=color)
        pyplot.ylabel(u'スケジューリング処理に要した時間 [s]', fontproperties=fp)
        pyplot.xlabel(self.__getLabel(each), fontproperties=fp)
        # pyplot.xticks(
        # [1.25, 2.25], [u'目盛りは', 'fontproperties=fp'], fontproperties=fp)
        # pyplot.title(u'タイトルはfontproperties=fp', fontproperties=fp)
        # pyplot.show()
        if close:
            pyplot.savefig("tmp/" + str(each) + ".png")
            pyplot.close()
        else:
            pyplot.savefig("tmp/" + str(each) + "_subeach" + ".png")

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
            if (d["snum"] > 100):
                continue
            result["all"].append(d["time"])
        print("")
        print("all average: " + str(sum(result["all"])/len(result["all"])))
        print("")


if __name__ == '__main__':
    args = sys.argv
    if (len(args) == 1):
        print 'usage: *.py file1 (file2 file3...)'
        quit()
    jh = JsonHelper(args[1:len(args)])
    jh.sort_by("turn")
    jh.sort_by("snum")
    jh.sort_by("cplx")
    jh.sort_by("lnum")
    # jh.sort_by("lnum", subeach="turn", exact={"snum": 100})
    # jh.sort_by("turn", subeach=None, exact={"snum": 100, "cplx": 2})
    # jh.sort_by("snum", subeach=None, exact={"cplx": 2})
    jh.getFlatAve()

"""
取得したデータは配列内dict形式。内訳は以下
# 結果出力に用いる各種情報
def save_tag
    @tagList = Hash.new ## データのタグリスト(rtcの実行順(turn)を除く)
    @tagList.store("type", @type) ## トポロジタイプ
    @tagList.store("snum", @numOfSwitch) ## スイッチ数
    @tagList.store("rnum", @numOfReq) ## RTC要求数
    # リンク数(switchNum-complexity)*complexityで算出可能
    @tagList.store("lnum", @edges.size)
    if (@type == "BA")
        @tagList.store("cplx", @complexity) ## 複雑度
    elsif (@type == "tree")
        @tagList.store("dep", @depth)
        @tagList.store("fan", @fanout)
    end
end
# 計測結果をresultに格納
    r = @tagList.clone
    r.store("turn", n) ## RTC実行順
    r.store("time", time) ## 処理時間
    r.store("tf", tf) ## add_rtc?
"""
