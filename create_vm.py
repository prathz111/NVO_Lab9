from openstack import connection

def create_vm(conn, network, flavor_name, image_name, vm_name):
    flavor = conn.compute.find_flavor(flavor_name)
    image = conn.compute.find_image(image_name)
    network_id = network.id
    server = conn.compute.create_server(
        name=vm_name,
        flavor_id=flavor.id,
        image_id=image.id,
        networks=[{"uuid": network_id}]
    )
    return server

def assign_floating_ip(conn, server):
    floating_ip = conn.network.create_ip(floating_network_id="public")
    conn.compute.add_floating_ip_to_server(server, floating_ip.floating_ip_address)
