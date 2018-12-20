require_relative "../rtc_manager"
# require_relative "../../vendor/topology/lib/topology"
# require "pio"

class RTCManagerTest
  def initialize
    @rtc_manager = RTCManager.new.tap(&:start)
    @topology = "Topology Class" ##dummy of Topology.new
    @edges = [] ## [[src,dst],[src,dst],,,]
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

  attr_reader :rtc_manager
  attr_reader :topology

  ## BAモデルに基づいたトポロジの生成
  def make_ba_topology(numOfSwitch, complexity)
    @type = "BA"
    @numOfSwitch = numOfSwitch.to_i
    @complexity = complexity.to_i
    ## barabasi_albert_graph.pyを外部実行
    sh ("python ~/trema/routing_switch/lib/test/barabasi_albert_graph.py #{@numOfSwitch} #{@complexity}")
    ## 生成されたリンクを@edgesに格納
    File.open(".edges") do |file|
      file.each_line do |line|
        str = line[1..line.size - 3].split(", ").map(&:to_i)
        @edges.push(str)
      end
    end
    make_link_and_make_host
  end

  ## フルメッシュトポロジを生成
  def make_fullmesh_topology(numOfSwitch)
    @type = "fullmesh"
    @numOfSwitch = numOfSwitch.to_i
    for src in Range.new(1, @numOfSwitch)
      for dst in Range.new(1, @numOfSwitch)
        next if (src == dst)
        @edges.push([src, dst])
      end
    end
    puts "edges : #{@edges}"
    make_link_and_make_host
  end

  ## トポロジ生成用のサンプル
  def make_sample
    @numOfSwitch = 4
    @edges = [[1, 2], [2, 3], [3, 4]]
    make_link_and_make_host
    @rtc_manager.scheduling?("h1", "h3", 2)
    @rtc_manager.scheduling?("h3", "h4", 2)
  end

  ## 指定回数のスケジューリング探索の実行
  def add_rtcs(num)
    num = num.to_i
    ## 重複しないようにnum回分のsrc,dstをランダムに選択(periodは重複可)
    srcList = []
    dstList = []
    l = Array.new(@numOfSwitch) { |index| index + 1 }
    popMax = @numOfSwitch
    num.times do
      srcList.push(l.delete_at(rand(popMax)))
      popMax -= 1
      dstList.push(l.delete_at(rand(popMax)))
      popMax -= 1
    end

    ## num回分探索の準備
    result = [] ## num回分の探索結果を格納 [r, r, ... , r]
    tagList = Hash.new ## データのタグリスト(rtcの実行順(turn)を除く)
    tagList.store("type", @type) ## トポロジタイプ
    tagList.store("snum", @numOfSwitch) ## スイッチ数
    tagList.store("rnum", num) ## RTC数
    tagList.store("lnum", @edges.size) ## リンク数(switchNum-complexity)*complexityで算出可能
    if (@type == "BA")
      tagList.store("cplx", @complexity) ## 複雑度
    elsif (@type == "tree")
      tagList.store("dep", @depth)
      tagList.store("fan", @fanout)
    end

    ## num回分探索
    for n in Range.new(1, num)
      src = srcList.pop
      dst = dstList.pop
      period = rand(4) + 2
      puts ""
      puts "schedulable?(src: h#{src}, dst: h#{dst}, period: #{period})"
      # 以下でスケジューリング処理の時間を計測
      st = Time.now
      tf = @rtc_manager.scheduling?(src, dst, period)
      puts time = (Time.now - st)
      ## 計測結果をresultに格納
      r = tagList.clone
      r.store("turn", n) ## RTC実行順
      r.store("time", time) ## 処理時間
      r.store("tf", tf) ## add_rtc?
      result.push(r)
    end
    return result
  end

  private

  def make_link_and_make_host
    ## 命名規則
    ## dpid:1において、dpid:2へのリンクで使用するポートは0x1:2
    ## またホストのMACアドレスは"h1"、ホストへのリンクで使用するポートは0x1:1
    @edges.each do |src, dst|
      @rtc_manager.add_port(Port.new(src, dst), @topology)
      @rtc_manager.add_port(Port.new(dst, src), @topology)
      @rtc_manager.add_link(Port.new(src, dst), Port.new(dst, src), @topology)
    end
    for n in Range.new(1, @numOfSwitch)
      @rtc_manager.add_port(Port.new(n, n), @topology)
      @rtc_manager.add_host("h" + n.to_s, Port.new(n, n), @topology) ## 本来はPio::Mac.new("11:11:11:11:11:11") だが簡略化
    end
  end
end

def sh(command)
  system(command) || fail("#{command} failed.")
  @logger.debug(command) if @logger
end

def output_json(file_name, hash)
  File.open(file_name, "w") do |file|
    JSON.dump(hash, file)
  end
end

if __FILE__ == $0
  rtcm = RTCManagerTest.new
  rtcm.make_ba_topology(20, 1)
  rtcm.add_rtcs(5)
end