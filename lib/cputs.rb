## お遊び
def cputs(color, obj)
  case color
  when "red"
    cc = 31
  when "green"
    cc = 32
  when "yellow"
    cc = 33
  when "blue"
    cc = 34
  when "magenta"
    cc = 35
  when "cyan"
    cc = 36
  else
    cc = 37 ## white
  end
  puts "\e[#{cc}m#{obj}\e[0m"
end

## for Error
def rputs(obj)
  puts "\e[31m#{obj}\e[0m"
end

## for True
def gputs(obj)
  puts "\e[32m#{obj}\e[0m"
end

## for Notice
def yputs(obj)
  puts "\e[33m#{obj}\e[0m"
end
