import random
from datetime import datetime, timedelta
import argparse

# Function to generate sudo privilege escalation logs
def generate_privilege_escalation_log(username=None, command_input=None):
    # Current timestamp
    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 1440))

    # Usernames to simulate escalation attempts
    usernames = ["admin", "user1", "guest", "test", "root", "vedika123"]
    username = username if username else random.choice(usernames)

    # Commands that users might try to execute with sudo
    commands = ["/bin/cat /etc/shadow", "/bin/cat /etc/passwd", "/usr/bin/apt update", "/usr/bin/vim /etc/hosts"]
    command = command_input if command_input else random.choice(commands)

    # Events: successful and failed sudo attempts
    events = [
        f"sudo: {username} : TTY=pts/{random.randint(0,5)} ; PWD=/home/{username} ; USER=root ; COMMAND={command}",
        f"sudo: {username} : {random.randint(1, 3)} incorrect password attempts ; TTY=pts/{random.randint(0,5)} ; PWD=/home/{username} ; USER=root ; COMMAND={command}"
    ]

    # Random event selection
    event = random.choice(events)

    # Generate a timestamp for the log entry
    formatted_timestamp = timestamp.strftime("%b %d %H:%M:%S")

    # Simulate a hostname or server name
    hostname = "server-1"

    # Return a complete log entry
    return f"{formatted_timestamp} {hostname} {event}"

# Function to generate multiple logs
def generate_privilege_escalation_logs(num_entries, username=None, command_input=None):
    log_entries = []
    for _ in range(num_entries):
        log_entries.append(generate_privilege_escalation_log(username, command_input))
    return log_entries

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vedika Authentication Log Generator')
    parser.add_argument('--username', type=str, help='Username')
    parser.add_argument('--command', type=str, help='Command executed')
    args = parser.parse_args()

    # Generate 100 privilege escalation log entries
    log_entries = generate_privilege_escalation_logs(100, args.username, args.command)

    # Write log entries to a file
    with open("privilege_escalation_log.txt", "w") as file:
        for entry in log_entries:
            file.write(entry + "\n")

    print("Authentication logs generated: privilege_escalation_log.txt")
