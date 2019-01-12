#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
import numpy
import matplotlib
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties
fp = FontProperties(
    fname="/usr/share/fonts/truetype/fonts-japanese-gothic.ttf")
matplotlib.rcParams['font.family'] = fp.get_name()
matplotlib.rcParams['pdf.fonttype'] = 42


class JsonHelper:
    def __init__(self, args):
        self.dics = []
        self.mode = args[0]
        for file in args[1:]:
            print("imported file: " + str(file))
            with open(str(file)) as f:
                self.dics.extend(json.load(f))
        print("data size: " + str(len(self.dics)))

    # x軸要素,完全一致条件,凡例を指定して処理時間の平均値を算出
    # ex) jh.sort_by("lnum", subeach="turn", exact={"snum": 100})
    def sort_by(self, target, each, subeach=None, **exact):
        self.target = target
        self.each = each
        self.subeach = subeach
        self.exact = exact
        print("")
        print("target: " + target)
        print("each: " + each)
        print("ExactMatch:" + str(exact))
        print("subeach:" + str(subeach))
        result = {}
        for d in self.dics:
            # falseの結果は除外
            if (target != "tf") and not d["tf"]:
                continue
            # ExactMatch
            if not self.__exactMatch(d):
                continue
            # resultに処理時間を格納
            if subeach is None:
                if d[each] not in result.keys():
                    result[d[each]] = []
                result[d[each]].append(self.__getValue(target, d))
            else:
                if d[subeach] not in result.keys():
                    result[d[subeach]] = {}
                if d[each] not in result[d[subeach]].keys():
                    result[d[subeach]][d[each]] = []
                result[d[subeach]][d[each]].append(self.__getValue(target, d))
        if subeach is None:
            self.__ave(result, each)
        else:
            ctr = 0
            plots = []
            for key, val in result.items():
                plots.append(self.__ave(val, each, False,
                                        "C{}".format(ctr), key))
                ctr += 1
            pyplot.close()

    def __getValue(self, target, d):
        if target == "time":
            return d["time"]
        elif target == "hop":
            return d["rhop"] - d["shop"]
        elif target == "tf":
            if d["tf"]:
                r = 100.0
            else:
                r = 0.0
            return r

    def __exactMatch(self, target):
        for key, val in self.exact.items():
            if not (target[str(key)] == int(val)):
                return False
        return True

    def __ave(self, dic, each, close=True, color="C{}".format(0), label=None):
        xval = []
        yval = []
        err = []
        errmin = []
        errmax = []
        for k, v in sorted(dic.items(), key=lambda x: x[0]):
            ave = sum(v)/len(v)
            print("key: " + str(k) + ", ave: " + str(ave))
            xval.append(k)
            yval.append(ave)
            # err.append(self.__calculate_std(v))
            # err.append(self.__calculate_maxmin(v))
            errmin.append(ave - min(v))
            errmax.append(max(v) - ave)
        err.append(errmin)
        err.append(errmax)
        if self.target == "tf":
            #plot = pyplot.bar(xval, yval, yerr=err, color=color, label=label)
            plot = pyplot.bar(xval, yval)
        else:
            #pyplot.errorbar(xval, yval, yerr=err,
            #                fmt="none", ecolor="lightgray")
            plot = pyplot.plot(xval, yval, self.plotmode,
                               markersize=4, color=color, label=label, marker="o")
        if self.subeach is not None:
            pyplot.legend(title=self.__getLabel(
                self.subeach), prop=fp)
        pyplot.ylabel(self.__getLabel(self.target), fontproperties=fp)
        pyplot.xlabel(self.__getLabel(each), fontproperties=fp)
        # pyplot.xticks(
        # [1.25, 2.25], [u'目盛りは', 'fontproperties=fp'], fontproperties=fp)
        # pyplot.title(u'タイトルはfontproperties=fp', fontproperties=fp)
        # pyplot.show()
        if close:
            pyplot.savefig("tmp/" + str(self.target) + "__" +
                           str(self.each) + self.__exact_to_s() + self.filetail + "." + self.mode)
            pyplot.close()
        else:
            pyplot.savefig("tmp/" + str(self.target) + "__" + str(self.each) +
                           "_" + str(self.subeach) + self.__exact_to_s() + self.filetail + "." + self.mode)
        return plot

    def __exact_to_s(self):
        if len(self.exact) == 0:
            s = ""
        else:
            s = "("
            for k, v in self.exact.items():
                s += str(k) + str(v)
            s += ")"
        return s

    def __getLabel(self, each):
        labels = {
            "snum": u"ネットワーク内に存在するOpenFlowスイッチの数",
            "rnum": u"入力された実時間通信要求の数",
            "lnum": u"ネットワーク内に存在するリンクの数",
            "turn": u"実時間通信要求の入力順",
            "cplx": u"BAモデルに基づくスケールフリーネットワークの複雑度",
            "dep": u"ツリートポロジの深さ",
            "fan": u"単一の親ノードに接続された子ノードの数",
            "time": u"スケジューリング処理に要した時間 [s]",
            "hop": u"通信毎の平均増加ホップ数",
            "hops": u"通信毎の累計増加ホップ数",
            "tf": u"スケジューリング可能率"
        }
        return labels.get(each, u"unknown")

    def getFlatAve(self):
        result = {}
        result["all"] = []
        for d in self.dics:
            if (d["snum"] > 100):
                continue
            result["all"].append(d["time"])
        print("")
        print("during time(ave): " + str(sum(result["all"])/len(result["all"])))

    def oresenplot(self):
        self.plotmode = ""
        self.filetail = "_ore"

    def dotplot(self):
        self.plotmode = "o"
        self.filetail = ""

    def getFlatTF(self):
        result = {}
        result["all"] = []
        for d in self.dics:
            if d["tf"]:
                result["all"].append(100.0)
            else:
                result["all"].append(0.0)
        print("")
        print("scheduling True(%): " + str(sum(result["all"])/len(result["all"])))

    # 平均からの偏差を求める
    def __find_difference(self, array):
        mean = sum(array)/len(array)
        diff = []
        for num in array:
            diff.append(num-mean)
        return diff

    # 標準偏差を求める
    def __calculate_std(self, array):
        diff = self.__find_difference(array)
        # 差の２乗を求める
        squared_diff = []
        for d in diff:
            squared_diff.append(d**2)
        # 分散を求める
        sum_squared_diff = sum(squared_diff)
        # return sum_squared_diff
        return (sum_squared_diff/len(array))**0.5


if __name__ == '__main__':
    args = sys.argv
    if (len(args) < 3) or ((args[1] != "png") and (args[1] != "pdf")):
        print 'usage: output_mode(pdf or png or show) *.py file1 (file2 file3...)'
        quit()
    jh = JsonHelper(args[1:])
    jh.getFlatAve()
    jh.getFlatTF()
    # jh.dotplot()
    # jh.sort_by("tf", "snum")

    #topo = "BA"
    topo = "tree"
    # topo = "no"
    if topo == "BA":
        # dot mode
        jh.dotplot()
        jh.sort_by("time", "turn")
        jh.sort_by("time", "turn", None, snum=100, cplx=2)
        jh.sort_by("time", "snum")
        jh.sort_by("time", "snum", None, cplx=2)
        jh.sort_by("time", "lnum")
        jh.sort_by("time", "lnum", "turn", snum=100)
        jh.sort_by("time", "cplx")

        jh.sort_by("hop", "turn")
        jh.sort_by("hop", "turn", None, snum=100, cplx=2)
        jh.sort_by("hop", "snum")
        jh.sort_by("hop", "snum", None, cplx=2)
        jh.sort_by("hop", "lnum")
        jh.sort_by("hop", "lnum", "turn", snum=100)  # oresen
        jh.sort_by("hop", "cplx")

        jh.sort_by("hop", "snum", "turn", cplx=2)  # oresen
        jh.sort_by("hop", "cplx", None, snum=100)

        # oresen mode
        jh.oresenplot()
        jh.sort_by("hop", "lnum", "turn", snum=100)  # oresen
        jh.sort_by("hop", "snum", "turn", cplx=2)  # oresen
    elif topo == "tree":
        # for tree(増加ホップ数は必ず0)
        # lnumとsnumがほぼ同義
        # dot mode
        jh.dotplot()
        jh.sort_by("time", "turn")
        jh.sort_by("time", "snum")
        jh.sort_by("time", "snum", "fan")
        jh.sort_by("time", "dep")
        jh.sort_by("time", "dep", fan=2)
        jh.sort_by("time", "dep", fan=3)
        jh.sort_by("time", "fan")
        jh.sort_by("tf", "snum")
        # oresen mode
        jh.oresenplot()


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
