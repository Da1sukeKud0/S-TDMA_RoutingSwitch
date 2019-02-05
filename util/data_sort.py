#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
import numpy
from scipy import optimize
import matplotlib
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties
fp = FontProperties(
    fname="/usr/share/fonts/truetype/fonts-japanese-gothic.ttf")
matplotlib.rcParams['font.family'] = fp.get_name()
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['font.size'] = 14


class JsonHelper:
    def __init__(self, args):
        self.dics = []
        self.format = args[0]
        self.dotplot()  # default
        for file in args[1:]:
            print("imported file: " + str(file))
            with open(str(file)) as f:
                self.dics.extend(json.load(f))
        print("data size: " + str(len(self.dics)))
        self.topotype = self.get_topotype()

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
        print("subeach:" + str(subeach))
        print("ExactMatch:" + str(exact))
        result = {}
        for d in self.dics:
            # falseの結果は除外
            if (target != "tf") and not d["tf"]:
                continue
            # ExactMatch
            if not self.__exactMatch(d):
                continue
            if (each == "v_dijk"):
                d[each] = self.__getValue("v_dijk", d)
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
            self.__ave(result)
        else:
            ctr = 0
            plots = []
            for key, val in result.items():
                plots.append(self.__ave(val, False, ctr, key))
                ctr += 1
            pyplot.close()

    def __getValue(self, target, d):
        if target == "time":
            return d["time"]
        elif target == "hop":
            return d["rhop"] - d["shop"]
        elif target == "hops":
            if type(d["rhops"]) is float:
                hops = d["rhops"] - d["shops"]
            elif type(d["rhops"]) is list:
                hops = sum(d["rhops"]) - sum(d["shops"])
            else:
                print("error")
                quit()
            return hops
        elif target == "cdi":
            return d["cdi"]
        elif target == "tf":
            if d["tf"]:
                r = 100.0
            else:
                r = 0.0
            return r
        elif target == "v_dijk":
            return self.v_dijkstra(d["snum"], d["cplx"])

    def __exactMatch(self, target):
        for key, val in self.exact.items():
            if not (target[str(key)] == int(val)):
                return False
        return True

    def __ave(self, dic, close=True, ctr=0, label=None):
        color = "C{}".format(ctr)
        xval = []
        yval = []
        # エラーバー
        stderr = []
        errmin = []
        errmax = []
        # 平均値化
        for k, v in sorted(dic.items(), key=lambda x: x[0]):
            ave = sum(v)/len(v)
            print("key: " + str(k) + ", ave: " + str(ave))
            xval.append(k)
            yval.append(ave)
            stderr.append(self.__calculate_std(v))
            errmin.append(ave - min(v))
            errmax.append(max(v) - ave)
        maxminerr = [errmin, errmax]
        # 棒グラフ・点グラフ・エラーバーの設定
        if self.target == "tf":
            # plot = pyplot.bar(xval, yval, yerr=err, color=color, label=label)
            # plot = pyplot.bar(xval, yval)
            # plot = pyplot.bar(map(lambda x: x+ctr*0.5, xval), yval)
            plot = pyplot.plot(xval, yval, "",
                               markersize=3, color=color, label=label, marker="o")
            # pyplot.yticks([0, 20, 40, 60, 80, 100])
            # pyplot.yticks([50, 60, 70, 80, 90, 100])
            # pyplot.yticks(range(80, 101, 2))
        else:
            # pyplot.errorbar(xval, yval, yerr=maxminerr,
                            # fmt="none", ecolor="lightgray")
            yval2 = [sum(yval[:i]) for i in range(len(yval))]
            plot = pyplot.plot(xval, yval, self.plotmode,
                               markersize=3, color=color, label=label, marker="o")
            xval = xval[1:]
            yval = yval[1:]
            # xval = [self.v_dijkstra(
            #     xval[i], label) for i in range(len(xval))]
            # plot = pyplot.plot(xval, yval, self.plotmode,
            #                    markersize=3, color=color, label=label, marker="o")
            if (self.target == "cdi"):
                pass
            # pyplot.yticks(range(0, 20, 2))
        plot = pyplot.plot(xval, yval)
        # plot = pyplot.plot(xval, self.__get_fit_ave_xval(xval, yval))
        # plot = pyplot.plot(xval, self.__get_fit_1d_xval(xval, yval))
        # plot = pyplot.plot(xval, self.__get_fit_2d_xval(xval, yval))
        # plot = pyplot.plot(xval, self.__get_fit_3d_xval(xval, yval))
        # plot = pyplot.plot(xval, self.__get_fit_dijk_xval(xval, yval))
        # 凡例の設定
        if self.subeach is not None:
            pyplot.legend(title=self.__getLabel(
                self.subeach), prop=fp, ncol=2)  # , loc="upper left")
        # ラベルの設定
        pyplot.ylabel(self.__getLabel(self.target),
                      fontproperties=fp, fontsize="larger")
        pyplot.xlabel(self.__getLabel(self.each),
                      fontproperties=fp, fontsize="larger")
        # x,y軸メモリの個別設定
        if (self.each == "lnum") and (len(xval) >= 10):
            pass
        elif (self.each == "snum") and ((len(xval) >= 10) or (self.get_topotype() == "tree")):
            pass
        elif (self.each == "v_dijk"):
            pass
        elif (self.get_topotype() == "tree") and (self.target == "time"):
            if (self.each == "turn"):
                pyplot.yticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5])
            elif (self.each == "cdi"):
                pyplot.yticks([int(x) for x in range(0, 20, 2)])
            elif (self.each == "lnum"):
                # pyplot.xticks(range(50, 251, 50))
                pass
        else:
            pyplot.xticks(xval)  # , fontsize="x-large")
        # pyplot.xticks(range(1, 6))
        # png, pdf(, show)
        # if self.format == "show":
        #     if close:
        #         pyplot.show()
        #     return plot
        if close:
            pyplot.savefig("tmp/" + str(self.topotype) + "/" + str(self.target) + "__" +
                           str(self.each) + self.__exact_to_s() + self.filetail + "." + self.format, bbox_inches='tight')
            pyplot.close()
        else:
            pyplot.savefig("tmp/" + str(self.topotype) + "/" + str(self.target) + "__" + str(self.each) + "_" + str(
                self.subeach) + self.__exact_to_s() + self.filetail + "." + self.format, bbox_inches='tight')
        return plot

    def __get_fit_ave_xval(self, xval, yval):
        ave = sum(yval)/len(yval)
        arr = []
        for i in range(10, 101, 5):
            arr.append(ave)
        return arr

    def __get_fit_1d_xval(self, xval, yval):
        def fit(x, a, b):
            return a*x + b
        xcur = optimize.curve_fit(fit, xval, yval)
        fitxval = []
        for x in xval:
            fitxval.append(fit(x, xcur[0][0], xcur[0][1]))
        return numpy.array(fitxval)

    def __get_fit_2d_xval(self, xval, yval):
        def fit(x, a, b, c):
            return a * x**2 + b * x + c
        xcur = optimize.curve_fit(fit, xval, yval)
        fitxval = []
        for x in xval:
            fitxval.append(fit(x, xcur[0][0], xcur[0][1], xcur[0][2]))
        print(str(xcur[0][0]) + " x^2 " +
              str(xcur[0][1]) + " x " + str(xcur[0][2]))
        return numpy.array(fitxval)

    def __get_fit_3d_xval(self, xval, yval):
        def fit(x, a, b, c, d):
            return a * x**3 + b * x**2 + c * x + d
        xcur = optimize.curve_fit(fit, xval, yval)
        fitxval = []
        for x in xval:
            fitxval.append(
                fit(x, xcur[0][0], xcur[0][1], xcur[0][2], xcur[0][3]))
        return numpy.array(fitxval)

    # 計測された処理時間はほぼ最短経路探索処理に依存
    # tc_dijkstra(snum) * turn>=5での平均実行回数(19.25) * (1+initial_phaseずらし回数)
    def __get_fit_dijk_xval(self, xval, yval):
        def fit(x, a, b):
            return a * (x**2) + b
        xcur = optimize.curve_fit(fit, xval, yval)
        fitxval = []
        for x in xval:
            fitxval.append(fit(x, xcur[0][0], xcur[0][1]))
        print(str(xcur[0][0]) + " x^2 " + str(xcur[0][1]))
        return numpy.array(fitxval)

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
            "cplx": u"ランダムネットワークの\n　　　複雑度",
            # "cplx": u"ランダムネットワークの複雑度",
            "dep": u"ツリートポロジの深さ",
            "fan": u"ファンアウト",
            "time": u"平均処理時間 [s]",
            "hop": u"通信毎の平均増加ホップ数",
            "hops": u"通信毎の平均総増加ホップ数",
            "tf": u"スケジューリング可能率 [%]",
            "cdi": u"最短経路探索の平均実行回数",
            "v_dijk": u"ダイクストラ法の最短経路探索におけるノード数"
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
        print("during time(ave): " +
              str(sum(result["all"])/len(result["all"])))

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
        print("scheduling True(%): " +
              str(sum(result["all"])/len(result["all"])))

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

    def get_topotype(self):
        return self.dics[0]["type"]

    def v_dijkstra(self, snum, c):
        return snum*(3+2*c)-2*c**2


if __name__ == '__main__':
    args = sys.argv
    # and (args[1] != "show")):
    if (len(args) < 3) or ((args[1] != "png") and (args[1] != "pdf")):
        print 'usage: output_format(pdf or png or show) *.py file1 (file2 file3...)'
        quit()
    jh = JsonHelper(args[1:])
    jh.getFlatAve()
    jh.getFlatTF()

    time = "time"
    hop = "hop"
    hops = "hops"
    tf = "tf"
    turn = "turn"
    snum = "snum"
    lnum = "lnum"
    cplx = "cplx"
    dep = "dep"
    fan = "fan"
    topo = jh.get_topotype()
    # topo = "else"
    if topo == "BA":
        jh.dotplot()
        # jh.sort_by("time", "snum", "turn")  # ba fit
        # jh.sort_by("time", "lnum", "turn")  # ba fit
        # jh.sort_by("time", "turn", cplx=2, snum=100)  # ba rnum20
        # jh.sort_by("cdi", "turn", cplx=2, snum=100)  # ba rnum20
        # jh.sort_by("hops", "snum", "turn")  # ba
        # jh.sort_by("hop", "snum", "turn")  # ba
        # jh.sort_by("hops", "lnum", "turn")  # ba
        # jh.sort_by("hops", "lnum", "turn", snum=100)  # ba
        # jh.sort_by("hop", "lnum", "turn")  # ba
        jh.sort_by("hops", "cplx", "turn")  # ba

        # jh.sort_by("tf", "snum", "turn")  # ba
        jh.oresenplot()
        # jh.sort_by("tf", "snum", "cplx")  # ba
        # jh.sort_by("tf", "turn", "cplx", snum=100)  # ba rnum20
    elif topo == "tree":
        # for tree(増加ホップ数は必ず0)
        # lnumとsnumがほぼ同義
        # dot mode
        jh.dotplot()
        # jh.sort_by("time", "snum", "turn")  # tree
        # jh.sort_by("time", "turn", snum=121)  # tree
        # jh.sort_by("cdi", "turn", snum=121)  # tree
        # jh.sort_by("time", "turn")
        # jh.sort_by("cdi", "turn")
        # jh.sort_by("time", "turn", snum=259)
        # jh.sort_by("cdi", "turn", snum=259)
        # jh.sort_by("time", "snum", "fan")
        # jh.sort_by("time", "dep")
        # # jh.sort_by("time", "dep", fan=2)
        # # jh.sort_by("time", "dep", fan=3)
        # jh.sort_by("time", "fan")

        # oresen mode
        jh.oresenplot()
        jh.sort_by("tf", "snum", "turn")
        jh.sort_by("tf", "turn", "lnum")
        # jh.sort_by("time", "snum", "turn")  # tree
    else:
        jh.dotplot()
        # jh.sort_by("time", "v_dijk", "turn", cplx=2)  # ba?
        # jh.sort_by("hops", "turn", "lnum")  # ba
        # jh.sort_by("hops", "lnum")  # ba
        # jh.sort_by("hops", "turn")  # ba
        # jh.sort_by("time", "snum", "fan")  # tree
        # jh.sort_by("time", "turn")  # tree
        # jh.sort_by("time", "turn", snum=259)  # tree
        # jh.sort_by("cdi", "turn")  # tree
        # jh.sort_by("cdi", "turn", snum=259)  # tree
        # jh.sort_by("tf", "turn", "snum")  # tree

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
r.store("shop", @rtc_manager.shortest_hop) ## 単純最短経路の平均ホップ数
r.store("rhop", @rtc_manager.real_hop) ## 実際に設定された経路の平均ホップ数
r.store("shops", @rtc_manager.shortest_hops) ## 単純最短経路の累計ホップ数
r.store("rhops", @rtc_manager.real_hops) ## 実際に設定された経路の累計ホップ数
result.push(r)
"""
