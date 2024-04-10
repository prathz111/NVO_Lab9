from openstack import connection
from create_virtual_network import create_virtual_network
from create_vm import create_vm, assign_floating_ip
from configure_bgp import configure_bgp_frr, configure_bgp_ryu

# Authentication credentials
auth = {
    'auth_url': "http://10.0.0.198/identity",
    'project_name': "NVO_lab9",
    'username': "praathz",
    'password': "prathz",
    'user_domain_name': "default",
    'project_domain_name': "default"
}

def main():
    conn = connection.Connection(**auth)

    # Create virtual networks
    network1, subnet1 = create_virtual_network(conn, "network1", "11.11.11.0/24")
    network2, subnet2 = create_virtual_network(conn, "network2", "12.12.12.0/24")

    # Create VMs
    vm1 = create_vm(conn, network1, "m1.tiny", "cirros", "vm1")
    vm2 = create_vm(conn, network1, "m1.tiny", "cirros", "vm2")
    vm3 = create_vm(conn, network2, "m1.tiny", "cirros", "vm3")

    # Assign floating IPs
    assign_floating_ip(conn, vm1)
    assign_floating_ip(conn, vm2)
    assign_floating_ip(conn, vm3)

    # SSH credentials
    ssh_username = "username"
    ssh_password = "password"

    # Install Docker on VM1
    install_docker(vm1.addresses['public'][0]['addr'], ssh_username, ssh_password)

    # Spin containers on VM1
    spin_containers(vm1.addresses['public'][0]['addr'], ssh_username, ssh_password)

    # Configure BGP FRR on container1
    configure_bgp_frr(vm1.addresses['public'][0]['addr'], ssh_username, ssh_password)

    # Configure BGP SDN RYU controller on container2
    configure_bgp_ryu(vm1.addresses['public'][0]['addr'], ssh_username, ssh_password)

if __name__ == "__main__":
    main()
