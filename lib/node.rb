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
