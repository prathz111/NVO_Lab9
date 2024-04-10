def install_docker(ip_address, username, password):
    vm = {
        'device_type': 'linux',
        'ip': ip_address,
        'username': username,
        'password': password,
    }
    net_connect = ConnectHandler(**vm)
    output = net_connect.send_command('sudo apt-get update && sudo apt-get install -y docker.io')
    print(output)
    net_connect.disconnect()

def spin_containers(ip_address, username, password):
    vm = {
        'device_type': 'linux',
        'ip': ip_address,
        'username': username,
        'password': password,
    }
    net_connect = ConnectHandler(**vm)
    output = net_connect.send_command('sudo docker run -d --name container1 FRRouting/frr')
    print(output)
    output = net_connect.send_command('sudo docker run -d --name container2 osrg/ryu:latest')
    print(output)
    net_connect.disconnect()
