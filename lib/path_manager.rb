require "graph"
require "path"
require "trema"

# L2 routing path manager
class PathManager < Trema::Controller
  def start
    @graph = Graph.new
    logger.info "Path Manager started."
  end

  # This method smells of :reek:FeatureEnvy but ignores them
  def packet_in(_dpid, message)
    path = maybe_create_shortest_path(message)
    ports = path ? [path.out_port] : @graph.external_ports
    ports.each do |each|
      send_packet_out(each.dpid,
                      raw_data: message.raw_data,
                      actions: SendOutPort.new(each.number))
    end
  end

  def add_port(port, _topology)
    @graph.add_link port.dpid, port
  end

  def delete_port(port, _topology)
    @graph.delete_node port
  end

  # TODO: update all paths
  def add_link(port_a, port_b, _topology)
    @graph.add_link port_a, port_b
  end

  def delete_link(port_a, port_b, _topology)
    @graph.delete_link port_a, port_b
    Path.find { |each| each.link?(port_a, port_b) }.each(&:destroy)
  end

  def add_host(mac_address, port, _topology)
    @graph.add_link mac_address, port
  end

  ## 最短経路探索のみを実行 public
  def shortest_path?(src_mac, dst_mac)
    shortest_path = @graph.dijkstra(src_mac, dst_mac)
    return false unless shortest_path
    puts shortest_path
    return shortest_path
    # Path.create shortest_path, packet_in
  end

  private

  def maybe_create_shortest_path(packet_in)
    shortest_path = @graph.dijkstra(packet_in.source_mac,
                                    packet_in.destination_mac)
    return unless shortest_path
    puts shortest_path
    Path.create shortest_path, packet_in
  end
end
