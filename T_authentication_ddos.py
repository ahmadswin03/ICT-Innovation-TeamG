import random
from datetime import datetime, timedelta
import argparse

usernames = ["alice", "bob", "charlie", "david", "eve", "frank", "grace", "henry"]
# List of random actions to simulate different types of SSH logs
log_types = [
    "Failed password",
    "Accepted password",
    "Connection closed",
    "PAM unable to",
    "Received disconnect",
    "Invalid user"
]

# Function to generate log entries
def generate_auth_log(num_attempts=100):
    base_time = datetime.now()
    log_entries = []
    
    for i in range(num_attempts):
        timestamp = (base_time + timedelta(seconds=i)).strftime('%b %d %H:%M:%S')
        ip_part = random.randint(1, 255)
        src_ip = f"192.168.1.{ip_part}"
        src_port = random.randint(1024, 65535)
        username = random.choice(usernames)
        log_type = random.choice(log_types)
        
        if log_type == "Failed password":
            log_entry = f"{timestamp} ubuntu-server sshd[{random.randint(1000, 9999)}]: Failed password for {username} from {src_ip} port {src_port} ssh2"
        elif log_type == "Accepted password":
            log_entry = f"{timestamp} ubuntu-server sshd[{random.randint(1000, 9999)}]: Accepted password for {username} from {src_ip} port {src_port} ssh2"
        elif log_type == "Connection closed":
            log_entry = f"{timestamp} ubuntu-server sshd[{random.randint(1000, 9999)}]: Connection closed by {src_ip} port {src_port} [preauth]"
        elif log_type == "PAM unable to":
            log_entry = f"{timestamp} ubuntu-server sshd[{random.randint(1000, 9999)}]: PAM unable to dlopen(pam_unix.so): Cannot open shared object file: No such file or directory"
        elif log_type == "Received disconnect":
            log_entry = f"{timestamp} ubuntu-server sshd[{random.randint(1000, 9999)}]: Received disconnect from {src_ip} port {src_port}: Bye Bye [preauth]"
        elif log_type == "Invalid user":
            log_entry = f"{timestamp} ubuntu-server sshd[{random.randint(1000, 9999)}]: Invalid user {username} from {src_ip} port {src_port}"
        
        log_entries.append(log_entry)
    
    return log_entries

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Authentication DDoS Log Generator')
    parser.add_argument('--num_attempts', type=int, help='Number of log entries to generate', default=100)
    parser.add_argument('--output_file', type=str, help='Output file name', default='auth_ddos.log')
    args = parser.parse_args()
    
    log_entries = generate_auth_log(num_attempts=args.num_attempts)
    
    with open(args.output_file, "w") as log_file:
        for log in log_entries:
            log_file.write(log + "\n")
    print(f"Authentication log generated and saved to {args.output_file}")
