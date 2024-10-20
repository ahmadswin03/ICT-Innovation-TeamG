import random
from datetime import datetime
import argparse

# Function to generate a log entry
def generate_log_entry(action, protocol, src_ip, dst_ip, src_port, dst_port, flags, size, direction):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"{timestamp}  Action: {action}  Protocol: {protocol}  Src IP: {src_ip}  Dst IP: {dst_ip}  Src Port: {src_port}  Dst Port: {dst_port}  Flags: {flags}  Size: {size}  Direction: {direction}"

# Function to generate a random IP address
def random_ip(prefix="192.168.1."):
    return prefix + str(random.randint(1, 255))

# Function to generate a DDoS attack (many blocked requests)
def generate_ddos_attack(dst_ip, num_entries=10):
    attack_log = []
    for i in range(num_entries):
        src_ip = random_ip(prefix="192.168.100.")  # Use a different prefix for attack IPs
        src_port = random.randint(65000, 65535)
        log_entry = generate_log_entry("BLOCK", "UDP", src_ip, dst_ip, src_port, 80, "", 1024, "SEND")
        attack_log.append(log_entry)
    return attack_log

# Function to generate normal traffic
def generate_normal_traffic(num_entries=10):
    normal_log = []
    for _ in range(num_entries):
        action = random.choice(["ALLOW", "BLOCK"])
        protocol = random.choice(["TCP", "UDP"])
        src_ip = random_ip()
        dst_ip = "10.0.0." + str(random.randint(1, 10))
        src_port = random.randint(10000, 60000)
        dst_port = random.choice([80, 443, 53])
        flags = random.choice(["SYN", "ACK", ""])
        size = random.randint(512, 2048)
        direction = random.choice(["SEND", "RECEIVE"])
        log_entry = generate_log_entry(action, protocol, src_ip, dst_ip, src_port, dst_port, flags, size, direction)
        normal_log.append(log_entry)
    return normal_log

# Main function to generate the firewall log
def generate_firewall_log(dst_ip=None, total_entries=50, output_file="firewall_log.log"):
    log_entries = []
    
    # Use provided dst_ip or default
    dst_ip = dst_ip if dst_ip else "10.0.0.5"
    
    # Number of entries per section
    normal_entries = total_entries // 5
    attack_entries = normal_entries
    
    # Generate initial normal traffic
    log_entries.extend(generate_normal_traffic(normal_entries))
    
    # Simulate a DDoS attack (flood of blocked requests)
    log_entries.extend(generate_ddos_attack(dst_ip, attack_entries))
    
    # Resume normal traffic after attack
    log_entries.extend(generate_normal_traffic(normal_entries))
    
    # Another wave of attack traffic
    log_entries.extend(generate_ddos_attack(dst_ip, attack_entries))
    
    # Final normal traffic
    log_entries.extend(generate_normal_traffic(normal_entries))
    
    # Write the log entries to a file
    with open(output_file, "w") as log_file:
        for log in log_entries:
            log_file.write(log + "\n")
    
    print(f"Firewall log generated and saved as '{output_file}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Firewall DDoS Log Generator')
    parser.add_argument('--dst_ip', type=str, help='Destination IP address of the attack')
    parser.add_argument('--total_entries', type=int, help='Total number of log entries to generate', default=50)
    parser.add_argument('--output_file', type=str, help='Output file name', default='firewall_log.log')
    args = parser.parse_args()
    
    generate_firewall_log(dst_ip=args.dst_ip, total_entries=args.total_entries, output_file=args.output_file)
