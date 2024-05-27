import socket
import threading
import ssl

# Configuration
LOCAL_HOST = 'localhost'
LOCAL_PORT = 55555
REMOTE_HOST = 'pop.gmail.com'
REMOTE_PORT = 995

# Local credentials
USER_CREDENTIALS = {
    'employee1': 'password1',
    'employee2': 'password2',
}

# Real credentials for the cloud email service
REAL_USERNAME = 'work.dharsh@gmail.com'
REAL_PASSWORD = 'brmo nosk unmr zglg'


def handle_client(client_socket):
    try:
        print("[INFO] Handling new client connection")
        
        # Connect to the remote POP3 server with SSL/TLS
        context = ssl.create_default_context()
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket = context.wrap_socket(raw_socket, server_hostname=REMOTE_HOST)
        remote_socket.connect((REMOTE_HOST, REMOTE_PORT))
        print("[INFO] Connected to remote POP3 server with SSL/TLS")

        # Receive greeting from remote server
        greeting = remote_socket.recv(4096)
        client_socket.send(greeting)
        print("[INFO] Sent greeting to client")

        # Authentication phase
        user_authenticated = False

        while not user_authenticated:
            data = client_socket.recv(4096).decode()
            print(f"[DEBUG] Received from client: {data.strip()}")
            if data.startswith('USER'):
                username = data.split()[1]
                client_socket.send(b'+OK send your password\r\n')
                print(f"[INFO] Requested password for username: {username}")
                password_data = client_socket.recv(4096).decode()
                if password_data.startswith('PASS'):
                    password = password_data.split()[1]
                    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                        # Authenticate with real credentials to the remote server
                        remote_socket.send(f'USER {REAL_USERNAME}\r\n'.encode())
                        remote_response = remote_socket.recv(4096)
                        print(f"[DEBUG] Sent USER command to remote server, received: {remote_response.strip()}")
                        remote_socket.send(f'PASS {REAL_PASSWORD}\r\n'.encode())
                        remote_response = remote_socket.recv(4096)
                        print(f"[DEBUG] Sent PASS command to remote server, received: {remote_response.strip()}")
                        if remote_response.startswith(b'+OK'):
                            user_authenticated = True
                            client_socket.send(b'+OK Proxy authentication successful\r\n')
                            print("[INFO] Proxy authentication successful")
                        else:
                            client_socket.send(b'-ERR Proxy authentication failed\r\n')
                            print("[ERROR] Proxy authentication failed")
                            break
                    else:
                        client_socket.send(b'-ERR Invalid username or password\r\n')
                        print("[ERROR] Invalid username or password")
                        break
                else:
                    client_socket.send(b'-ERR Invalid PASS command\r\n')
                    print("[ERROR] Invalid PASS command")
                    break
            else:
                client_socket.send(b'-ERR Invalid USER command\r\n')
                print("[ERROR] Invalid USER command")
                break

        if user_authenticated:
            # Forward the rest of the conversation
            def forward_client_to_server():
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    remote_socket.send(data)
                    print(f"[DEBUG] Forwarded to server: {data.strip()}")

            def forward_server_to_client():
                while True:
                    data = remote_socket.recv(4096)
                    if not data:
                        break
                    client_socket.send(data)
                    print(f"[DEBUG] Forwarded to client: {data.strip()}")

            client_to_server_thread = threading.Thread(target=forward_client_to_server)
            server_to_client_thread = threading.Thread(target=forward_server_to_client)

            client_to_server_thread.start()
            server_to_client_thread.start()

            client_to_server_thread.join()
            server_to_client_thread.join()

        client_socket.close()
        remote_socket.close()
        print("[INFO] Closed client and remote sockets")
    except Exception as e:
        print(f"[ERROR] {e}")
        client_socket.close()

def start_proxy():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((LOCAL_HOST, LOCAL_PORT))
    proxy_socket.listen(5)
    print(f"[*] Listening on {LOCAL_HOST}:{LOCAL_PORT}")

    while True:
        client_socket, addr = proxy_socket.accept()
        print(f"[INFO] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_proxy()
    
