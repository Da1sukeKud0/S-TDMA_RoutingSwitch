# Put unvisited nodes on a queue
# Solves the shortest path problem: Find path from "source" to "target"
# that uses the fewest number of edges
# It's not recursive (like depth first search)
#
# The steps are quite simple:
# * Put s into a FIFO queue and mark it as visited
# * Repeat until the queue is empty:
#   - Remove the least recently added node n
#   - add each of n's unvisited adjacents to the queue and
#     mark them as visited
require "set"

class BreadthFirstSearch
  def initialize(graph)
    # @node = source_node
    @visited = []
    @edge_to = {}
    # bfs(source_node, dst)
    graph.keys.map { |each| Node.new(each) }
    graph.map do |name, neighbors|
      for neighbor in neighbors
        puts "#{name}, #{neighbor}"
        node_a.adjacents << node_b
        node_b.adjacents << node_a
      end
      # Node.new(name)
    end
    # @graph = graph
  end

  class Node
    attr_accessor :obj, :adjacents

    def initialize(obj)
      # I'm using a Set instead of an Array to
      # avoid duplications. We don't want node1
      # connected to node2 twice.
      @adjacents = Set.new
      @obj = obj
      puts "called"
    end

    def obj?(obj)
      return self if obj == @obj
    end

    def to_s
      @obj
    end
  end

  def shortest_path_to(node)
    return unless has_path_to?(node)
    path = []

    while (node != @node)
      path.unshift(node) # unshift adds the node to the beginning of the array
      node = @edge_to[node]
    end

    path.unshift(@node)
  end

  def run(src, dst)
    bfs(src).shortest_path_to(dst)
  end

  private

  def bfs(node)
    # Remember, in the breadth first search we always
    # use a queue. In ruby we can represent both
    # queues and stacks as an Array, just by using
    # the correct methods to deal with it. In this case,
    # we use the "shift" method to remove an element
    # from the beginning of the Array.

    # First step: Put the source node into a queue and mark it as visited
    queue = []
    queue << node
    @visited << node

    # Second step: Repeat until the queue is empty:
    # - Remove the least recently added node n
    # - add each of n's unvisited adjacents to the queue and mark them as visited
    while queue.any?
      current_node = queue.shift # remove first element
      current_node.adjacents.each do |adjacent_node|
        next if @visited.include?(adjacent_node)
        queue << adjacent_node
        @visited << adjacent_node
        @edge_to[adjacent_node] = current_node
      end
    end
    return self
  end

  # If we visited the node, so there is a path
  # from our source node to it.
  def has_path_to?(node)
    @visited.include?(node)
  end
end
