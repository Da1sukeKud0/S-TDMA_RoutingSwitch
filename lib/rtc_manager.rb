require "graph"
require "path"
require "trema"
require "path_manager"

##
##　実時間通信要求に対し経路スケジューリングおよび時刻スケジューリングを行う
##
class RTCManager < Trema::Controller
  def start
    @path_manager = PathManager.new.tap(&:start)
    @timeslot_table = Hash.new { |hash, key| hash[key] = [] } ## {timeslot=>[rtc,rtc,,,], ,,}
    # @timeslot_table[0] = @path_manager
    @period_list = [] ## 周期の種類を格納(同じ数値の周期も重複して格納)
    logger.info "RTC Manager started."
  end

  def periodSchedule(src, dst, period)
    rtc = RTC.new(src, dst, period)
    initial_phase = 0 ##初期位相0に設定
    ## 0~periodの間でスケジューリング可能な初期位相を探す
    while (initial_phase < period)
      if (routeSchedule(rtc, topo, initial_phase)) ##スケジューリング可
        puts "スケジューリング可能です"
        puts ""
        # puts @timeslot_table
        # @timeslot_table.each do |timeslot, exist_rtcs|
        #   puts "timeslot: #{timeslot}"
        #   exist_rtcs.each do |i|
        #     puts i.route
        #   end
        # end
        # test(@timeslot_table, topo)
        return true
      else ##スケジューリング不可
        initial_phase += 1
      end
    end
    puts "####################"
    puts "####################"
    puts "####### false ######"
    puts "####################"
    puts "####################"
    return false
  end

  def routeSchedule(rtc, topo, initial_phase)
    if (@timeslot_table.all? { |key, each| each.size == 0 }) ##既存のrtcがない場合
      tmp_slot = PathManager.new.tap(&:start)
      route = tmp_slot.shortest_path?(rtc.src, rtc.dst) ## edited
      if (route) ##経路が存在する場合は使用するスロットにrtcを格納
        rtc.setSchedule(initial_phase, route)
        for i in Range.new(0, rtc.period - 1)
          if ((i + initial_phase) % rtc.period == 0)
            @timeslot_table[i].push(rtc)
          else
            @timeslot_table[i] = []
          end
        end
        add_period(rtc.period)
      else ##ルートなし
        return false
      end
    end
  end

  ## 以下は@path_managerへのアクセサ
  # This method smells of :reek:FeatureEnvy but ignores them
  def packet_in(_dpid, message)
    puts "packet_in is called"
    @path_manager.packet_in(_dpid, message)
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
end
