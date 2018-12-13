require "graph"
require "path"
require "trema"
require "path_manager"

# L2 routing path manager
class RTCManager < Trema::Controller
  def start
    @path_manager = PathManager.new.tap(&:start)
    logger.info "RTC Manager started."
  end

  # This method smells of :reek:FeatureEnvy but ignores them
  def packet_in(_dpid, message)
    @path_manager.packet_in(_dpid, message)
  end

  def add_port(port, _topology)
    @path_manager.add_port(port, _topology)
  end

  def delete_port(port, _topology)
    @path_manager.delete_port(port, _topology)
  end

  # TODO: update all paths
  def add_link(port_a, port_b, _topology)
    @path_manager.add_link(port_a, port_b, _topology)
  end

  def delete_link(port_a, port_b, _topology)
    @path_manager.delete_link(port_a, port_b, _topology)
  end

  def add_host(mac_address, port, _topology)
    @path_manager.add_host(mac_address, port, _topology)
  end
end
