## 実時間通信タスク
## 送信元/宛先idおよび通信周期は初期入力
## スケジューリング可能であれば通信経路とタイムスロットIDを獲得
## RoutingSwitch版
class RTC
  def initialize(source_mac, destination_mac, period)
    @source_mac = source_mac ## Pio::Mac
    @destination_mac = destination_mac ## Pio::Mac
    @period = period ## 通信周期(タイムスロット単位)
    @rtc_id = ((0..9).to_a + ("a".."z").to_a + ("A".."Z").to_a).sample(5).join
    puts "rtc_id: #{@rtc_id}"
  end

  attr_reader :source_mac
  attr_reader :destination_mac
  attr_reader :period
  attr_reader :initial_phase
  attr_reader :route
  attr_reader :rtc_id

  ## 通信経路とタイムスロットIDの格納
  def setSchedule(initial_phase, route)
    @initial_phase = initial_phase
    @route = route
    # puts "ip= #{initial_phase}, route= #{route}"
    # puts "route= #{route}"
    return self
  end

  def display
    puts "rtc_id: #{@rtc_id}, path: " + @route.map(&:to_s).join(" -> ") if route
  end
end
