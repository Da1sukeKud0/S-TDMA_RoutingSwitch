require_relative "../rtc_manager"
require_relative "../../vendor/topology/lib/topology"
require "pio"

class RTCManagerTest
  def initialize
    @rtc_manager = RTCManager.new.tap(&:start)
    @topology = Topology.new
  end

  attr_reader :rtc_manager
  attr_reader :topology

  ## main
  ## フルメッシュトポロジを生成
  def make_fullmesh_topology(numOfSwitch)
    @type = "fullmesh"
    @numOfSwitch = numOfSwitch.to_i
    for src in Range.new(1, @numOfSwitch)
      for dst in Range.new(1, @numOfSwitch)
        next if (src == dst)
        puts "add link: #{src} to #{dst}"
        add_switch2switch_link(src, dst)
      end
      mac_address = "mac" + src.to_s
      maybe_add_host(mac_address, src)
    end
  end

  def make_test
    numOfSwitch = 4
    edges = [[1, 2], [2, 3], [3, 4]]
    ## port,link作成
    edges.each do |src, dst|
      @rtc_manager.add_port(Port.new(src, dst), @topology)
      @rtc_manager.add_port(Port.new(dst, src), @topology)
      @rtc_manager.add_link(Port.new(src, dst), Port.new(dst, src), @topology)
    end
    for i in Range.new(1, numOfSwitch)
      @rtc_manager.add_port(Port.new(i, i), @topology)
      @rtc_manager.add_host("h" + i.to_s, Port.new(i, i), @topology)
    end
    ## host生成
    # for i in Range.new(1, numOfSwitch)
    #   @rtc_manager.add_host("h" + i.to_s, Port.new(i, i), @topology)
    # end
    # @rtc_manager.add_host(Pio::Mac.new("11:11:11:11:11:11"), Port.new(1, 1), @topology)
    # @rtc_manager.add_host(Pio::Mac.new("22:22:22:22:22:22"), Port.new(2, 2), @topology)
    # @rtc_manager.add_host(Pio::Mac.new("33:33:33:33:33:33"), Port.new(3, 3), @topology)
    # @rtc_manager.add_host(Pio::Mac.new("44:44:44:44:44:44"), Port.new(4, 4), @topology)
    ## rtc
    # @rtc_manager.scheduling?(Pio::Mac.new("11:11:11:11:11:11"), Pio::Mac.new("44:44:44:44:44:44"), 2)
    @rtc_manager.scheduling?("h1", "h3", 2)
    @rtc_manager.scheduling?("h3", "h4", 2)
  end

  def make_link(src, dst)
  end

  def make_host
  end
end

Port = Struct.new(:dpid, :port_no) do
  alias_method :number, :port_no

  def self.create(attrs)
    new attrs.fetch(:dpid), attrs.fetch(:port_no)
  end

  def <=>(other)
    [dpid, number] <=> [other.dpid, other.number]
  end

  def to_s
    "#{format "%#x", dpid}:#{number}"
  end
end

if __FILE__ == $0
  rtcm = RTCManagerTest.new
  rtcm.make_test
end
