require_relative "../rtc"

old = RTC.new(1, 2, 3)
old.setSchedule(4, 5)
new = old.clone
new.setSchedule(6, 7)
puts old.inspect
puts new.inspect
