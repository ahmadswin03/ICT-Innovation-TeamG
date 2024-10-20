import random
import time
import argparse

# Function to generate a random IP address
def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

# Function to generate a random port number
def generate_port():
    return random.randint(20, 65535)

# Function to generate random flags for TCP
def generate_tcp_flags():
    flags = ["SYN", "ACK", "PSH", "FIN", "URG", "RST"]
    return random.sample(flags, random.randint(1, 3))

# Function to simulate a log entry with both TCP and UDP
def generate_log_entry():
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    src_ip = generate_ip()
    dst_ip = generate_ip()
    src_port = generate_port()
    dst_port = generate_port()
    
    # Randomly choose whether the action is BLOCK or ALLOW
    action = random.choice(["BLOCK", "ALLOW"])
    
    # Randomly choose between TCP and UDP for each entry
    protocol = random.choice(["TCP", "UDP"])
    
    # Common protocols for UDP include DNS (port 53), SNMP (port 161), etc.
    if protocol == "UDP":
        # For UDP, no flags are needed
        flags = "N/A"
        
        # Simulate realistic UDP traffic sizes (smaller packet sizes generally)
        size = random.randint(50, 50000)  # UDP tends to have smaller packets
        
    else:  # For TCP traffic
        flags = ",".join(generate_tcp_flags())
        
        # Simulate TCP packet size (larger, more variable)
        size = random.randint(500, 1000000)
    
    # Direction of the traffic
    direction = random.choice(["RECEIVE", "SEND"])
    
    # Return formatted log entry
    log_entry = (
        f"{timestamp} Action:{action} Protocol:{protocol} "
        f"SrcIP:{src_ip} DstIP:{dst_ip} SrcPort:{src_port} "
        f"DstPort:{dst_port} Flags:{flags} Size:{size} Direction:{direction}"
    )
    return log_entry

# Function to simulate firewall logs and write them to a file
def simulate_firewall_logs(file_name, num_entries=100):
    log_entries = [generate_log_entry() for _ in range(num_entries)]
    
    # Write log entries to the file
    with open(file_name, "w") as log_file:
        log_file.write("\n".join(log_entries))
    
    print(f"Firewall log generated: {file_name}")

def main():
    parser = argparse.ArgumentParser(description="Daniyal's Firewall Log Simulator")
    parser.add_argument('--num_entries', type=int, default=100, help='Number of firewall log entries to generate')
    args = parser.parse_args()

    simulate_firewall_logs("daniyal_firewall_log.txt", num_entries=args.num_entries)

if __name__ == "__main__":
    main()
