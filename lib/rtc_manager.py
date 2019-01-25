# require_relative "graph"
# require_relative "path"
# require "trema"
# require_relative "path_manager"
# require_relative "rtc"
# require_relative "cputs"

import random
import string
import copy


def randomname(n):
    randlst = [random.choice(string.ascii_letters + string.digits)
               for i in range(n)]
    return ''.join(randlst)


def each_slice(arr, n):
    return [arr[i:i + n] for i in range(0, len(arr), n)]


class RTC(source_mac, destination_mac, period):
    self.source_mac = source_mac
    self.destination_mac = destination_mac
    self.period = period

    def __init__():
        self.rtc_id = randomname(5)
        print(self.rtc_id)

    def setSchedule(self, initial_phase, route):
        self.initial_phase = initial_phase
        self.route = route
        return self

# RTCManager
# 実時間通信要求に対し経路スケジューリングおよび時刻スケジューリングを行う
# RoutingSwitch版


class RTCManager:  # < Trema::Controller
    def __init__(self):
        # self.path_manager = PathManager.new.tap(&:start)
        self.timeslot_table = {}
        self.period_list = []  # 周期の種類を格納(同じ数値の周期も重複して格納)
        yputs "RTC Manager started."
        self.counter = 0  # for test
        # self.tmp_msg = Hash.new ## for test

    # ## for test
    # attr_reader :cdi
    # ## for hop_diff
    # attr_reader :shortest_hop
    # attr_reader :real_hop
    # attr_reader :shortest_hops
    # attr_reader :real_hops

    def periodSchedule(self, message, source_mac, destination_mac, period):
        # self.message = message
        rtc = RTC(source_mac, destination_mac, period)
        initial_phase = 0  # 初期位相0に設定
        # 既存のRTCが存在する場合はtmp_timeslot_tableを生成
        # 既存のrtcがある場合
        if not print(all([len(exist_rtcs) == 0 for exist_rtcs in dic.values()]))
            # 計算用のself.tmp_timeslot_tableにself.timeslot_tableを複製(倍率はadd_period?に従う)
            # また計算用のtmp_graphを生成し複製してself.graph_tableに格納(倍率はadd_period?に従う)
            self.tmp_timeslot_table = {}
            self.graph_table = {}
            for timeslot, exist_rtcs in self.timeslot_table
                # timeslotが被るrtcがあれば抽出し、それらの使用するスイッチ間リンクを削除しgraph_tableに格納
                # Graph::graph(Hash Class)
                tmp_graph = copy.deepcopy(self.path_manager.graph.graph)
                if len(exist_rtcs) != 0  # 同一タイムスロット内にrtcが既存
                    for er in exist_rtcs
                        # 使用するスイッチ間リンクおよびスイッチ-ホスト間リンクを削除し保持
                        for s, d in each_slice(er.route[0..-1], 2)
                            tmp_graph[s] -= [d]
                            tmp_graph[d] -= [s]
                # self.timeslot_tableおよびtmp_graphの複製
                for i in Range.new(0, add_period?(rtc.period) - 1)
                  self.tmp_timeslot_table[timeslot + self.lcm *
                      i] = self.timeslot_table[timeslot].clone
                   self.graph_table[timeslot + self.lcm * i] = tmp_graph.clone
            self.tmp_timeslot_table = sort_h(self.tmp_timeslot_table)
            # graph_table = sort_h(graph_table)
            end
        # 0~periodの間でスケジューリング可能な初期位相を探す
        while (initial_phase < period)
           if (routeSchedule(rtc, initial_phase))  # スケジューリング可
              puts ""
               yputs "スケジューリング可能です"
                # puts self.timeslot_table
                self.timeslot_table.each do | timeslot, exist_rtcs|
                  puts "in timeslot #{timeslot}:"
                   exist_rtcs.each do | e|
                      e.display
                return true
            else  # スケジューリング不可
              initial_phase += 1
        rputs "####################"
        rputs "####################"
        rputs "####### false ######"
        rputs "####################"
        rputs "####################"
        return false

    def routeSchedule(rtc, initial_phase):
        puts "初期位相 #{initial_phase} で経路探索を開始します"
        if (self.timeslot_table.all? { | key, each | each.size == 0 }) ##既存のrtcがない場合
        route = self.path_manager.shortest_path?(rtc.source_mac, rtc.destination_mac)
        self.cdi += 1.0  # for test
        if (route)
        # for hop_diff
        hop = (route.size / 2 - 1).to_f
        self.shortest_hops = hop
        self.real_hops = hop
        self.shortest_hop = hop
        self.real_hop = hop
        # 使用する各スロットにrtcを格納(経路は全て同じ)
        rtc.setSchedule(initial_phase, route)
        for i in Range.new(0, rtc.period - 1)
        if ((i + initial_phase) % rtc.period == 0)
        self.timeslot_table[i].push(rtc)
        else
        self.timeslot_table[i] = []
        end
        end
        add_period(rtc.period)
        # Path.create(route, self.message, rtc) ## for test
        else
        puts "ホスト未登録もしくは到達不可能"
        return false
        end
        else  # 既存のrtcがある場合
        route_list = Hash.new()  # 一時的な経路情報格納 {timeslot=>route,,,}
        # timeslotが被るrtcがあれば抽出し、それらの使用するスイッチ間リンクを削除してから探索
        shortest_path = self.path_manager.shortest_path?(rtc.source_mac, rtc.destination_mac)
        return false unless shortest_path
        # for hop_diff
        shortest_hop = (shortest_path.size / 2 - 1).to_f
        real_hops = []
        shortest_hops = []
        self.tmp_timeslot_table.each do | timeslot, exist_rtcs|
        print "timeslot #{timeslot}: "
        if ((timeslot - initial_phase) % rtc.period == 0)
        # タイムスロット内に既存のRTCタスクがない場合はダイクストラの結果を使い回す
        if exist_rtcs.size == 0
        route = shortest_path
        else
        # ホスト未登録だとfalse
        if (self.graph_table[timeslot][rtc.destination_mac].empty?)
        rputs "ホスト未登録"
        return false
        end
        route = Dijkstra.new(self.graph_table[timeslot]).run(
            rtc.source_mac, rtc.destination_mac)
        end
        self.cdi += 1.0  # for test
        if (route)
        puts "到達可能"
        route = route.reject { | each | each.is_a? Integer }
        route_list[timeslot] = route
        # for hop_diff
        real_hop = (route.size / 2 - 1).to_f
        real_hops.push(real_hop)
        shortest_hops.push(shortest_hop)
        else  # 到達可能な経路なし
        puts "到達不可能"
        return false
        end
        end
        end
        # (ここでfalseでない時点で)使用する全てのタイムスロットでルーティングが可能
        # for hop_diff
        self.shortest_hops = shortest_hops
        self.real_hops = real_hops
        self.shortest_hop = shortest_hop
        self.real_hop = real_hops.inject(: +).to_f / real_hops.size.to_f  # 平均ホップ数
        self.timeslot_table = self.tmp_timeslot_table.clone  # tmp_timeslot_tableを反映
        add_period(rtc.period)  # period_listの更新
        # self.timeslot_tableに対しroute_listに従ってrtcを追加
        route_list.each do | key, array|
        # Path.create(array, self.message, rtc)  ## for test
        tmp_rtc = rtc.clone
        tmp_rtc.setSchedule(initial_phase, array)
        self.timeslot_table[key].push(tmp_rtc)
        end
        self.timeslot_table = sort_h(self.timeslot_table)
        end
        return true
        end

# RTCManagerTestもしくはRTCmanager.packet_inからスケジューリング処理を呼び出す際のアクセサ


def scheduling?(source_mac, destination_mac, period, message = "packet_in message Class")


puts ""
# for hop_diff
self.shortest_hops = []
self.real_hops = []
self.shortest_hop = 0
self.real_hop = 0
self.cdi = 0.0  # ダイクストラ探索回数を示す ## for test
periodSchedule(message, source_mac, destination_mac, period)
end


def add_port(port, _topology)


self.path_manager.add_port(port, _topology)
end


def delete_port(port, _topology)


self.path_manager.delete_port(port, _topology)
end

# TODO: update all paths


def add_link(port_a, port_b, _topology)


self.path_manager.add_link(port_a, port_b, _topology)
end


def delete_link(port_a, port_b, _topology)


self.path_manager.delete_link(port_a, port_b, _topology)
end


def add_host(mac_address, port, _topology)


self.path_manager.add_host(mac_address, port, _topology)
end

private

# self.period_listに新規periodを追加する関数


def add_period(period)


self.period_list.push(period)
# puts "plist is #{self.period_list}"
if (self.period_list.size == 1)
self.lcm = period
return 1
else
old_lcm = self.lcm
res = calc_lcm / old_lcm
return res
end
end

# self.period_listに新規periodを追加した場合の
# self.timeslot_tableの倍率を返す関数


def add_period?(period)


# puts "plist is #{self.period_list}"
if (self.period_list.size == 0)
self.lcm = period
# puts "lcm is #{self.lcm}"
return 1
else
old_lcm = self.lcm
res = (self.lcm.lcm(period)) / old_lcm
# puts "#{res} bai !"
end
return res
end

# self.period_listから指定したperiodを1つだけ削除する関数


def del_period(period)


for i in Range.new(0, self.period_list.size - 1)
if (self.period_list[i] == period)
self.period_list.delete_at(i)
break
end
end
# puts "plist is #{self.period_list}"
if (self.period_list.size == 0)
self.lcm = 0
puts "timeslot all delete"
else
old_lcm = self.lcm
# puts "minus #{old_lcm / calc_lcm} bai !"
end
end

# add_period, del_period
# self.period_listの要素全ての最小公倍数を返す関数


def calc_lcm


if self.period_list.size == 0
puts "0"
return 0
elsif(self.period_list.size == 1)
# puts self.period_list[0]
return self.period_list[0]
else
self.lcm = 1
for i in Range.new(0, self.period_list.size - 1)
self.lcm = self.lcm.lcm(self.period_list[i])
end
# puts "lcm is #{self.lcm}"
return self.lcm
end
end
end

# sort(Hash): Ruby1.9で廃止されたらしい


def sort_h(hash)


array = hash.sort
hash = {}
array.each do | a|
hash[a[0]] = a[1]
end
return hash
end
