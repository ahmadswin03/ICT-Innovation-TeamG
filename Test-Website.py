import os  # Provides functions for interacting with the operating system, such as file path operations.
import subprocess  # Used to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
import glob  # Used for filename pattern matching, finding all the pathnames matching a specified pattern.
from dash import dcc, html, Input, Output, State
import dash

# Initialize Dash app
app = dash.Dash(__name__)

# Page layout
app.layout = html.Div([
    # Area 1: BoRui's ExfiltrationAttack.py(firewall log) and BDAuthScript.py
    html.Div([
        html.H1("Exfiltration Attack's Firewall Log Simulator"),
        html.P("Customise this firewall log generation:"),

        # Firewall log input fields
        html.Div([
            html.Label("Protocol:"),
            dcc.Dropdown(
                id='firewall-protocol',
                options=[
                    {'label': 'TCP', 'value': 'TCP'},
                    {'label': 'UDP', 'value': 'UDP'}
                ],
                placeholder='Select Protocol'
            ),
            html.Label("Direction:"),
            dcc.Dropdown(
                id='firewall-direction',
                options=[
                    {'label': 'SEND', 'value': 'SEND'},
                    {'label': 'RECEIVE', 'value': 'RECEIVE'}
                ],
                placeholder='Select Direction'
            ),
            html.Button('Generate Firewall Log', id='generate-firewall-button', n_clicks=0)
        ], style={'margin-bottom': '20px'}),

        html.H2("Firewall Log Output"),
        dcc.Textarea(
            id='firewall-log-output',
            value='',
            style={'width': '100%', 'height': 300}
        ),

        html.P("Customise this authentication log generation:"),

        # Authentication log input fields
        html.Div([
            html.Label("Service:"),
            dcc.Dropdown(
                id='auth-service',
                options=[
                    {'label': 'SSH', 'value': 'sshd'},
                    {'label': 'Sudo', 'value': 'sudo'},
                    {'label': 'Login', 'value': 'login'},
                    {'label': 'CRON', 'value': 'CRON'}
                ],
                placeholder='Select Service'
            ),
            html.Label("Username:"),
            dcc.Input(
                id='auth-username',
                type='text',
                placeholder='Username'
            ),
            html.Label("Event Type:"),
            dcc.Dropdown(
                id='auth-event-type',
                options=[],
                placeholder='Select Event Type'
            ),
            # Added Number of Entries Input Field
            html.Label("Number of Entries:"),
            dcc.Input(
                id='auth-num-entries',
                type='number',
                placeholder='Number of Entries',
                min=1,
                step=1
            ),
            html.Button('Generate Authentication Log', id='generate-auth-button', n_clicks=0)
        ]),

        html.H2("Authentication Log Output"),
        dcc.Textarea(
            id='auth-log-output',
            value='',
            style={'width': '100%', 'height': 300}
        )
    ], style={'border': '1px solid black', 'padding': '10px', 'margin-bottom': '20px'}),

    # Area 2: Ahmad's firewall log simulation script and authentication log simulation script.
    html.Div([
        html.H1("Back Door Attack's Firewall Log Simulator"),
        html.P("Customize this firewall log generation:"),

        # Ahmad's Firewall log input fields
        html.Div([
            html.Label("Protocol:"),
            dcc.Dropdown(
                id='ahmad-firewall-protocol',
                options=[
                    {'label': 'TCP', 'value': 'TCP'},
                    {'label': 'UDP', 'value': 'UDP'}
                ],
                placeholder='Select Protocol'
            ),
            html.Label("Direction:"),
            dcc.Dropdown(
                id='ahmad-firewall-direction',
                options=[
                    {'label': 'INBOUND', 'value': 'INBOUND'},
                    {'label': 'OUTBOUND', 'value': 'OUTBOUND'}
                ],
                placeholder='Select Direction'
            ),
            html.Button('Generate the Firewall Log', id='generate-ahmad-firewall-button', n_clicks=0)
        ], style={'margin-bottom': '20px'}),

        html.H2("Firewall Log Output"),
        dcc.Textarea(
            id='ahmad-firewall-log-output',
            value='',
            style={'width': '100%', 'height': 300}
        ),

        html.P("Customise this authentication log generation:"),

        # Ahmad's Authentication log input fields
        html.Div([
            html.Label("Service:"),
            dcc.Dropdown(
                id='ahmad-auth-service',
                options=[
                    {'label': 'SSH', 'value': 'sshd'},
                    {'label': 'Sudo', 'value': 'sudo'},
                    {'label': 'Cron', 'value': 'cron'},
                    {'label': 'Systemd', 'value': 'systemd'},
                    {'label': 'Su', 'value': 'su'}
                ],
                placeholder='Select Service'
            ),
            html.Label("Username:"),
            dcc.Input(
                id='ahmad-auth-username',
                type='text',
                placeholder='Username'
            ),
            html.Label("Event Type:"),
            dcc.Dropdown(
                id='ahmad-auth-event-type',
                options=[],
                placeholder='Select Event Type'
            ),
            html.Button('Generate the Authentication Log', id='generate-ahmad-auth-button', n_clicks=0)
        ]),

        html.H2("Authentication Log Output"),
        dcc.Textarea(
            id='ahmad-auth-log-output',
            value='',
            style={'width': '100%', 'height': 300}
        )
    ], style={'border': '1px solid black', 'padding': '10px', 'margin-bottom': '20px'}),

    # Area 3: Vedika's scripts
    html.Div([
        html.H1("Privilege escalation's Log Simulator"),
        html.P("Customise this firewall log generation:"),

        # Vedika's Firewall log input fields
        html.Div([
            html.Label("IP Address:"),
            dcc.Input(
                id='vedika-firewall-ip',
                type='text',
                placeholder='e.g., 192.168.1.1'
            ),
            html.Label("Event:"),
            dcc.Dropdown(
                id='vedika-firewall-event',
                options=[
                    {'label': 'Privilege Escalation Success', 'value': 'privilege_escalation_success'},
                    {'label': 'Privilege Escalation Failure', 'value': 'privilege_escalation_failure'}
                ],
                placeholder='Select Event'
            ),
            html.Button('Generate Firewall Log', id='generate-vedika-firewall-button', n_clicks=0)
        ], style={'margin-bottom': '20px'}),

        html.H2("Firewall Log Output"),
        dcc.Textarea(
            id='vedika-firewall-log-output',
            value='',
            style={'width': '100%', 'height': 300}
        ),

        html.P("Customise this authentication log generation:"),

        # Vedika's Authentication log input fields
        html.Div([
            html.Label("Username:"),
            dcc.Input(
                id='vedika-auth-username',
                type='text',
                placeholder='Username'
            ),
            html.Label("Command:"),
            dcc.Input(
                id='vedika-auth-command',
                type='text',
                placeholder='Command'
            ),
            html.Button('Generate Authentication Log', id='generate-vedika-auth-button', n_clicks=0)
        ]),

        html.H2("Authentication Log Output"),
        dcc.Textarea(
            id='vedika-auth-log-output',
            value='',
            style={'width': '100%', 'height': 300}
        )
    ], style={'border': '1px solid black', 'padding': '10px', 'margin-bottom': '20px'}),

    # Area 4: Tee Mea's scripts
    html.Div([
        html.H1("DDOS Attack's Log Simulator"),
        html.P("Customise the firewall log generation:"),

        # Tee Mea's Firewall log input fields
        html.Div([
            html.Label("Destination IP:"),
            dcc.Input(
                id='tee-mea-firewall-dst-ip',
                type='text',
                placeholder='e.g., 10.0.0.5'
            ),
            html.Label("Total Entries:"),
            dcc.Input(
                id='tee-mea-firewall-total-entries',
                type='number',
                placeholder='Total Entries'
            ),
            html.Button('Generate Firewall Log', id='generate-tee-mea-firewall-button', n_clicks=0)
        ], style={'margin-bottom': '20px'}),

        html.H2("Firewall Log Output"),
        dcc.Textarea(
            id='tee-mea-firewall-log-output',
            value='',
            style={'width': '100%', 'height': 300}
        ),

        html.P("Customise the authentication log generation:"),

        # Tee Mea's Authentication log input fields
        html.Div([
            html.Label("Number of Attempts:"),
            dcc.Input(
                id='tee-mea-auth-num-attempts',
                type='number',
                placeholder='Number of Attempts'
            ),
            html.Button('Generate Authentication Log', id='generate-tee-mea-auth-button', n_clicks=0)
        ]),

        html.H2("Authentication Log Output"),
        dcc.Textarea(
            id='tee-mea-auth-log-output',
            value='',
            style={'width': '100%', 'height': 300}
        )
    ], style={'border': '1px solid black', 'padding': '10px', 'margin-bottom': '20px'}),

    # Area 5: Andrew's scripts
    html.Div([
        html.H1("Worm Attack's Log Simulator"),
        html.P("Customise the firewall log generation:"),

        # Andrew's Firewall log input fields
        html.Div([
            html.Label("Server IP:"),
            dcc.Input(
                id='andrew-firewall-server-ip',
                type='text',
                placeholder='e.g., 192.168.100.20'
            ),
            html.Button('Generate Firewall Log', id='generate-andrew-firewall-button', n_clicks=0)
        ], style={'margin-bottom': '20px'}),

        html.H2("Firewall Log Output"),
        dcc.Textarea(
            id='andrew-firewall-log-output',
            value='',
            style={'width': '100%', 'height': 300}
        ),

        html.P("Customise the authentication log generation:"),

        # Andrew's Authentication log input fields
        html.Div([
            html.Label("Number of Entries:"),
            dcc.Input(
                id='andrew-auth-num-entries',
                type='number',
                placeholder='Number of Entries'
            ),
            html.Button('Generate Authentication Log', id='generate-andrew-auth-button', n_clicks=0)
        ]),

        html.H2("Authentication Log Output"),
        dcc.Textarea(
            id='andrew-auth-log-output',
            value='',
            style={'width': '100%', 'height': 300}
        )
    ], style={'border': '1px solid black', 'padding': '10px'}),

    # Area 6: Daniyal's scripts
    html.Div([
        html.H1("Password Cracking Log Simulator"),
        html.P("Customise this firewall log generation:"),

        # Daniyal's Firewall log input fields
        html.Div([
            html.Label("Source IP:"),
            dcc.Input(
                id='daniyal-firewall-src-ip',
                type='text',
                placeholder='e.g., 172.16.0.1'
            ),
            html.Label("Event Type:"),
            dcc.Dropdown(
                id='daniyal-firewall-event-type',
                options=[
                    {'label': 'Data Exfiltration', 'value': 'data_exfiltration'},
                    {'label': 'Unauthorized Access', 'value': 'unauthorized_access'}
                ],
                placeholder='Select Event Type'
            ),
            html.Button('Generate Firewall Log', id='generate-daniyal-firewall-button', n_clicks=0)
        ], style={'margin-bottom': '20px'}),

        html.H2("Firewall Log Output"),
        dcc.Textarea(
            id='daniyal-firewall-log-output',
            value='',
            style={'width': '100%', 'height': 300}
        ),

        html.P("Customise this authentication log generation:"),

        # Daniyal's Authentication log input fields
        html.Div([
            html.Label("Username:"),
            dcc.Input(
                id='daniyal-auth-username',
                type='text',
                placeholder='Username'
            ),
            html.Label("Action:"),
            dcc.Input(
                id='daniyal-auth-action',
                type='text',
                placeholder='Action'
            ),
            html.Button('Generate Authentication Log', id='generate-daniyal-auth-button', n_clicks=0)
        ]),

        html.H2("Authentication Log Output"),
        dcc.Textarea(
            id='daniyal-auth-log-output',
            value='',
            style={'width': '100%', 'height': 300}
        )
    ], style={'border': '1px solid black', 'padding': '10px', 'margin-bottom': '20px'})
])

# Dynamic update of event type options (Area 1)
@app.callback( # Updates the options of the "Event Type" dropdown based on the service selected by the user in the "Service" dropdown.

    Output('auth-event-type', 'options'), # 0utput to the options property of the dropdown with id='auth-event-type'
    [Input('auth-service', 'value')] # Triggered by changes in the value property of the dropdown with id='auth-service'
)
def update_event_type_options(service):
    if service == 'sshd': # Service type selected by the user from the "Service" drop-down menu.
        return [
            {'label': 'Login Success', 'value': 'login_success'},
            {'label': 'Login Failure', 'value': 'login_failure'}
        ]
    elif service == 'sudo':
        return [
            {'label': 'Sudo Usage', 'value': 'sudo_usage'}
        ]
    elif service == 'login':
        return [
            {'label': 'Login Success', 'value': 'login_success'},
            {'label': 'Login Failure', 'value': 'login_failure'}
        ]
    elif service == 'CRON':
        return [
            {'label': 'Cron Event', 'value': 'cron_event'}
        ]
    else:
        return []

# Dynamic update of event type options (Area 2)
@app.callback(
    Output('ahmad-auth-event-type', 'options'),
    [Input('ahmad-auth-service', 'value')]
)
def update_ahmad_event_type_options(service):
    if service == 'sshd':
        return [
            {'label': 'Accepted Password', 'value': 'accepted_password'},
            {'label': 'Failed Password', 'value': 'failed_password'},
            {'label': 'Connection Closed', 'value': 'connection_closed'}
        ]
    elif service == 'sudo':
        return [
            {'label': 'Sudo Command', 'value': 'sudo_command'}
        ]
    elif service == 'cron':
        return [
            {'label': 'Cron Session', 'value': 'cron_session'}
        ]
    elif service == 'systemd':
        return [
            {'label': 'Started User Manager', 'value': 'started_user_manager'}
        ]
    elif service == 'su':
        return [
            {'label': 'Session Opened', 'value': 'session_opened'}
        ]
    else:
        return []

# Callback function: Generate firewall log and display results (Area 1)
@app.callback( #When the user clicks the "Generate Firewall Log" button, this callback function runs the ExfiltrationAttack.py script to generate firewall logs and displays the generated log content in the "Firewall Log Output" area on the page
    Output('firewall-log-output', 'value'),
    [Input('generate-firewall-button', 'n_clicks')],
    [State('firewall-protocol', 'value'),
     State('firewall-direction', 'value')]
)
def update_firewall_output(n_clicks, protocol, direction):
    if n_clicks > 0: # Executes the log generation logic only if the button has been clicked at least once
        try:
            # Get the absolute path of the target script
            script_path = os.path.abspath('Python/ExfiltrationAttack.py')
            print(f"Target script path: {script_path}")

            # Check if the script exists
            if not os.path.exists(script_path):
                return f"Script file not found: {script_path}"

            # Build the command with arguments
            command = ['python3', script_path] # Initialises the command list with the Python interpreter and the script path.
            if protocol:
                command += ['--protocol', protocol] #  If the user has selected a protocol, append the --protocol argument.
            if direction:
                command += ['--direction', direction]

            # Run the simulation script and capture stdout and stderr
            result = subprocess.run(
                command, # The command and arguments to run.
                check=True, # Raises a CalledProcessError if the script exits with a non-zero status.
                stdout=subprocess.PIPE, # Captures the standard output of the script.
                stderr=subprocess.PIPE, # Captures the standard error of the script.
                text=True #  Treats the output as text strings instead of bytes.
            )

            # Retrieve the latest generated log file
            log_files = glob.glob('exfiltration_logs_*.log') #Uses glob to find all files matching the pattern exfiltration_logs_*.log
            if not log_files:
                return "No log files were generated."
            latest_log_file = max(log_files, key=os.path.getmtime) # elects the most recently modified log file from the list.

            # Read the content of the log file
            with open(latest_log_file, 'r') as file:
                log_content = file.read() # Reads the entire content of the log file.

            # Include script output in the displayed content
            output = '' # Initialises an empty string to accumulate output
            if result.stdout: # If there is standard output from the script, append it to the output string.
                output += f"Script Output:\n{result.stdout}\n"
            if result.stderr:
                output += f"Script Error Output:\n{result.stderr}\n"
            output += log_content #Append the log file content to the output string.

            return output
        except subprocess.CalledProcessError as e:
            # Capture errors when running the script
            error_msg = f"Error running the script:\n{e.stderr}\nCommand: {e.cmd}\nExit code: {e.returncode}"
            return error_msg
        except Exception as e:
            return f"An unknown error occurred: {e}"
    else:
        return '' # If the button has not been clicked, returns an empty string, leaving the textarea empty.

# Callback function: Generate authentication log and display results (Area 1)
@app.callback(
    Output('auth-log-output', 'value'),
    [Input('generate-auth-button', 'n_clicks')],
    [State('auth-service', 'value'),
     State('auth-username', 'value'),
     State('auth-event-type', 'value'),
     State('auth-num-entries', 'value')]  # Added State for Number of Entries
)
def update_auth_output(n_clicks, service, username, event_type, num_entries):
    if n_clicks > 0:
        try:
            # Get the absolute path of the target script
            script_path = os.path.abspath('Python/BDAuthScript.py')
            print(f"Target script path: {script_path}")

            # Check if the script exists
            if not os.path.exists(script_path):
                return f"Script file not found: {script_path}"

            # Build the command with arguments
            command = ['python3', script_path]
            if num_entries:
                command += ['--num_entries', str(int(num_entries))]  # Pass --num_entries
            else:
                command += ['--num_entries', '200']  # Default value

            if service:
                command += ['--service', service]
            if username:
                if not username.isalnum():
                    return "Invalid username. Please use alphanumeric characters only."
                command += ['--username', username]
            if event_type:
                command += ['--event_type', event_type]

            # Run the authentication log generation script
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Retrieve the latest generated auth log file
            log_files = glob.glob('auth*.log')
            if not log_files:
                return "No authentication log files were generated."
            latest_log_file = max(log_files, key=os.path.getmtime)

            # Read the content of the auth log file
            with open(latest_log_file, 'r') as file:
                log_content = file.read()

            # Include script output in the displayed content
            output = ''
            if result.stdout:
                output += f"Script Output:\n{result.stdout}\n"
            if result.stderr:
                output += f"Script Error Output:\n{result.stderr}\n"
            output += log_content

            return output
        except subprocess.CalledProcessError as e:
            # Capture errors when running the script
            error_msg = f"Error running the authentication script:\n{e.stderr}\nCommand: {e.cmd}\nExit code: {e.returncode}"
            return error_msg
        except Exception as e:
            return f"An unknown error occurred: {e}"
    else:
        return ''

# Callback function: Generate Ahmad's firewall log and display results (Area 2)
@app.callback(
    Output('ahmad-firewall-log-output', 'value'),
    [Input('generate-ahmad-firewall-button', 'n_clicks')],
    [State('ahmad-firewall-protocol', 'value'),
     State('ahmad-firewall-direction', 'value')]
)
def update_ahmad_firewall_output(n_clicks, protocol, direction):
    if n_clicks > 0:
        try:
            script_path = os.path.abspath('Python/Ahmad_Firewall_Log_Script.py')
            print(f"Target script path: {script_path}")
            if not os.path.exists(script_path):
                return f"Script file not found: {script_path}"
            command = ['python3', script_path]
            if protocol:
                command += ['--protocol', protocol]
            if direction:
                command += ['--direction', direction]
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Read the log file
            log_file = 'authentication_backdoor_logfile.txt'
            if not os.path.exists(log_file):
                return "No log files were generated."
            with open(log_file, 'r') as file:
                log_content = file.read()
            output = ''
            if result.stdout:
                output += f"Script Output:\n{result.stdout}\n"
            if result.stderr:
                output += f"Script Error Output:\n{result.stderr}\n"
            output += log_content
            return output
        except subprocess.CalledProcessError as e:
            error_msg = f"Error running the script:\n{e.stderr}\nCommand: {e.cmd}\nExit code: {e.returncode}"
            return error_msg
        except Exception as e:
            return f"An unknown error occurred: {e}"
    else:
        return ''

# Callback function: Generate Ahmad's authentication log and display results (Area 2)
@app.callback(
    Output('ahmad-auth-log-output', 'value'),
    [Input('generate-ahmad-auth-button', 'n_clicks')],
    [State('ahmad-auth-service', 'value'),
     State('ahmad-auth-username', 'value'),
     State('ahmad-auth-event-type', 'value')]
)
def update_ahmad_auth_output(n_clicks, service, username, event_type):
    if n_clicks > 0:
        try:
            script_path = os.path.abspath('Python/Ahmad_Auth_Log_Script.py')
            print(f"Target script path: {script_path}")
            if not os.path.exists(script_path):
                return f"Script file not found: {script_path}"
            command = ['python3', script_path]
            if service:
                command += ['--service', service]
            if username:
                if not username.isalnum():
                    return "Invalid username. Please use alphanumeric characters only."
                command += ['--username', username]
            if event_type:
                command += ['--event_type', event_type]
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Read the log file
            log_file = 'auth_log.txt'
            if not os.path.exists(log_file):
                return "No authentication log files were generated."
            with open(log_file, 'r') as file:
                log_content = file.read()
            output = ''
            if result.stdout:
                output += f"Script Output:\n{result.stdout}\n"
            if result.stderr:
                output += f"Script Error Output:\n{result.stderr}\n"
            output += log_content
            return output
        except subprocess.CalledProcessError as e:
            error_msg = f"Error running the authentication script:\n{e.stderr}\nCommand: {e.cmd}\nExit code: {e.returncode}"
            return error_msg
        except Exception as e:
            return f"An unknown error occurred: {e}"
    else:
        return ''

# Callback function: Generate Vedika's firewall log and display results (Area 3)
@app.callback(
    Output('vedika-firewall-log-output', 'value'),
    [Input('generate-vedika-firewall-button', 'n_clicks')],
    [State('vedika-firewall-ip', 'value'),
     State('vedika-firewall-event', 'value')]
)
def update_vedika_firewall_output(n_clicks, ip_address, event):
    if n_clicks > 0:
        try:
            script_path = os.path.abspath('Python/V_generate_firewall_logs.py')
            print(f"Target script path: {script_path}")
            if not os.path.exists(script_path):
                return f"Script file not found: {script_path}"
            command = ['python3', script_path]
            if ip_address:
                command += ['--ip_address', ip_address]
            if event:
                command += ['--event', event]
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Read the log file
            log_file = 'firewall_priv_escalation_logs.txt'
            if not os.path.exists(log_file):
                return "No log files were generated."
            with open(log_file, 'r') as file:
                log_content = file.read()
            output = ''
            if result.stdout:
                output += f"Script Output:\n{result.stdout}\n"
            if result.stderr:
                output += f"Script Error Output:\n{result.stderr}\n"
            output += log_content
            return output
        except subprocess.CalledProcessError as e:
            error_msg = f"Error running the firewall script:\n{e.stderr}\nCommand: {e.cmd}\nExit code: {e.returncode}"
            return error_msg
        except Exception as e:
            return f"An unknown error occurred: {e}"
    else:
        return ''

# Callback function: Generate Vedika's authentication log and display results (Area 3)
@app.callback(
    Output('vedika-auth-log-output', 'value'),
    [Input('generate-vedika-auth-button', 'n_clicks')],
    [State('vedika-auth-username', 'value'),
     State('vedika-auth-command', 'value')]
)
def update_vedika_auth_output(n_clicks, username, command_input):
    if n_clicks > 0:
        try:
            script_path = os.path.abspath('Python/V_generate_auth_logs.py')
            print(f"Target script path: {script_path}")
            if not os.path.exists(script_path):
                return f"Script file not found: {script_path}"
            command = ['python3', script_path]
            if username:
                if not username.isalnum():
                    return "Invalid username. Please use alphanumeric characters only."
                command += ['--username', username]
            if command_input:
                command += ['--command', command_input]
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Read the log file
            log_file = 'privilege_escalation_log.txt'
            if not os.path.exists(log_file):
                return "No authentication log files were generated."
            with open(log_file, 'r') as file:
                log_content = file.read()
            output = ''
            if result.stdout:
                output += f"Script Output:\n{result.stdout}\n"
            if result.stderr:
                output += f"Script Error Output:\n{result.stderr}\n"
            output += log_content
            return output
        except subprocess.CalledProcessError as e:
            error_msg = f"Error running the authentication script:\n{e.stderr}\nCommand: {e.cmd}\nExit code: {e.returncode}"
            return error_msg
        except Exception as e:
            return f"An unknown error occurred: {e}"
    else:
        return ''

# Callback function: Generate Tee Mea's firewall log and display results (Area 4)
@app.callback(
    Output('tee-mea-firewall-log-output', 'value'),
    [Input('generate-tee-mea-firewall-button', 'n_clicks')],
    [State('tee-mea-firewall-dst-ip', 'value'),
     State('tee-mea-firewall-total-entries', 'value')]
)
def update_tee_mea_firewall_output(n_clicks, dst_ip, total_entries):
    if n_clicks > 0:
        try:
            script_path = os.path.abspath('Python/T_firewall_ddos.py')
            print(f"Target script path: {script_path}")
            if not os.path.exists(script_path):
                return f"Script file not found: {script_path}"
            command = ['python3', script_path]
            if dst_ip:
                command += ['--dst_ip', dst_ip]
            if total_entries:
                command += ['--total_entries', str(int(total_entries))]
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Read the log file
            log_file = 'firewall_log.log'
            if not os.path.exists(log_file):
                return "No log files were generated."
            with open(log_file, 'r') as file:
                log_content = file.read()
            output = ''
            if result.stdout:
                output += f"Script Output:\n{result.stdout}\n"
            if result.stderr:
                output += f"Script Error Output:\n{result.stderr}\n"
            output += log_content
            return output
        except subprocess.CalledProcessError as e:
            error_msg = f"Error running the firewall script:\n{e.stderr}\nCommand: {e.cmd}\nExit code: {e.returncode}"
            return error_msg
        except Exception as e:
            return f"An unknown error occurred: {e}"
    else:
        return ''

# Callback function: Generate Tee Mea's authentication log and display results (Area 4)
@app.callback(
    Output('tee-mea-auth-log-output', 'value'),
    [Input('generate-tee-mea-auth-button', 'n_clicks')],
    [State('tee-mea-auth-num-attempts', 'value')]
)
def update_tee_mea_auth_output(n_clicks, num_attempts):
    if n_clicks > 0:
        try:
            script_path = os.path.abspath('Python/T_authentication_ddos.py')
            print(f"Target script path: {script_path}")
            if not os.path.exists(script_path):
                return f"Script file not found: {script_path}"
            command = ['python3', script_path]
            if num_attempts:
                command += ['--num_attempts', str(int(num_attempts))]
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Read the log file
            log_file = 'auth_ddos.log'
            if not os.path.exists(log_file):
                return "No authentication log files were generated."
            with open(log_file, 'r') as file:
                log_content = file.read()
            output = ''
            if result.stdout:
                output += f"Script Output:\n{result.stdout}\n"
            if result.stderr:
                output += f"Script Error Output:\n{result.stderr}\n"
            output += log_content
            return output
        except subprocess.CalledProcessError as e:
            error_msg = f"Error running the authentication script:\n{e.stderr}\nCommand: {e.cmd}\nExit code: {e.returncode}"
            return error_msg
        except Exception as e:
            return f"An unknown error occurred: {e}"
    else:
        return ''

# Callback function: Generate Andrew's firewall log and display results (Area 5)
@app.callback(
    Output('andrew-firewall-log-output', 'value'),
    [Input('generate-andrew-firewall-button', 'n_clicks')],
    [State('andrew-firewall-server-ip', 'value')]
)
def update_andrew_firewall_output(n_clicks, server_ip):
    if n_clicks > 0:
        try:
            script_path = os.path.abspath('Python/andrew_worm_sim_log_firewall.py')
            print(f"Target script path: {script_path}")
            if not os.path.exists(script_path):
                return f"Script file not found: {script_path}"
            command = ['python3', script_path]
            if server_ip:
                command += ['--server_ip', server_ip]
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Read the log file
            log_file = 'simulated_firewall_logs.txt'
            if not os.path.exists(log_file):
                return "No log files were generated."
            with open(log_file, 'r') as file:
                log_content = file.read()
            output = ''
            if result.stdout:
                output += f"Script Output:\n{result.stdout}\n"
            if result.stderr:
                output += f"Script Error Output:\n{result.stderr}\n"
            output += log_content
            return output
        except subprocess.CalledProcessError as e:
            error_msg = f"Error running the firewall script:\n{e.stderr}\nCommand: {e.cmd}\nExit code: {e.returncode}"
            return error_msg
        except Exception as e:
            return f"An unknown error occurred: {e}"
    else:
        return ''

# Callback function: Generate Andrew's authentication log and display results (Area 5)
@app.callback(
    Output('andrew-auth-log-output', 'value'),
    [Input('generate-andrew-auth-button', 'n_clicks')],
    [State('andrew-auth-num-entries', 'value')]
)
def update_andrew_auth_output(n_clicks, num_entries):
    if n_clicks > 0:
        try:
            script_path = os.path.abspath('Python/andrew_worm_sim_log_auth.py')
            print(f"Target script path: {script_path}")
            if not os.path.exists(script_path):
                return f"Script file not found: {script_path}"
            command = ['python3', script_path]
            if num_entries:
                command += ['--num_entries', str(int(num_entries))]
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Read the log file
            log_file = 'simulated_authentication_logs.txt'
            if not os.path.exists(log_file):
                return "No authentication log files were generated."
            with open(log_file, 'r') as file:
                log_content = file.read()
            output = ''
            if result.stdout:
                output += f"Script Output:\n{result.stdout}\n"
            if result.stderr:
                output += f"Script Error Output:\n{result.stderr}\n"
            output += log_content
            return output
        except subprocess.CalledProcessError as e:
            error_msg = f"Error running the authentication script:\n{e.stderr}\nCommand: {e.cmd}\nExit code: {e.returncode}"
            return error_msg
        except Exception as e:
            return f"An unknown error occurred: {e}"
    else:
        return ''

# Callback function: Generate Daniyal's firewall log and display results (Area 6)
@app.callback(
    Output('daniyal-firewall-log-output', 'value'),
    [Input('generate-daniyal-firewall-button', 'n_clicks')],
    [State('daniyal-firewall-src-ip', 'value'),
     State('daniyal-firewall-event-type', 'value')]
)
def update_daniyal_firewall_output(n_clicks, src_ip, event_type):
    if n_clicks > 0:
        try:
            script_path = os.path.abspath('Python/Daniyal_Firewall_Log_Script.py')
            print(f"Target script path: {script_path}")
            if not os.path.exists(script_path):
                return f"Script file not found: {script_path}"
            command = ['python3', script_path]
            if src_ip:
                command += ['--src_ip', src_ip]
            if event_type:
                command += ['--event_type', event_type]
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Read the log file
            log_file = 'daniyal_firewall_log.txt'
            if not os.path.exists(log_file):
                return "No firewall log files were generated."
            with open(log_file, 'r') as file:
                log_content = file.read()
            output = ''
            if result.stdout:
                output += f"Script Output:\n{result.stdout}\n"
            if result.stderr:
                output += f"Script Error Output:\n{result.stderr}\n"
            output += log_content
            return output
        except subprocess.CalledProcessError as e:
            error_msg = f"Error running the firewall script:\n{e.stderr}\nCommand: {e.cmd}\nExit code: {e.returncode}"
            return error_msg
        except Exception as e:
            return f"An unknown error occurred: {e}"
    else:
        return ''

# Callback function: Generate Daniyal's authentication log and display results (Area 6)
@app.callback(
    Output('daniyal-auth-log-output', 'value'),
    [Input('generate-daniyal-auth-button', 'n_clicks')],
    [State('daniyal-auth-username', 'value'),
     State('daniyal-auth-action', 'value')]
)
def update_daniyal_auth_output(n_clicks, username, action):
    if n_clicks > 0:
        try:
            script_path = os.path.abspath('Python/Daniyal_Auth_Log_Script.py')
            print(f"Target script path: {script_path}")
            if not os.path.exists(script_path):
                return f"Script file not found: {script_path}"
            command = ['python3', script_path]
            if username:
                if not username.isalnum():
                    return "Invalid username. Please use alphanumeric characters only."
                command += ['--username', username]
            if action:
                command += ['--action', action]
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Read the log file
            log_file = 'daniyal_auth_log.txt'
            if not os.path.exists(log_file):
                return "No authentication log files were generated."
            with open(log_file, 'r') as file:
                log_content = file.read()
            output = ''
            if result.stdout:
                output += f"Script Output:\n{result.stdout}\n"
            if result.stderr:
                output += f"Script Error Output:\n{result.stderr}\n"
            output += log_content
            return output
        except subprocess.CalledProcessError as e:
            error_msg = f"Error running the authentication script:\n{e.stderr}\nCommand: {e.cmd}\nExit code: {e.returncode}"
            return error_msg
        except Exception as e:
            return f"An unknown error occurred: {e}"
    else:
        return ''

# Run the Dash server
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
