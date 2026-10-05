import subprocess

def run_cmd(cmd, input_text=None):
    result = subprocess.run(
        cmd,
        input=input_text,
        text=True,
        capture_output=True,
        check=True
    )
    return result.stdout.strip()

def generate_private_key():
    return run_cmd(["wg", "genkey"])

def generate_public_key(private_key: str):
    return run_cmd(["wg", "pubkey"], input_text=private_key)

def generate_preshared_key():
    return run_cmd(["wg", "genpsk"])


from ipaddress import ip_interface, ip_network

def get_next_client_ip(server):
    interface = ip_interface(server.address_cidr)
    network = interface.network
    server_ip = interface.ip

    used_ips = {server_ip}
    for client in server.clients.all():
        client_ip = ip_interface(client.address).ip
        used_ips.add(client_ip)

    for ip in network.hosts():
        if ip not in used_ips:
            return f"{ip}/32"

    raise ValueError("No available IPs left in network")

def render_server_config(server):
    lines = [
        "[Interface]",
        f"Address = {server.address_cidr}",
        f"ListenPort = {server.listen_port}",
        f"PrivateKey = {server.private_key}",
        "",
    ]

    for client in server.clients.filter(enabled=True):
        lines.extend([
            f"# Client: {client.name}",
            "[Peer]",
            f"PublicKey = {client.public_key}",
            f"PresharedKey = {client.preshared_key}",
            f"AllowedIPs = {client.address}",
            "",
        ])

    return "\n".join(lines)
def render_client_config(client):
    server = client.server
    return "\n".join([
        "[Interface]",
        f"PrivateKey = {client.private_key}",
        f"Address = {client.address}",
        f"DNS = {client.dns or server.dns}",
        "",
        "[Peer]",
        f"PublicKey = {server.public_key}",
        f"PresharedKey = {client.preshared_key}",
        f"Endpoint = {server.public_endpoint}:{server.listen_port}",
        "AllowedIPs = 0.0.0.0/0, ::/0",
        "PersistentKeepalive = 25",
    ])