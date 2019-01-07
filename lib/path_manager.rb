require_relative "graph"
require_relative "path"
require "trema"

# L2 routing path manager
class PathManager < Trema::Controller
  def start
    @graph = Graph.new
    logger.info "Path Manager started."
  end

  attr_accessor :graph

  # This method smells of :reek:FeatureEnvy but ignores them
  def packet_in(_dpid, message, mode = "shared")
    if (mode == "shared")
      path = maybe_create_shortest_path(message)
      ports = path ? [path.out_port] : @graph.external_ports
      ports.each do |each|
        send_packet_out(each.dpid,
                        raw_data: message.raw_data,
                        actions: SendOutPort.new(each.number))
      end
    else
      puts "exclusive"
    end
  end

  def add_port(port, _topology)
    @graph.add_link(port.dpid, port)
  end

  def delete_port(port, _topology)
    @graph.delete_node(port)
  end

  # TODO: update all paths
  def add_link(port_a, port_b, _topology)
    @graph.add_link(port_a, port_b)
  end

  def delete_link(port_a, port_b, _topology)
    @graph.delete_link(port_a, port_b)
    Path.find { |each| each.link?(port_a, port_b) }.each(&:destroy)
    ## TODO: 上記処理でExclusive Modeのpathオブジェクトも消えてしまう。どうする？
  end

  def add_host(mac_address, port, _topology)
    @graph.add_link(mac_address, port)
  end

  ## 最短経路探索のみを実行(Path.createはRTC側で実行) public
  def shortest_path?(src_mac, dst_mac)
    shortest_path = @graph.dijkstra(src_mac, dst_mac)
  end

  def delete_used_link(path)
  end

  private

  def maybe_create_shortest_path(packet_in)
    shortest_path = @graph.dijkstra(packet_in.source_mac, packet_in.destination_mac) ## [Pio::Mac, (Topology::Port)*2n, Pio::Mac]
    return false unless shortest_path ## falseを追記
    Path.create(shortest_path, packet_in)
  end
end
