import random # Used for generating random numbers and selecting random elements.
import datetime # Used for handling dates and times
import argparse #  Used for parsing command-line arguments

# Define main user and attacker user
main_user = 'alice'      # Main user
attack_user = 'hacker'   # Attacker's new user

# Define user UIDs
user_uids = {'alice': 1000, 'hacker': 1001}

# Define hostname
hostname = 'ubuntu-server'

# Define other global variables
local_ip = '192.168.1.10'  # Local host IP
foreign_ips = [f'203.0.113.{i}' for i in range(1, 5)]  # Suspicious external IP addresses
services = ['sshd', 'sudo', 'login', 'CRON'] # Lists possible service names, including "sshd", "sudo", "login", and "CRON"
pam_modules = ['pam_unix', 'pam_lastlog', 'pam_env', 'pam_systemd'] #Lists PAM (Pluggable Authentication Modules) module names
tty_devices = [f'/dev/tty{i}' for i in range(1, 7)] #Generates a list of TTY device paths

def generate_timestamps(num_entries, start_time):
    # Generate a list of sequential timestamps, each entry 1 to 10 seconds apart
    timestamps = []
    for i in range(num_entries):
        if i == 0:
            timestamps.append(start_time)
        else:
            timestamps.append(timestamps[-1] + datetime.timedelta(seconds=random.randint(1, 10))) # Generate a series of sequential timestamps, each spaced 1 to 10 seconds apart randomly
    return timestamps

def generate_pam_auth_log(timestamp, user):
    service = random.choice(['login', 'sshd', 'sudo'])
    pam_module = random.choice(pam_modules)
    pid = random.randint(1000, 9999)
    # Creates the first log entry indicating that PAM failed to load the specified module.
    log_entry = '{} {} {}[{}]: PAM unable to dlopen({}.so): {}\n'.format(
        timestamp.strftime('%b %d %H:%M:%S'),
        hostname,
        service,
        pid,
        pam_module,
        'Cannot open shared object file: No such file or directory'
    )
    # Appends a second log entry to the first one, indicating that PAM is adding a faulty
    log_entry += '{} {} {}[{}]: PAM adding faulty module: {}.so\n'.format(
        timestamp.strftime('%b %d %H:%M:%S'),
        hostname,
        service,
        pid,
        pam_module
    )
    return log_entry 

def generate_cron_log(timestamp, user):
    uid = user_uids.get(user, 1000)
    session_action = random.choice(['opened', 'closed'])
    pid = random.randint(1000, 9999)
    # Generate log entries for the CRON service, recording the opening or closing of CRON sessions
    log_entry = '{} {} CRON[{}]: pam_unix(cron:session): session {} for user {}(uid={}) by (uid=0)\n'.format(
        timestamp.strftime('%b %d %H:%M:%S'),
        hostname,
        pid,
        session_action,
        user,
        uid
    )
    return log_entry

def generate_login_failure_log(timestamp, user):
    tty = random.choice(tty_devices)
    pid = random.randint(1000, 9999)
    attempt_number = random.randint(1, 5)
    # Generate log entries for failed login attempts.
    log_entry = "{} {} login[{}]: FAILED LOGIN ({}) on '{}' FOR '{}', Authentication failure\n".format(
        timestamp.strftime('%b %d %H:%M:%S'),
        hostname,
        pid,
        attempt_number,
        tty,
        user
    )
    return log_entry

def generate_sudo_log(timestamp, user, uid, success=True):
    pid = random.randint(1000, 9999)
    if success:
        session_action = random.choice(['opened', 'closed'])
        log_entry = '{} {} sudo: pam_unix(sudo:session): session {} for user root(uid=0) by {}(uid={})\n'.format(
            timestamp.strftime('%b %d %H:%M:%S'),
            hostname,
            session_action,
            user,
            uid
        )
    else:
        # Unauthorised sudo attempt
        log_entry = '{} {} sudo: pam_unix(sudo:auth): authentication failure; logname={} uid={} euid={} tty=/dev/pts/{} ruser={} rhost=  user={}\n'.format(
            timestamp.strftime('%b %d %H:%M:%S'),
            hostname,
            user,
            uid,
            uid,
            random.randint(0, 10),
            user,
            user
        )
    return log_entry

def generate_useradd_log(timestamp, new_user):
    pid = random.randint(1000, 9999)
    uid = user_uids.get(new_user, 1001)
    # Generate log entries for adding new users, recording detailed information about the new user such as username, UID, GID, home directory, and shell
    log_entry = '{} {} useradd[{}]: new user: name={}, UID={}, GID={}, home=/home/{}, shell=/bin/bash\n'.format(
        timestamp.strftime('%b %d %H:%M:%S'),
        hostname,
        pid,
        new_user,
        uid,
        uid,
        new_user
    )
    return log_entry

def generate_usermod_log(timestamp, new_user):
    pid = random.randint(1000, 9999)
    #  Generate log entries for modifying users, recording the addition of the new user to the 'sudo' group
    log_entry = "{} {} usermod[{}]: add '{}' to group 'sudo'\n".format(
        timestamp.strftime('%b %d %H:%M:%S'),
        hostname,
        pid,
        new_user
    )
    return log_entry

def generate_ssh_port_forwarding_log(timestamp, user, ip):
    pid = random.randint(1000, 9999)
    # Generate SSH port forwarding log entries, recording requests to forward remote ports
    log_entry = '{} {} sshd[{}]: Received request to forward remote port {} to {}\n'.format(
        timestamp.strftime('%b %d %H:%M:%S'),
        hostname,
        pid,
        random.randint(8000, 9000),
        ip
    )
    return log_entry

def generate_ssh_login_attempt(timestamp, user, ip, success=True):
    port = random.randint(1024, 65535)
    pid = random.randint(1000, 9999)
    if success:
        outcome = 'Accepted password'
        log_entry = '{} {} sshd[{}]: {} for {} from {} port {} ssh2\n'.format(
            timestamp.strftime('%b %d %H:%M:%S'),
            hostname,
            pid,
            outcome,
            user,
            ip,
            port
        )
    else:
        outcome = 'Failed password'
        log_entry = '{} {} sshd[{}]: {} for {} from {} port {} ssh2\n'.format(
            timestamp.strftime('%b %d %H:%M:%S'),
            hostname,
            pid,
            outcome,
            user,
            ip,
            port
        )
        # Add connection closed log
        log_entry += '{} {} sshd[{}]: Connection closed by {} port {} [preauth]\n'.format(
            timestamp.strftime('%b %d %H:%M:%S'),
            hostname,
            pid,
            ip,
            port
        )
    return log_entry

def main():
    # Uses the argparse module to create a command-line argument parser
    parser = argparse.ArgumentParser(description="BDAuthScript Authentication Log Simulator")
    parser.add_argument('--num_entries', type=int, default=200, help='Number of log entries to generate')
    parser.add_argument('--service', type=str, help='Service name (e.g., sshd, sudo, login, CRON)')
    parser.add_argument('--username', type=str, help='Username for authentication events')
    parser.add_argument('--event_type', type=str, help='Type of authentication event (e.g., login_success, login_failure)')
    args = parser.parse_args() # Parses the command-line arguments and stores them in the args variable
    
    # Assigns the parsed arguments to corresponding variables
    num_entries = args.num_entries  # Use the provided number of entries
    service = args.service
    username = args.username
    event_type = args.event_type

    # Validate service if provided
    if service and service not in services:
        print(f"Invalid service: {service}. Must be one of {services}.")
        return

    # Validate event_type if provided
    valid_event_types = {
        'sshd': ['login_success', 'login_failure', 'connection_closed'],
        'sudo': ['sudo_usage'],
        'login': ['login_success', 'login_failure'],
        'CRON': ['cron_event']
    }

    if event_type:
        if not service:
            print("Event type specified without service. Please specify the service.")
            return
        if event_type not in valid_event_types.get(service, []):
            print(f"Invalid event_type '{event_type}' for service '{service}'. Valid options: {valid_event_types.get(service, [])}")
            return

    # Get current time and generate log filename
    current_time = datetime.datetime.now()
    log_filename = 'auth' + current_time.strftime('%Y%m%d%H%M%S') + '.log'
    
    start_time = datetime.datetime.now().replace(hour=1, minute=0, second=0, microsecond=0) # Sets the start time for log generation to 1:00 AM of the current day, mock the attack time
    timestamps = generate_timestamps(num_entries, start_time)
    
    # Simulate multiple authentication failures and abnormal logins before the attack
    attack_phase = False
    attack_started = False
    failure_count = 0

    # Opens the log file in write mode.
    with open(log_filename, 'w') as log_file:
        for i, timestamp in enumerate(timestamps): # Iterates over each generated timestamp to create corresponding log entries
            if not attack_started and random.random() < 0.1:
                # Start simulating an attack
                attack_phase = True
                attack_started = True
                # Attacker leverages a vulnerability or has obtained credentials
                # Generate a log entry for disconnect
                log_entry = '{} {} sshd[{}]: Received disconnect from {} port {}: 11: Bye Bye [preauth]\n'.format(
                    timestamp.strftime('%b %d %H:%M:%S'),
                    hostname,
                    random.randint(1000, 9999),
                    random.choice(foreign_ips),
                    random.randint(1024, 65535)
                )
                log_file.write(log_entry)
                # Attacker successfully logs in as alice
                log_entry = generate_ssh_login_attempt(timestamp + datetime.timedelta(seconds=5), main_user, random.choice(foreign_ips), success=True)
                log_file.write(log_entry)
                # Attacker creates a new user
                new_user = attack_user
                log_entry = generate_useradd_log(timestamp + datetime.timedelta(minutes=1), new_user)
                log_file.write(log_entry)
                log_entry = generate_usermod_log(timestamp + datetime.timedelta(minutes=2), new_user)
                log_file.write(log_entry)
                # Attacker successfully uses sudo with the new user
                log_entry = generate_sudo_log(timestamp + datetime.timedelta(minutes=3), new_user, user_uids[new_user], success=True)
                log_file.write(log_entry)
                # Attacker uses SSH port forwarding
                log_entry = generate_ssh_port_forwarding_log(timestamp + datetime.timedelta(minutes=4), new_user, random.choice(foreign_ips))
                log_file.write(log_entry)
                attack_phase = False  # End of attack phase
            else:
                # Normal system activity logs
                if random.random() < 0.8: # 80% chance to generate attack traffic
                    log_type = random.choice([
                        'pam_auth',
                        'cron',
                        'sudo',
                        'ssh_login'
                    ])
                    if service and service != log_type:
                        # If a specific service is specified, skip unrelated log types
                        continue
                    if log_type == 'pam_auth':
                        if username:
                            log_entry = generate_pam_auth_log(timestamp, username)
                        else:
                            log_entry = generate_pam_auth_log(timestamp, main_user)
                    elif log_type == 'cron':
                        log_entry = generate_cron_log(timestamp, main_user)
                    elif log_type == 'sudo':
                        if username:
                            log_entry = generate_sudo_log(timestamp, username, user_uids.get(username, 1000), success=True)
                        else:
                            log_entry = generate_sudo_log(timestamp, main_user, user_uids[main_user], success=True)
                    elif log_type == 'ssh_login':
                        if username:
                            log_entry = generate_ssh_login_attempt(timestamp, username, local_ip, success=True)
                        else:
                            log_entry = generate_ssh_login_attempt(timestamp, main_user, local_ip, success=True)
                else:
                    # Occasionally simulate failed login attempts
                    if service == 'sshd' and event_type == 'login_failure' and username:
                        log_entry = generate_ssh_login_attempt(timestamp, username, local_ip, success=False)
                    else:
                        log_entry = generate_ssh_login_attempt(timestamp, main_user, local_ip, success=False)
                log_file.write(log_entry)

    print(f"Log file '{log_filename}' has been generated.")

if __name__ == "__main__":
    main()
