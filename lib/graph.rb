require_relative "dijkstra"

# Network topology graph
class Graph
  def initialize
    @graph = Hash.new([].freeze)
  end

  attr_reader :graph

  def fetch(node)
    @graph.fetch(node)
  end

  def delete_node(node)
    fail unless node.is_a?(Topology::Port)
    @graph.delete(node)
    @graph[node.dpid] -= [node]
  end

  def add_link(node_a, node_b)
    @graph[node_a] += [node_b]
    @graph[node_b] += [node_a]
  end

  def delete_link(node_a, node_b)
    @graph[node_a] -= [node_b]
    @graph[node_b] -= [node_a]
  end

  def external_ports
    @graph.select do |key, value|
      key.is_a?(Topology::Port) && value.size == 1
    end.keys
  end

  def dijkstra(source_mac, destination_mac)
    return false if @graph[destination_mac].empty?
    route = Dijkstra.new(@graph).run(source_mac, destination_mac)
    return false unless route
    route.reject { |each| each.is_a? Integer } ## return Array
  end
end
