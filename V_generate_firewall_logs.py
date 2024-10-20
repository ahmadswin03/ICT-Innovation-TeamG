import random
from datetime import datetime, timedelta
import argparse

def generate_firewall_priv_escalation_log(ip_address=None, event=None):
    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 1440))

    # Use provided IP address or generate a random one
    if ip_address:
        ip_address = ip_address
    else:
        ip_address = f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"

    # List of possible usernames
    usernames = ["admin", "user1", "guest", "test", "root"]
    username = random.choice(usernames)

    # Use provided event or select one based on probability
    if event:
        event = event
    else:
        event = random.choices(
            ["privilege_escalation_success", "privilege_escalation_failure"],
            weights=[0.3, 0.7],
            k=1
        )[0]

    return f"{timestamp}, {ip_address}, {event}, {username}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vedika Firewall Log Generator')
    parser.add_argument('--ip_address', type=str, help='IP Address')
    parser.add_argument('--event', choices=['privilege_escalation_success', 'privilege_escalation_failure'], help='Event type')
    args = parser.parse_args()

    # Generate 100 log entries
    log_entries = [generate_firewall_priv_escalation_log(args.ip_address, args.event) for _ in range(100)]

    # Write log entries to a file and print them to the console
    log_filename = "firewall_priv_escalation_logs.txt"
    with open(log_filename, "w") as file:
        for entry in log_entries:
            file.write(entry + "\n")

    print(f"Privilege escalation log file generated: {log_filename}")
