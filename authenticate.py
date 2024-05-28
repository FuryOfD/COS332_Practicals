# Local credentials
USER_CREDENTIALS = {
    'employee1': 'password1',
    'employee2': 'password2',
}

# Real credentials for the cloud email service
REAL_USERNAME = 'work.dharsh@gmail.com'
REAL_PASSWORD = 'brmo nosk unmr zglg'

def authenticateUser(client_socket, remote_socket):
    user_authenticated = False
    client_socket.send(b'+OK send your username\r\n')
    client_buffer = b''
    
    
    try:
        while not user_authenticated:
            data = client_socket.recv(1024)
            if not data:
                break
            client_buffer += data

            while b'\r\n' in client_buffer:
                line, client_buffer = client_buffer.split(b'\r\n', 1)
                line = line.decode().strip()
                print(f"[DEBUG] Received from client: {line}")

                if line.upper().startswith('USER'):
                    username = line.split()[1]
                    client_socket.send(b'+OK send your password\r\n')
                    print(f"[INFO] Requested password for username: {username}")

                    data = client_socket.recv(1024)
                    if not data:
                        break
                    client_buffer += data

                    if b'\r\n' in client_buffer:
                        line, client_buffer = client_buffer.split(b'\r\n', 1)
                        line = line.decode().strip()
                        print(f"[DEBUG] Received from client: {line}")

                        if line.upper().startswith('PASS'):
                            password = line.split()[1]
                            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                                # Authenticate with real credentials to the remote server
                                remote_socket.send(f'USER {REAL_USERNAME}\r\n'.encode())
                                remote_response = remote_socket.recv(1024).decode().strip()
                                print(f"[DEBUG] Sent USER command to remote server, received: {remote_response}")

                                if remote_response.startswith('+OK'):
                                    remote_socket.send(f'PASS {REAL_PASSWORD}\r\n'.encode())
                                    remote_response = remote_socket.recv(1024).decode().strip()
                                    print(f"[DEBUG] Sent PASS command to remote server, received: {remote_response}")

                                    if remote_response.startswith('+OK'):
                                        user_authenticated = True
                                        client_socket.send(b'+OK Proxy authentication successful\r\n')
                                        print("[INFO] Proxy authentication successful")
                                    else:
                                        client_socket.send(b'-ERR Proxy authentication failed\r\n')
                                        print("[ERROR] Proxy authentication failed")
                                        break
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

    except Exception as e:
        print(f"[ERROR] {e}")
        client_socket.send(b'-ERR Authentication error\r\n')
            
    return user_authenticated