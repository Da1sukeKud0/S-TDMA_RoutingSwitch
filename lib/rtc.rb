## 実時間通信タスク
## 送信元/宛先idおよび通信周期は初期入力
## スケジューリング可能であれば通信経路とタイムスロットIDを獲得
## RoutingSwitch版
class RTC
  def initialize(src, dst, period)
    @src = src ## mac_addressの予定
    @dst = dst ## mac_addressの予定
    @period = period ## 通信周期（タイムスロット単位）
    rtc_id = ((0..9).to_a + ("a".."z").to_a + ("A".."Z").to_a).sample(5).join
    puts "rtc_id: #{rtc_id}"
  end

  attr_reader :src
  attr_reader :dst
  attr_reader :period
  attr_reader :initial_phase
  attr_reader :route
  attr_reader :rtc_id

  ## 通信経路とタイムスロットIDの格納
  def setSchedule(initial_phase, route)
    @initial_phase = initial_phase
    @route = route
    # puts "ip= #{initial_phase}, route= #{route}"
    puts "route= #{route}"
    return self
  end
end
