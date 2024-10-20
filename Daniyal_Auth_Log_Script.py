from datetime import datetime, timedelta
import random
import argparse

# List of usernames for brute force attempts
usernames = ["john", "doe", "mike", "sarah", "lucy", "jane", "sam", "kate"]

# Function to generate brute force log entries
def generate_brute_force_log(num_attempts=100):
    base_time = datetime.now()
    log_entries = []
    
    # Simulating repeated failed attempts from multiple IP addresses
    for i in range(num_attempts):
        timestamp = (base_time + timedelta(seconds=i)).strftime('%b %d %H:%M:%S')
        ip_part = random.randint(1, 255)  # Randomize IP address
        src_ip = f"192.168.1.{ip_part}"
        src_port = random.randint(1024, 65535)  # Random port number
        username = random.choice(usernames)  # Pick random username
        log_entry = f"{timestamp} ubuntu-server sshd[{random.randint(1000, 9999)}]: Failed password for {username} from {src_ip} port {src_port} ssh2"
        log_entries.append(log_entry)
    
    return log_entries

# Function to save the brute force log to a file
def save_brute_force_log_to_file(filename="daniyal_auth_log.txt", num_attempts=100):
    log_entries = generate_brute_force_log(num_attempts)
    with open(filename, "w") as log_file:
        for log in log_entries:
            log_file.write(log + "\n")
    print(f"Brute force authentication log generated and saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Daniyal's Authentication Log Simulator")
    parser.add_argument('--num_attempts', type=int, default=100, help='Number of authentication attempts to simulate')
    args = parser.parse_args()

    save_brute_force_log_to_file(num_attempts=args.num_attempts)

if __name__ == "__main__":
    main()
