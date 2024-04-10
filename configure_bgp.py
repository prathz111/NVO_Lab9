from netmiko import ConnectHandler

bgp_commands = [
    'vtysh',  # Enter vtysh
    'conf t',  # Enter configuration mode
    'router bgp 20',  #  BGP AS number
    'neighbor 13.13.13.1 remote-as 20',  #  neighbor configuration
    'exit',  #  BGP configuration
    'exit'  #  vtysh
]

def configure_bgp_frr(ip_address, username, password):
    vm = {
        'device_type': 'linux',
        'ip': ip_address,
        'username': username,
        'password': password,
    }
    net_connect = ConnectHandler(**vm)
    net_connect.send_command_timing("service frr start")
    net_connect.send_config_set(bgp_commands)
    net_connect.disconnect()
    print("BGP FRR configured successfully.")

def configure_bgp_ryu(ip_address, username, password):
    vm = {
        'device_type': 'linux',
        'ip': ip_address,
        'username': username,
        'password': password,
    }
    net_connect = ConnectHandler(**vm)
    net_connect.send_command_timing("sudo ryu-manager --verbose --bgp-app-config-file bgp.conf.py ryu/services/protocols/bngp/application.py ryu/ryu/app/simple_switch_13.py &")
    net_connect.send_command_timing("sudo ovs-vsctl add-br mybridge")                                          # create a bridge 
    net_connect.send_command_timing("sudo ovs-vsctl add-port mybridge eth0")    # add a port to the bridge
    net_connect.send_command_timing("sudo ovs-vsctl set bridge mybridge protocols=OpenFlow13") # set the bridge to use OpenFlow version 13
    net_connect.send_command_timing("sudo ovs-vsctl set-controller mybridge tcp:"+ip_address+":6633")
    net_connect.disconnect()
    print("BGP SDN RYU controller configured successfully.")
