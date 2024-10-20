import random
from datetime import datetime, timedelta
import argparse

def generate_regular_log_traffic(server_ip, timestamp):
    traffic_type = random.choice(["HTTP", "DNS", "ICMP", "HTTPS", "DHCP", "TELNET", "SSH"])

    if traffic_type == "HTTP":
        timestamp += timedelta(seconds=1)
        action = "ALLOW"
        protocol = "TCP"
        source_ip_address = "SOURCEIP"
        destination_ip_address = server_ip
        source_port = random.randint(49152, 65535)
        destination_port = 80
        path = "RECEIVE"

    elif traffic_type == "DNS":
        timestamp += timedelta(seconds=1)
        action = "ALLOW"
        protocol = "UDP"
        source_ip_address = server_ip
        destination_ip_address = "DESTIP"
        source_port = random.randint(49152, 65535)
        destination_port = 53
        path = "SEND"

    elif traffic_type == "ICMP":
        timestamp += timedelta(seconds=1)
        action = "DROP"
        protocol = "ICMP"
        source_ip_address = "SOURCEIP"
        destination_ip_address = server_ip
        source_port = ""
        destination_port = ""
        path = "RECEIVE"

    elif traffic_type == "HTTPS":
        timestamp += timedelta(seconds=1)
        action = "ALLOW"
        protocol = "TCP"
        source_ip_address = "SOURCEIP"
        destination_ip_address = server_ip
        source_port = random.randint(49152, 65535)
        destination_port = 443
        path = "RECEIVE"

    elif traffic_type == "DHCP":
        timestamp += timedelta(seconds=1)
        action = "ALLOW"
        protocol = "UDP"
        source_ip_address = "SOURCEIP"
        destination_ip_address = server_ip
        source_port = random.randint(49152, 65535)
        destination_port = 67
        path = "RECEIVE"

    elif traffic_type == "TELNET":
        timestamp += timedelta(seconds=1)
        action = "DROP"
        protocol = "TCP"
        source_ip_address = "SOURCEIP"
        destination_ip_address = server_ip
        source_port = random.randint(49152, 65535)
        destination_port = 23
        path = "RECEIVE"

    elif traffic_type == "SSH":
        timestamp += timedelta(seconds=1)
        action = "ALLOW"
        protocol = "TCP"
        source_ip_address = "SOURCEIP"
        destination_ip_address = server_ip
        source_port = random.randint(49152, 65535)
        destination_port = 22
        path = "RECEIVE"

    log_entry = f"{timestamp} {action} {protocol} {source_ip_address} {destination_ip_address} {source_port} {destination_port} {path}"
    return log_entry

def generate_worm_propagation_log(server_ip):
    x = server_ip.rsplit(".")
    timestamp = datetime.now()
    action = "ALLOW"
    protocol = "TCP"
    source_ip_address = server_ip
    source_port = random.randint(49152, 65535)
    destination_port = random.choice(["22", "23", "25", "80", "135", "139", "445", "593", "3389", "4444", "8080"])
    path = "SEND"

    log_entries = []

    for i in range(1, 256):
        if i != int(x[3]):
            destination_ip_address = f"{x[0]}.{x[1]}.{x[2]}.{i}"
            timestamp += timedelta(seconds=1)
            log_entry = f"{timestamp} {action} {protocol} {source_ip_address} {destination_ip_address} {source_port} {destination_port} {path}"
            log_entries.append(log_entry)
            if random.random() <= 0.6:
                log_entries.append(generate_regular_log_traffic(server_ip, timestamp))

    return log_entries

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Andrew Worm Simulation Firewall Log Generator')
    parser.add_argument('--server_ip', type=str, help='Server IP address', default='192.168.100.20')
    parser.add_argument('--output_file', type=str, help='Output file name', default='simulated_firewall_logs.txt')
    args = parser.parse_args()

    log_entries = generate_worm_propagation_log(args.server_ip)
    # Print log entries to console
    print(*log_entries, sep="\n")

    # Write log entries to file
    with open(args.output_file, "w") as file:
        for entry in log_entries:
            file.write(entry + "\n")

    print(f"Firewall log generated and saved as '{args.output_file}'")
