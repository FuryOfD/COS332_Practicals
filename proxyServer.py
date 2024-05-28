import socket
import ssl
import threading


# Local credentials for employees
USER_CREDENTIALS = {
    'employee1': 'password1',
    'employee2': 'password2',
}

# Real credentials for the cloud email service
REAL_USERNAME = 'work.dharsh@gmail.com'
REAL_PASSWORD = 'brmo nosk unmr zglg'

# Function to connect and authenticate with the real POP3 server - Gmail
def pop3_connect_and_authenticate():
    try:
        context = ssl.create_default_context()
        with socket.create_connection(('pop.gmail.com', 995)) as sock:
            with context.wrap_socket(sock, server_hostname='pop.gmail.com') as ssock:
                print("[INFO] Connected to remote POP3 server with SSL/TLS")
                greeting = ssock.recv(1024).decode()
                print(f"[DEBUG] Server greeting: {greeting.strip()}")

                ssock.sendall(f"USER {REAL_USERNAME}\r\n".encode())
                response = ssock.recv(1024).decode()
                print(f"[DEBUG] Sent USER command, received: {response.strip()}")
                if not response.startswith('+OK'):
                    return False, ssock, "Invalid USER command response from remote server."

                ssock.sendall(f"PASS {REAL_PASSWORD}\r\n".encode())
                response = ssock.recv(1024).decode()
                print(f"[DEBUG] Sent PASS command, received: {response.strip()}")
                if not response.startswith('+OK'):
                    return False, ssock, "Invalid PASS command response from remote server."

                return True, ssock, None

    except Exception as e:
        return False, None, f"[ERROR] {e}"

# Function to handle client requests and relay messages between client and remote server
def handle_client(client_socket):
    try:
        client_socket.send(b'+OK POP3 proxy server ready\r\n')
        authenticated = False
        client_buffer = b''
        username = None

        while not authenticated:
            data = client_socket.recv(1024)
            if not data:
                break
            client_buffer += data

            while b'\r\n' in client_buffer:
                line, client_buffer = client_buffer.split(b'\r\n', 1)
                line = line.decode().strip()
                print(f"[DEBUG] Received from client: {line}")

                if line.upper().startswith('USER'):
                    try:
                        username = line.split()[1]
                        client_socket.send(b'+OK send your password\r\n')
                        print(f"[INFO] Requested password for username: {username}")
                    except IndexError:
                        client_socket.send(b'-ERR Missing username\r\n')
                        continue

                elif line.upper().startswith('PASS'):
                    try:
                        password = line.split()[1]
                        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                            authenticated, remote_socket, error = pop3_connect_and_authenticate()
                            if authenticated:
                                client_socket.send(b'+OK Proxy authentication successful\r\n')
                                print("[INFO] Proxy authentication successful")
                                # Relay messages between client and remote server
                                while True:
                                    client_data = client_socket.recv(1024)
                                    if not client_data:
                                        break
                                    remote_socket.sendall(client_data)
                                    remote_data = remote_socket.recv(1024)
                                    if not remote_data:
                                        break
                                    client_socket.sendall(remote_data)
                            else:
                                client_socket.send(f'-ERR {error}\r\n'.encode())
                                break
                        else:
                            client_socket.send(b'-ERR Invalid username or password\r\n')
                            break
                    except IndexError:
                        client_socket.send(b'-ERR Missing password\r\n')
                        continue
                else:
                    client_socket.send(b'-ERR Invalid command\r\n')

    except Exception as e:
        print(f"[ERROR] {e}")
        client_socket.send(b'-ERR Authentication error\r\n')
    finally:
        client_socket.close()


# Function to start the proxy server - Works on port 1100
def start_proxy_server(host='127.0.0.1', port=1100):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[INFO] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_proxy_server()
