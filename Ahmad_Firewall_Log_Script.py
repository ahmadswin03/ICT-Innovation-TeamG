import random
from datetime import datetime, timedelta
import argparse

def generate_authentication_backdoor_log(protocol, direction):
    # Generate random date and time within the last day
    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 1440))
    date = timestamp.strftime("%Y-%m-%d")
    time = timestamp.strftime("%H:%M:%S")
    
    # Randomize IP addresses and ports
    src_ip = f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
    dst_ip = f"10.0.{random.randint(0, 255)}.{random.randint(0, 255)}"  # Internal IP, signaling an inside target
    src_port = random.randint(1000, 65535)
    
    # Use a mix of common and uncommon destination ports
    dst_port = random.choice([22, 80, 443, 8080, random.randint(1024, 65535)])  # Standard and non-standard ports

    # Use provided protocol or default
    protocol = protocol if protocol else random.choice(['TCP', 'UDP'])
    
    # Action with weighted randomness to reflect suspicious patterns
    action = random.choices(
        ["LOGIN_SUCCESS", "LOGIN_FAILURE", "ACCESS_DENIED"], 
        weights=[0.2, 0.6, 0.2], 
        k=1
    )[0]
    
    # Flags that may correspond with backdoor behavior
    flags = random.choice(["SYN", "ACK"]) if action == "LOGIN_SUCCESS" else "RST"
    
    # Data size is randomized, with a slight emphasis on smaller packets for repeated attempts
    size = random.randint(50, 500) if action != "LOGIN_SUCCESS" else random.randint(500, 1500)
    
    # Use provided direction or default
    direction = direction if direction else random.choice(['INBOUND', 'OUTBOUND'])
    
    # Log entry in the specified format
    return f"{date} {time} | Action: {action} | Protocol: {protocol} | Src IP: {src_ip} | Dst IP: {dst_ip} | Src Port: {src_port} | Dst Port: {dst_port} | Flags: {flags} | Size: {size} | Direction: {direction}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ahmad Firewall Log Generator')
    parser.add_argument('--protocol', choices=['TCP', 'UDP'], help='Protocol type', default=None)
    parser.add_argument('--direction', choices=['INBOUND', 'OUTBOUND'], help='Traffic direction', default=None)
    args = parser.parse_args()

    # Use default values if not provided
    protocol = args.protocol if args.protocol else random.choice(['TCP', 'UDP'])
    direction = args.direction if args.direction else random.choice(['INBOUND', 'OUTBOUND'])

    # Generate backdoor-related authentication log entries
    authentication_backdoor_logs = [generate_authentication_backdoor_log(protocol, direction) for _ in range(100)]

    # Write log entries to a file
    with open("authentication_backdoor_logfile.txt", "w") as file:
        for entry in authentication_backdoor_logs:
            file.write(entry + "\n")

    print("Backdoor Authentication logs generated successfully.")
