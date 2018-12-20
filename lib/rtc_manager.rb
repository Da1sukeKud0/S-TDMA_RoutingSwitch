require "graph"
require "path"
require "trema"
require "path_manager"
require "rtc"
require "cputs"

## RTCManager
## 実時間通信要求に対し経路スケジューリングおよび時刻スケジューリングを行う
## RoutingSwitch版
class RTCManager < Trema::Controller
  def start
    @path_manager = PathManager.new.tap(&:start)
    @timeslot_table = Hash.new { |hash, key| hash[key] = [] } ## {timeslot=>[rtc,rtc,,,], ,,}
    @period_list = [] ## 周期の種類を格納(同じ数値の周期も重複して格納)
    logger.info "RTC Manager started."
    @counter = 0 ## for test
    @tmp_msg = Hash.new ## for test
  end

  def periodSchedule(message, source_mac, destination_mac, period)
    @message = message
    rtc = RTC.new(source_mac, destination_mac, period)
    initial_phase = 0 ##初期位相0に設定
    ## 0~periodの間でスケジューリング可能な初期位相を探す
    while (initial_phase < period)
      if (routeSchedule(rtc, initial_phase)) ##スケジューリング可
        yputs "スケジューリング可能です"
        puts ""
        # puts @timeslot_table
        @timeslot_table.each do |timeslot, exist_rtcs|
          puts "in timeslot: #{timeslot}"
          exist_rtcs.each do |e|
            e.display
          end
        end
        return true
      else ##スケジューリング不可
        initial_phase += 1
      end
    end
    rputs "####################"
    rputs "####################"
    rputs "####### false ######"
    rputs "####################"
    rputs "####################"
    return false
  end

  def routeSchedule(rtc, initial_phase)
    if (@timeslot_table.all? { |key, each| each.size == 0 }) ##既存のrtcがない場合
      route = @path_manager.shortest_path?(rtc.source_mac, rtc.destination_mac)
      if (route) ## 経路あり
        ## 使用する各スロットにrtcを格納(経路は全て同じ)
        rtc.setSchedule(initial_phase, route)
        for i in Range.new(0, rtc.period - 1)
          if ((i + initial_phase) % rtc.period == 0)
            @timeslot_table[i].push(rtc)
          else
            @timeslot_table[i] = []
          end
        end
        add_period(rtc.period)
        Path.create(route, @message, "Exclusive")
      else ## 経路なし
        return false
      end
    else ## 既存のrtcがある場合
      ## 計算用のtmp_timeslot_tableに@timeslot_tableを複製(倍率はadd_period?に従う)
      tmp_timeslot_table = Hash.new { |hash, key| hash[key] = [] }
      @timeslot_table.each do |timeslot, exist_rtcs|
        for i in Range.new(0, add_period?(rtc.period) - 1)
          tmp_timeslot_table[timeslot + @lcm * i] = @timeslot_table[timeslot].clone
        end
      end
      tmp_timeslot_table = sort_h(tmp_timeslot_table)
      route_list = Hash.new() ## 一時的な経路情報格納 {timeslot=>route,,,}
      ## timeslotが被るrtcがあれば抽出し、それらの使用するスイッチ間リンクを削除してから探索
      tmp_timeslot_table.each do |timeslot, exist_rtcs|
        puts "tsl=#{timeslot}"
        if ((timeslot - initial_phase) % rtc.period == 0)
          tmp_graph = @path_manager.graph.graph.clone ## Graph::graph(Hash Class)
          if (exist_rtcs.size != 0) ## 同一タイムスロット内にrtcが既存
            puts "既存のRTCあるよ"
            for er in exist_rtcs
              puts "each_rtc=#{er}"
              er.route[2..-3].each_slice(2) do |s, d| ## 使用するスイッチ間リンクを削除し保持
                # puts "delete link: #{s} to #{d}"
                tmp_graph[s] -= [d]
                tmp_graph[d] -= [s]
              end
            end
          end
          ##
          return false if tmp_graph[rtc.destination_mac].empty? ## ホスト未登録だとfalse
          route = Dijkstra.new(tmp_graph).run(rtc.source_mac, rtc.destination_mac)
          return false unless route ## 到達可能な経路なし
          route_list[timeslot] = route.reject { |each| each.is_a? Integer }
        end
      end
      ## (ここでfalseでない時点で)使用する全てのタイムスロットでルーティングが可能
      @timeslot_table = tmp_timeslot_table.clone ## tmp_timeslot_tableを反映
      add_period(rtc.period) ## period_listの更新
      ## @timeslot_tableに対しroute_listに従ってrtcを追加
      route_list.each do |key, array|
        Path.create(array, @message, "Exclusive") ##同じ経路でもpathが生成されてしまう・・・？
        tmp_rtc = rtc.clone
        tmp_rtc.setSchedule(initial_phase, array)
        @timeslot_table[key].push(tmp_rtc)
      end
      @timeslot_table = sort_h(@timeslot_table)
    end
    return true
  end

  ## 以下は@path_managerへのアクセサ
  # This method smells of :reek:FeatureEnvy but ignores them
  def packet_in(_dpid, message, mode = "shared")
    if (mode == "shared")
      puts "packet_in is called (shared)"
      @path_manager.packet_in(_dpid, message, mode)
      # for p in Path.all
      #   puts ""
      #   puts "mode: #{p.mode}, path: #{p.full_path}"
      # end
    else
      puts "packet_in is called (exclusive)"
      # @path_manager.packet_in(_dpid, message, mode) ## 現時点では何もしない
    end

    @counter += 1
    @tmp_msg[@counter] = message
    ## RTCManagerのテストは以下に記述
    if (@counter == 6)
      yputs "Test started."
      puts ""
      periodSchedule(@tmp_msg[1], @tmp_msg[1].source_mac, @tmp_msg[1].destination_mac, 2)
      periodSchedule(@tmp_msg[4], @tmp_msg[4].source_mac, @tmp_msg[4].destination_mac, 5)
    end
  end

  def add_port(port, _topology)
    @path_manager.add_port(port, _topology)
  end

  def delete_port(port, _topology)
    @path_manager.delete_port(port, _topology)
  end

  # TODO: update all paths
  def add_link(port_a, port_b, _topology)
    @path_manager.add_link(port_a, port_b, _topology)
  end

  def delete_link(port_a, port_b, _topology)
    @path_manager.delete_link(port_a, port_b, _topology)
  end

  def add_host(mac_address, port, _topology)
    @path_manager.add_host(mac_address, port, _topology)
  end

  private

  ## routeSchedule
  ## @period_listに新規periodを追加する関数
  def add_period(period)
    @period_list.push(period)
    puts "plist is #{@period_list}"
    if (@period_list.size == 1)
      @lcm = period
      return 1
    else
      old_lcm = @lcm
      res = calc_lcm / old_lcm
      return res
    end
  end

  ## routeSchedule
  ## @period_listに新規periodを追加した場合の
  ## @timeslot_tableの倍率を返す関数
  def add_period?(period)
    puts "plist is #{@period_list}"
    if (@period_list.size == 0)
      @lcm = period
      # puts "lcm is #{@lcm}"
      return 1
    else
      old_lcm = @lcm
      res = (@lcm.lcm(period)) / old_lcm
      # puts "#{res} bai !"
    end
    return res
  end

  ## routeSchedule
  ## @period_listから指定したperiodを1つだけ削除する関数
  def del_period(period)
    for i in Range.new(0, @period_list.size - 1)
      if (@period_list[i] == period)
        @period_list.delete_at(i)
        break
      end
    end
    puts "plist is #{@period_list}"
    if (@period_list.size == 0)
      @lcm = 0
      puts "timeslot all delete"
    else
      old_lcm = @lcm
      # puts "minus #{old_lcm / calc_lcm} bai !"
    end
  end

  ## add_period, del_period
  ## @period_listの要素全ての最小公倍数を返す関数
  def calc_lcm
    if @period_list.size == 0
      puts "0"
      return 0
    elsif (@period_list.size == 1)
      # puts @period_list[0]
      return @period_list[0]
    else
      @lcm = 1
      for i in Range.new(0, @period_list.size - 1)
        @lcm = @lcm.lcm(@period_list[i])
      end
      # puts "lcm is #{@lcm}"
      return @lcm
    end
  end
end

## sort(Hash)
def sort_h(hash)
  array = hash.sort
  hash = {}
  array.each do |a|
    hash[a[0]] = a[1]
  end
  return hash
end
