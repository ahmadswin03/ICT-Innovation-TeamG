import random # These Python standard library modules already inrodue in my auth log simulation script.
import logging
from datetime import datetime, timedelta
import ipaddress
import uuid
import argparse
import sys # Provides access to variables and functions that interact with the Python interpreter

#  This line configures the basic settings for logging, setting the logging level to ERROR. This means that only log messages with a level of ERROR and above (such as CRITICAL) will be recorded.
logging.basicConfig(level=logging.ERROR)

# List of suspicious external IP addresses
suspicious_ips = [
    "203.0.113.10",
    "198.51.100.20",
    "192.0.2.30",
    "185.199.108.153",
    "185.199.109.153"
]

# generates a random internal IP address that falls within the private IP address ranges
def generate_internal_ip():
    first_octet = random.choice([10, 172, 192])
    if first_octet == 10:
        ip = f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    elif first_octet == 172:
        ip = f"172.{random.randint(16, 31)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    else:
        ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
    return ip

# generates a random external IP address
def generate_external_ip(use_suspicious=False):
    if use_suspicious or random.random() < 0.5: # If use_suspicious is True or a random number is less than 50%, it randomly selects a suspicious IP address from the suspicious_ips list
        return random.choice(suspicious_ips)
    else: # Otherwise, it generates a random public IP address, ensuring that the IP does not belong to private, loopback, multicast, or reserved address ranges
        while True:
            first_octet = random.randint(1, 223)
            ip_str = f"{first_octet}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
            ip = ipaddress.IPv4Address(ip_str)
            if not (ip.is_private or ip.is_loopback or ip.is_multicast or ip.is_reserved):
                return ip_str

def decide_action(protocol, source_ip, direction):
    if direction == 'RECEIVE' and source_ip in suspicious_ips: # If the direction is RECEIVE and the source IP is in the suspicious_ips list, it returns "BLOCK", indicating that the connection should be blocked.
        return "BLOCK"
    else:
        return random.choice(["ALLOW", "BLOCK"])

# Randomly generates TCP flag bits
def generate_tcp_flags():
    flags = []
    syn = random.choice([True, False])
    ack = random.choice([True, False]) if not syn else False
    fin = random.choice([True, False]) if not syn else False
    psh = random.choice([True, False])
    rst = random.choice([True, False]) if not syn and not fin else False
    urg = random.choice([True, False])

    if syn:
        flags.append("SYN")
    if ack:
        flags.append("ACK")
    if fin:
        flags.append("FIN")
    if psh:
        flags.append("PSH")
    if rst:
        flags.append("RST")
    if urg:
        flags.append("URG")

    return ','.join(flags) if flags else "NONE"

# constructs a complete log entry string containing the following fields
def construct_log_entry(timestamp, action, protocol, source_port, destination_port, size, src_ip, dst_ip, direction):
    flags = generate_tcp_flags() if protocol == "TCP" else "N/A"
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S') # YYYY-MM-DD HH:MM:SS
    log_entry = ( 
        f"{timestamp_str} Action:{action} Protocol:{protocol} "
        f"SrcIP:{src_ip} DstIP:{dst_ip} "
        f"SrcPort:{source_port} DstPort:{destination_port} "
        f"Flags:{flags} Size:{size} Direction:{direction}"
    )
    return log_entry

# Generates a destination port number based on the protocol type
def generate_destination_port(protocol):
    if protocol == "TCP":
        common_ports = [80, 443, 22, 21]
    else:  # UDP
        common_ports = [53, 123, 161]
    return random.choice(common_ports + [random.randint(1024, 65535)])

# Generates a single exfiltration attack-related log entry and returns a list of generated log entries along with the updated timestamp.
def generate_exfiltration_log(base_timestamp, protocol=None, direction=None):
    # Use user inputs or default values
    protocol = protocol if protocol else random.choice(["TCP", "UDP"])
    direction = direction if direction else random.choice(["SEND", "RECEIVE"])
    destination_port = generate_destination_port(protocol)

    # Initialise log entries list
    log_entries = []

    # Generate basic fields
    internal_ip = generate_internal_ip()
    external_ip = generate_external_ip()
    time_increment = timedelta(seconds=0)

    size = random.randint(5000, 1000000)
    source_port = random.randint(1024, 65535)

    # Determine source and destination IP based on direction
    if direction == "SEND":
        src_ip = internal_ip
        dst_ip = external_ip
    else:
        src_ip = external_ip
        dst_ip = internal_ip

    action = decide_action(protocol, src_ip, direction) # Determine whether to ALLOW or BLOCK based on protocol, source IP, and direction

    # Plus a time increment (random 1 to 5 seconds) to generate the current log entry's timestamp.
    temp_timestamp = base_timestamp + time_increment
    time_increment += timedelta(seconds=random.randint(1, 5))

    # Generate the log entry string and add it to the log_entries list.
    log_entry = construct_log_entry(
        temp_timestamp, action, protocol, source_port, destination_port,
        size, src_ip, dst_ip, direction
    )
    log_entries.append(log_entry)

    # Return log entries and updated timestamp
    return log_entries, base_timestamp + time_increment

def generate_log_entries(entry_count=100, base_timestamp=None, protocol=None, direction=None):

    if base_timestamp is None:
        base_timestamp = datetime.now()
    log_entries = []
    current_timestamp = base_timestamp
    try:
        # While the length of log_entries is less than entry_count, call generate_exfiltration_log to generate log entries and update current_timestamp.
        while len(log_entries) < entry_count:
            entries, current_timestamp = generate_exfiltration_log(
                current_timestamp,
                protocol=protocol,
                direction=direction
            )
            if len(log_entries) + len(entries) > entry_count: #  If the number of generated log entries exceeds entry_count, truncate the excess entries.
                entries = entries[:entry_count - len(log_entries)]
            log_entries.extend(entries)
    except Exception as e:
        logging.error(f"Error generating logs: {e}")
        print(f"Error generating logs: {e}")
    return log_entries

def write_logs_to_file(filename, log_entries):

    try:
        with open(filename, 'w') as file:
            for entry in log_entries:
                file.write(entry + "\n")
    except (IOError, OSError) as e:
        logging.error(f"Error writing to file: {e}")
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Exfiltration Attack Log Simulator') # Create a command-line argument parser.
    parser.add_argument('--protocol', choices=['TCP', 'UDP'], help='Protocol type', default=None)
    parser.add_argument('--direction', choices=['SEND', 'RECEIVE'], help='Traffic direction', default=None)
    args = parser.parse_args() # Parses the command-line arguments and stores them in args

    # Provide feedback on default values
    if not args.protocol:
        print("No protocol specified. Using default protocol.")
    if not args.direction:
        print("No direction specified. Using default direction.")

    # Set global base_timestamp
    base_timestamp = datetime.now() - timedelta(days=random.randint(0, 7))

    # Generate 100 simulated Exfiltration attack firewall logs
    logs = generate_log_entries(
        100,
        base_timestamp=base_timestamp,
        protocol=args.protocol,
        direction=args.direction
    )

    # Sort logs by timestamp to ensure chronological order
    try:
        # Extracts and parses the timestamp from a log entry
        def parse_timestamp(log_line):
            try:
                date_str = ' '.join(log_line.split(' ')[:2])
                timestamp = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                return timestamp
            except (IndexError, ValueError) as e:
                logging.error(f"Error parsing timestamp: {e}, log line: {log_line}")
                return None  # Exclude unparseable logs from sorting

        logs = [log for log in logs if parse_timestamp(log) is not None]
        logs.sort(key=parse_timestamp)
    except Exception as e:
        logging.error(f"Error sorting logs: {e}")
        print(f"Error sorting logs: {e}")

    # Generate a unique log file name using base_timestamp and UUID
    timestamp_str = base_timestamp.strftime("%Y%m%d_%H%M%S")
    filename = f"exfiltration_logs_{timestamp_str}_{uuid.uuid4()}.log"

    # Write logs to the generated log file
    write_logs_to_file(filename, logs)

    print(f"Simulated Exfiltration attack logs generated and written to {filename}")
