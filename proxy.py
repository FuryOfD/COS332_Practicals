import socket
import threading
import ssl
from authenticate import authenticateUser

# Configuration
LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 55555
REMOTE_HOST = 'pop.gmail.com'
REMOTE_PORT = 995

def handle_client(client_socket):
    try:
        print("[INFO] Handling new client connection")
        
        # Connect to the remote POP3 server with SSL/TLS
        context = ssl.create_default_context()
        with socket.create_connection((REMOTE_HOST, REMOTE_PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=REMOTE_HOST) as ssock:
                print("[INFO] Connected to remote POP3 server with SSL/TLS")
                # raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # remote_socket = context.wrap_socket(raw_socket, server_hostname=REMOTE_HOST)
                # remote_socket.connect((REMOTE_HOST, REMOTE_PORT))
                # print("[INFO] Connected to remote POP3 server with SSL/TLS")

                # Receive greeting from remote server
                greeting = ssock.recv(1024)
                client_socket.send(greeting)
                print(f"[INFO] Sent greeting to client: {greeting.strip()}")

                # Authentication phase
                user_authenticated = authenticateUser(client_socket, ssock)


                if user_authenticated:
                    # Forward the rest of the conversation
                    def forward_client_to_server():
                        while True:
                            data = client_socket.recv(1024)
                            if not data:
                                break
                            ssock.send(data)
                            print(f"[DEBUG] Forwarded to server: {data.strip()}")

                    def forward_server_to_client():
                        while True:
                            data = ssock.recv(1024)
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
                ssock.close()
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