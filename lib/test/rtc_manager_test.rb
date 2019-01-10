require_relative "../rtc_manager"
require_relative "../../vendor/topology/lib/topology"
# require "pio"
require "json"
require_relative "../cputs"

class RTCManagerTest
  def initialize(edges = [])
    @rtc_manager = RTCManager.new.tap(&:start)
    @topology = "Topology Class" ##dummy of Topology.new
    @edges = edges ## [[src,dst],[src,dst],,,]
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

  ## ツリートポロジを生成
  def make_tree_topology(depth, fanout)
    @type = "tree"
    @depth = depth.to_i
    @fanout = fanout.to_i
    node = 1
    papa = [], child = [1]
    ## ホストまで含めたツリーの深さなので@depth - 1でループ
    (@depth - 1).times do
      papa = child
      child = []
      ## 親ノードに@fanout個の子ノードを接続
      for p in papa
        @fanout.times do
          node += 1
          @edges.push([p, node])
          # puts "add link: #{p} to #{node}"
          child.push(node)
        end
      end
    end
    @numOfSwitch = node
    ## 最も若いノードにそれぞれfanout個のホストを付加(廃止)
    #   hnode = 0
    #   for c in child
    #     @fanout.times do
    #       hnode += 1
    #       mac_address = "mac" + hnode.to_s
    #       puts "add link: #{c} to host#{hnode.to_s}"
    #     end
    #   end
    ## 最若ノードのみでなく全てのノードにホストを付加する(ツリーの定義にあっているのか？)
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

  ## 指定回数分の実時間通信要求を生成
  def make_testcase(numOfReq)
    @numOfReq = numOfReq.to_i
    ## 重複しないようにnum回分のsrc,dstをランダムに選択(periodは重複可)
    @srcList = []
    @dstList = []
    @periodList = []
    l = Array.new(@numOfSwitch) { |index| index + 1 }
    popMax = @numOfSwitch
    @numOfReq.times do
      @srcList.push("h" + (l.delete_at(rand(popMax))).to_s)
      popMax -= 1
      @dstList.push("h" + (l.delete_at(rand(popMax))).to_s)
      popMax -= 1
      @periodList.push(rand(4) + 2)
    end
    save_tag
  end

  ## 指定回数分のスケジューリング探索
  def run_testcase(srcList = @srcList.clone, dstList = @dstList.clone, periodList = @periodList.clone)
    result = [] ## @numOfReq回分の探索結果を格納 [r, r, ... , r]
    for n in Range.new(1, srcList.size)
      src = srcList.pop
      dst = dstList.pop
      period = periodList.pop
      puts ""
      puts "schedulable?(src: #{src}, dst: #{dst}, period: #{period})"
      # 以下でスケジューリング処理の時間を計測
      st = Time.now
      tf = @rtc_manager.scheduling?(src, dst, period)
      puts time = (Time.now - st)
      ## 計測結果をresultに格納
      r = @tagList.clone
      r.store("turn", n) ## RTC実行順
      r.store("time", time) ## 処理時間
      r.store("tf", tf) ## add_rtc?
      r.store("shop", @rtc_manager.shortest_hop) ## 単純最短経路の平均ホップ数
      r.store("rhop", @rtc_manager.real_hop) ## 実際に設定された経路の平均ホップ数
      r.store("shops", @rtc_manager.shortest_hops) ## 単純最短経路の累計ホップ数
      r.store("rhops", @rtc_manager.real_hops) ## 実際に設定された経路の累計ホップ数
      result.push(r)
    end
    return result
  end

  def save_testcase
    hash = Hash.new
    hash.store("edges", @edges)
    hash.store("numOfReq", @numOfReq)
    hash.store("srcList", @srcList)
    hash.store("dstList", @dstList)
    hash.store("periodList", @periodList)
  end

  private

  def make_link_and_make_host
    ## 命名規則
    ## dpid:1において、dpid:2へのリンクで使用するポートは0x1:2
    ## またホストのMACアドレスは"h1"、ホストへのリンクで使用するポートは0x1:1
    @edges.each do |src, dst|
      @rtc_manager.add_port(Topology::Port.new(src, dst), @topology)
      @rtc_manager.add_port(Topology::Port.new(dst, src), @topology)
      @rtc_manager.add_link(Topology::Port.new(src, dst), Topology::Port.new(dst, src), @topology)
    end
    for n in Range.new(1, @numOfSwitch)
      @rtc_manager.add_port(Topology::Port.new(n, n), @topology)
      @rtc_manager.add_host("h" + n.to_s, Topology::Port.new(n, n), @topology) ## 本来はPio::Mac.new("11:11:11:11:11:11") だが簡略化
    end
  end

  ## 結果出力に用いる各種情報
  def save_tag
    @tagList = Hash.new ## データのタグリスト(rtcの実行順(turn)を除く)
    @tagList.store("type", @type) ## トポロジタイプ
    @tagList.store("snum", @numOfSwitch) ## スイッチ数
    @tagList.store("rnum", @numOfReq) ## RTC要求数
    @tagList.store("lnum", @edges.size) ## リンク数(switchNum-complexity)*complexityで算出可能
    if (@type == "BA")
      @tagList.store("cplx", @complexity) ## 複雑度
    elsif (@type == "tree")
      @tagList.store("dep", @depth)
      @tagList.store("fan", @fanout)
    end
  end
end

def sh(command)
  system(command) || fail("#{command} failed.")
  @logger.debug(command) if @logger
end

def output_json(hash)
  File.open(@file_name, "w") do |file|
    JSON.dump(hash, file)
  end
end

## BAモデルでの各種パラメータを自動設定し実行
def test_BA_loop(snum_min = 10, snum_max = 100, snum_interval = 5, cplx_min = 1, cplx_max = 5, loops = 10)
  rputs "snum_min: #{snum_min}, snum_max: #{snum_max}, snum_interval: #{snum_interval}, cplx_min: #{cplx_min}, cplx_max: #{cplx_max}, loops: #{loops}"
  output = []
  snum = snum_min
  while (snum <= snum_max)
    cplx = cplx_min
    while (cplx <= cplx_max)
      loops.times do
        rtcm = RTCManagerTest.new
        rtcm.make_ba_topology(snum, cplx)
        rtcm.make_testcase(5)
        puts res = rtcm.run_testcase
        res.each { |each| output.push(each) }
      end
      cplx += 1
    end
    snum += snum_interval
  end
  output_json(output)
end

def test_lineprof
  require "rblineprof"
  require "rblineprof-report"
  target = /#{Dir.pwd}\/./
  output = []
  rtcm = RTCManagerTest.new
  rtcm.make_ba_topology(100, 2)
  rtcm.make_testcase(5)
  profile = lineprof(target) do
    puts @res = rtcm.run_testcase
  end
  @res.each { |each| output.push(each) }
  output_json(output)
  LineProf.report(profile)
end

def test_BA_max
  snum = 100
  cplx = 2
  rtcm = RTCManagerTest.new
  rtcm.make_ba_topology(snum, cplx)
  rtcm.make_testcase(5)
  puts rtcm.run_testcase
end

## ツリートポロジの各種パラメータを自動設定し実行
def test_tree_loop(loops = 100)
  dep_and_fo = [[3,2],[3,3],[3,4],[4,2],[4,3],[5,2],[6,2]] ## snum<=150の範囲でテストケース作成
  rputs "dep_and_fo: #{dep_and_fo}"
  rputs "loops: #{loops}"
  #rputs "depth_min: #{dep_min}, depth_max: #{dep_max}, fanout_min: #{fo_min}, fanout_max: #{fo_max}, loops: #{loops}"
  output = []
  dep_and_fo.each do |dep,fo|
    puts "#{dep},#{fo}"
    loops.times do
      rtcm = RTCManagerTest.new
      rtcm.make_tree_topology(dep, fo)
      rtcm.make_testcase(5)
      puts res = rtcm.run_testcase
      res.each { |each| output.push(each) }
    end
  end
  output_json(output)
end

def calc_tree_snum(dep, fo)
  res = 0
  oya = 1
  dep.times do
    res += oya*fo
    oya *= fo
  end
  puts "depth: #{dep}, fanout: #{fo} =>> #{res}"
  return res
end

if __FILE__ == $0
  ARGV[0] = "bamax" if ARGV[0] == nil
  @file_name = "test/rtcm_" + ARGV[0] + "_" + Time.new.strftime("%Y%m%d_%H%M") + ".json"
  case ARGV[0]
  when "baloop"
    rputs "test_BA_loop is called."
    test_BA_loop(*ARGV[1..7].map(&:to_i))
  when "treeloop"
    rputs "test_tree_loop is called."
    test_tree_loop(*ARGV[1].to_i)
  when "lineprof"
    rputs "test_lineprof is called."
    rputs "※このモードでの実行時間はlineprofにより大幅に伸びます"
    test_lineprof
  when "bamax"
    rputs "test_BA_max is called."
    test_BA_max
  else
    rputs "test_BA_max is called."
    test_BA_max
  end
end
