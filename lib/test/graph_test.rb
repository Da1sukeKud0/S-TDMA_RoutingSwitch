require_relative "../breadth_first_search"
require_relative "../dijkstra"
require_relative "../graph"
require "pio"

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
puts "finds the shortest path to a node"

graph = Graph.new
# graph.add_edge(@node1, @node2)
# graph.add_edge(@node1, @node4)
# graph.add_edge(@node2, @node3)
# graph.add_edge(@node2, @node5)
# graph.add_edge(@node3, @node4)
# graph.add_edge(@node3, @node6)
# graph.add_edge(@node4, @node6)
# graph.add_edge(@node5, @node6)

t = "TopologyDummy"
p11 = Port.new(1, 1)
p22 = Port.new(2, 2)
p33 = Port.new(3, 3)
p44 = Port.new(4, 4)
p55 = Port.new(5, 5)
p66 = Port.new(6, 6)

p12 = Port.new(1, 2)
p14 = Port.new(1, 4)
p23 = Port.new(2, 3)
p25 = Port.new(2, 5)
p34 = Port.new(3, 4)
p36 = Port.new(3, 6)
p46 = Port.new(4, 6)
p56 = Port.new(5, 6)

p21 = Port.new(2, 1)
p41 = Port.new(4, 1)
p32 = Port.new(3, 2)
p52 = Port.new(5, 2)
p43 = Port.new(4, 3)
p63 = Port.new(6, 3)
p64 = Port.new(6, 4)
p65 = Port.new(6, 5)

graph.add_link(p11.dpid, p11)
graph.add_link(p12.dpid, p12)
graph.add_link(p14.dpid, p14)
graph.add_link(p21.dpid, p21)
graph.add_link(p22.dpid, p22)
graph.add_link(p23.dpid, p23)
graph.add_link(p25.dpid, p25)
graph.add_link(p32.dpid, p32)
graph.add_link(p33.dpid, p33)
graph.add_link(p34.dpid, p34)
graph.add_link(p36.dpid, p36)
graph.add_link(p41.dpid, p41)
graph.add_link(p43.dpid, p43)
graph.add_link(p44.dpid, p44)
graph.add_link(p46.dpid, p46)
graph.add_link(p52.dpid, p52)
graph.add_link(p56.dpid, p56)
graph.add_link(p64.dpid, p64)
graph.add_link(p65.dpid, p65)
graph.add_link(p66.dpid, p66)

h1 = Pio::Mac.new("11:11:11:11:11:11")
h2 = Pio::Mac.new("22:22:22:22:22:22")
h3 = Pio::Mac.new("33:33:33:33:33:33")
h4 = Pio::Mac.new("44:44:44:44:44:44")
h5 = Pio::Mac.new("55:55:55:55:55:55")
h6 = Pio::Mac.new("66:66:66:66:66:66")
graph.add_link(h1, p11)
graph.add_link(h2, p22)
graph.add_link(h3, p33)
graph.add_link(h4, p44)
graph.add_link(h5, p55)
graph.add_link(h6, p66)

graph.add_link(p12, p21)
graph.add_link(p14, p41)
graph.add_link(p23, p32)
graph.add_link(p25, p52)
graph.add_link(p34, p43)
graph.add_link(p36, p63)
graph.add_link(p46, p64)
graph.add_link(p56, p65)

puts Dijkstra.new(graph.graph).run(h1, h6)

bfs = BreadthFirstSearch.new(graph.graph)
# puts path = BreadthFirstSearch.new(graph.graph).run(@node4, @node5)
