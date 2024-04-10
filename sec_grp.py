from openstack import connection

def allow_icmp_traffic(security_group_name):
    conn = connection.Connection(**credentials)
    group = find_security_group(conn, security_group_name)
    if group:
        add_icmp_rules(conn, group.id)
    else:
        print(f"Security group '{security_group_name}' not found.")

def allow_vn_traffic(security_group_name, *network_cidrs):
    conn = connection.Connection(**credentials)
    group = find_security_group(conn, security_group_name)
    if group:
        add_vn_rules(conn, group.id, network_cidrs)
    else:
        print(f"Security group '{security_group_name}' not found.")

def find_security_group(conn, name):
    groups = list(conn.network.security_groups(name=name))
    return groups[0] if groups else None

def add_icmp_rules(conn, group_id):
    rules = [
        {'security_group_id': group_id, 'direction': 'ingress', 'protocol': 'icmp', 'remote_ip_prefix': '0.0.0.0/0'},
        {'security_group_id': group_id, 'direction': 'egress', 'protocol': 'icmp', 'remote_ip_prefix': '0.0.0.0/0'}
    ]
    for rule in rules:
        conn.network.create_security_group_rule(**rule)

def add_vn_rules(conn, group_id, cidrs):
    rules = [
        {'security_group_id': group_id, 'direction': 'ingress', 'protocol': None, 'remote_ip_prefix': cidr} for cidr in cidrs,
        {'security_group_id': group_id, 'direction': 'egress', 'protocol': None, 'remote_ip_prefix': cidr} for cidr in cidrs
    ]
    for rule in rules:
        conn.network.create_security_group_rule(**rule)
