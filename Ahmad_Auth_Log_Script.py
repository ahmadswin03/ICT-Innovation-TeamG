import random
from datetime import datetime, timedelta
import argparse

def generate_auth_log(service, username, event_type):
    # Generate random timestamp within the past day
    timestamp = (datetime.now() - timedelta(minutes=random.randint(0, 1440))).strftime("%b %d %H:%M:%S")
    
    # Hostname
    hostname = "server-host"
    
    # Process ID associated with the service
    process_id = random.randint(1000, 5000)
    
    # Action details depending on the service and event type
    if service == "sshd":
        if event_type == "accepted_password":
            auth_action = f"Accepted password for {username} from {random_ip()} port {random.randint(1024, 65535)} ssh2"
        elif event_type == "failed_password":
            auth_action = f"Failed password for {username} from {random_ip()} port {random.randint(1024, 65535)} ssh2"
        elif event_type == "connection_closed":
            auth_action = f"Connection closed by authenticating user {username} {random_ip()} port {random.randint(1024, 65535)}"
        else:
            auth_action = "Unknown event"
    elif service == "sudo":
        if event_type == "sudo_command":
            auth_action = f"{username} : TTY=pts/0 ; PWD=/home/{username} ; USER=root ; COMMAND=/bin/ls"
        else:
            auth_action = "Unknown event"
    elif service == "cron":
        auth_action = f"(CRON) INFO (pid {process_id}) session opened for user {username}"
    elif service == "systemd":
        auth_action = f"Started User Manager for UID {random.randint(1000, 5000)}"
    elif service == "su":
        auth_action = f"session opened for user {username} by (uid=0)"
    else:
        auth_action = "Unknown service"

    # Construct the log entry
    return f"{timestamp} {hostname} {service}[{process_id}]: {auth_action}"

def random_ip():
    # Helper function to generate random IP addresses
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ahmad Authentication Log Generator')
    parser.add_argument('--service', choices=['sshd', 'sudo', 'cron', 'systemd', 'su'], help='Service name', default=None)
    parser.add_argument('--username', type=str, help='Username', default=None)
    parser.add_argument('--event_type', type=str, help='Event type', default=None)
    args = parser.parse_args()

    # Use default values if not provided
    service = args.service if args.service else random.choice(['sshd', 'sudo', 'cron', 'systemd', 'su'])
    username = args.username if args.username else random.choice(['user1', 'admin', 'root'])
    event_type = args.event_type if args.event_type else 'default_event'

    # Generate authentication log entries
    auth_logs = [generate_auth_log(service, username, event_type) for _ in range(100)]

    # Write log entries to a file
    with open("auth_log.txt", "w") as file:
        for entry in auth_logs:
            file.write(entry + "\n")

    print("Authentication logs generated")
