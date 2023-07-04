import socket
import concurrent.futures

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

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            client_socket, address = server_socket.accept()

            # Execute the handle_client function in a separate thread
            executor.submit(handle_client, client_socket, address)

if __name__ == "__main__":
    host = "127.0.0.1"  # Enter your desired host IP address
    port = 8888  # Enter your desired port number
    start_server(host, port)
