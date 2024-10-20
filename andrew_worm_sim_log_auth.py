import random
from datetime import datetime, timedelta
import argparse

def generate_regular_authlog_entry(timestamp):
    traffic_type = random.choice([
        "reg_success_logon", "failed_login", "sudo_usage", "ssh_key_auth",
        "ssh_session_closed", "system_reboot", "user_switch", "password_changes"
    ])

    if traffic_type == "reg_success_logon":
        hostname = "localhost"
        service_name = "sshd"
        process_id = "12345"
        message = "Accepted password for admin from 192.168.1.100 port 51234 ssh2"

    elif traffic_type == "failed_login":
        hostname = "localhost"
        service_name = "sshd"
        process_id = "12345"
        message = "Failed password for invalid user guest from 192.168.1.101 port 51235 ssh2"

    elif traffic_type == "sudo_usage":
        hostname = "localhost"
        service_name = "sudo"
        process_id = "user1"
        message = "TTY=pts/0 ; PWD=/home/user1 ; USER=root ; COMMAND=/bin/ls"

    elif traffic_type == "ssh_key_auth":
        hostname = "localhost"
        service_name = "sshd"
        process_id = "12345"
        message = "Accepted publickey for user1 from 192.168.1.100 port 51234 ssh2: RSA SHA256:"

    elif traffic_type == "ssh_session_closed":
        hostname = "localhost"
        service_name = "sshd"
        process_id = "12345"
        message = "pam_unix(sshd:session): session closed for user user1"

    elif traffic_type == "system_reboot":
        hostname = "localhost"
        service_name = "systemd-logind"
        process_id = "1234"
        message = "System is rebooting."

    elif traffic_type == "user_switch":
        hostname = "localhost"
        service_name = "su:"
        process_id = ""
        message = "(to root) user1 on pts/0"

    elif traffic_type == "password_changes":
        hostname = "localhost"
        service_name = "passwd"
        process_id = "11333"
        message = "pam_unix(passwd:chauthtok): password changed for user1"

    log_entry = f"{timestamp} {hostname} {service_name}[{process_id}]: {message}"
    return log_entry

def generate_worm_propagation_authlog_entry(timestamp):
    attack_variance = random.choice([
        "failed_sus_login", "success_unauth_access", "new_user",
        "privilege_escalation", "config_change", "abnormal_logouts"
    ])

    if attack_variance == "failed_sus_login":
        hostname = "localhost"
        service_name = "sshd"
        process_id = "1234"
        message = "Failed password for root from 192.168.1.10 port 54457 ssh2"

    elif attack_variance == "success_unauth_access":
        hostname = "localhost"
        service_name = "sshd"
        process_id = "6789"
        message = "Accepted password for root from 192.168.1.10 port 54458 ssh2"

    elif attack_variance == "new_user":
        hostname = "localhost"
        service_name = "useradd"
        process_id = "7890"
        message = "new user: name='wormuser', UID=1002, GID=1002, home=/home/wormuser"

    elif attack_variance == "privilege_escalation":
        hostname = "localhost"
        service_name = "sudo"
        process_id = ""
        message = "wormuser : TTY=pts/1 ; PWD=/home/wormuser ; USER=root ; COMMAND=/bin/bash"

    elif attack_variance == "config_change":
        hostname = "localhost"
        service_name = "sshd"
        process_id = "7892"
        message = "Received signal 15; terminating."

    elif attack_variance == "abnormal_logouts":
        hostname = "localhost"
        service_name = "sshd"
        process_id = "8901"
        message = "Received disconnect from 192.168.1.10: 11: Bye Bye [preauth]"

    log_entry = f"{timestamp} {hostname} {service_name}[{process_id}]: {message}"
    return log_entry

def generate_simulation_auth_log(num_entries):
    log_entries = []
    timestamp = datetime.now()

    for _ in range(num_entries):
        timestamp += timedelta(seconds=0.7)
        log_entries.append(generate_regular_authlog_entry(timestamp))
        if random.random() <= 0.2:
            timestamp += timedelta(seconds=0.7)
            log_entries.append(generate_worm_propagation_authlog_entry(timestamp))

    return log_entries

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Andrew Worm Simulation Authentication Log Generator')
    parser.add_argument('--num_entries', type=int, help='Number of log entries to generate', default=20)
    parser.add_argument('--output_file', type=str, help='Output file name', default='simulated_authentication_logs.txt')
    args = parser.parse_args()

    log_entries = generate_simulation_auth_log(args.num_entries)
    # Print log entries to console
    print(*log_entries, sep="\n")

    # Write log entries to file
    with open(args.output_file, "w") as file:
        for entry in log_entries:
            file.write(entry + "\n")

    print(f"Authentication log generated and saved to '{args.output_file}'")
