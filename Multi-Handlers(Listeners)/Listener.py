import socket
import threading

def handle_client(client_socket, address):
    print(f"Connected: {address}")

    # Handle client requests or perform desired actions
    # Example: Echo back client messages
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        client_socket.sendall(data)

    print(f"Disconnected: {address}")
    client_socket.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()

        # Create a new thread for each client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    host = "127.0.0.1"  # Enter your desired host IP address
    port = 8888  # Enter your desired port number
    start_server(host, port)

